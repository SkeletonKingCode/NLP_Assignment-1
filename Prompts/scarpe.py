import requests
from bs4 import BeautifulSoup
import re
import time
import os

# Configuration
BASE_URL = "https://www.urdupoint.com"
LIST_URL_TEMPLATE = "https://www.urdupoint.com/kids/category/moral-stories-page{}.html"
OUTPUT_DIR = "urdu_stories_dataset"
LINKS_FILE = "all_story_links.txt"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
}

# Tags
TAG_EOS = " <EOS>"
TAG_EOP = " <EOP>"
TAG_EOD = " <EOD>"

# Urdu Sentence Punctuation Regex
URDU_PUNCT_REGEX = r'([۔؟!])'

# Setup Folders
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_urdu_text(text):
    """Splits text into sentences and appends tags."""
    if not text: return ""
    parts = re.split(URDU_PUNCT_REGEX, text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i].strip() + parts[i+1]
        if sentence:
            sentences.append(sentence + TAG_EOS)
    if len(parts) % 2 != 0 and parts[-1].strip():
        sentences.append(parts[-1].strip() + TAG_EOS)
    return " ".join(sentences)

def scrape_story_content(story_url):
    """Fetches and parses a single story page."""
    try:
        response = requests.get(story_url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"
        
        content_div = soup.find('div', class_='detail_text_ads')
        if not content_div: return None

        paragraphs = content_div.find_all(['p', 'div', 'span'], class_=re.compile(r'urdu|ar-huruf|txt_sc'))
        processed_body = []
        for p in paragraphs:
            txt = p.get_text(strip=True)
            if len(txt) > 30: 
                processed_body.append(process_urdu_text(txt) + TAG_EOP)
        
        return {"title": title, "body": "\n".join(processed_body) + TAG_EOD}
    except:
        return None

def run_scraper(start_page, end_page):
    # Open the links file in append mode
    with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
        for page_num in range(start_page, end_page + 1):
            print(f"\n--- Crawling List Page {page_num} ---")
            list_url = LIST_URL_TEMPLATE.format(page_num)
            
            try:
                response = requests.get(list_url, headers=HEADERS)
                soup = BeautifulSoup(response.content, 'html.parser')
                story_links = soup.find_all('a', class_='sharp_box')
                
                for link in story_links:
                    href = link.get('href')
                    if not href: continue
                    
                    full_url = href if href.startswith('http') else BASE_URL + href
                    
                    # 1. Save the link to our file immediately
                    links_log.write(full_url + "\n")
                    links_log.flush() # Forces writing to disk
                    
                    # 2. Scrape the content
                    story_data = scrape_story_content(full_url)
                    if story_data:
                        # Clean title for Linux filename
                        safe_title = "".join(x for x in story_data['title'][:50] if x.isalnum() or x==' ').strip()
                        file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(f"SOURCE: {full_url}\n")
                            f.write(f"TITLE: {story_data['title']}\n\n")
                            f.write(story_data['body'])
                        print(f"Successfully scraped: {story_data['title']}")
                    
                    time.sleep(1.2) # Polite delay
                    
            except Exception as e:
                print(f"Error on page {page_num}: {e}")

# Run for 100 pages
if __name__ == "__main__":
    print(f"Starting Scraper. Links will be saved to {LINKS_FILE}")
    run_scraper(1, 100)