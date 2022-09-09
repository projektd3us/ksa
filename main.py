from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import product

DRIVER_PATH = "driver\\chromedriver.exe"  # chrome driver path
BASE_URL = "https://ksaretail.ro"  # base url to use while crawling
QUERY = ''  # search terms

options = Options()  # init chrome options
options.headless = False  # run headless (visually hides crawl)
options.add_argument("--window-size=1920,1080")  # default window size for testing, running headless anyways

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def stepThroughPages():
    globalProductList = []

    for pageNumber in range(1, 2):  # go page by page
        driver.get(BASE_URL + "/shop/category/recent-adaugate-floresti-185/page/" + str(pageNumber))  # make url and access
        pageSoup = BeautifulSoup(driver.page_source, 'html.parser')  # get html of page
        globalProductList.extend(parsePage(pageSoup))  # call page parser and append found to gl

    return globalProductList  # un-parsed list


def parsePage(pageSoup):  # go through a page prod by prod
    productList = []
    for prod in pageSoup.find_all(class_='oe_product'):
        pLink = prod.find('a', class_='d-block h-100')
        driver.get(BASE_URL + pLink['href'])  # make url and access
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "availability_messages"))
        )
        productPageSoup = BeautifulSoup(driver.page_source, 'html.parser')  # get html of page
        productList.append(parseProduct(productPageSoup))
    return productList


def parseProduct(productPageSoup):  # go through a product page to get details
    productDetails = product.Product()
    productDetails.name = productPageSoup.find('h1', class_="te_product_name").getText()
    productDetails.priceToday = productPageSoup.find('b', class_="text-warning").find('span', class_="oe_currency_value").getText()
    productDetails.priceFull = productPageSoup.find('span', class_="text-danger oe_default_price").find('span', class_="oe_currency_value").getText()
    productDetails.stock = productPageSoup.find('div', class_="availability_messages o_not_editable").getText()

    return productDetails


def test():
    listp = stepThroughPages()
    for p in listp:
        print(p)
    # stepThroughPages()
    driver.close()
    driver.quit()  # exit drive


test()
