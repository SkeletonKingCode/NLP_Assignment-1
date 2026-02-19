import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

# Urdu Unicode ranges (for detecting actual Urdu text)
URDU_UNICODE_RANGE = r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]'

# Common boilerplate / ad phrases to remove
BOILERPLATE_PHRASES = [
    "جاری ہے",
    "LIVEAn error occurred",
    "Advertisement",
    "Please try again later",
    "Tap to unmute",
    "Learn more"
]

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def contains_urdu(text):
    """Return True if the text contains at least one Urdu character."""
    return bool(re.search(URDU_UNICODE_RANGE, text))

def is_boilerplate(text):
    """Return True if the text matches any known boilerplate phrase."""
    text_clean = re.sub(r'\s+', '', text)  # remove whitespace for comparison
    for phrase in BOILERPLATE_PHRASES:
        if phrase in text_clean:
            return True
    return False

def clean_paragraph(raw_para):
    """
    Remove HTML artifacts and non-Urdu fragments from a paragraph string.
    Returns cleaned text or None if the paragraph should be discarded.
    """
    # Remove leading HTML-like remnants (e.g., 'mb15">')
    cleaned = re.sub(r'^[^>\s]*>', '', raw_para)
    cleaned = cleaned.strip()

    # Discard if empty or too short (less than 3 characters)
    if len(cleaned) < 3:
        return None

    # Discard if it contains no Urdu characters
    if not contains_urdu(cleaned):
        return None

    # Discard if it's known boilerplate
    if is_boilerplate(cleaned):
        return None

    return cleaned

def process_urdu_text(text):
    """
    Process Urdu text:
      1. Remove all quotation marks.
      2. Replace multiple dots (....) with a space.
      3. Replace Urdu punctuation (۔ ؟ !) with <EOS> (the punctuation is removed).
      4. Ensure the text ends with <EOS> if it doesn't already.
    Returns a string with sentences separated by <EOS>.
    """
    if not text:
        return ""

    # 1. Remove quotation marks (including curly quotes)
    quote_chars = '"\'"”“‘’'
    translator = str.maketrans('', '', quote_chars)
    text = text.translate(translator)

    # 2. Replace multiple dots (ellipsis) with a space
    text = re.sub(r'\․{1,}', ' ', text)
    text = re.sub(r'\.{1,}', ' ', text)

    # 3. Replace Urdu punctuation with <EOS>
    punct_marks = ['۔', '؟', '!']
    for punct in punct_marks:
        text = text.replace(punct, f' {TAG_EOS.strip()} ')

    # 4. Clean up extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # 5. Ensure the last sentence gets an <EOS> if missing
    if not text.endswith(TAG_EOS):
        text += TAG_EOS

    return text

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = "eager"
    driver = uc.Chrome(options=options)
    return driver

