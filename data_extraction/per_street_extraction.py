from selenium.webdriver.common.by import By
from data_extraction.single_page_extraction import Extract
from navigation.navigation import browser_reset
from navigation.navigation import click_element
from navigation.navigation import navigate_to
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import multiprocessing as mp
import concurrent.futures

# Function that will get all of the parcel Id numbers for every property on this street
def get_parcels(browser):
    return None

# Function that will get the amount of total parcel id numbers
# If there in only one page, then it depends on how many items are in the table.
# Otherwise find the last page and then how many items are in the table on the last page
# Total number of parcel ids = (pages - 1) * 15 + parcels_on_last_page
# For testing purposes:
# street_name = "HIGH PARK" municipality = "PITTSBURGH - 11TH WARD" - only one page
# street_name = "STANTON" municipality = "MILLVALE" - more than 10 pages
# TODO: Handle edge cases
# You can go from page index 1 - 10. Page index 10 is the '...'
# Once you get to the second page, clicking on page_index 1 will take you to the previous page
# You have to start at page_index = 2 and go to 11. This is the same for all pages that have an '...'
# For example if a property has 41 pages, page_index 1 - 10 will run like normal (one time through)
# Once you get past 10 you need to reset starting at 2 going to 11 (2nd time through). Do this part again (3) and again (4).
# When you are on the last page 
def num_of_pages(browser, street_name, municipality):
    
    browser_reset(browser, street_name, municipality)
    
    page_index = 1
    max_pages = 20
    print(f"On page {page_index}...")

    while page_index < max_pages:
        try:
            
            click_element(browser, By.XPATH, f"//tbody/tr[17]/td/a[{page_index}]")
            print(f"Clicking page {page_index + 1}...")
        except TimeoutException:
            print(f"{page_index + 1} page(s) for {street_name}")
            return page_index + 1
    return None

def click_links_on_page(browser, street_name, municipality, real_estate_data, page_index=None):
    # Creating an instance of the Extract class
    extractor = Extract(browser)
    # The maximum amount of properties on a page
    max_property_index = 17
    property_index = 2
    while property_index < max_property_index:
        try:
            # Creating a dictionary where the data will go from each extraction
            # This will eventually go into a list of dictionaries that will become a dataframe
            property_data = {}
            print("Resetting Browser...")

            # Resetting the Browser. Needs to happen at every iteration
            browser_reset(browser, street_name, municipality)

            if page_index not in (None, 0):

                # Clicking the correct page number
                click_element(
                    browser, By.XPATH, f"//tbody/tr[17]/td/a[{page_index}]")
                # Clicking the correct property
            print(f"Clicking property {property_index - 1}...")
            click_element(browser, By.XPATH,
                          f"//tbody/tr[{property_index}]/td[1]/a")

            extractor.extract_gen_info(property_data)
            navigate_to(browser, "Header1_lnkBuilding")
            extractor.extract_build_info(property_data)
            navigate_to(browser, "Header1_lnkTax")
            extractor.extract_tax_info(property_data)

            # At the end of each iteration, append the dictionary to the
            # list that will eventually be a dataframe
            real_estate_data.append(property_data)
        except AttributeError as e:
            print("An element was not found:", e)
            print(f"{page_index + 1} pages for {street_name}")
        property_index += 1 


def click_property_link(browser, property_index, street_name, municipality, page_index=None):
    try:
        property_data = {}
        extractor = Extract(browser)

        print(f"Resetting Browser for property index {property_index}")
        browser_reset(browser, street_name, municipality)
        if page_index not in (None, 0):
            # Clicking the correct page number
            click_element(
                browser, By.XPATH, f"//tbody/tr[17]/td/a[{page_index}]")
            
        print(f"Clicking property {property_index - 1}...")
        click_element(browser, By.XPATH,
                    f"//tbody/tr[{property_index}]/td[1]/a")
            
        extractor.extract_gen_info(property_data)
        navigate_to(browser, "Header1_lnkBuilding")
        extractor.extract_build_info(property_data)
        navigate_to(browser, "Header1_lnkTax")
        extractor.extract_tax_info(property_data)
        return property_data
    except AttributeError as e:
        print("An element was not found:", e)
        print(f"{page_index + 1} pages for {street_name}")
        return None
    except NoSuchElementException as e:
        print(f"Property element not found on page {page_index} for property index {property_index}")
        return None
    except TimeoutException as e:
        print(f"Page {page_index} took too long to load for property index {property_index}")
        return None