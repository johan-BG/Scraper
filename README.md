## Scraper

A Scrapy-based web scraper that downloads documents, performs OCR (Optical Character Recognition) on them, and extracts metadata such as authors, publication year, and language. The metadata is saved as JSON and checksums are used to detect changes or duplicates.

## Features

- Crawls websites recursively and respects `robots.txt`
- Extracts content from PDF files using OCR (via Tesseract)
- Metadata extraction includes:
  - Author(s)
  - Publication year
  - Language
  - Content (from OCR)
  - Checksum for file change detection
- Saves metadata as JSON for each document
- Handles large PDFs efficiently

## 🛠 Installation

To install all required dependencies (both system and Python packages), use the provided `install.sh` script.

### Prerequisites

- Python 3.7 or higher
- Bash-compatible terminal (Linux/macOS or WSL on Windows)

### Steps

1. **Make the script executable**:

   ```bash
   chmod +x install.sh
