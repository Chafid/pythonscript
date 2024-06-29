from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
import json
import html

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Set up the driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the page
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
driver.get(url)

try:
    # Wait for a key element to be present (adjust the selector as needed)
    element = WebDriverWait(driver, 20)
    print("Page is ready!")

    # Get the rendered HTML
    html_content = driver.page_source
    
    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    result = soup.find_all('script')
    json_object = json.loads(result[4].text)
    ranking = 1
    for movies in json_object['itemListElement']:
        #convert if there are any ' character in the title
        movie_name = html.unescape(movies['item']['name'])
        rating = movies['item']['aggregateRating']['ratingValue']
        if ('alternateName' in movies['item']):
            movie_name_alt = html.unescape(movies['item']['alternateName'])
            print(ranking, movie_name, ". Also known as: ",  movie_name_alt, rating)
        else:
            print(ranking, movie_name, rating)
        ranking = ranking + 1

except TimeoutException:
    print("Loading took too much time!")

finally:
    # Close the browser
    driver.quit()