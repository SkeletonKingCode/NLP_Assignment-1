# Gemini:

## 1

~~~prompt
You are are a Data Science and Scraping expert.
I am using firefox on Ubuntu 24.04 Linux. I want to scrap urdu children stories from urdupoint. What are the best tools for this?
~~~

## 2

~~~prompt
This is the html for the stories list page and an example story page write a python script to scrap data of these stories into text along appending tags, <EOS> end of sentence, <EOP> end of paragraph and <EOP> end of story
>>HTML of "Moral Stories Page" and "Garor ki Saza"
~~~

## 3

~~~prompt
Yes, thank you for correcting my EOD mistake
https://www.urdupoint.com/kids/category/moral-stories-page1.html
Link, pages increase -page1 -> -page2 -> -page3-> ... -> -page100
~~~


## 4

~~~prompt
Save the all the links in a file too
~~~


## 5

~~~prompt
The script did not get anything nor give error, I think it was stopped by cloudflare, use undetected selenium webdriver to bypass it.
~~~


## 6

~~~prompt
It is going to links and saving the links but either the text is not getting extracted or it is not saving properly:
```python
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
TAG_EOS = " <EOS>" # End of Sentence
TAG_EOP = " <EOP>" # End of Paragraph
TAG_EOD = " <EOD>" # End of Story

# Urdu Sentence Punctuation Regex (Full stop, Question mark, Exclamation)
URDU_PUNCT_REGEX = r'([۔؟!])'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_urdu_text(text):
    """Splits text into sentences and appends <EOS> tags."""
    if not text: return ""
    # Split by punctuation but keep the mark
    parts = re.split(URDU_PUNCT_REGEX, text)
    sentences = []
    for i in range(0, len(parts) - 1, 2):
        sentence = parts[i].strip() + parts[i+1]
        if sentence:
            sentences.append(sentence + TAG_EOS)
    
    # Catch trailing text without punctuation
    if len(parts) % 2 != 0 and parts[-1].strip():
        sentences.append(parts[-1].strip() + TAG_EOS)
        
    return " ".join(sentences)

def get_driver():
    """Initializes the undetected chrome driver."""
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox") # Required for some Ubuntu environments
    options.add_argument("--disable-dev-shm-usage")
    # Uncomment the next line if you want the window to be invisible:
    # options.add_argument("--headless") 
    
    driver = uc.Chrome(options=options)
    return driver

def scrape_urdu_point(start_page, end_page):
    driver = get_driver()
    
    try:
        with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
            for page_num in range(start_page, end_page + 1):
                print(f"\n--- 📄 Navigating to List Page {page_num} ---")
                list_url = LIST_URL_TEMPLATE.format(page_num)
                
                driver.get(list_url)
                # Random sleep to mimic human behavior
                time.sleep(random.uniform(3, 6)) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                # Find links with class 'sharp_box' as identified in your HTML
                story_links = soup.find_all('a', class_='sharp_box')
                
                if not story_links:
                    print("⚠️ No links found. Cloudflare might be blocking or selectors changed.")
                    continue

                for link in story_links:
                    href = link.get('href')
                    if not href: continue
                    full_url = href if href.startswith('http') else BASE_URL + href
                    
                    # Log the link
                    links_log.write(full_url + "\n")
                    links_log.flush()

                    # Visit the story page
                    print(f"   📖 Scraping: {full_url}")
                    driver.get(full_url)
                    time.sleep(random.uniform(0,.5))
                    
                    story_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Extract Title
                    title_tag = story_soup.find('h1')
                    title = title_tag.get_text(strip=True) if title_tag else "Untitled"

                    # Content is usually in 'detail_text_ads'
                    content_div = story_soup.find('div', class_='detail_text_ads')
                    if not content_div: continue

                    # Find paragraphs using 'urdu' or 'ar-huruf' classes
                    p_tags = content_div.find_all(['p', 'span'], class_=re.compile(r'urdu|ar-huruf'))
                    
                    processed_paragraphs = []
                    for p in p_tags:
                        txt = p.get_text(strip=True)
                        if len(txt) > 20:
                            processed_txt = process_urdu_text(txt)
                            processed_paragraphs.append(processed_txt + TAG_EOP)

                    if processed_paragraphs:
                        # Save result
                        filename = "".join(x for x in title[:50] if x.isalnum() or x==' ').strip()
                        file_path = os.path.join(OUTPUT_DIR, f"{filename}.txt")
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(f"TITLE: {title}\n")
                            f.write("\n".join(processed_paragraphs))
                            f.write(TAG_EOD)
                        
                    # Delay between stories
                    time.sleep(random.uniform(1, 2))

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_urdu_point(1, 100)
```
do you need the example html structure again?

