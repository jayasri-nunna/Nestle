import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import spacy
import re

options = webdriver.ChromeOptions()
#Adding local chrome profile path so that the cookies and captcha verification data is saved
options.add_argument(r"--user-data-dir=/Users/manoharcheabrolu/Library/Application Support/Google/Chrome/Default")
driver = webdriver.Chrome(options=options)

#Search for google.com
driver.get("https://www.google.com/")
#Expand the browser to fit the screen
driver.maximize_window()
#Assigning a wait variable to use in script
wait = WebDriverWait(driver, 5)

#Try and except for handling cookies
try:
    driver.find_element(By.XPATH, "//button[@id='L2AGLb']").click()
except:
    print("no cookies")

#Locate the search box by ID
search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='APjFqb']")))
#add the term automation in the search box
search_box.send_keys("automation")
#click enter to start the search
search_box.send_keys(Keys.RETURN)

#try block to check for recaptcha and solve it manually only once if it appears, this data will be stored in local profile
try:
    captcha_present = wait.until(
        EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
    )
    print("CAPTCHA detected! solve it manually.")
    time.sleep(100)
except:
    print("No CAPTCHA detected. Proceeding.")

#find wikipedia url and click on it
wikipedia_link = driver.find_element(By.PARTIAL_LINK_TEXT, "wikipedia")
wikipedia_link.click()

# Load the English model
nlp = spacy.load("en_core_web_sm")

page_text = driver.find_element(By.TAG_NAME, "body").text
# Process the text
doc = nlp(page_text)

# Regex pattern to find years (simple pattern for numbers, optionally followed by BC or AD)
year_pattern = re.compile(r'(\d{3,4})(?:\s*(BC|AD))?', re.IGNORECASE)
earliest_year = None
earliest_sentence = None
#used sents to iterate over the sentences processed by the en_core_web_sm english model and processed the whole page text in doc variable
for sent in doc.sents:
    match = year_pattern.search(sent.text)
    if match:
        year_str, era = match.groups()
        try:
            year_num = int(year_str)
            if era.upper() == 'BC':
                year_num = -year_num  # BC → negative

            if earliest_year is None or year_num < earliest_year:
                earliest_year = year_num
                earliest_sentence = sent.text


        except ValueError:
            continue  # Skip if year_str isn't a number

if earliest_sentence:
    print("Earliest automatic process:", earliest_sentence.strip())
else:
    print("No valid year with era found.")
