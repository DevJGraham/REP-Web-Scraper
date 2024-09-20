import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
from data_extraction.single_page_extraction import Extract
from data_extraction.per_street_extraction import num_of_pages
from functools import partial

start = time.time()
browser = webdriver.Chrome()
url = "https://www2.alleghenycounty.us/RealEstate/Tax.aspx?ParcelID=0177S00203000000&SearchType=2&CurrRow=5&SearchName=&SearchStreet=UNION&SearchNum=&SearchMuni=854&SearchParcel=&pin=0177S00203000000"

street_name = "UNION"
municipality = "Swissvale"

print(num_of_pages(browser, street_name, municipality))

end = time.time()
print("Time Difference", end - start)


