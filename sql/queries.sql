/*
 * Query 1: Find top freelancers with the highest average rating and at least 3 reviews
 * Description: This query identifies the most highly-rated freelancers who have received 
 * at least 3 reviews, showing their name, average rating, number of reviews, and hourly rate.
 * Concepts: JOIN, GROUP BY, HAVING, WHERE clause
 */
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name AS freelancer_name,
    up.avg_rating,
    COUNT(r.id) AS review_count,
    up.hourly_rate
FROM 
    users u
JOIN 
    user_profiles up ON u.id = up.user_id
JOIN 
    reviews r ON u.id = r.reviewee_id
WHERE 
    u.role = 'freelancer'
GROUP BY 
    u.id, u.first_name, u.last_name, up.avg_rating, up.hourly_rate
HAVING 
    COUNT(r.id) >= 3
ORDER BY 
    up.avg_rating DESC, review_count DESC
LIMIT 10;


/*
 * Query 2: Find projects with the most bids and their average bid amount
 * Description: This query identifies projects that are attracting the most interest from freelancers,
 * showing the project details, number of bids, and the average bid amount.
 * Concepts: JOIN, GROUP BY, Subquery, WHERE clause
 */
SELECT 
    p.id,
    p.title,
    p.status,
    u.first_name || ' ' || u.last_name AS client_name,
    COUNT(b.id) AS bid_count,
    ROUND(AVG(b.amount), 2) AS avg_bid_amount,
    p.budget_min,
    p.budget_max,
    (SELECT COUNT(*) FROM bids WHERE project_id = p.id AND status = 'accepted') AS accepted_bids
FROM 
    projects p
JOIN 
    users u ON p.client_id = u.id
LEFT JOIN 
    bids b ON p.id = b.project_id
WHERE 
    p.status = 'open'
GROUP BY 
    p.id, p.title, p.status, u.first_name, u.last_name
HAVING 
    COUNT(b.id) > 0
ORDER BY 
    bid_count DESC, p.created_at DESC;


/*
 * Query 3: Find clients who have spent the most on completed contracts
 * Description: This query identifies the clients who have invested the most in freelancer contracts,
 * showing the total amount spent, number of contracts, and average contract value.
 * Concepts: JOIN, GROUP BY, WHERE clause, aggregate functions
 */
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name AS client_name,
    COUNT(c.id) AS completed_contracts,
    SUM(c.amount) AS total_spent,
    ROUND(AVG(c.amount), 2) AS avg_contract_value
FROM 
    users u
LEFT JOIN 
    contracts c ON u.id = c.client_id
WHERE 
    u.role = 'client'
    AND c.status = 'completed'
GROUP BY 
    u.id, u.first_name, u.last_name
ORDER BY 
    total_spent DESC
LIMIT 10;


/*
 * Query 4: Find active contracts with upcoming deadlines in the next 7 days
 * Description: This query identifies contracts that are about to reach their deadline,
 * helping project managers monitor projects that might need attention or follow-up.
 * Concepts: Multiple JOINs, WHERE clause with date calculations, ORDER BY
 */
SELECT 
    c.id AS contract_id,
    c.title AS contract_title,
    p.title AS project_title,
    c.end_date AS deadline,
    current_date AS today,
    (c.end_date - current_date) AS days_remaining,
    client.first_name || ' ' || client.last_name AS client_name,
    freelancer.first_name || ' ' || freelancer.last_name AS freelancer_name,
    c.amount
FROM 
    contracts c
JOIN 
    projects p ON c.project_id = p.id
JOIN 
    users client ON c.client_id = client.id
JOIN 
    users freelancer ON c.freelancer_id = freelancer.id
WHERE 
    c.status = 'active'
    AND c.end_date BETWEEN current_date AND (current_date + INTERVAL '7 days')
ORDER BY 
    days_remaining ASC, c.amount DESC;


/*
 * Query 5: Find freelancers with relevant skills for a specific project
 * Description: This query helps clients find suitable freelancers for their projects based on required skills,
 * showing freelancers who have the required skills in their profile, sorted by their rating and experience.
 * Concepts: Subquery in WHERE clause, JOIN, ORDER BY
 */
WITH project_skills AS (
    SELECT 
        id,
        LOWER(skills_required) AS skills_required
    FROM 
        projects
    WHERE 
        id = 123
)
SELECT 
    u.id,
    u.first_name || ' ' || u.last_name AS freelancer_name,
    up.headline,
    up.skills,
    up.avg_rating,
    up.hourly_rate,
    (SELECT COUNT(*) FROM contracts WHERE freelancer_id = u.id AND status = 'completed') AS completed_projects
FROM 
    users u
JOIN 
    user_profiles up ON u.id = up.user_id
JOIN 
    project_skills ps ON 
        LOWER(up.skills) LIKE '%' || ps.skills_required || '%'
WHERE 
    u.role = 'freelancer'
ORDER BY 
    up.avg_rating DESC NULLS LAST,
    completed_projects DESC,
    up.hourly_rate ASC;