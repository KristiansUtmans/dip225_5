from os import path, mkdir
from selenium.webdriver.common.by import By
from datetime import datetime


def containsValue(element, values):
    element = element.lower()
    for value in values:
        if value.lower() in element:
            return True
    return False

def acceptCookiesIfPromptPresent(driver):
    cookieConfirmSection = driver.find_elements(By.XPATH, "//div[@id='cookie_confirm_dv']")
    # If no cookie elements are found present on the page and cookie banner is not hidden
    if len(cookieConfirmSection) != 0 and 'display: none' not in cookieConfirmSection[0].get_attribute('style'):
        # Accept cookies
        driver.find_element(By.XPATH, ".//div/table/tbody/tr/td[2]/button").click()

def calculatePriceDifference(averagePrices, model, price):
    modelSet = set(model.split(' '))
    for averagePriceModel in averagePrices.keys():
        averagePriceModelSet = set(averagePriceModel.split(' '))
        if averagePriceModelSet.issubset(modelSet):
            return price - averagePrices[averagePriceModel]
    return 0

def getListingPriceDifferenceColor(listingPriceDifference):
    # Price formatting thresholds and colors
    if listingPriceDifference >= 200:
        return 'FE0000' # 200+ eur more expensive
    elif listingPriceDifference >= 100:
        return 'FF5733' # 100 to 200 eur more expensive
    elif listingPriceDifference >= 50:
        return 'FFC300' # 50 to 100 eur more expensive
    elif listingPriceDifference >= -25:
        return 'E0E0E0' # 25 eur price difference, pretty much the same
    elif listingPriceDifference >= -100:
        return 'B6F397' # 25 to 100 eur cheaper
    elif listingPriceDifference > -200:
        return '78E93F' # 100 to 200 eur cheaper
    elif listingPriceDifference <= -200:
        return '00D01E' # 200+ eur cheaper

def saveWorkbook(wb):
    fileDate = datetime.now().strftime('%d_%m_%Y')
    fileNumber = 1

    while path.exists(f"output/{fileDate}/{fileDate}_{str(fileNumber)}.xlsx"):
        fileNumber += 1

    if not path.exists(f"output/{fileDate}"):
        mkdir(f"output/{fileDate}")

    wb.save(f"output/{fileDate}/{fileDate}_{str(fileNumber)}.xlsx")