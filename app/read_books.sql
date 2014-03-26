CREATE TABLE read_books
(
    user_id INTEGER,   
    book_id INTEGER,   
    FOREIGN KEY(book_id) REFERENCES book (id),   
    FOREIGN KEY(user_id) REFERENCES user (id),
    UNIQUE(book_id, user_id)
)
