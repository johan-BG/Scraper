### Scraper

This project is a **recursive web scraper** built using **Scrapy**, **Tesseract OCR**, and **spaCy NLP**. It is designed to crawl the given url's scanned books archive, download PDF files, extract text using OCR, and retrieve metadata such as author name, publication year, and language.

---

## 🧠 Features

- Recursively crawls web pages for PDFs.
- Extracts text from PDF files using Tesseract OCR.
- Extracts metadata like:
  - **Title** (from link text)
  - **Author** (via regex and NLP fallback)
  - **Publication Year**
  - **Language** (auto-detected)
  - **Checksum** (for file integrity and update detection)
- Skips already downloaded or unchanged files using checksum verification.
- Saves metadata as `.json` files alongside the PDFs.
- Obeys `robots.txt` and respects download delays.

---

## 📁 Project Structure

