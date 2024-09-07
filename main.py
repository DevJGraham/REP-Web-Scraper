from data_extraction.single_page_extraction import get_df
from data_extraction.per_street_extraction import click_links_on_page
from data_extraction.per_street_extraction import click_property_link
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import concurrent.futures
import time
import functools

# Takes 3.4 minutes without multiprocessing
# TODO: Make a function that finds how many pages the number has and set it to max pages
# TODO: Make a function that finds out how many properties are on the last page and then make run the click preprty links with the updated property count
# TODO: Run through any other types of exceptions I could run into and make sure the program will keep running even if it runs into errors

start = time.time()
# Creating a browser for Google Chrome


# List that will hold all of the data
real_estate_data = []

# Testing with this street_name and municipality
# street_name = "FORWARD"
# municipality = "114 14th Ward - PITTSBURGH"

street_name = "UNION"
municipality = "Swissvale"

max_pages = 20  # Set this to your desired maximum number of pages
page_index = 1

# Function that retrieves property data for a single property based on the provided property index
# A new browser will be opened for each property, allowing the tasks to run in parallel
def get_property_data(property_index, street_name, municipality, page_index):
    browser = webdriver.Chrome()
    try:
        property_data = click_property_link(browser, property_index, street_name, municipality, page_index)
    finally:
        browser.close()
    return property_data

try:
    while page_index <= max_pages:
        try:
            print("Extracting data from page...")
            if __name__ == '__main__':
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [executor.submit(get_property_data, property_index, street_name, municipality, page_index) for property_index in range(2,17)]
                    
                    # For each future from futures, as they are completed, append the result to the real_estate_data list
                    for future in concurrent.futures.as_completed(futures):
                        result = future.result()
                        if result is not None:
                            real_estate_data.append(result)
                        else:
                            print(f"Skipping property index due to an error on page {page_index}.")
                            continue
            print(f"Page Index {page_index} indexing")
            page_index += 1
        except TimeoutException:
            print(f"{page_index + 1} page(s) for {street_name}")
            break
    else:
        print(f"Reached the maximum number of pages: {max_pages}")
finally:
    print(f"Data extracted for {street_name}...")


df = get_df(real_estate_data)
print("Success...")
print(df)
# df.to_csv('UNION_AVE_RealEstateData(Parallel).csv', index=False, sep=';')

end = time.time()
print("Time Difference", end - start)
