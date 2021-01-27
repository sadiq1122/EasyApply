import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import re


class EasyApplyLinkedin:

    def __init__(self, data):
        """ :parameter"""
        self.name = data["name"]
        self.password = data["password"]
        self.keyword = data["keyword"]
        self.location = data["location"]
        self.driver = webdriver.Chrome(executable_path="C:\\Users\\Sadiq\\Desktop\\ktechExpo\\chromedriver.exe")

    def login_linkedin(self):
        self.driver.get("https://www.linkedin.com/login")
        username = self.driver.find_element_by_id("username")
        username.clear()
        username.send_keys(self.name)
        password = self.driver.find_element_by_id('password')
        password.clear()
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)

    def job_search(self):
        time.sleep(2)
        jobs_link = self.driver.find_element_by_link_text("Jobs")
        jobs_link.click()
        time.sleep(3)
        search_keywords = self.driver.find_element_by_xpath("//input[starts-with(@id,'jobs-search-box-keyword')]")
        search_keywords.clear()
        search_keywords.send_keys(self.keyword)
        time.sleep(2)
        search_location = self.driver.find_element_by_xpath("//input[starts-with(@id,'jobs-search-box-location')]")
        search_location.clear()
        search_location.send_keys(self.location)
        time.sleep(2)
        search_location.send_keys(Keys.RETURN)

    def job_filter(self):
        time.sleep(3)
        all_filters = self.driver.find_element_by_xpath("//button[@aria-label='All filters']")
        all_filters.click()
        time.sleep(2)
        easy_apply_box = self.driver.find_element_by_xpath("//label[@for='advanced-filter-linkedinFeatures-f_AL']")
        time.sleep(1)
        easy_apply_box.click()
        time.sleep(2)
        filters_apply_btn = self.driver.find_element_by_xpath(
            "//button[@aria-label='Apply selected filters and show results']")
        time.sleep(3)
        filters_apply_btn.click()

    def find_offers(self):
        # finding no of results we got
        time.sleep(3)
        total_results = self.driver.find_element_by_class_name("display-flex.t-12.t-black--light.t-normal")
        print(total_results.text)
        total_results_int = int(total_results.text.split(' ', 1)[0].replace(",", ""))
        print(total_results_int)
        time.sleep(2)
        current_page = self.driver.current_url

        results = self.driver.find_elements_by_class_name(
            "jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
        for result in results:
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            titles = self.driver.find_elements_by_class_name(
                "disabled.ember-view.job-card-container__link.job-card-list__title")
            for title in titles:
                self.submit_application(title)

        if total_results_int > 24:
            time.sleep(3)

            # find the last page and create url for all the Pages
            find_pages = self.driver.find_elements_by_class_name(
                "artdeco-pagination__indicator artdeco-pagination__indicator--number ember-view")
            total_pages = find_pages[len(find_pages) - 1].text
            total_pages_int = int(re.sub(r"[^\d.]", "", total_pages))
            get_last_page = self.driver.find_element_by_xpath(
                "//button[@aria-label='Page " + str(total_pages_int) + "']")
            get_last_page.send_keys(Keys.RETURN)
            time.sleep(2)
            last_page = self.driver.current_url
            total_jobs = int(last_page.split('start=', 1)[1])
            # go through all available pages and job offers and apply
            for page_number in range(25, total_jobs + 25, 25):
                self.driver.get(current_page + '&start=' + str(page_number))
                time.sleep(2)
                results_ext = self.driver.find_elements_by_class_name(
                    "jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
                for result_ext in results_ext:
                    hover_ext = ActionChains(self.driver).move_to_element(result_ext)
                    hover_ext.perform()
                    titles_ext = result_ext.find_elements_by_class_name(
                        "disabled.ember-view.job-card-container__link.job-card-list__title")
                    for title_ext in titles_ext:
                        self.submit_application(title_ext)
        else:
            self.close_session()

    def submit_application(self, job_ad):
        print("sadiq")
        print("You are applying for job ", job_ad.text)
        job_ad.send_keys(Keys.RETURN)
        time.sleep(3)

        try:
            in_apply = self.driver.find_element_by_xpath("//button[@data-control-name='jobdetails_topcard_inapply']")
            in_apply.send_keys(Keys.RETURN)
        except NoSuchElementException:
            print("You already applied for this job, Got to next Job")
            pass
        time.sleep(1)
        try:
            submit = self.driver.find_element_by_xpath("//button[@data-control-name='submit_unify']")
            submit.send_keys(Keys.RETURN)
            print("DIrect apply is there ", job_ad.text)
        except NoSuchElementException:
            print("No direct applicatiojn, moving to next")
            try:
                time.sleep(2)
                discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                time.sleep(1)
                discard.send_keys(Keys.RETURN)
                time.sleep(2)
                discard_confirm = self.driver.find_element_by_xpath("//button[@data-test-dialogue-primary-btn]")
                time.sleep(2)
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(3)
            except NoSuchElementException:
                pass

        # try:
        #     submit = self.driver.find_element_by_xpath("//button[@data-control-name='submit_unify']")
        #     submit.send_keys(Keys.RETURN)
        # except NoSuchElementException:
        #     print("No direct application , going to next")
        #     try:
        #         #discard if possible
        #         discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn])
        #
        #
    def close_session(self):
        print("the session is closed, See you later")
        self.driver.close()

    def apply(self):
        """Apply to job offers"""

        self.driver.maximize_window()
        self.login_linkedin()
        time.sleep(5)
        self.job_search()
        time.sleep(5)
        self.job_filter()
        time.sleep(2)
        self.find_offers()
        time.sleep(2)
        self.close_session()


if __name__ == "__main__":
    with open("config.json") as config_file:
        data = json.load(config_file)

    bot = EasyApplyLinkedin(data)
    bot.apply()
