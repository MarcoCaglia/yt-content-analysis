"""Utility Module for scrapers."""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class count_elements(object):
    """Counts the occurances of an element on a webpage.

    Proceeds if the counts surpasses a threshold.

    locator - used to find the element
    returns the WebElement once it has the particular css class
    """

    def __init__(self, locator, count):
        self.locator = locator
        self.count = int(count)

    def __call__(self, driver):
        elements = driver.find_elements(*self.locator)   # Finding the referenced element
        is_robots_txt = self.check_robot(driver)
        print(len(elements))
        if (len(elements) >= self.count) or is_robots_txt:
            return elements
        else:
            return False

    def check_robot(self, driver):
        element = driver.find_elements(By.XPATH, "/html/body/pre")
        if element:
            text = element.get_attribute("text")
            if "robots.txt" in text:
                return text
        return False
