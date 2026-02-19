import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    options.page_load_strategy=("eager")
    driver = uc.Chrome(options=options)
    return driver

def collect_story_links(driver, start_page, end_page):
    """First collect all story links from all pages"""
    all_links = []
    
    for page_num in range(start_page, end_page + 1):
        print(f"\n--- Collecting links from Story List Page {page_num} ---")
        driver.get(LIST_URL_TEMPLATE.format(page_num))
        time.sleep(random.uniform(2, 3))
        
        # Wait for the links to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sharp_box'))
        )
        
        # Find story links using Selenium
        story_links = driver.find_elements(By.CSS_SELECTOR, 'a.sharp_box')
        
        for link in story_links:
            try:
                href = link.get_attribute('href')
                if href:
                    full_url = href if href.startswith('http') else BASE_URL + href
                    all_links.append(full_url)
                    print(f"   Collected: {full_url}")
            except:
                continue  # Skip if we can't get the href
        
        # Save links as we go
        with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
            for url in all_links[-len(story_links):]:  # Just save the newly collected ones
                links_log.write(url + "\n")
    
    return all_links

def scrape_story(driver, url):
    """Scrape a single story"""
    print(f"   Scraping: {url}")
    driver.get(url)
    time.sleep(random.uniform(3, 5))

    # 1. Get the Title
    try:
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.phead'))
        )
        title = title_element.text.strip()
    except:
        title = "Untitled Story"
    print(f"   Title: {title}")

    # 2. Locate the main content container that holds the story text
    content_selectors = [
        "div.txt_detail",                     # Common class for UrduPoint details
        "div[style='text-align: right;']",    # Direct style match from HTML
        "div.article_content",                 # Fallback
        "div.story-content"                    # Another possible class
    ]

    story_container = None
    for selector in content_selectors:
        try:
            story_container = driver.find_element(By.CSS_SELECTOR, selector)
            if story_container:
                print(f"   Found content container with selector: {selector}")
                break
        except:
            continue

    if not story_container:
        print("   No story container found!")
        return None

    # 3. Extract full text and split into paragraphs
    full_text = story_container.text
    # Split by two or more newlines (common paragraph breaks)
    raw_paragraphs = [p.strip() for p in re.split(r'\n\s*\n', full_text) if p.strip()]

    if not raw_paragraphs:
        print("   No paragraphs extracted!")
        return None

    # 4. Discard the first paragraph (assumed to be author name)
    story_paragraphs = raw_paragraphs[1:]   # Remove first line (author)

    # 5. Process each paragraph with sentence tags
    processed_paragraphs = []
    for i, para in enumerate(story_paragraphs):
        # Process sentences within the paragraph (add <EOS>)
        processed_para = process_urdu_text(para) + TAG_EOP
        processed_paragraphs.append(processed_para)

        # Debug: show first paragraph preview
        if i == 0:
            print(f"   [DEBUG] First story paragraph preview: {processed_para[:100]}...")

    # 6. Save to file
    if processed_paragraphs:
        safe_title = "".join(x for x in title[:50] if x.isalnum() or x==' ').strip()
        if not safe_title:
            safe_title = f"story_{int(time.time())}"
        
        file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"TITLE: {title}\n\n")
            f.write("\n".join(processed_paragraphs))
            f.write(TAG_EOD)
        print(f"      Saved: {safe_title}.txt")
        return file_path
    else:
        print("   No content extracted for this story")
        return None
    
def scrape_urdu_point(start_page, end_page):
    driver = get_driver()
    try:
        # Step 1: Collect all story links first
        print("=== STEP 1: Collecting all story links ===")
        story_links = collect_story_links(driver, start_page, end_page)
        print(f"\nTotal links collected: {len(story_links)}")
        
        # Step 2: Scrape each story
        print("\n=== STEP 2: Scraping individual stories ===")
        for i, url in enumerate(story_links, 1):
            print(f"\n--- Story {i}/{len(story_links)} ---")
            try:
                scrape_story(driver, url)
                time.sleep(random.uniform(1, 2))  # Be polite between requests
            except Exception as e:
                print(f"   Error scraping {url}: {str(e)}")
                continue
        
        print(f"\n=== Scraping Complete! ===")
        print(f"Links saved to: {LINKS_FILE}")
        print(f"Stories saved to: {OUTPUT_DIR}/")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_urdu_point(1, 1)