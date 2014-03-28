# coding=utf-8

sql_select_posts = u"""
select
    count(post.id) count,
    b.*,
    c.dt,
    Group_Concat('<div>'||post.body||'</div>','<hr>') body
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
        id not in (select book_id from read_books where user_id=1)

    ) b
    join
        (select
             book_id,
             max(pub_date) as dt
         from
             post
         where
            id not in (select post_id from read_posts where user_id=1)
         group by
            book_id
        ) c
            on  b.id = c.book_id
     join post on post.book_id = b.id
group by b.id
"""

sql_mark_read_book = u"insert or ignore into read_book(book_id, user_id) values(:book_id, :user_id)"

sql_mark_read_post = u"insert or ignore into read_post(post_id, user_id) " \
                  u"select post.id, :user_id from post where book_id = :book_id"

sql_mark_unread_book = u"delete from read_book where book_id=:book_id and user_id=:user_id"

sql_mark_unread_post = u"delete from read_post where user_id=:user_id and post_id in" \
                        u" (select id from post where book_id=:book_id)"
