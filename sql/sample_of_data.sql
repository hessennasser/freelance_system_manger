-- Sample data for users table
INSERT INTO users (email, password_hash, role, first_name, last_name, bio) VALUES
('john.client@example.com', 'hashed_password_1', 'client', 'John', 'Smith', 'Business owner looking for developers'),
('sarah.client@example.com', 'hashed_password_2', 'client', 'Sarah', 'Johnson', 'Marketing agency owner'),
('mike.dev@example.com', 'hashed_password_3', 'freelancer', 'Mike', 'Brown', 'Full-stack developer with 5 years experience'),
('lisa.designer@example.com', 'hashed_password_4', 'freelancer', 'Lisa', 'Chen', 'UI/UX designer specialized in mobile apps'),
('alex.writer@example.com', 'hashed_password_5', 'freelancer', 'Alex', 'Martinez', 'Content writer and SEO specialist');

-- Sample data for user_profiles table
INSERT INTO user_profiles (user_id, headline, hourly_rate, company_name, skills) VALUES
(1, 'CEO at TechCorp', NULL, 'TechCorp Inc.', NULL),
(2, 'Founder at MarketBoost', NULL, 'MarketBoost Agency', NULL),
(3, 'Senior Full-Stack Developer', 65.00, NULL, 'JavaScript, React, Node.js, PostgreSQL'),
(4, 'UI/UX Designer & Mobile Specialist', 75.00, NULL, 'Figma, Adobe XD, Sketch, UI Design, Mobile Design'),
(5, 'Content Writer & SEO Expert', 45.00, NULL, 'Content Writing, SEO, Copywriting, Blog Posts');

-- Sample data for projects table
INSERT INTO projects (client_id, title, description, budget_min, budget_max, status, skills_required) VALUES
(1, 'E-commerce Website Development', 'Need a developer to build an online store for my business with product catalog, shopping cart, and payment integration.', 3000.00, 5000.00, 'open', 'JavaScript, React, Node.js, E-commerce'),
(1, 'Mobile App UI Design', 'Looking for a designer to create UI mockups for our fitness tracking mobile app.', 1000.00, 2000.00, 'in_progress', 'UI Design, Mobile Design, Figma'),
(2, 'SEO Content for Marketing Blog', 'Need 10 high-quality blog posts about digital marketing strategies, each around 1500 words.', 500.00, 1000.00, 'open', 'Content Writing, SEO, Marketing');

-- Sample data for bids table
INSERT INTO bids (project_id, freelancer_id, amount, duration_days, proposal, status) VALUES
(1, 3, 4500.00, 30, 'I have extensive experience with e-commerce sites and can deliver a high-quality solution within 30 days.', 'pending'),
(2, 4, 1800.00, 14, 'As a UI/UX specialist with mobile app focus, I can create beautiful and intuitive designs for your fitness app.', 'accepted'),
(3, 5, 800.00, 21, 'I can write engaging marketing content that is SEO optimized and will help increase your site traffic.', 'pending');

-- Sample data for contracts table
INSERT INTO contracts (project_id, bid_id, client_id, freelancer_id, title, description, amount, start_date, end_date, status) VALUES
(2, 2, 1, 4, 'Fitness App UI Design Project', 'Design of complete UI for iOS and Android fitness tracking application', 1800.00, '2025-04-15', '2025-04-29', 'active');

-- Sample data for messages table
INSERT INTO messages (sender_id, receiver_id, project_id, message, is_read) VALUES
(1, 4, 2, 'Hi Lisa, just checking in on the progress of the UI designs. Any updates?', false),
(4, 1, 2, 'Hello John! I''ve completed the home screen and workout tracking screens. I''ll send you the mockups tomorrow.', true),
(3, 1, 1, 'I''ve submitted a bid for your e-commerce project. I''d be happy to discuss the requirements in more detail.', false),
(5, 2, 3, 'Thank you for posting your content writing project. I''ve submitted a proposal and would love to work with you.', false);
