import datetime
import re
import time

from click import argument
from selenium.common import NoSuchWindowException, NoSuchCookieException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Adding local chrome profile path so that the cookies and captcha verification data is saved
"""options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=/Users/manoharcheabrolu/Library/Application Support/Google/Chrome/Default")
driver = webdriver.Chrome(options=options)"""



driver = webdriver.Chrome()
driver.get("https://www.google.com/")
driver.maximize_window()

#Assigning 100sec timeout to solve recaptcha manually
wait = WebDriverWait(driver, 100)

#Try block for handling cookies
try:
    driver.find_element(By.XPATH, "//button[@id='L2AGLb']").click()
except NoSuchElementException:
    print("No cookies popup detected")


search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//textarea[@id='APjFqb']")))
search_box.send_keys("automation", Keys.RETURN)


#try block to check for recaptcha and solve it manually if it appears
try:
    driver.find_element(By.XPATH, "//iframe[@title='reCAPTCHA']")
    print("CAPTCHA detected! solve it manually.")
    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='logo']//*[name()='svg']")))

except NoSuchElementException:
    print("No CAPTCHA detected. Proceeding.")

#find wikipedia url and click on it
try:
    wikipedia_link = driver.find_element(By.PARTIAL_LINK_TEXT, "wikipedia.org")
    wikipedia_link.click()

    #Getting the whole page text into a variable
    page_text = driver.find_element(By.TAG_NAME, "body").text

    # Splitting sentences using regex on '.', '!', or '?' followed by whitespace or newline
    sentences = re.split(r'(?<=[.!?])\s+|\n+', page_text)

    # Find years with and without BC/AD
    year_pattern = re.compile(r'(\d{3,4})(?:\s*(BC|AD))?', re.IGNORECASE)

    earliest_year = None
    earliest_sentence = None


    for sent in sentences:
        match = year_pattern.search(sent)
        if match:
            year_str, era = match.groups()
            try:
                year_num = int(year_str)
                if era and era.upper() == 'BC':
                    year_num = -year_num  # BC → negative

                if earliest_year is None or year_num < earliest_year:
                    earliest_year = year_num
                    earliest_sentence = sent.strip()
            # skip if year_str is not a number
            except ValueError:
                continue

    #Step 4 : Taking screenshot
    timestamp = datetime.datetime.now()
    if earliest_sentence:
        try:
            # Try to locate the sentence inside a <p> or any tag that contains it
            paragraphs = driver.find_elements(By.TAG_NAME, "p")

            for para in paragraphs:
                if earliest_sentence in para.text:
                    driver.execute_script("arguments[0].scrollIntoView();", para)
                    break

            # Take full browser window screenshot and save it
            driver.save_screenshot(f"Earliest_year_sentence_{timestamp}.png")

        except NoSuchElementException:
            print("Could not locate the sentence on the page:")

    else:
        print("No valid year with era found.")
except NoSuchElementException:
    print("No wikipedia link found")
driver.quit()