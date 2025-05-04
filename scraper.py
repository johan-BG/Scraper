import scrapy
import spacy
from langdetect import detect
from scrapy.crawler import CrawlerProcess
import os
import re
import pytesseract
from pdf2image import convert_from_bytes
from datetime import datetime
import hashlib
from PIL import Image
import io
import json

class RecursiveOCRSpider(scrapy.Spider):
    name = "recursive_ocr"
    start_urls = ['https://sanskritdocuments.org/scannedbooks/asisanskritpdfs.html']
    visited_urls = set()

    custom_settings = {
        'DOWNLOAD_WARNSIZE': 100 * 1024 * 1024, 
        'DOWNLOAD_MAXSIZE': 200 * 1024 * 1024, 
        'DOWNLOAD_DELAY': 2,
        'ROBOTSTXT_OBEY': True,
        'FILES_STORE': './downloads',
        'LOG_LEVEL': 'ERROR'
    }

    def parse(self, response):
      self.visited_urls.add(response.url)

      for link in response.css('a'):
          link_text = link.css('::text').get()
          href = link.css('::attr(href)').get()
          if href:
              full_url = response.urljoin(href)
              if full_url.endswith(('.pdf', '.epub', '.html')):
                  yield scrapy.Request(
                      full_url,
                      callback=self.save_and_ocr_file,
                      meta={'title': link_text.strip() if link_text else ''}
                  )
              elif full_url not in self.visited_urls and self.allowed_domain(full_url):
                  yield scrapy.Request(full_url, callback=self.parse)

    def allowed_domain(self, url):
        return url.startswith(self.start_urls[0])

    def save_and_ocr_file(self, response):
        os.makedirs("downloads", exist_ok=True)
        filename = os.path.basename(response.url.split('?')[0])
        filepath = os.path.join("downloads", filename)
        jsonfile = filepath.replace('.pdf','.json')
        current_checksum = hashlib.sha256(response.body).hexdigest()

        if os.path.exists(filepath) and os.path.exists(jsonfile):
          with open(jsonfile, 'r') as f:
              old_metadata = json.load(f)
          if old_metadata.get("checksum") == current_checksum:
              print(f"Skipping {filename}: already downloaded and unchanged.")
              return
        with open(filepath, 'wb') as f:
          f.write(response.body)
        if filename.endswith(".pdf"):
            title = response.meta.get("title")
            metadata = self.extract_text_and_metadata(response.body, response.url,filepath,title)
            if metadata:
                with open(jsonfile, 'w') as f:
                    json.dump(metadata, f)
                print(metadata)

    def extract_text_and_metadata(self, file_bytes, download_url,file_path,title):
        try:
            nlp = spacy.load("en_core_web_sm")
            images = convert_from_bytes(file_bytes)
            full_text = ""

            for image in images[:20]:
                text = pytesseract.image_to_string(image, lang='eng+san')#+hin+tam+tel+kan+ben+guj+ori
                full_text += text + "\n"

            # --- NLP for author ---
            author_regex = re.search(r'(?i)(?:by|author|written\sby)\s+([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', full_text)
            if author_regex:
                authors = [author_regex.group(1)]
            else:
                # --- Secondary NLP fallback ---
                doc = nlp(full_text)
                people = list({ent.text for ent in doc.ents if ent.label_ == "PERSON"})
                authors = people[:3] if people else ["Unknown"]

            # --- Publication year ---
            year_match = re.search(r'(19|20)\d{2}', full_text)
            pub_year = year_match.group(0) if year_match else "Unknown"

            # --- Language detection ---
            try:
                language = detect(full_text)
            except:
                language = "und"

            # --- Checksum ---
            checksum = hashlib.sha256(file_bytes).hexdigest()

            id = os.path.basename(file_path).replace(".pdf", "")

            metadata = {
                "site": "sanskritdocuments.org",
                "document_id": id,
                "title": title,
                "authors": authors,
                "pub_year": pub_year,
                "language": language,
                "download_url": download_url,
                "checksum": checksum,
                "scraped_at": datetime.utcnow().isoformat() + "Z",
                "content": full_text.strip()
            }

            return metadata

        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return None
