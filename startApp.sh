#!/bin/bash

# Check if we're inside a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "No virtual environment found. Activating..."
    # Activate the virtual environment (adjust the path to your venv)
    source /home/skwan/koobyte/.venv/bin/activate
else
    echo "Virtual environment is already activated."
fi

# Run Gunicorn app
echo "Starting Gunicorn app..."
gunicorn -b 0.0.0.0:8080 --access-logfile /home/skwan/logs/access.log wsgi:app
