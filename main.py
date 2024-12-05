from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import scrapping
from config import EC
from config import wait
from config import driver
from search_req import *
from login import perform_login
from search import search
from auth_credential import *
from scrapping import Extract
from Collecting import collect_into_dataframe,save_dataframe_to_csv
from search_req import country
import time
driver.get("https://www.linkedin.com")

perform_login(driver=driver, email=email, password=password, wait=wait, ec=EC)
# time.sleep(60*60)
WebDriverWait(driver, 20).until(EC.url_contains("feed"))
driver.get("https://www.linkedin.com/jobs/")
WebDriverWait(driver, 20).until(EC.url_contains("job"))


for job in job_list:
    try:
        search(title=job,wait=wait,ec=EC,country=country,driver=driver)
        time.sleep(2)
        data = Extract(driver=driver,wait=wait,ec=EC)

        data.load_data()
        print("salom")

        csv_name = job
        save_dataframe_to_csv(collect_into_dataframe(
            name_companies=data.get_name_companies(),
            job_titles=data.get_job_titles(),
            location_jobs=data.get_location_jobs(),
            post_dates=data.get_post_dates(),
            skills=data.get_skills(),
            sources=data.get_sources(),
            logo_urls=data.get_logo_urls(),
            country=country,
            job=job,
            file_name_skills=csv_name),csv_name)
    except Exception as e:
        print(e)
