from io import BytesIO

from openpyxl.drawing.image import Image
from openpyxl.styles import Alignment, Font, NamedStyle
from openpyxl.worksheet.hyperlink import Hyperlink
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from openpyxl import Workbook

def containsValue(element, values):
    element = element.lower()
    for value in values:
        if value.lower() in element:
            return True
    return False

def acceptCookiesIfPromptPresent():
    cookieConfirmSection = driver.find_elements(By.XPATH, "//div[@id='cookie_confirm_dv']")
    # If no cookie elements are found present on the page and cookie banner is not hidden
    if len(cookieConfirmSection) != 0 and 'display: none' not in cookieConfirmSection[0].get_attribute('style'):
        # Accept cookies
        driver.find_element(By.XPATH, ".//div/table/tbody/tr/td[2]/button").click()

service = Service()
option = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=option)


url = "https://www.ss.lv/lv/electronics/computers/completing-pc/"
categoryXPath = "//span[@class='filter_opt_dv'][4]/select"
dealTypeXPath = "//span[@class='filter_opt_dv'][3]/select"
listingXPath = "//div[@class='filter_second_line_dv']/following::table[1]//tr[position()>1 and position()<last()]"
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

# Fetch page count
pageCount = int(driver.find_element(By.XPATH, "//a[@class='navi'][last() - 1]").text)

# Create new Excel workbook
wb = Workbook()
ws = wb.active
# Set Excel header field values
ws.title = 'Videokartes'
ws['A1'] = 'Modelis'
ws['B1'] = 'Zīmols'
ws['C1'] = 'Lietota'
ws['D1'] = 'Cena'
ws['E1'] = 'Attēls'
ws['G1'] = 'Saite'

listingRow = 2
hyperlinkStyle = NamedStyle(name='hyperlink', font=Font(underline='single', color='0563C1'))

# Not using enumerate with listingRow because represented listing count in Excel will not be always equal to the fetched listing count
for i in range(pageCount):

    # Show only "Sell" listings
    driver.find_element(By.XPATH, dealTypeXPath).click()
    driver.find_element(By.XPATH, dealTypeXPath + "/option[text()='Pārdod']").click()

    # Fetch listings
    listings = driver.find_elements(By.XPATH, listingXPath)

    for listing in listings:
        acceptCookiesIfPromptPresent()
        listingUrl = listing.find_element(By.XPATH, ".//td[2]/a").get_attribute("href")
        listingPictureData = listing.find_element(By.XPATH, ".//td[2]/a/img").screenshot_as_png
        listingRegion = listing.find_element(By.XPATH, ".//td[3]/div[@class='ads_region']").text
        listingBrand, listingModel = listing.find_element(By.XPATH, ".//td[4]").text.split("\n")
        listingUsed = "Jā" if listing.find_element(By.XPATH, ".//td[7]").text == "lietota" else "Nē"
        listingPrice = listing.find_element(By.XPATH, ".//td[8]").text
        listingPrice = int(listingPrice[:listingPrice.find(' €')].replace(',', ''))
        if containsValue(listingModel, includedModels) and not containsValue(listingModel, excludedModels) and not containsValue(listingRegion, excludedRegions) and 100 < listingPrice < 1000:
            ws[f'A{listingRow}'] = listingModel
            ws[f'B{listingRow}'] = listingBrand
            ws[f'C{listingRow}'] = listingUsed
            ws[f'D{listingRow}'] = listingPrice
            listingPictureStream = BytesIO(listingPictureData)
            listingPicture = Image(listingPictureStream)
            ws.add_image(listingPicture, f'E{listingRow}')
            ws[f'G{listingRow}'] = listingUrl
            ws[f'G{listingRow}'].style = hyperlinkStyle
            ws[f'G{listingRow}'].hyperlink = Hyperlink(ref=listingUrl, target=listingUrl)
            listingRow += 1

    # Navigate to next page
    driver.find_element(By.XPATH, "//a[@class='navi'][last()]").click()
    sleep(0.25)

# Excel file graphical formatting

# Header formatting
for cell in ws[1]:
    cell.alignment = Alignment(horizontal='center', vertical='center')
    cell.font = Font(bold=True, size=18)

# Width formatting
for col in ws.columns:
    max_length = 0
    letter = col[0].column_letter
    for cell in col:
        value = cell.value
        if value is not None and len(str(value)) > max_length:
            max_length = len(value)
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[letter].width = adjusted_width

# Height formatting
for row in ws.iter_rows():
    ws.merge_cells(start_row=row[0].row, end_row=row[0].row, start_column=row[4].column, end_column=row[5].column)
    ws.row_dimensions[row[0].row].height = 50

wb.save("dip225_5.xlsx")