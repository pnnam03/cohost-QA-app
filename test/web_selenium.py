from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set the path to the Microsoft Edge WebDriver executable
edge_driver_path = 'msedgedriver.exe'

# Create an instance of the WebDriver
driver = webdriver.Edge(service=Service(edge_driver_path))

# Now you can use the 'driver' object to automate Microsoft Edge
base_url = 'https://totheweb.com/learning_center/tools-convert-html-text-to-plain-text-for-content-review/'
driver.get(base_url)
driver.implicitly_wait(5)
urls = []

# read the urls
with open('url.txt', 'r') as file:
    urls = file.readlines()
urls = [url.strip() for url in urls]

# this is for debug
print('number of urls: ',len(urls))

# find_element
search_box = driver.find_element(By.ID, "url")
search_button = driver.find_element(By.ID, 'submit')

# send first key to proc the captcha
driver.implicitly_wait(1)
search_box.send_keys('')

# wait till user finished captcha
while True:
    key = input('Press any key to continue ...')
    if key != '':
        break

# this is for debug
print(len(urls))


# main function to request data
for url in urls:
    # print this for debug
    print(url)

    # clear the search_box and add new query
    search_box.clear()
    driver.implicitly_wait(0.5)
    search_box.send_keys(f'{url}')
    driver.implicitly_wait(0.5)

    search_button.click()
    driver.implicitly_wait(5)


    # get the result
    page_text_result = driver.find_element(By.ID, 'page-text-result')
    text = page_text_result.text
    # print(text)

    if not os.path.exists("text/"):
        os.mkdir("text/")

    local_domain = "new_cohost.vn"
    if not os.path.exists("text/"+local_domain+"/"):
        os.mkdir("text/" + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists("processed"):
        os.mkdir("processed")

    print('1-st step done')
    fname = 'text/'+local_domain+'/'+url[len('https://'):].replace("/", "_") + ".txt"
    with open(fname, "w", encoding='utf-8') as file:
        file.write(text)
    print('2-nd step done')
    time.sleep(10)

print('end process')
time.sleep(1000)
    # searchBox.send_keys(Keys.RETURN)


# recaptcha-checkbox-checked