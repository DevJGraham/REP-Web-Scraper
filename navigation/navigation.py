from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# url to come back to when typing in a new street name and municipality
home_base_url = "https://www2.alleghenycounty.us/RealEstate/Search.aspx"

# Resets the browser after data has been extracted for the first property


def browser_reset(browser, street_name, municipality):
    browser.get(home_base_url)
    try:
        print("Browser Reset Initiating...")
        # Testing for Street Name box
        street_name_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "txtStreetName"))
        )
        # Writing to Street Name Box
        street_name_box.send_keys(street_name.strip())
    except TimeoutError as e:
        print("An element was not found:", e)

    try:
        # Testing for Municipality box
        municipality_box = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, "ddlMuniCode"))
        )
        # Writing to Municipality box
        municipality_box.send_keys(municipality.strip())
    except TimeoutError as e:
        print("An element was not found:", e)

    try:
        # Testing for search button
        search_box = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.ID, "btnSearch"))
        )
        # Clicking search button
        search_box.click()
    except TimeoutError as e:
        print("An element was not found:", e)


def navigate_to(browser, button_id):
    # Testing for button_id
    button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, button_id))
    )
    button.click()
