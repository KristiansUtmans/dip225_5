from selenium.webdriver.common.by import By
from time import sleep


averagePricesXPath = "//table[@aria-label='gpu comparison table']/tbody/tr"
usdToEurRate = 0.91

def fetchAveragePrices(driver):
    print("Fetching average prices...")
    averagePricesDict = {}
    averagePricePageCount = int(driver.find_element(By.XPATH, "//nav[@aria-label='pagination navigation']/ul/li[last()-1]").text) - 1
    # Fetch new graphic card average prices
    for i in range(averagePricePageCount):
        print(f"{round(i / averagePricePageCount * 100)}% done")
        averagePrices = driver.find_elements(By.XPATH, averagePricesXPath)
        for averagePrice in averagePrices:
            averagePriceName = averagePrice.find_element(By.XPATH, ".//td[1]/a").text.lower()
            averagePriceName = averagePriceName.replace('geforce ','').replace('radeon ', '')
            averagePriceValue = averagePrice.find_element(By.XPATH, ".//td[5]/div/a/div/div").text
            averagePriceValue = int(int(averagePriceValue.replace('$', '').replace('\n|', '')) * usdToEurRate)

            averagePricesDict[averagePriceName] = averagePriceValue

        # Navigate to next page
        driver.find_element(By.XPATH, "//nav[@aria-label='pagination navigation']/ul/li[last()]").click()
        sleep(0.25)
    print("Finished fetching average prices.")
    return averagePricesDict