~~~


## 7

~~~prompt
>>HTML of "Garor ki Saza" again
~~~



## 8

~~~prompt
Titles and article number <h2 class="urdu fs24 lh48 ar rtl txt_blue"><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">غرور کی سزا</span> - <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">تحریر نمبر</span> 2922</h2>

All paragraphs are in <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;"> urdu-text</span>, title in 
~~~

## 9 New Chat

~~~prompt
You are an data scraping and python expert.
Complete python script to scrap data of these stories into text along appending tags, <EOS> end of sentence use function, <EOP> end of paragraph since each span is a paragraph use that and <EOD> end of story  . Print the title and 1st span so I know if the code it working:

Title Tag:
```html
<h1 class="phead">Gharoor Ki Saza - Article No. 2922</h1>
```

Story Paragraph exact tags and css:
```html
<div id="main_wrap">
    <div class="container" id="main_content">
        <div class="main_bar">
            <div class="shad_box mb10">
                <div class="txt_detail urdu ar rtl">
                    <div style="text-align: right;">
                        <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">احسن ساتویں جماعت کا طالب علم تھا۔وہ اپنے ماں باپ کے ساتھ دریا کنارے چھوٹے سے گھر میں رہتا تھا۔وہ لوگ بہت غریب تھے۔احسن کے ابو ایک معمولی مچھیرے تھے۔وہ دن بھر مچھلیاں پکڑتے، مگر ان کے ہاتھ بہت کم مچھلیاں آتی تھیں۔کبھی تو ان کے گھر میں فاقے بھی ہو جاتے تھے۔</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
```

```python
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

# Urdu Sentence Punctuation Regex
URDU_PUNCT_REGEX = r'([۔؟!])'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def process_urdu_text(text):
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

def get_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox") 
    options.add_argument("--disable-dev-shm-usage")
    # Using windowed mode helps bypass initial Cloudflare checks
    driver = uc.Chrome(options=options)
    return driver

def scrape_urdu_point(start_page, end_page):
    driver = get_driver()
    try:
        with open(LINKS_FILE, "a", encoding="utf-8") as links_log:
            for page_num in range(start_page, end_page + 1):
                print(f"\n--- Story List Page {page_num} ---")
                driver.get(LIST_URL_TEMPLATE.format(page_num))
                time.sleep(random.uniform(4, 6)) 
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                story_links = soup.find_all('a', class_='sharp_box')
                
                for link in story_links:
                    href = link.get('href')
                    if not href: continue
                    full_url = href if href.startswith('http') else BASE_URL + href
                    
                    links_log.write(full_url + "\n")
                    links_log.flush()

                    print(f"   Scraping: {full_url}")
                    driver.get(full_url)
                    # Wait for Urdu font scripts to render
                    time.sleep(random.uniform(3, 5))
                    
                    story_soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    ### Write Text extraction Code

                    if processed_paragraphs:
                        safe_title = "".join(x for x in title[:50] if x.isalnum() or x==' ').strip()
                        file_path = os.path.join(OUTPUT_DIR, f"{safe_title}.txt")
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(f"TITLE: {title}\n\n")
                            f.write("\n".join(processed_paragraphs))
                            f.write(TAG_EOD)
                        print(f"      ✅ Saved: {safe_title}.txt")

                    time.sleep(random.uniform(1, 2))
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_urdu_point(1, 100)
```
~~~

# DeepSeek:

## 1

~~~prompt
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
    options.page_load_strategy("eager")
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
                    # Option 1: If the structure is exactly as shown
                
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

Change the code so it use selenium instead of beautiful soup for parsing
~~~

---

## 2

~~~prompt
--- Story List Page 1 ---
   Scraping: https://www.urdupoint.com/kids/detail/moral-stories/allah-ka-dost-2923.html
