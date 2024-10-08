from selenium.webdriver.common.by import By
from data_extraction.single_page_extraction import Extract
from navigation.navigation import browser_reset
from navigation.navigation import click_element
from navigation.navigation import navigate_to


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
