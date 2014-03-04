select
    book.*,
    authors
from
    book
    left join (select 
        book_id,
        Group_Concat(author.name) authors
     from
        book_authors join author on author_id = author.id
     group by book_id
    ) a  on book.id = a.book_id
