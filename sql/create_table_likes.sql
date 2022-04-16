DROP TABLE IF EXISTS likes;

CREATE TABLE likes(
    tweet_id        INTEGER,
    user_id         TEXT,
    FOREIGN KEY (tweet_id)
        REFERENCES tweets(tweet_id),
    FOREIGN KEY (user_id)
        REFERENCES users(user_id),
    PRIMARY KEY(tweet_id, user_id)
);