from selenium.webdriver.common.by import By


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
        return 'FE0000'
    elif listingPriceDifference >= 100:
        return 'FF5733'
    elif listingPriceDifference >= 50:
        return 'FFC300'
    elif listingPriceDifference >= -25:
        return 'FFFFFF'
    elif listingPriceDifference >= -50:
        return 'AFF5B7'
    elif listingPriceDifference >= -100:
        return '52C860'
    elif listingPriceDifference >= -200:
        return '02C60F'

def saveWorkbook(wb):
    wb.save('dip225_5.xlsx')