#!/bin/sh
(cd attacking-website; python manage.py runserver 0.0.0.0:8080) &
(cd vulnerable-bank; python manage.py runserver 0.0.0.0:8081)