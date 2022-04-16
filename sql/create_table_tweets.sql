DROP TABLE IF EXISTS tweets;

CREATE TABLE tweets(
    tweet_id            INTEGER PRIMARY KEY,
    tweet_title         TEXT NOT NULL,
    tweet_description   TEXT NOT NULL,
    tweet_image_url     TEXT,
    tweet_created_at    TEXT NOT NULL,
    tweet_updated_at    TEXT,
    user_id             TEXT NOT NULL,
    FOREIGN KEY(user_id)
        REFERENCES users(user_id)
);