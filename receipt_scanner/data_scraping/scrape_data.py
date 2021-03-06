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
URL_DATA = '../data/url_list.csv'


#### OBTAIN LIST OF URLS TO SCRAPE ####
url_list = []

with open(URL_DATA, 'r') as file:
	reader = csv.reader(file)
	for row in reader:
		url_list.append(str(row[0]))

#### SET UP SELENIUM CHROMEDRIVER ####
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='/Users/jasonzhao/Downloads/chromedriver', chrome_options = option)

#### LOOP OVER EACH URL ####
count = 0

for url in url_list:
	print(count)
	count += 1
	
	driver.get(url)

	if driver.current_url == "https://guide.ethical.org.au/guide/browse/companies/":
		print("URL not valid.")
		continue

	company_name = driver.find_element_by_tag_name('h1').text
	paragraphs = driver.find_elements_by_tag_name('p')
	strongs = driver.find_elements_by_tag_name('strong')
	tds = driver.find_elements_by_tag_name('td')
	h2s = driver.find_elements_by_tag_name('h2')
	links = driver.find_elements_by_tag_name('a')
	trs = driver.find_elements_by_tag_name('tr')

	print("H1: ")
	print(company_name)
	print("PARAGRAPHS: ")
	for p in paragraphs:
		print(p.text)
	print("STRONGS: ")
	for s in strongs:
		print(s.text)
	print("TDS: ")
	for td in tds:
		print(td.text)
	print("H2S: ")
	for h2 in h2s:
		print(h2.text)
	print("LINKS: ")
	for link in links:
		print(link.text)
	print("TRS: ")
	for tr in trs:
		print(tr.text)





#loop over each url
#access info from each url
#open csv to write