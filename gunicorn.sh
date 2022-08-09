#!/bin/sh
# Here we will be spinning up multiple threads with multiple worker processess(-w) and perform a binding.
gunicorn app:"create_app('$FLASK_ENV')" -w 2 --threads 1 -b localhost:9999