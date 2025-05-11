/*
 * PART 1: CREATE A SEQUENCE
 * 
 * Description: Creating a custom sequence for generating invoice numbers
 * with a specific format (INV-YY-XXXXXXX)
 */

-- First, create a sequence to generate the numeric portion of the invoice number
CREATE SEQUENCE invoice_number_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

-- Create a function to generate formatted invoice numbers with year prefix
CREATE OR REPLACE FUNCTION generate_invoice_number()
RETURNS TEXT AS $$
DECLARE
    next_val INTEGER;
    year_part TEXT;
BEGIN
    -- Get the next value from the sequence
    next_val := nextval('invoice_number_seq');
    
    -- Get the current year as 2-digit format
    year_part := to_char(current_date, 'YY');
    
    -- Format the invoice number: INV-YY-XXXXXXX (padded to 7 digits)
    RETURN 'INV-' || year_part || '-' || LPAD(next_val::TEXT, 7, '0');
END;
$$ LANGUAGE plpgsql;

/*
 * PART 2: CREATE A VIEW
 * 
 * Description: Creating a comprehensive view that presents project and contract data
 * in a format that's useful for reporting and analysis
 */

CREATE OR REPLACE VIEW project_performance_view AS
SELECT
    p.id AS project_id,
    p.title AS project_title,
    p.status AS project_status,
    
    -- Client information
    client.id AS client_id,
    client.first_name || ' ' || client.last_name AS client_name,
    
    -- Freelancer information (if contract exists)
    freelancer.id AS freelancer_id,
    freelancer.first_name || ' ' || freelancer.last_name AS freelancer_name,
    fp.avg_rating AS freelancer_rating,
    
    -- Contract details
    c.id AS contract_id,
    c.amount AS contract_amount,
    c.start_date,
    c.end_date,
    c.status AS contract_status,
    
    -- Duration metrics
    CASE 
        WHEN c.completed_at IS NOT NULL THEN 
            c.completed_at::DATE - c.start_date
        WHEN c.status = 'active' THEN 
            CURRENT_DATE - c.start_date
        ELSE NULL
    END AS days_duration,
    
    -- Financial metrics
    p.budget_min,
    p.budget_max,
    CASE 
        WHEN p.budget_max > 0 AND c.amount IS NOT NULL THEN
            ROUND((c.amount - p.budget_min) / NULLIF(p.budget_min, 0) * 100, 2)
        ELSE NULL
    END AS budget_min_variance_pct,
    
    -- Bid metrics
    (SELECT COUNT(*) FROM bids WHERE project_id = p.id) AS total_bids,
    (SELECT MIN(amount) FROM bids WHERE project_id = p.id) AS min_bid,
    (SELECT MAX(amount) FROM bids WHERE project_id = p.id) AS max_bid,
    (SELECT AVG(amount) FROM bids WHERE project_id = p.id) AS avg_bid,
    
    -- Review data
    client_review.rating AS client_rating_for_freelancer,
    client_review.comment AS client_review,
    freelancer_review.rating AS freelancer_rating_for_client,
    freelancer_review.comment AS freelancer_review,
    
    -- Timestamp information
    p.created_at AS project_created_at,
    c.created_at AS contract_created_at,
    c.completed_at AS contract_completed_at
FROM
    projects p
JOIN
    users client ON p.client_id = client.id
LEFT JOIN
    contracts c ON p.id = c.project_id
LEFT JOIN
    users freelancer ON c.freelancer_id = freelancer.id
LEFT JOIN
    user_profiles fp ON freelancer.id = fp.user_id
LEFT JOIN
    reviews client_review ON 
        c.id = client_review.contract_id AND 
        client_review.reviewer_id = client.id AND
        client_review.reviewee_id = freelancer.id
LEFT JOIN
    reviews freelancer_review ON 
        c.id = freelancer_review.contract_id AND 
        freelancer_review.reviewer_id = freelancer.id AND
        freelancer_review.reviewee_id = client.id;

-- Example query using the view (for demonstration purposes)
-- SELECT * FROM project_performance_view WHERE project_status = 'completed' ORDER BY contract_completed_at DESC;

/*
 * Additional useful view: Active Freelancer Performance Dashboard
 */
CREATE OR REPLACE VIEW freelancer_performance_dashboard AS
WITH freelancer_stats AS (
    SELECT
        u.id AS freelancer_id,
        COUNT(DISTINCT c.id) AS total_contracts,
        COUNT(DISTINCT CASE WHEN c.status = 'completed' THEN c.id ELSE NULL END) AS completed_contracts,
        COUNT(DISTINCT CASE WHEN c.status = 'cancelled' THEN c.id ELSE NULL END) AS cancelled_contracts,
        SUM(CASE WHEN c.status = 'completed' THEN c.amount ELSE 0 END) AS total_earnings,
        AVG(CASE WHEN c.status = 'completed' THEN c.amount ELSE NULL END) AS avg_contract_value,
        AVG(CASE WHEN c.status = 'completed' THEN (c.completed_at::DATE - c.start_date) ELSE NULL END) AS avg_completion_days
    FROM
        users u
    LEFT JOIN
        contracts c ON u.id = c.freelancer_id
    WHERE
        u.role = 'freelancer'
    GROUP BY
        u.id
)
SELECT
    u.id,
    u.first_name || ' ' || u.last_name AS freelancer_name,
    up.headline,
    up.skills,
    up.hourly_rate,
    up.avg_rating,
    fs.total_contracts,
    fs.completed_contracts,
    fs.cancelled_contracts,
    CASE 
        WHEN fs.total_contracts > 0 THEN
            ROUND((fs.completed_contracts::numeric / fs.total_contracts) * 100, 2)
        ELSE 0
    END AS completion_rate,
    fs.total_earnings,
    fs.avg_contract_value,
    fs.avg_completion_days,
    (SELECT COUNT(*) FROM bids b WHERE b.freelancer_id = u.id) AS total_bids,
    (SELECT COUNT(*) FROM bids b WHERE b.freelancer_id = u.id AND b.status = 'accepted') AS accepted_bids,
    CASE 
        WHEN (SELECT COUNT(*) FROM bids b WHERE b.freelancer_id = u.id) > 0 THEN
            ROUND((SELECT COUNT(*) FROM bids b WHERE b.freelancer_id = u.id AND b.status = 'accepted')::numeric / 
                  (SELECT COUNT(*) FROM bids b WHERE b.freelancer_id = u.id) * 100, 2)
        ELSE 0
    END AS bid_success_rate,
    u.created_at AS member_since
FROM
    users u
JOIN
    user_profiles up ON u.id = up.user_id
LEFT JOIN
    freelancer_stats fs ON u.id = fs.freelancer_id
WHERE
    u.role = 'freelancer'
ORDER BY
    up.avg_rating DESC NULLS LAST,
    fs.total_earnings DESC NULLS LAST;