Allah Ka Dost - Article No. 2923
Found 0 spans
Traceback (most recent call last):
  File "/home/syedmalyun/Code/Semester-6/NLP/Theory/Assignments/Assignment-1/Scraping/scarper.py", line 125, in <module>
    scrape_urdu_point(1, 100)
  File "/home/syedmalyun/Code/Semester-6/NLP/Theory/Assignments/Assignment-1/Scraping/scarper.py", line 66, in scrape_urdu_point
    href = link.get_attribute('href')
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/syedmalyun/Applications/miniconda/envs/urdu-scraper/lib/python3.11/site-packages/selenium/webdriver/remote/webelement.py", line 213, in get_attribute
    attribute_value = self.parent.execute_script(
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/syedmalyun/Applications/miniconda/envs/urdu-scraper/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 518, in execute_script
    return self.execute(command, {"script": script, "args": converted_args})["value"]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/syedmalyun/Applications/miniconda/envs/urdu-scraper/lib/python3.11/site-packages/selenium/webdriver/remote/webdriver.py", line 432, in execute
    self.error_handler.check_response(response)
  File "/home/syedmalyun/Applications/miniconda/envs/urdu-scraper/lib/python3.11/site-packages/selenium/webdriver/remote/errorhandler.py", line 232, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.StaleElementReferenceException: Message: stale element reference: stale element not found
  (Session info: chrome=145.0.7632.75); For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception
Stacktrace:
#0 0x5dd891486cca <unknown>
#1 0x5dd890e96682 <unknown>
#2 0x5dd890eab09b <unknown>
#3 0x5dd890ea9b31 <unknown>
#4 0x5dd890e9e1b9 <unknown>
#5 0x5dd890e9e2f3 <unknown>
#6 0x5dd890e9c369 <unknown>
#7 0x5dd890ea0339 <unknown>
#8 0x5dd890f350d9 <unknown>
#9 0x5dd890f3404b <unknown>
#10 0x5dd890edd88f <unknown>
#11 0x5dd890ede651 <unknown>
#12 0x5dd89144b119 <unknown>
#13 0x5dd89144e021 <unknown>
#14 0x5dd8914378d9 <unknown>
#15 0x5dd89144ebee <unknown>
#16 0x5dd89141dc50 <unknown>
#17 0x5dd891473318 <unknown>
#18 0x5dd8914734e8 <unknown>
#19 0x5dd891485313 <unknown>
#20 0x77a5ada9caa4 <unknown>
#21 0x77a5adb29c6c <unknown>
~~~

---

## 3

~~~prompt
It is only getting the Author name, instead of using span get the whole text from the div and separate paragraphs perhaps by '\n' or  another method. Make sure it correctly inserts the special tokens for end of sentence, paragraph and story
```output
...
--- Story 1/12 ---
   Scraping: https://www.urdupoint.com/kids/detail/moral-stories/allah-ka-dost-2923.html
   Title: Allah Ka Dost - Article No. 2923
   Found 3 elements with selector: div[style='text-align: right;'] span
[<undetected_chromedriver.webelement.WebElement (session="440805419d6a73865b151b5be6895805", element="f.C23D8A7DBAE58338540F5ED2286C22D0.d.7C861B1C70569B22724CA30A5D891B78.e.221")>, <undetected_chromedriver.webelement.WebElement (session="440805419d6a73865b151b5be6895805", element="f.C23D8A7DBAE58338540F5ED2286C22D0.d.7C861B1C70569B22724CA30A5D891B78.e.222")>, <undetected_chromedriver.webelement.WebElement (session="440805419d6a73865b151b5be6895805", element="f.C23D8A7DBAE58338540F5ED2286C22D0.d.7C861B1C70569B22724CA30A5D891B78.e.223")>]
   [DEBUG] 1st Paragraph Preview: محمد شاہد حفیظ <EOS> <EOP>...
      Saved: Allah Ka Dost  Article No 2923.txt
...
```
<div id="main_wrap">
    <div class="container" id="main_content">
        <div class="main_bar">
            <div class="shad_box mb10">
                <div class="txt_detail urdu ar rtl">
                    <div style="text-align: right;"><span style="color: rgb(255, 0, 0); --darkreader-inline-color: var(--darkreader-text-ff0000, #ff2727);" data-darkreader-inline-color=""><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">محمد شاہد حفیظ</span></span><br><span style="color: rgb(255, 0, 0); --darkreader-inline-color: var(--darkreader-text-ff0000, #ff2727);" data-darkreader-inline-color=""></span><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میں ایک استاد ہوں اور میرا مضمون اسلامیات ہے۔نئے اسکول میں آج میرا پہلا دن تھا۔اسی وجہ سے خوشی بھی تھی اور ڈر بھی۔اسی خوشی میں، میں نے ناشتہ بھی برائے نام کیا اور وقت سے کچھ دیر پہلے ہی اسکول پہنچ گیا۔پرنسپل صاحب سے ملنے کے بعد مجھے ایک کلاس میں بھیج دیا گیا۔</span><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">کلاس روم میں خوب شور ہو رہا تھا۔تمام بچے اپنی عادت و فطرت کے مطابق زور زور سے باتیں کر رہے تھے۔میں نے کمرے میں قدم رکھا تو سب کو سانپ سونگھ گیا۔سب کے سب خاموشی سے سیدھے بیٹھ گئے۔پھر اچانک کلاس کی دائیں جانب سے</span> ”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">کلاس اسٹینڈ</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">کی آواز گونجی۔یہ یقینا کلاس مانیٹر تھا۔اس کی آواز سن کر سب بچے با ادب کھڑے ہو گئے۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">سِٹ ڈاؤن پلیز۔</span><p></p><p class="hide_desk ac urdu rtl fs18 lh36" style="color: rgb(102, 102, 102); --darkreader-inline-color: var(--darkreader-text-666666, #fcf0e0);" data-darkreader-inline-color="">(<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">جاری ہے</span>)</p><div id="teads_upw"><div id="teads"></div></div>


<div class="clear"></div>
<div align="center" style="text-align:center; padding-top:0px;padding-bottom:0px; margin:0 auto;">
	<div id="div-gpt-ad-outstream-wrap"><div id="div-gpt-ad-outstream"></div></div>
    <div id="div-gpt-ad-1x1-wrap"><div id="div-gpt-ad-1x1"></div></div>
</div>
<div class="clear"></div>

<script>
	document.getElementById("teads_upw").innerHTML = '<div id="teads"></div>';
	
	document.getElementById("div-gpt-ad-outstream-wrap").innerHTML = '<div id="div-gpt-ad-outstream"></div>';
	document.getElementById("div-gpt-ad-1x1-wrap").innerHTML = '<div id="div-gpt-ad-1x1"></div>';
	
	googletag.cmd.push(function() { googletag.display("div-gpt-ad-outstream"); });
	googletag.cmd.push(function() { googletag.display("div-gpt-ad-1x1"); });
</script><div id="eng_mob_ad_wrap"><script>
	if(upgj_x <= 800){
		//googletag.defineSlot('/21678054/up-v2/mobile-middle', [300, 250], 'gpt-middle-banner').addService(googletag.pubads());
		document.getElementById("div-gpt-ad-outstream-wrap").innerHTML = '<div id="gpt-middle-banner-in"><div id="gpt-middle-banner"></div></div>';
		googletag.cmd.push(function() { googletag.display('gpt-middle-banner'); });
	}
</script></div><p style="margin-top:0px;">“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میں نے ہاتھ سے اشارہ کرتے ہوئے کہا۔</span></p><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">سب بیٹھ گئے۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">شاید آپ جانتے ہوں کہ اب، میں آپ کو اسلامیات پڑھایا کروں گا۔</span>“<br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">یس سر</span>!“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">چند بچوں کی آواز آئی۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">آج پہلی بار آپ کی کلاس لے رہا ہوں، اسی لئے آج کچھ نہیں پڑھاؤں گا۔پہلے میں اپنا تعارف کراؤں گا، پھر ایک ایک کر کے آپ سب کے بارے میں جاننا چاہوں گا۔</span>“<br><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">استاد کا شاگردوں سے بڑا گہرا تعلق ہوتا ہے۔استاد معلم ہے اور اس کا کام علم و آگہی دینا ہے۔</span><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">یہی کام گھر میں ماں باپ بھی کرتے ہیں۔اسی لحاظ سے کہا جاتا ہے کہ استاد باپ کی جگہ ہوتا ہے، لیکن میرے نزدیک استاد ہی بہترین دوست ہے۔شاگردوں کو استاد کا احترام کرتے ہوئے اس سے بے تکلف بھی ہونا چاہیے، تاکہ وہ اپنے مسائل پر استاد سے بات کر سکیں۔اس سے مشورہ کر سکیں اور استاد ان کی راہنمائی کر سکے۔چند لمحے کلاس میں خاموشی چھائی رہی پھر کچھ ملی جلی آوازیں اُبھریں۔</span><div class="clear mt2"></div><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">تھینک یو سر</span>!“<br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اب میں اپنا تعارف کرا دوں۔میرا نام شہاب حیدر ہے۔صحافت میں ایم اے کیا ہے، مگر عملی طور پر تدریسی میدان میں آ گیا۔پڑھانا میرا شوق ہی نہیں، بلکہ اس سے مجھے دلی اطمینان ہوتا ہے۔میں نے اسلامیات کا مضمون اس لئے منتخب کیا ہے کہ آپ کو حقیقی اسلام سے آگاہ کروں اور آپ کو محبِ وطن شہری بناؤں۔اب آپ لوگ باری باری اپنا تعارف کرا دیں۔</span><div class="clear mt2"></div>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میں نے پہلی قطار میں داہنی جانب بیٹھے لڑکے کی طرف اشارہ کیا۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">سر</span>! <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میرا نام عمر احمد ہے۔میرے ابو کا نام حیات احمد ہے۔وہ ایک بینک منیجر ہیں۔</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اس کے والد کا سن کر ساری کلاس پر رعب طاری ہو گیا۔اتنے میں دوسرا لڑکا کھڑا ہو گیا۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">سر</span>! <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میرا نام حمزہ ہے۔میرے ابو ایک پرائیویٹ فرم میں جنرل منیجر ہیں۔</span>“<br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اوہ</span>.... <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">یہ بھی منیجر</span>․․․․“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میرے منہ سے نکلا۔</span><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اس کے بعد تیسرا لڑکا کھڑا ہوا۔وہ بھی پہلے دونوں سے کم نظر نہیں آ رہا تھا۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">مجھے ذیشان کہتے ہیں۔میرے ابو ایک تاجر ہیں ان کا کپڑے کا کاروبار ہے۔</span>“<br><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">ان سب کے تعارف میں حیران کن بات ان کا خاندانی پس منظر تھا، جسے وہ فخریہ انداز میں بیان کر رہے تھے۔یہ بات مجھے اچھی نہ لگی۔آگے بھی تعارف ہوا تو تمام لڑکے اعلیٰ اور کھاتے پیتے گھرانوں کے چشم و چراغ ثابت ہوئے، کیونکہ یہ ایک مہنگا اور معیاری اسکول تھا۔</span><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">غریب لوگوں کے بچے تو اس کا صرف سوچ سکتے تھے۔ابھی انھی خیالوں میں مگن تھا کہ ایک لڑکا جو لائن کے آخری ڈیسک پر بیٹھا تھا، اُٹھ کھڑا ہوا۔اس کا چہرہ اعتماد سے خالی نظر آ رہا تھا۔میں نے اس سے تعارف کے لئے کہا تو وہ قدرے ہچکچاتے ہوئے بولا</span>:”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">سر</span>! <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میرا نام محمد علی ہے۔میرا تعلق ایک عام سے گھرانے سے ہے۔</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">کلاس کے تمام لڑکے اس کی طرف دیکھنے لگے تو وہ شرمندہ سا ہو گیا۔</span><div class="clear mt2"></div><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">آپ کے ابو کیا کام کرتے ہیں؟</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میں نے تجسس سے پوچھا۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">جی</span>․․․․․<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">جی</span>․․․․․<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">وہ</span>․․․․․ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اللہ کے دوست ہیں۔</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اس کا جواب سن کر کلاس میں قہقہے گونجنے لگے، مگر میری سنجیدگی دیکھ کر خاموش ہو گئے۔</span><br>”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">اللہ کے دوست</span>․․․․․<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">وہ کیسے</span>! <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">کیا آپ اس کی وضاحت کریں گے؟</span>“<br><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">جی وہ محنت مزدوری کرتے ہیں۔ہمارے نبی کریم صلی اللہ علیہ و آلہ وسلم کا ارشاد ہے کہ ہاتھ سے کمانے والا اللہ کا دوست ہے تو میرے ابو بھی اللہ کے دوست ہوئے، کیونکہ وہ اپنے ہاتھ سے کماتے ہیں۔</span><div class="clear mt2"></div><span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">وہ سارا دن محنت مزدوری کرتے ہیں، تاکہ میری فیس ادا کر سکیں اور مجھے بہتر سے بہتر تعلیم دلوا سکیں۔وہ کہتے ہیں تم خوب محنت کرو اور بڑے آدمی بننا۔اس کا جواب سن کر میں حیران رہ گیا۔اس قدر پختہ یقین کا بچہ دیکھ کر دل کو سکون ملا۔میں نے اسے شاباش دی اور پوری کلاس سے مخاطب ہوا</span>:”<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">واقعی ہاتھ سے کمانے والا اللہ کا دوست ہوتا ہے۔محنت کی عظمت اور برکت سے کون واقف نہیں ہے۔آپ کے ابو کا مقام بہت بلند ہے۔آپ کو اس پر فخر ہونا چاہیے۔کئی انبیائے کرام بھی اپنے ہاتھ کی کمائی کھایا کرتے تھے۔</span>“ <span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">میں نے محسوس کیا کہ میری بات کا پوری کلاس پر اثر ہو رہا ہے اور مجھے خوشی تھی کہ میں پوری کلاس کو محنت کی عظمت سمجھانے میں کامیاب ہوا۔</span></div>
                </div>
            </div>
        </div>
    </div>
</div>
~~~


---

## 4

~~~prompt
Almost perfect. here is the code for improving, Give me the complete final version with correcte data cleaning for non urdu characters
```python
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
    """Scrape a single story using BeautifulSoup on page source"""
    print(f"   Scraping: {url}")
    driver.get(url)
    time.sleep(random.uniform(3, 5))
    
    # Get page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # --- 1. Get the Title ---
    title_tag = soup.find('h1', class_='phead')
    title = title_tag.get_text(strip=True) if title_tag else "Untitled Story"
    print(f"   Title: {title}")
    
    # --- 2. Locate the main story container ---
    # Try multiple possible containers (based on observed structure)
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
    
    # --- 3. Extract paragraphs from the container ---
    # Convert the container to string and split by <br> tags to get paragraphs
    container_html = str(story_container)
    
    # Replace <br>, <br/>, </p> with a special marker (e.g., "||PARAGRAPH||")
    # Also handle <div class="clear"> which sometimes separates paragraphs
    for tag in ['<br>', '<br/>', '</p>', '<div class="clear']:
        container_html = container_html.replace(tag, '||PARAGRAPH||')
    
    # Now parse the modified HTML to get text
    temp_soup = BeautifulSoup(container_html, 'html.parser')
    raw_text = temp_soup.get_text()
    
    # Split by the marker to get paragraphs
    raw_paragraphs = [p.strip() for p in raw_text.split('||PARAGRAPH||') if p.strip()]
    
    # --- 4. Process each paragraph with sentence tags and add <EOP> ---
    processed_paragraphs = []
    for i, para in enumerate(raw_paragraphs):
        if para:
            # Process sentences (add <EOS>)
            p_text = process_urdu_text(para) + TAG_EOP
            processed_paragraphs.append(p_text)
            
            # Debug first paragraph
            if i == 0:
                print(f"   [DEBUG] 1st Paragraph Preview: {p_text[:100]}...")
    
    # --- 5. Save to file ---
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
        print("   No content extracted")
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
```

Just need to correct the post cleaning of the data as advertisements get in the way along with weird mb15, hidden content like:
<p class="hide_desk ac urdu rtl fs18 lh36" style="color: rgb(102, 102, 102); --darkreader-inline-color: var(--darkreader-text-666666, #fcf0e0);" data-darkreader-inline-color="">(<span class="ar-huruf nastaleeq3" style="font-size:1.25em; line-height:1.8em;">جاری ہے</span>)</p>
```Output
TITLE: Allah Ka Dost - Article No. 2923

mb15"> <EOS> <EOP>
mb15"> 
محمد شاہد حفیظ <EOS> <EOP>
میں ایک استاد ہوں اور میرا مضمون اسلامیات ہے۔ <EOS> نئے اسکول میں آج میرا پہلا دن تھا۔ <EOS> اسی وجہ سے خوشی بھی تھی اور ڈر بھی۔ <EOS> اسی خوشی میں، میں نے ناشتہ بھی برائے نام کیا اور وقت سے کچھ دیر پہلے ہی اسکول پہنچ گیا۔ <EOS> پرنسپل صاحب سے ملنے کے بعد مجھے ایک کلاس میں بھیج دیا گیا۔ <EOS> <EOP>
mt2">کلاس روم میں خوب شور ہو رہا تھا۔ <EOS> تمام بچے اپنی عادت و فطرت کے مطابق زور زور سے باتیں کر رہے تھے۔ <EOS> میں نے کمرے میں قدم رکھا تو سب کو سانپ سونگھ گیا۔ <EOS> سب کے سب خاموشی سے سیدھے بیٹھ گئے۔ <EOS> پھر اچانک کلاس کی دائیں جانب سے ”کلاس اسٹینڈ“ کی آواز گونجی۔ <EOS> یہ یقینا کلاس مانیٹر تھا۔ <EOS> اس کی آواز سن کر سب بچے با ادب کھڑے ہو گئے۔ <EOS> <EOP>
”سِٹ ڈاؤن پلیز۔ <EOS> <EOP>
(جاری ہے) <EOS> <EOP>
">


LIVEAn error occurred. Please try again laterTap to unmuteLearn moreAdvertisement <EOS> <EOP>
">
“ میں نے ہاتھ سے اشارہ کرتے ہوئے کہا۔ <EOS> <EOP>
mt2">سب بیٹھ گئے۔ <EOS> <EOP>
”شاید آپ جانتے ہوں کہ اب، میں آپ کو اسلامیات پڑھایا کروں گا۔ <EOS> “ <EOS> <EOP>
”یس سر! <EOS> “ چند بچوں کی آواز آئی۔ <EOS> <EOP>
”آج پہلی بار آپ کی کلاس لے رہا ہوں، اسی لئے آج کچھ نہیں پڑھاؤں گا۔ <EOS> پہلے میں اپنا تعارف کراؤں گا، پھر ایک ایک کر کے آپ سب کے بارے میں جاننا چاہوں گا۔ <EOS> “ <EOS> <EOP>
استاد کا شاگردوں سے بڑا گہرا تعلق ہوتا ہے۔ <EOS> استاد معلم ہے اور اس کا کام علم و آگہی دینا ہے۔ <EOS> <EOP>
mt2">یہی کام گھر میں ماں باپ بھی کرتے ہیں۔ <EOS> اسی لحاظ سے کہا جاتا ہے کہ استاد باپ کی جگہ ہوتا ہے، لیکن میرے نزدیک استاد ہی بہترین دوست ہے۔ <EOS> شاگردوں کو استاد کا احترام کرتے ہوئے اس سے بے تکلف بھی ہونا چاہیے، تاکہ وہ اپنے مسائل پر استاد سے بات کر سکیں۔ <EOS> اس سے مشورہ کر سکیں اور استاد ان کی راہنمائی کر سکے۔ <EOS> چند لمحے کلاس میں خاموشی چھائی رہی پھر کچھ ملی جلی آوازیں اُبھریں۔ <EOS> <EOP>
mt2"> <EOS> <EOP>
”تھینک یو سر! <EOS> “ <EOS> <EOP>
”اب میں اپنا تعارف کرا دوں۔ <EOS> میرا نام شہاب حیدر ہے۔ <EOS> صحافت میں ایم اے کیا ہے، مگر عملی طور پر تدریسی میدان میں آ گیا۔ <EOS> پڑھانا میرا شوق ہی نہیں، بلکہ اس سے مجھے دلی اطمینان ہوتا ہے۔ <EOS> میں نے اسلامیات کا مضمون اس لئے منتخب کیا ہے کہ آپ کو حقیقی اسلام سے آگاہ کروں اور آپ کو محبِ وطن شہری بناؤں۔ <EOS> اب آپ لوگ باری باری اپنا تعارف کرا دیں۔ <EOS> <EOP>
mt2">“ میں نے پہلی قطار میں داہنی جانب بیٹھے لڑکے کی طرف اشارہ کیا۔ <EOS> <EOP>
”سر! <EOS> میرا نام عمر احمد ہے۔ <EOS> میرے ابو کا نام حیات احمد ہے۔ <EOS> وہ ایک بینک منیجر ہیں۔ <EOS> “ اس کے والد کا سن کر ساری کلاس پر رعب طاری ہو گیا۔ <EOS> اتنے میں دوسرا لڑکا کھڑا ہو گیا۔ <EOS> <EOP>
”سر! <EOS> میرا نام حمزہ ہے۔ <EOS> میرے ابو ایک پرائیویٹ فرم میں جنرل منیجر ہیں۔ <EOS> “ <EOS> <EOP>
”اوہ.... یہ بھی منیجر․․․․“ میرے منہ سے نکلا۔ <EOS> <EOP>
mt2">اس کے بعد تیسرا لڑکا کھڑا ہوا۔ <EOS> وہ بھی پہلے دونوں سے کم نظر نہیں آ رہا تھا۔ <EOS> <EOP>
”مجھے ذیشان کہتے ہیں۔ <EOS> میرے ابو ایک تاجر ہیں ان کا کپڑے کا کاروبار ہے۔ <EOS> “ <EOS> <EOP>
ان سب کے تعارف میں حیران کن بات ان کا خاندانی پس منظر تھا، جسے وہ فخریہ انداز میں بیان کر رہے تھے۔ <EOS> یہ بات مجھے اچھی نہ لگی۔ <EOS> آگے بھی تعارف ہوا تو تمام لڑکے اعلیٰ اور کھاتے پیتے گھرانوں کے چشم و چراغ ثابت ہوئے، کیونکہ یہ ایک مہنگا اور معیاری اسکول تھا۔ <EOS> <EOP>
mt2">غریب لوگوں کے بچے تو اس کا صرف سوچ سکتے تھے۔ <EOS> ابھی انھی خیالوں میں مگن تھا کہ ایک لڑکا جو لائن کے آخری ڈیسک پر بیٹھا تھا، اُٹھ کھڑا ہوا۔ <EOS> اس کا چہرہ اعتماد سے خالی نظر آ رہا تھا۔ <EOS> میں نے اس سے تعارف کے لئے کہا تو وہ قدرے ہچکچاتے ہوئے بولا:”سر! <EOS> میرا نام محمد علی ہے۔ <EOS> میرا تعلق ایک عام سے گھرانے سے ہے۔ <EOS> “ کلاس کے تمام لڑکے اس کی طرف دیکھنے لگے تو وہ شرمندہ سا ہو گیا۔ <EOS> <EOP>
mt2"> <EOS> <EOP>
”آپ کے ابو کیا کام کرتے ہیں؟ <EOS> “ میں نے تجسس سے پوچھا۔ <EOS> <EOP>
”جی․․․․․جی․․․․․وہ․․․․․ اللہ کے دوست ہیں۔ <EOS> “ اس کا جواب سن کر کلاس میں قہقہے گونجنے لگے، مگر میری سنجیدگی دیکھ کر خاموش ہو گئے۔ <EOS> <EOP>
”اللہ کے دوست․․․․․وہ کیسے! <EOS> کیا آپ اس کی وضاحت کریں گے؟ <EOS> “ <EOS> <EOP>
جی وہ محنت مزدوری کرتے ہیں۔ <EOS> ہمارے نبی کریم صلی اللہ علیہ و آلہ وسلم کا ارشاد ہے کہ ہاتھ سے کمانے والا اللہ کا دوست ہے تو میرے ابو بھی اللہ کے دوست ہوئے، کیونکہ وہ اپنے ہاتھ سے کماتے ہیں۔ <EOS> <EOP>
mt2">وہ سارا دن محنت مزدوری کرتے ہیں، تاکہ میری فیس ادا کر سکیں اور مجھے بہتر سے بہتر تعلیم دلوا سکیں۔ <EOS> وہ کہتے ہیں تم خوب محنت کرو اور بڑے آدمی بننا۔ <EOS> اس کا جواب سن کر میں حیران رہ گیا۔ <EOS> اس قدر پختہ یقین کا بچہ دیکھ کر دل کو سکون ملا۔ <EOS> میں نے اسے شاباش دی اور پوری کلاس سے مخاطب ہوا:”واقعی ہاتھ سے کمانے والا اللہ کا دوست ہوتا ہے۔ <EOS> محنت کی عظمت اور برکت سے کون واقف نہیں ہے۔ <EOS> آپ کے ابو کا مقام بہت بلند ہے۔ <EOS> آپ کو اس پر فخر ہونا چاہیے۔ <EOS> کئی انبیائے کرام بھی اپنے ہاتھ کی کمائی کھایا کرتے تھے۔ <EOS> “ میں نے محسوس کیا کہ میری بات کا پوری کلاس پر اثر ہو رہا ہے اور مجھے خوشی تھی کہ میں پوری کلاس کو محنت کی عظمت سمجھانے میں کامیاب ہوا۔ <EOS> <EOP> <EOD>
```
~~~

---

## 5

~~~prompt
It Works! Now we just need to do final adjustments, since we are training a simple model remove all qoutation marks, don't just add <EOS> replace the ۔؟! 
~~~

---

## 6

~~~prompt
replace .... with " "
give me only that code
~~~

---

## 7

~~~prompt
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
                time.sleep(random.uniform(.5, 1))  # Be polite between requests
            except Exception as e:
                print(f"   Error scraping {url}: {str(e)}")
                continue

        print(f"\n=== Scraping Complete! ===")
        print(f"Links saved to: {LINKS_FILE}")
        print(f"Stories saved to: {OUTPUT_DIR}/")

    finally:
        driver.quit()
    driver.quit()

if __name__ == "__main__":
    # Start with page 1 only for testing; change as needed
    scrape_urdu_point(1, 1)

Instead of extracting all links and then moving to step 2 is it possible to extract a story link, scrap and save the story and move to the next
~~~
