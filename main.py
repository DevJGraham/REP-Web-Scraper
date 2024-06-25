from data_extraction.extract import Extract
from data_extraction.extract import get_df
from utils.utils import get_xpath
from navigation import navigation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

# Creating a browser for Google Chrome
browser = webdriver.Chrome()

# Creating an instance of the Extract class
extractor = Extract(browser)

real_estate_data = []

# Testing with this street_name and municipality
street_name = "PORTLAND"
municipality = "PITTSBURGH - 11TH WARD"


for property_index in range(2, 17):
    try:
        navigation.browser_reset(browser, street_name, municipality)

        navigation.click_element(browser, By.XPATH,
                                 f"//tbody/tr[{property_index}]/td[1]/a")

        # Creating a dictionary where the data will go from each extraction
        # This will eventually go into a list of dictionaries that will become a dataframe
        property_data = {}

        # These will extract data and put the extracted data into the proeprty_data dictionary
        extractor.extract_gen_info(property_data)
        navigation.navigate_to(browser, "Header1_lnkBuilding")
        extractor.extract_build_info(property_data)
        navigation.navigate_to(browser, "Header1_lnkTax")
        extractor.extract_tax_info(property_data)

        # At the end of each iteration, append the dictionary to the list that will eventually be a dataframe
        real_estate_data.append(property_data)
    except AttributeError as e:
        print("An element was not found:", e)
    property_index += 1

df = get_df(real_estate_data)
print("Success...")
print(df)
df.to_csv('Portland_RealEstateData_pg1.csv', index=False, sep=';')
