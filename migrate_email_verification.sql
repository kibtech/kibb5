-- Migration script to remove email verification requirements
-- Run this in your database to update existing users

-- For PostgreSQL:
UPDATE users SET email_verified = TRUE;
UPDATE admin_users SET email_verified = TRUE;

-- For SQLite:
-- UPDATE users SET email_verified = 1;
-- UPDATE admin_users SET email_verified = 1;

-- For MySQL:
-- UPDATE users SET email_verified = 1;
-- UPDATE admin_users SET email_verified = 1;

-- Verify the changes
SELECT COUNT(*) as total_users, 
       COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_users
FROM users;

SELECT COUNT(*) as total_admin_users, 
       COUNT(CASE WHEN email_verified = TRUE THEN 1 END) as verified_admin_users
FROM admin_users;

-- Optional: Check if any users still have email_verified = FALSE
SELECT COUNT(*) as unverified_users FROM users WHERE email_verified = FALSE;
SELECT COUNT(*) as unverified_admin_users FROM admin_users WHERE email_verified = FALSE;
