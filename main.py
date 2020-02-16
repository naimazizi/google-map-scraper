from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "keyword",
    type=str,
    help="search query in google map")
parser.add_argument(
    "--location",
    type=str,
    help="specific location of keyword, default is empty",
    default='',
    required=False)
parser.add_argument(
    "--limit",
    type=int,
    help="limit of search result, default is 30",
    default=30,
    required=False)
parser.add_argument(
    "--output",
    type=str,
    help="output file of scraped data, default is output.tsv",
    default='output.tsv',
    required=False)

args = parser.parse_args()

location = args.location
keyword = args.keyword
keyword = "{} {}".format(keyword, location)
keyword = "https://www.google.com/maps/search/{}".format(
    '+'.join(keyword.split(' ')))
print(keyword)

limit = args.limit
output = args.output

options = Options()
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(
    options=options)
driver.set_window_size(1120, 550)

driver.get(keyword)

search_counts = 0

website_class = ".//*[@class='section-result-action" +\
    " section-result-action-wide']"
title_class = ".//*[@class='section-result-title']/span"
details_class = ".//*[@class='section-result-details']"
location_class = ".//*[@class='section-result-location']"


class MaxResultReached(Exception):
    pass


def parse_result(
        result: WebElement,
        xpath: str,
        attr: str,
        args: str = None) -> str:

    out = None
    try:
        if args is None:
            out = str(getattr(result.find_element_by_xpath(xpath), attr))
        else:
            out = str(getattr(result.find_element_by_xpath(xpath), attr)(args))
    except NoSuchElementException:
        pass
    return out


try:
    with open(output, 'w') as f:
        f.write('title\tdetails\tlocation\twebsite\n')

        while(True):
            results = WebDriverWait(driver, 30).until(
                EC.visibility_of_all_elements_located((
                    By.CLASS_NAME, "section-result")))

            for result in results:
                title = parse_result(result, title_class, 'text')
                details = parse_result(result, details_class, 'text')
                loc = parse_result(result, location_class, 'text')
                website = parse_result(
                    result, website_class, 'get_attribute', 'href')

                tsv_out = '{}\t{}\t{}\t{}'.format(
                    title, details, loc, website)

                f.write(tsv_out)
                f.write('\n')

                search_counts = search_counts + 1
                if search_counts >= limit:
                    raise MaxResultReached

            next_button = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.ID, "n7lv7yjyC35__section-pagination-button-next")))

            if (next_button.get_attribute('disabled') or
                    next_button.get_attribute('disabled') == 'true'):
                break

            next_button.click()

except MaxResultReached:
    pass
finally:
    driver.quit()
