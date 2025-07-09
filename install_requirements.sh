#!/bin/bash

# Exit on error
set -e

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Created virtual environment in ./venv"
fi

# Activate venv
source venv/bin/activate

echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt

echo "All requirements installed." 