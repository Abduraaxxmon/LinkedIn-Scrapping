import time
import re
from datetime import datetime,timedelta
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from websocket import warning
from deep_translator import GoogleTranslator

from config import driver,wait,EC

# from main import wait,EC

class Extract:
    def __init__(self,driver,wait,ec):
        self.driver=driver
        self.wait=wait
        self.ec=ec

        self.name_companies = []
        self.job_titles = []
        self.location_jobs = []
        self.post_dates = []
        self.logo_urls = []
        self.sources = []
        self.skills = []
    def load_data(self):

        pagination_num = 1

        while True:
            time.sleep(2)
            li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ember-view.occludable-update[data-occludable-job-id]')))
            print(f"Page {pagination_num}: Found {len(li_elements)} job listings")
            # Iterate through the job list items and perform actions
            for li in li_elements:
                try:
                    li.click()
                    time.sleep(1)

                    self.__extract_data()


                except Exception as e:
                    print(f"Error interacting with job listing: {e}")

            # Attempt to navigate to the next page
            try:
                pagination_button = driver.find_element(By.XPATH, f'//button[@aria-label="Page {pagination_num + 1}"]')
                pagination_button.click()
                print(f"Moving to page {pagination_num + 1}")
                pagination_num += 1
                time.sleep(3)  # Wait for the next page to load

            except NoSuchElementException:
                print("No more pages available or pagination button not found")
                break

                # name_company = []
                # job_titles = []
                # location_job = []
                # post_date = []
                # logo_url = []
                # source = []
                # skill = []

    def __extract_data(self):
        time.sleep(1.3)
        # //*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[1]
        name_companies_xpath=".//div[contains(@class, 'job-details-jobs-unified-top-card__company-name')]"
        name_company= self.translate_to_english(self.__get_text_or_nan((By.XPATH, name_companies_xpath)))



        job_title_xpath= ".t-24.t-bold.inline"
        job_title= self.translate_to_english(self.__get_text_or_nan((By.CSS_SELECTOR, job_title_xpath)))
        #
        location_xpath= '//*[@id="main"]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span[1]'
        location= self.__get_text_or_nan((By.XPATH, location_xpath))
        # print(location)
        #
        post_dates_xpath='//span[contains(text(), "ago")]'
        post_date= self.__convert_to_date(self.__get_text_or_nan((By.XPATH, post_dates_xpath)))

        #
        logo_url_xpath="//img[contains(@class, 'EntityPhoto-square-4') and contains(@src, 'company-logo')]"
        # logo_url= self.__get_text_or_nan((By.XPATH, logo_url_xpath))
        # logo_url = self.driver.find_element(By.XPATH, logo_url_xpath).get_attribute('src')
        logo_url = wait.until(EC.presence_of_element_located((By.XPATH, logo_url_xpath))).get_attribute('src')
        #
        skills_xpath='.job-details-how-you-match__skills-item-subtitle'
        skill= self.__get_text_or_nan((By.CSS_SELECTOR, skills_xpath)).replace("and","")


        #
        source=driver.current_url

        self.name_companies.append(name_company)
        self.job_titles.append(job_title)
        self.location_jobs.append(location)
        self.post_dates.append(post_date)
        self.skills.append(skill)
        self.sources.append(source)
        self.logo_urls.append(logo_url)


        print(f" NAME: {name_company},DATE: {post_date},SKILL: {skill},JOB_TITLE: {job_title},LOCATION: {location},LOGO_URL: {logo_url},SOURSE: {source}")
        self.i=+1
    def __get_text_or_nan(self,locator):
        try:
            element = self.wait.until(EC.presence_of_element_located((locator)))
            return element.text.strip() if element and element.text.strip() else "NaN"
        except Exception as e:
            return "NaN"

    def __convert_to_date(self,ago_text):

        current_date = datetime.now()
        match = re.match(r"(\d+)\s*(\w+)\s*ago", ago_text)

        if not match:
            return current_date.strftime("%Y/%m/%d")  # Return today's date if no match

        value, unit = int(match.group(1)), match.group(2)

        if "minute" in unit:
            delta = timedelta(minutes=value)
        elif "hour" in unit:
            delta = timedelta(hours=value)
        elif "day" in unit:
            delta = timedelta(days=value)
        elif "week" in unit:
            delta = timedelta(weeks=value)
        elif "month" in unit:
            delta = timedelta(days=value * 30)  # Approximation for months
        elif "year" in unit:
            delta = timedelta(days=value * 365)  # Approximation for years
        else:
            delta = timedelta(0)  # Default to no change

        calculated_date = current_date - delta
        return calculated_date.strftime("%m/%d/%Y")

    def __clean_skills_as_text(self,raw_skills_text):

        # Remove unwanted characters like quotes, newlines, etc., and split by commas
        skills = re.split(r',\s*', raw_skills_text.strip())

        # Remove any leading or trailing spaces
        cleaned_skills = [skill.strip() for skill in skills]

        # Join the cleaned skills back into a single text string
        return ', '.join(cleaned_skills)

    def translate_to_english(self,text):
        try:
            # Translate any non-English text to English
            return GoogleTranslator(source='auto', target='en').translate(text).strip('"')
        except Exception as e:
            print(f"Error during translation: {e}")
            return text  # Return original text in case of any error



# Getter for _name_companies
    def get_name_companies(self):
        return self.name_companies

        # Getter for _job_titles

    def get_job_titles(self):
        return self.job_titles

        # Getter for _location_jobs

    def get_location_jobs(self):
        return self.location_jobs

        # Getter for _post_dates

    def get_post_dates(self):
        return self.post_dates

        # Getter for _logo_urls

    def get_logo_urls(self):
        return self.logo_urls

        # Getter for _sources

    def get_sources(self):
        return self.sources

        # Getter for _skills

    def get_skills(self):
        return self.skills