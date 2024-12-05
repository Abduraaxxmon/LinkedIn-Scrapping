import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By



def search( title, country,wait,ec,driver):
    WebDriverWait(driver, 20).until(ec.url_contains("job"))

    job_location = wait.until(ec.presence_of_element_located((By.XPATH, "//input[@autocomplete='address-level2']")))
    jobs_entered_button = wait.until(
        ec.presence_of_element_located((By.XPATH, "//input[contains(@class, 'jobs-search-box__text-input')]")))

    job_location.clear()
    jobs_entered_button.clear()
    time.sleep(1)

    jobs_entered_button.send_keys(title)
    job_location.send_keys(country)
    time.sleep(1)


    job_location.send_keys(Keys.ENTER)

