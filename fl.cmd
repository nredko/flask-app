curl -D - -d"name=Nike000" -d"pass=715434" -d"persistent_login=1"  -d"form_id=user_login_block"  -c cookies.txt http://flibusta.net/node?destination=node -o login.html
curl -b cookies.txt http://flibusta.net/b/356183  -o out.html
