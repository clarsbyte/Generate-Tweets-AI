from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

class GetTweets:

    
    def __init__(self, username):
        self.username = username.lower()
        #self.service = Service(self.PATH)
        self.target_url = f'https://nitter.net/{self.username}'
        self.collected_tweets = [] 
        self.processed_tweet_ids = set()  
        
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--headless=new')  
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def wait_for_tweets_to_load(self, driver, timeout=30):
        """Wait for tweets to load before scraping."""
        try:
            print("Waiting for page to load...")
            wait = WebDriverWait(driver, timeout)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            
            time.sleep(5)
            
            timeline_items = driver.find_elements(By.CLASS_NAME, 'timeline-item')
            if timeline_items:
                print(f"Found {len(timeline_items)} timeline items")
                return True
            
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article')))
                return True
            except TimeoutException:
                 print("Timeout waiting for articles to load")
                 return False
            
        except TimeoutException:
            print("Timeout waiting for page to load")
            return False

    def generate_tweet_id(self, tweet_text, username):
        """Generate a simple ID for tweet deduplication."""
        return f"{username}_{hash(tweet_text[:50])}"

    def collect_new_tweets(self, driver):
        """Collect new tweets from the current page state."""
        new_tweets = []
        articles = driver.find_elements(By.CLASS_NAME, 'timeline-item')
        
        for article in articles:
            try:
                article_html = article.get_attribute('outerHTML')
                soup = BeautifulSoup(article_html, 'html.parser')
                
                username_element = soup.find('a', {'class': 'username'})
                if not username_element:
                    continue
                    
                username = username_element.text
                if username.lower() != f'@{self.username.lower()}':
                    continue
                
                tweet_text_element = soup.find('div', {'class': 'tweet-content'})
                if not tweet_text_element:
                    continue
                    
                tweet_text = tweet_text_element.get_text(strip=True)
                
                if not tweet_text or len(tweet_text) < 3:
                    continue
                    
                if tweet_text.lower().startswith('rt @') and len(tweet_text.split()) < 5:
                    continue
                
                tweet_id = self.generate_tweet_id(tweet_text, username)
                
                if tweet_id in self.processed_tweet_ids:
                    continue
                
                tweet_data = {
                    'user': username,
                    'text': tweet_text,
                    'tweet_id': tweet_id,
                    'tweet_number': len(self.collected_tweets) + len(new_tweets) + 1
                }
                
                new_tweets.append(tweet_data)
                self.processed_tweet_ids.add(tweet_id)
                
            except Exception as e:
                continue
        
        return new_tweets

    def click_load_more_button(self, driver):
        """Click the 'Load more' button if it exists."""
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            load_more_selectors = [
                "div.show-more a", 
                "//div[contains(@class, 'show-more')]//a[contains(text(), 'Load more')]",  
            ]
            
            for i, selector in enumerate(load_more_selectors):
                try:
                    if i == 0:  
                        elements = driver.find_elements(By.CSS_SELECTOR, selector)
                    else: 
                        elements = driver.find_elements(By.XPATH, selector)
                    
                    if elements:
                        element = elements[0]
                        print(f"Found load more element with selector: {selector}")
                        print(f"Element text: '{element.text}', visible: {element.is_displayed()}, enabled: {element.is_enabled()}")
                        
                        if element.is_displayed() and element.is_enabled():
                            driver.execute_script("arguments[0].scrollIntoView(true);", element)
                            time.sleep(1)
                            
                            try:
                                before_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
                                element.click()
                                print(f"Successfully clicked load more button: {element.text}")
                                print(f"Timeline items before click: {before_count}")
                                
                                time.sleep(6)  
                                after_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
                                print(f"Timeline items after click: {after_count}")
                                
                                if after_count > before_count:
                                    return True
                                else:
                                    return False
                                    
                            except ElementClickInterceptedException:
                                before_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
                                driver.execute_script("arguments[0].click();", element)
                                
                                time.sleep(6)
                                after_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
                                
                                if after_count > before_count:
                                    print(f"Click successful! Added {after_count - before_count} new items")
                                    return True
                                else:
                                    print("Click succeeded but no new content loaded")
                                    return False
                        else:
                            print(f"Element found but not clickable (visible: {element.is_displayed()}, enabled: {element.is_enabled()})")
                except Exception as e:
                    print(f"Error with selector {selector}: {e}")
                    continue
            
            print("No clickable 'Load more' button found")
            return False
            
        except Exception as e:
            print(f"Error clicking load more button: {e}")
            return False

    def load_more_tweets(self, driver, target_count=23):
        """Load more tweets until we have enough valid ones, collecting tweets at each step."""
        attempts = 0
        max_attempts = 10 
        
        initial_tweets = self.collect_new_tweets(driver)
        self.collected_tweets.extend(initial_tweets)
        
        while attempts < max_attempts and len(self.collected_tweets) < target_count:
            print(f"Attempt {attempts + 1}: Current total: {len(self.collected_tweets)} tweets")
            
            initial_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
            
            clicked_load_more = self.click_load_more_button(driver)
            
            if not clicked_load_more:
                for i in range(3):
                    driver.execute_script("window.scrollBy(0, 800);")
                    time.sleep(1)
            
            time.sleep(3)
            new_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
            
            new_tweets = self.collect_new_tweets(driver)
            if new_tweets:
                self.collected_tweets.extend(new_tweets)
                print(f"Collected {len(new_tweets)} new tweets. Total: {len(self.collected_tweets)}")
                
            else:
                print("No new tweets collected in this attempt")
            
            if new_count == initial_count:
                print(f"No new timeline items loaded after attempt {attempts + 1}")
                for i in range(5):
                    driver.execute_script("window.scrollBy(0, 1000);")
                    time.sleep(0.5)
                time.sleep(2)
                
                extra_tweets = self.collect_new_tweets(driver)
                if extra_tweets:
                    self.collected_tweets.extend(extra_tweets)
                    print(f"Extra scrolling yielded {len(extra_tweets)} more tweets")
                else:
                    final_count = len(driver.find_elements(By.CLASS_NAME, 'timeline-item'))
                    if final_count == new_count:
                        print("No more content available - reached end of timeline")
                        break
            else:
                print(f"Loaded {new_count - initial_count} new timeline items")
            
            attempts += 1
            
            if len(self.collected_tweets) >= target_count:
                print(f"Target reached! Collected {len(self.collected_tweets)} tweets")
                break
        
        print(f"Final result: {len(self.collected_tweets)} tweets after {attempts} attempts")
        return len(self.collected_tweets)

    def save_tweets_to_file(self, tweets_data, filename=None):
        """Save tweets data to a JSON file."""
        if filename is None:
            filename = f'tweets.json'
            
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets_data, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(tweets_data)} tweets to {filename}")

    def get(self, target_count=23):
        try:
            self.driver.get(self.target_url)
            
            if not self.wait_for_tweets_to_load(self.driver):
                print("Failed to load initial tweets")
                return
            
            final_count = self.load_more_tweets(self.driver, target_count=target_count)
            
            if len(self.collected_tweets) > target_count:
                self.collected_tweets = self.collected_tweets[:target_count]
                print(f"Trimmed to target count: {len(self.collected_tweets)} tweets")
            
            if self.collected_tweets:
                self.save_tweets_to_file(self.collected_tweets)
                print(f"Successfully scraped {len(self.collected_tweets)} valid tweets from @{self.username}")
                
                for i, tweet in enumerate(self.collected_tweets[:5], 1):
                    print(f"{i}. {tweet['text'][:100]}...")
                if len(self.collected_tweets) > 5:
                    print(f"... and {len(self.collected_tweets) - 5} more tweets")
            else:
                print(f"No valid tweets from @{self.username} found")
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()
            print("Browser closed")