import requests
from bs4 import BeautifulSoup
import re
import time
import os

# Configuration
BASE_URL = "https://www.urdupoint.com"
LIST_URL_TEMPLATE = "https://www.urdupoint.com/kids/category/moral-stories-page{}.html"
OUTPUT_DIR = "../urdu_stories_dataset"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
}

# Tags
TAG_EOS = " <EOS>"
TAG_EOP = " <EOP>"
TAG_EOD = " <EOD>"

# Urdu Sentence Punctuation Regex
URDU_PUNCT_REGEX = r'([۔؟!])'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_urdu_text(text):
    """Splits text into sentences and appends tags."""
    if not text: return ""
    
    # Split by punctuation, keeping the punctuation mark
    parts = re.split(URDU_PUNCT_REGEX, text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i].strip() + parts[i+1]
        if sentence:
            sentences.append(sentence + TAG_EOS)
    
    # Catch any trailing text
    if len(parts) % 2 != 0 and parts[-1].strip():
        sentences.append(parts[-1].strip() + TAG_EOS)
        
    return " ".join(sentences)

def scrape_story_content(story_url):
    """Fetches and parses a single story page."""
    try:
        response = requests.get(story_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.find('h1').get_text(strip=True) if soup.find('h1') else "Untitled"
        
        # Based on UrduPoint structure, content is often in 'detail_text_ads'
        content_div = soup.find('div', class_='detail_text_ads')
        if not content_div:
            return None

        # Process each paragraph/div inside the content area
        # We target common containers for Urdu text
        paragraphs = content_div.find_all(['p', 'div', 'span'], class_=re.compile(r'urdu|ar-huruf|txt_sc'))
        
        processed_body = []
        for p in paragraphs:
            txt = p.get_text(strip=True)
            if len(txt) > 20: # Ignore short snippets/ads
                processed_txt = process_urdu_text(txt)
                processed_body.append(processed_txt + TAG_EOP)
        
        return {
            "title": title,
            "body": "\n".join(processed_body) + TAG_EOD
        }
    except Exception as e:
        print(f"Error scraping {story_url}: {e}")
        return None

def run_scraper(start_page, end_page):
    """Iterates through list pages and extracts stories."""
    all_links=list()
    for page_num in range(start_page, end_page + 1):
        print(f"--- Processing List Page {page_num} ---")
        list_url = LIST_URL_TEMPLATE.format(page_num)
        all_links=list()
        try:
            response = requests.get(list_url, headers=HEADERS)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all story links using the 'sharp_box' class from your file
            story_links = soup.find_all('a', class_='sharp_box')
            page_links=list()
            for link in story_links:
                href = link.get('href')
                if not href: continue
                
                full_url = href if href.startswith('http') else BASE_URL + href
                page_links.append(full_url)
                # Scrape the actual story
                story_data = scrape_story_content(full_url)
                
                if story_data:
                    # Save to file
                    filename = "".join(x for x in story_data['title'][:30] if x.isalnum() or x==' ')
                    file_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
                    
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(f"TITLE: {story_data['title']}\n")
                        f.write(story_data['body'])
                    
                    print(f"Saved: {story_data['title']}")
                
                # Respectful delay
                time.sleep(1.5)
            all_links.append(page_links)
        except Exception as e:
            print(f"Error on list page {page_num}: {e}")
    return all_links
# Start scraping from page 1 to 100
links=run_scraper(1, 100)
