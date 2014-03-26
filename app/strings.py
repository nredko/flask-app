# coding=utf-8

select_posts = u"""
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
     where 
        id not in (select post_id from read_posts where user_id=:user_id)

    ) b
    join
        (select
             book_id,
             max(pub_date) as dt
         from
             post
         where 
            id not in (select post_id from read_posts where user_id=:user_id)
         group by
            book_id
        ) c
            on  b.id = c.book_id
     join post on post.book_id = b.id
group by b.id"""