def collect_story_links(driver, start_page, end_page):
    """First collect all story links from all pages."""
    all_links = []

    for page_num in range(start_page, end_page + 1):
        print(f"\n--- Collecting links from Story List Page {page_num} ---")
        driver.get(LIST_URL_TEMPLATE.format(page_num))
        time.sleep(random.uniform(.5, 1))

        # Wait for the links to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sharp_box'))
        )

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
    """Scrape a single story using BeautifulSoup on page source."""
    print(f"   Scraping: {url}")
    driver.get(url)
    time.sleep(random.uniform(.5, 1))

    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # --- 1. Get the Title ---
    title_tag = soup.find('h1', class_='phead')
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Story"
    print(f"   Title: {title}")

    # --- 2. Locate the main story container ---
    story_container = None
    possible_containers = [
        ('div', {'class': 'txt_detail'}),
        ('div', {'style': 'text-align: right;'}),
        ('div', {'class': 'article_content'})
    ]
    for tag, attrs in possible_containers:
        story_container = soup.find(tag, attrs=attrs)
        if story_container:
            break

    if not story_container:
        print("   No story container found")
        return None

    # --- 3. Remove unwanted elements that contain boilerplate or ads ---
    # Remove elements with class 'hide_desk' (often contain "جاری ہے")
    for hidden in story_container.find_all(class_='hide_desk'):
        hidden.decompose()
    # Remove script tags and other noise
    for script in story_container.find_all(['script', 'ins', 'iframe']):
        script.decompose()

    # --- 4. Extract paragraphs by splitting on <br> and block elements ---
    # Convert container to string and insert paragraph markers at natural breaks
    container_html = str(story_container)

    # Replace <br> and </p> with a paragraph marker
    for tag in ['<br>', '<br/>', '</p>']:
        container_html = container_html.replace(tag, '||PARAGRAPH||')

    # Also handle <div class="clear"> which often separates paragraphs
    container_html = re.sub(r'<div\s+class="clear[^>]*>', '||PARAGRAPH||', container_html)

    # Now parse the modified HTML to get text
    temp_soup = BeautifulSoup(container_html, 'html.parser')
    raw_text = temp_soup.get_text()

    # Split by the marker to get raw paragraphs
    raw_paragraphs = [p.strip() for p in raw_text.split('||PARAGRAPH||') if p.strip()]

    # --- 5. Clean and filter paragraphs ---
    cleaned_paragraphs = []
    for para in raw_paragraphs:
        cleaned = clean_paragraph(para)
        if cleaned:
            cleaned_paragraphs.append(cleaned)

    # --- 6. Process each cleaned paragraph with sentence tags and add <EOP> ---
    processed_paragraphs = []
    for i, para in enumerate(cleaned_paragraphs):
        if para:
            # process_urdu_text now removes quotes and replaces punctuation with <EOS>
            p_text = process_urdu_text(para) + TAG_EOP
            processed_paragraphs.append(p_text)
            if i == 0:
                print(f"   [DEBUG] 1st Paragraph Preview: {p_text[:100]}...")

    # --- 7. Save to file ---
    if processed_paragraphs:
        title = re.sub(r'\s+', '+_', title)
        safe_title = "".join(x for x in title[:50] if x.isalnum() or x == '_').strip()
        if not safe_title:
            safe_title = f"story_{int(time.time())}"

        file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            # f.write(f"TITLE: {title}\n\n")
            f.write("".join(processed_paragraphs[1:]))
            f.write(TAG_EOD)
        print(f"      Saved: {safe_title}.txt")
        return file_path
    else:
        print("   No content extracted")
        return None

def scrape_urdu_point(start_page, end_page):
    driver = get_driver()
    try:
        print("=== Starting scraping (page-by-page, story-by-story) ===")
        for page_num in range(start_page, end_page + 1):
            list_url = LIST_URL_TEMPLATE.format(page_num)
            print(f"\n--- Processing Story List Page {page_num}: {list_url} ---")
            driver.get(list_url)
            time.sleep(random.uniform(.5, 1))

            # Wait for links to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.sharp_box'))
            )

            # Find all story links on this page and extract hrefs immediately
            story_elements = driver.find_elements(By.CSS_SELECTOR, 'a.sharp_box')
            hrefs = []
            for elem in story_elements:
                try:
                    href = elem.get_attribute('href')
                    if href:
                        full_url = href if href.startswith('http') else BASE_URL + href
                        hrefs.append(full_url)
                except:
                    continue

            print(f"Found {len(hrefs)} links on page {page_num}")

            # Process each URL
            for idx, url in enumerate(hrefs, 1):
                try:
                    print(f"\n   --- Story {idx} on page {page_num} ---")
                    # Log the link
                    with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
                        links_log.write(url + "\n")

                    # Scrape the story
                    scrape_story(driver, url)

                    # After scraping, navigate back to the list page
                    driver.back()
                    # Wait for the list page to reload before next iteration
                    time.sleep(random.uniform(1, 2))

                except Exception as e:
                    print(f"   Error processing {url}: {str(e)}")
                    # Try to recover by going back to the list page
                    try:
                        driver.get(list_url)
                        time.sleep(random.uniform(1, 2))
                    except:
                        pass
                    continue

        print(f"\n=== Scraping Complete! ===")
        print(f"Links saved to: {LINKS_FILE}")
        print(f"Stories saved to: {OUTPUT_DIR}/")

    finally:
        driver.quit()
        time.sleep(1)
        print("Quiting chromium")

if __name__ == "__main__":
    # Start with page 1 only for testing; change as needed
    scrape_urdu_point(1, 50)