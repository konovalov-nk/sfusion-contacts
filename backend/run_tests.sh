#!/usr/bin/env sh
export DJANGO_DATABASE_TEST=sqlite
clear
echo 'Running mamba for the first time...'
python manage.py mamba
#mamba --format=documentation
echo "Watching for file changes..."
. "./watch.sh" "python manage.py mamba"