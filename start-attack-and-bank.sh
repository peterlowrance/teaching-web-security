(cd attacking-website; python manage.py runserver 0.0.0.0:8080) &
(cd vulnerable-bank; python manage.py runserver 0.0.0.0:8081)

# (cd attacking-website; daphne -b 0.0.0.0 -p 8080 mysite.asgi:application) &
# (cd vulnerable-bank; daphne -b 0.0.0.0 -p 8081 mysite.asgi:application)
