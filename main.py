from data_extraction.single_page_extraction import get_df
from data_extraction.per_street_extraction import click_links_on_page
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

# Creating a browser for Google Chrome
browser = webdriver.Chrome()

# List that will hold all of the data
real_estate_data = []

# Testing with this street_name and municipality
street_name = "UNION"
municipality = "Swissvale"

max_pages = 20  # Set this to your desired maximum number of pages
page_index = 0
while page_index <= max_pages:
    try:
        print("Extracting data from page...")
        click_links_on_page(
            browser, street_name, municipality, real_estate_data, page_index)
        page_index += 1
    except TimeoutException:
        print(f"{page_index + 1} page(s) for {street_name}")
        break
else:
    print(f"Reached the maximum number of pages: {max_pages}")

df = get_df(real_estate_data)
print("Success...")
print(df)
df.to_csv('UNION_AVE_RealEstateData.csv', index=False, sep=';')

browser.close()
