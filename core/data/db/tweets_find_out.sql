CREATE TABLE tweets_find_out (
   id INTEGER NOT NULL,
   term VARCHAR(100),
   search_type VARCHAR(30),
   max_tweets INTEGER,
   created DATETIME,
   user_id INTEGER,
   PRIMARY KEY (id),
   FOREIGN KEY(user_id) REFERENCES users (id)
)
