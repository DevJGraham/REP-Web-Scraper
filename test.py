import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd

start = time.time()
browser = webdriver.Chrome()
url = "https://www2.alleghenycounty.us/RealEstate/Tax.aspx?ParcelID=0177S00203000000&SearchType=2&CurrRow=5&SearchName=&SearchStreet=UNION&SearchNum=&SearchMuni=854&SearchParcel=&pin=0177S00203000000"
browser.get(url)
current_year = datetime.now().year


# try:
#     # Optionally wait for a few seconds to allow the page to fully load (useful for debugging)
#     time.sleep(5)

#     # Print the page title to ensure the page has loaded correctly
#     print("Page Title:", browser.title)

#     # Wait for the element to be present and visible
#     element = WebDriverWait(browser, 20).until(
#         EC.visibility_of_element_located(
#             (By.XPATH, "//*[@id=\"lblTaxInfo\"]/table/tbody/tr[2]/td[2]"))
#     )

#     # print("Element HTML: ", element.get_attribute('outerHTML'))

#     # Extract the text value from the element
#     value_2024 = element.text
#     print("Extracted Value:", value_2024)

# except Exception as e:
#     print("An error occurred:", e)
#     # Optionally, print the page source for debugging purposes
#     print(browser.page_source)
# finally:
#     # Close the browser after completion
#     browser.quit()

property_data = {}
real_estate_data = []


def extract_tax_info(browser, property_data):
    for xpath_value in range(2, 6):
        year = current_year - (xpath_value - 2)
        property_data[f"{year}"] = browser.find_element(
            By.XPATH, f"//*[@id=\"lblTaxInfo\"]/table/tbody/tr[{xpath_value}]/td[2]").text


def get_df(real_estate_data):
    df = pd.DataFrame(real_estate_data, columns=[
        f'{current_year}',
        f'{current_year - 1}',
        f'{current_year - 2}',
        f'{current_year - 3}'
    ])
    return df


extract_tax_info(browser, property_data)
real_estate_data.append(property_data)
df = get_df(real_estate_data)
# print(property_data)
print(df)

end = time.time()
print("Time difference", end - start)
