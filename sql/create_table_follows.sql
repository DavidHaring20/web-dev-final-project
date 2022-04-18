DROP TABLE IF EXISTS follows;

CREATE TABLE follows(
    follower_user_id TEXT,
    followed_user_id TEXT,
    UNIQUE(follower_user_id, followed_user_id),
    FOREIGN KEY (follower_user_id)
        REFERENCES users(user_id),
    FOREIGN KEY (followed_user_id)
        REFERENCES users(user_id),
    PRIMARY KEY(follower_user_id, followed_user_id)
);