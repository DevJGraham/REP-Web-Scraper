from datetime import datetime
import pandas as pd
from navigation.navigation import navigate_to
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_year = datetime.now().year


class Extract:
    # Constructor Method of the class
    # When the Extract class is called, an
    # instance of the this contructor method is created
    def __init__(self, browser):
        self.browser = browser

    # Method that extracts data from the general info page
    # Including Sale_Price, Owner_Name, Sale_Date, Owner_Mailing
    def extract_gen_info(self, property_data):
        try:
            # Extract info from Gen Info page and put it into the property_data dictionary
            property_data["Sale_Price"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblSalePrice"))
            ).text
            property_data["Property_Address"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "BasicInfo1_lblAddress"))
            ).text
            property_data["Owner_Name"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "BasicInfo1_lblOwner"))
            ).text
            property_data["Sale_Date"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblSaleDate"))
            ).text
            property_data["Owner_Mailing"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblChangeMail"))
            ).text

        except AttributeError as e:
            print("An element was not found:", e)

    # Method that extracts data from the building info page
    # Including bedroom_count, bathroom_count, use_code, sq_ft
    def extract_build_info(self, property_data):
        try:
            navigate_to(self.browser, "Header1_lnkBuilding")
            # Extract info from Building Info page and put it into the property_data dictionary
            property_data["bedroom_count"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblResBedrooms"))
            ).text
            property_data["bathroom_count"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblResFullBath"))
            ).text
            property_data["use_code"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblUse"))
            ).text
            property_data["sq_ft"] = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.ID, "lblResLiveArea"))
            ).text

        except AttributeError as e:
            print("An element was not found:", e)

    # Method that extracts the tax status for the last four years
    def extract_tax_info(self, property_data):
        navigate_to(self.browser, "Header1_lnkTax")
        for xpath_value in range(2, 6):
            year = current_year - (xpath_value - 2)
            property_data[f"{year}"] = self.browser.find_element(
                By.XPATH, f"//*[@id=\"lblTaxInfo\"]/table/tbody/tr[{xpath_value}]/td[2]").text

        # Method that creates and returns a data frame with columns= the data that we just extracted


def get_df(real_estate_data):
    df = pd.DataFrame(real_estate_data, columns=[
        'Property_Address',
        'Owner_Name',
        'Owner_Mailing',
        'Sale_Date',
        'Sale_Price',
        'bedroom_count',
        'bathroom_count',
        'use_code',
        'sq_ft',
        f'{current_year}',
        f'{current_year - 1}',
        f'{current_year - 2}',
        f'{current_year - 3}'
    ])
    return df
