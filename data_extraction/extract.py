from utils.utils import make_soup
import pandas as pd


class Extract:

    # Constructor Method of the class
    # When the Extract class is called, an
    # instance of the this contructor method is created
    def __init__(self, browser):
        self.browser = browser

    # Method that extracts data from the general info page
    # Including Sale_Price, Owner_Name, Sale_Date, Owner_Mailing
    def extract_gen_info(self, property_data):
        # Opening Page
        soup = make_soup(self.browser)

        try:
            # Extract info from Gen Info page and put it into the property_data dictionary
            property_data["Sale_Price"] = soup.select_one(
                '#lblSalePrice').getText(strip=True)
            property_data["Property_Address"] = soup.select_one(
                '#BasicInfo1_lblAddress').getText(strip=True)
            property_data["Owner_Name"] = soup.select_one(
                '#BasicInfo1_lblOwner').getText(strip=True)
            property_data["Sale_Date"] = soup.select_one(
                '#lblSaleDate').getText(strip=True)
            property_data["Owner_Mailing"] = soup.select_one(
                '#lblChangeMail').getText(strip=True)

        except AttributeError as e:
            print("An element was not found:", e)

    # Method that extracts data from the building info page
    # Including bedroom_count, bathroom_count, use_code, sq_ft
    def extract_build_info(self, property_data):
        # Opening Page
        soup = make_soup(self.browser)

        try:
            # Extract info from Building Info page and put it into the property_data dictionary
            property_data["bedroom_count"] = soup.select_one(
                '#lblResBedrooms').get_text(strip=True)
            property_data["bathroom_count"] = soup.select_one(
                '#lblResFullBath').get_text(strip=True)
            property_data["use_code"] = soup.select_one(
                '#lblUse').get_text(strip=True)
            property_data["sq_ft"] = soup.select_one(
                '#lblResLiveArea').get_text(strip=True)

        except AttributeError as e:
            print("An element was not found:", e)

    # Method that extracts data from the tax info page
    # Including tax_status
    def extract_tax_info(self, property_data):
        # Checking for presence of "UNPAID" in the HTML
        if "UNPAID" in self.browser.page_source:
            tax_status = "unpaid"
        else:
            tax_status = "paid"

        # Adding tax_status into the property_data dictionary
        property_data["tax_status"] = tax_status

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
        'tax_status'])
    return df
