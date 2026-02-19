import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import re
import time
import random
import os

# Configuration
BASE_URL = "https://www.urdupoint.com"
LIST_URL_TEMPLATE = "https://www.urdupoint.com/kids/category/moral-stories-page{}.html"
OUTPUT_DIR = "urdu_stories_dataset"
LINKS_FILE = "all_story_links.txt"

# Requested Tags
TAG_EOS = " <EOS>" 
TAG_EOP = " <EOP>" 
TAG_EOD = " <EOD>" 

# Urdu Sentence Punctuation Regex - Handles typical Urdu stops
URDU_PUNCT_REGEX = r'([۔؟!])'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_urdu_text(text):
    if not text: return ""
    # Split text by punctuation while keeping the punctuation mark
    parts = re.split(URDU_PUNCT_REGEX, text)
    sentences = []
    
    # Reassemble sentences with the punctuation and add EOS tag
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i].strip() + parts[i+1]
        if sentence:
            sentences.append(sentence + TAG_EOS)
            
    # Handle any trailing text without punctuation
    if len(parts) % 2 != 0 and parts[-1].strip():
        sentences.append(parts[-1].strip() + TAG_EOS)
        
    return " ".join(sentences)

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver

def scrape_urdu_point(start_page, end_page):
    driver = get_driver()
    try:
        with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
            for page_num in range(start_page, end_page + 1):
                print(f"\n--- Story List Page {page_num} ---")
                driver.get(LIST_URL_TEMPLATE.format(page_num))
                time.sleep(random.uniform(1, 2)) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # Selecting the specific story link boxes
                story_links = soup.find_all('a', class_='sharp_box')
                
                for link in story_links:
                    href = link.get('href')
                    if not href: continue
                    full_url = href if href.startswith('http') else BASE_URL + href
                    
                    links_log.write(full_url + "\n")
                    links_log.flush()

                    print(f"   Scraping: {full_url}")
                    driver.get(full_url)
                    time.sleep(random.uniform(3, 5))
                    
                    story_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # --- Text Extraction Logic ---
                    # 1. Get the Title
                    title_tag = story_soup.find('h1', class_='phead')
                    title = title_tag.get_text(strip=True) if title_tag else "Untitled Story"
                    print(title)

                    # 2. Get the Paragraphs (Spans inside the specific div)
                    processed_paragraphs = []
                    # Find all spans within div[style="text-align: right;"] that have the class 'nastaleeq3'
                    right_aligned_div = story_soup.find('div', class_='txt_detail')
                    print(right_aligned_div.get_text())
                    spans = story_soup.find_all("span", style="font-size:1.25em; line-height:1.8em;")
                    print(spans)
                    for i, span in enumerate(spans):
                        raw_text = span.get_text(strip=True)
                        print(raw_text)
                        if raw_text:
                            # Process sentences and add <EOP>
                            p_text = process_urdu_text(raw_text) + TAG_EOP
                            processed_paragraphs.append(p_text)
                            
                            # Print 1st span of 1st paragraph for debugging as requested
                            if i == 0:
                                print(f"   [DEBUG] Title: {title}")
                                print(f"   [DEBUG] 1st Span: {p_text[:100]}...")

                    # 3. Save to file
                    if processed_paragraphs:
                        # Clean title for filename
                        safe_title = "".join(x for x in title[:50] if x.isalnum() or x==' ').strip()
                        file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            # Note: We don't add tags to the Title unless you want them there too
                            f.write(f"TITLE: {title}\n\n")
                            f.write("\n".join(processed_paragraphs))
                            f.write(TAG_EOD)
                        print(f"      Saved: {safe_title}.txt")

                    time.sleep(random.uniform(1, 2))
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_urdu_point(1, 100)