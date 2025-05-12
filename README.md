# Freelance Marketplace Platform

## 🧠 Project Idea

Build a full-stack freelance marketplace platform where **clients** can post
projects and **freelancers** can bid, get hired, deliver work, and get reviewed.

Inspired by platforms like Upwork and Freelancer.com, this system supports:

- Project posting
- Bidding and hiring
- Contract management
- Ratings & reviews
- Messaging system

---

## 🗄️ Database Schema Overview

We used PostgreSQL with support for ENUM types and relational integrity.

### 🔹 ENUM Types

- `user_role`: `client`, `freelancer`
- `project_status`: `open`, `in_progress`, `completed`, `cancelled`
- `bid_status`: `pending`, `accepted`, `rejected`
- `contract_status`: `active`, `completed`, `cancelled`

---

## 👤 Users Table

Stores basic user account info.

| Field             | Type           |
| ----------------- | -------------- |
| id                | SERIAL PK      |
| email             | VARCHAR UNIQUE |
| password_hash     | VARCHAR        |
| role              | user_role ENUM |
| first_name        | VARCHAR        |
| last_name         | VARCHAR        |
| profile_image_url | VARCHAR        |
| bio               | TEXT           |

---

## 📄 User Profiles

Additional profile info for freelancers.

| Field       | Type       |
| ----------- | ---------- |
| user_id     | FK → users |
| headline    | VARCHAR    |
| hourly_rate | DECIMAL    |
| skills      | TEXT       |
| avg_rating  | DECIMAL    |

---

## 📁 Projects

Projects posted by clients.

| Field           | Type       |
| --------------- | ---------- |
| id              | SERIAL PK  |
| client_id       | FK → users |
| title           | VARCHAR    |
| description     | TEXT       |
| budget_min      | DECIMAL    |
| budget_max      | DECIMAL    |
| status          | ENUM       |
| skills_required | TEXT       |

---

## 💸 Bids

Bids submitted by freelancers for projects.

| Field         | Type          |
| ------------- | ------------- |
| id            | SERIAL PK     |
| project_id    | FK → projects |
| freelancer_id | FK → users    |
| amount        | DECIMAL       |
| duration_days | INTEGER       |
| proposal      | TEXT          |
| status        | ENUM          |

---

## 📜 Contracts

Formal agreement between client and freelancer.

| Field         | Type          |
| ------------- | ------------- |
| id            | SERIAL PK     |
| project_id    | FK → projects |
| bid_id        | FK → bids     |
| client_id     | FK → users    |
| freelancer_id | FK → users    |
| title         | VARCHAR       |
| amount        | DECIMAL       |
| start_date    | DATE          |
| end_date      | DATE          |
| status        | ENUM          |

---

## ⭐ Reviews

User-to-user feedback on completed contracts.

| Field       | Type           |
| ----------- | -------------- |
| id          | SERIAL PK      |
| contract_id | FK → contracts |
| reviewer_id | FK → users     |
| reviewee_id | FK → users     |
| rating      | INTEGER        |
| comment     | TEXT           |

---

## 💬 Messages

In-platform communication between users.

| Field       | Type                     |
| ----------- | ------------------------ |
| id          | SERIAL PK                |
| sender_id   | FK → users               |
| receiver_id | FK → users               |
| project_id  | FK → projects (optional) |
| message     | TEXT                     |
| is_read     | BOOLEAN                  |

---

## ⚙️ Functionality Highlights

### 👨‍💼 For Clients:

- Post and manage projects
- Review freelancer bids
- Award contracts
- Leave reviews for completed work

### 👩‍💻 For Freelancers:

- Create profile with skills and rate
- Browse and bid on projects
- Manage contracts and deadlines
- Receive and respond to client messages

### 📈 Analytics Features:

- Top freelancers by rating
- Projects with most bids
- Clients with highest spend
- Contracts ending soon
- Skill-based freelancer match

---

## ✅ Triggers & Automation

- `updated_at` auto-updates on modification
- Average rating recalculated after each new review

---
