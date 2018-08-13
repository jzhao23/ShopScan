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

#make url list
#loop over each url
#access info from each url
#open csv to write


option = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path='/Users/jasonzhao/Downloads/chromedriver', chrome_options = option)


driver.get()