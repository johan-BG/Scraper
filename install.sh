#!/bin/bash
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-all libgl1

echo "Installing Python packages..."
pip install -r requirements.txt

echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo "Installation complete."