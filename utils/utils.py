from bs4 import BeautifulSoup


def make_soup(browser):
    # Create a BeautifulSoup object from the html content
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    return soup
