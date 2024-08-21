import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
from data_extraction.single_page_extraction import Extract
from functools import partial

start = time.time()
browser = webdriver.Chrome()
url = "https://www2.alleghenycounty.us/RealEstate/Tax.aspx?ParcelID=0177S00203000000&SearchType=2&CurrRow=5&SearchName=&SearchStreet=UNION&SearchNum=&SearchMuni=854&SearchParcel=&pin=0177S00203000000"
browser.get(url)
current_year = datetime.now().year

extractor = Extract(browser)


property_data = {}
real_estate_data = []

property_index = list(range(2, 17))

print(property_index)

def get_df(real_estate_data):
    df = pd.DataFrame(real_estate_data, columns=[
        f'{current_year}',
        f'{current_year - 1}',
        f'{current_year - 2}',
        f'{current_year - 3}'
    ])
    return df


extractor.extract_tax_info(property_data)
real_estate_data.append(property_data)
df = get_df(real_estate_data)
# print(property_data)
print(df)

def funct(a, b, c, d):
    result = a * b * c * d
    return result

part = partial(funct, a=2, b=3, c=4)

print(part, "partial function value")

final = part(d=5)

print(final, "final value after completing the partial function")


end = time.time()
print("Time difference", end - start)
