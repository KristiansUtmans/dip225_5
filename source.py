from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)


url = "https://www.ss.lv/lv/electronics/computers/completing-pc/"
categoryXPath = "//span[@class='filter_opt_dv'][4]/select"
listingXPath = "//div[@class='filter_second_line_dv']/following::table[1]//tr[position()>1 and position()<32]"
includedModels = [
    "rtx", "rx"
]
excludedModels = [
    "6500", "6600", "5700", "5600", "3050"
]
excludedRegions = [
    "Liepāja un raj.", "Daugavpils un raj.", "Rēzekne un raj.", "Bauska un raj."
]
driver.get(url)
sleep(2)

# Select category
driver.find_element(By.XPATH, categoryXPath).click()
driver.find_element(By.XPATH, categoryXPath + "/option[text()='Video']").click()

# Fetch listings
listings = driver.find_elements(By.XPATH, listingXPath)
for listing in listings:
    listingUrl = listing.find_element(By.XPATH, ".//td[2]/a").get_attribute("href")
    listingPicture = listing.find_element(By.XPATH, ".//td[2]/a/img").screenshot_as_base64
    listingRegion = listing.find_element(By.XPATH, ".//td[3]/div[@class='ads_region']").text
    listingBrand, listingModel = listing.find_element(By.XPATH, ".//td[4]").text.split("\n")
    listingUsed = listing.find_element(By.XPATH, ".//td[7]").text == "lietota"
    listingPrice = listing.find_element(By.XPATH, ".//td[8]").text
    print()