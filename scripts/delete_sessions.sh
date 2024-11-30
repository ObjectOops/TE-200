#!/bin/bash

./manage.py shell -c '

from django.contrib.sessions.models import Session

sessions = Session.objects.all().delete()

'
