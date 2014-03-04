select
    count(post.id) count,
    b.*,
    c.dt,
    Group_Concat(post.body) body
from
    (select
        book.*,
        authors
     from
        book
        left join 
        (select 
            book_id,
            Group_Concat(
            SUBSTR(' '||name,1+length(rtrim(' '||name, 'ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮёйцукенгшщзхъфывапролджэячсмитьбюQWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm`1234567890-=~!@#$%^&*()_+|",./<>?'))) 
            ) authors
         from
            book_authors join author on author_id = author.id
         group by book_id
        ) a  
        on book.id = a.book_id
    ) b
    join
        (select
             book_id,
             max(pub_date) as dt
         from
             post
         group by
            book_id
        ) c
            on  b.id = c.book_id
     join post on post.book_id = b.id
group by
    b.id