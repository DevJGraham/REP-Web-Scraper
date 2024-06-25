from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


def make_soup(browser):
    # Create a BeautifulSoup object from the html content
    page_source = browser.page_source
    soup = BeautifulSoup(page_source, "html.parser")
    return soup


def get_xpath(elm):
    e = elm
    xpath = elm.tag_name
    while e.tag_name != "html":
        e = e.find_element(By.XPATH, "..")
        neighbours = e.find_elements(By.XPATH, "../" + e.tag_name)
        level = e.tag_name
        if len(neighbours) > 1:
            level += "[" + str(neighbours.index(e) + 1) + "]"
        xpath = level + "/" + xpath
    return "/" + xpath
