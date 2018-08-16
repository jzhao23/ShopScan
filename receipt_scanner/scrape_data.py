#### PACKAGES ####
import time
import csv
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

####GLOBALS####
CHROME_DRIVER = '/Users/jasonzhao/Downloads/chromedriver'
WEBSITE = 'https://guide.ethical.org.au/company/?company=0'
URL_DATA = './data/url_list.csv'


#### OBTAIN LIST OF URLS TO SCRAPE ####
url_list = []

with open(URL_DATA, 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		url_list.append(str(row))

#### SET UP SELENIUM CHROMEDRIVER ####
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='/Users/jasonzhao/Downloads/chromedriver', chrome_options = option)

#### LOOP OVER EACH URL ####
for url in url_list:
	driver.get(url)
	time.sleep(10)
	print(driver.find_elements_by_tag_name('h1').text)



#loop over each url
#access info from each url
#open csv to write