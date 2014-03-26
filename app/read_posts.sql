CREATE TABLE read_posts
(
    user_id INTEGER,   
    post_id INTEGER,   
    FOREIGN KEY(post_id) REFERENCES post (id),   
    FOREIGN KEY(user_id) REFERENCES user (id),
    UNIQUE(post_id, user_id)

)