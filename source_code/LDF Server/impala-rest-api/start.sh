#!/bin/sh
# redis-server # Also needs to be executed
gunicorn wsgi:app -b 0.0.0.0:5000
