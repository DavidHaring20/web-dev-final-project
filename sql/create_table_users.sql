DROP TABLE IF EXISTS users;

CREATE TABLE users(
    user_id TEXT PRIMARY KEY,
    user_first_name TEXT NOT NULL,
    user_middle_name TEXT,
    user_last_name TEXT NOT NULL,
    user_address TEXT NOT NULL,
    user_age INTEGER NOT NULL,
    user_username TEXT UNIQUE NOT NULL,
    user_email TEXT UNIQUE NOT NULL,
    user_password TEXT NOT NULL,
    user_role TEXT NOT NULL
);