#!/bin/bash
# Firebase Setup Validator for Unix/Linux/macOS
# Runs the Firebase validation script with proper environment

echo "========================================"
echo "Firebase Setup Validator"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it first: python -m venv venv"
    echo ""
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run validation script
python scripts/validate_firebase.py

# Exit with the same code as the validation script
exit $?
