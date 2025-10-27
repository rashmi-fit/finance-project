#!/bin/bash
# Script to run the Finance Analytics Spark Application

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed. Spark requires Java 8 or 11."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/installed" ]; then
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    touch venv/installed
fi

# Run the application
echo "Running Finance Analytics Spark Application..."
python src/main/python/finance_analytics.py

# Deactivate virtual environment
deactivate
