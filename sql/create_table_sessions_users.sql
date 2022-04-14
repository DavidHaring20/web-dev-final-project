DROP TABLE IF EXISTS sessions_users;

CREATE TABLE sessions_users(
    session_id      INTEGER PRIMARY KEY,
    user_id         TEXT UNIQUE NOT NULL,
    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);