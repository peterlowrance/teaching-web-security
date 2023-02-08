#!/bin/sh
(cd attacking-website; python manage.py runserver 0.0.0.0:8080) &
(cd vulnerable-socialmedia; python manage.py runserver 0.0.0.0:8081)
