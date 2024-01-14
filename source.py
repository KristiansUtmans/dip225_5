from io import BytesIO

from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from openpyxl import Workbook
from openpyxl.worksheet.dimensions import Dimension
def containsValue(element, values):
    element = element.lower()
    for value in values:
        if value.lower() in element:
            return True
    return False

def acceptCookiesIfPromptPresent():
    if 'display: none' not in driver.find_element(By.XPATH, "//div[@id='cookie_confirm_dv']").get_attribute('style'):
        driver.find_element(By.XPATH, ".//div/table/tbody/tr/td[2]/button").click()

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
sleep(1)

# Select category
driver.find_element(By.XPATH, categoryXPath).click()
driver.find_element(By.XPATH, categoryXPath + "/option[text()='Video']").click()

# Fetch listings
listings = driver.find_elements(By.XPATH, listingXPath)

# Create new Excel workbook
wb = Workbook()
ws = wb.active
ws.title = 'Videokartes'
ws['A1'] = 'Modelis'
ws['B1'] = 'Zīmols'
ws['C1'] = 'Lietota'
ws['D1'] = 'Cena'
ws['E1'] = 'Attēls'
ws['G1'] = 'Saite'
listingRow = 2

# Not using enumerate with listingRow because represented listing count in Excel will not be always equal to the fetched listing count
for listing in listings:
    acceptCookiesIfPromptPresent()
    listingUrl = listing.find_element(By.XPATH, ".//td[2]/a").get_attribute("href")
    listingPictureData = listing.find_element(By.XPATH, ".//td[2]/a/img").screenshot_as_png
    listingRegion = listing.find_element(By.XPATH, ".//td[3]/div[@class='ads_region']").text
    listingBrand, listingModel = listing.find_element(By.XPATH, ".//td[4]").text.split("\n")
    listingUsed = "Jā" if listing.find_element(By.XPATH, ".//td[7]").text == "lietota" else "Nē"
    listingPrice = listing.find_element(By.XPATH, ".//td[8]").text
    if containsValue(listingModel, includedModels) and not containsValue(listingModel, excludedModels) and not containsValue(listingRegion, excludedRegions):
        ws[f'A{listingRow}'] = listingModel
        ws[f'B{listingRow}'] = listingBrand
        ws[f'C{listingRow}'] = listingUsed
        ws[f'D{listingRow}'] = listingPrice
        listingPictureStream = BytesIO(listingPictureData)
        listingPicture = Image(listingPictureStream)
        ws.add_image(listingPicture, f'E{listingRow}')
        ws[f'G{listingRow}'] = listingUrl
        listingRow += 1
