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