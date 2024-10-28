import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import unittest
from selenium.webdriver.support import expected_conditions as EC
import sys
import logging
logging.basicConfig(filename='test_results.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class InsiderWebsiteTest(unittest.TestCase):
    driver = None
    long_break_time = 5
    short_break_time = 3

    @classmethod
    def setUpClass(cls):
        options = Options()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--headless')
        cls.driver = webdriver.Remote('http://selenium-service:4444/wd/hub', options=options)
        cls.driver.get('https://useinsider.com/')

    def test_1_check_home_page_load(self):
        expected_title = '#1 Leader in Individualized, Cross-Channel CX — Insider'
        self.assertEqual(expected_title, self.driver.title, 'HOME_PAGE_NOT_LOAD')
        logging.info(f"{self._testMethodName} - Home page loaded successfully.")

    def test_2_check_career_page_load(self):
        self.driver.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]').click()
        self.driver.find_element(By.XPATH, '//*[@id="navbarNavDropdown"]/ul[1]/li[6]/div/div[2]/a[2]').click()
        expected_career_title = 'Ready to disrupt? | Insider Careers'
        self.assertEqual(expected_career_title, self.driver.title, 'CAREER_PAGE_NOT_LOAD')

        try:
            location_slider = self.driver.find_element(By.XPATH, '//*[@id="location-slider"]/div/ul')
        except:
            location_slider = None
        self.assertFalse(location_slider is None, 'LOCATION_SLIDER_NOT_FOUND')

        try:
            teams = self.driver.find_element(By.XPATH, '//*[@id="career-find-our-calling"]/div/div/div[2]')
        except:
            teams = None
        self.assertFalse(teams is None, 'TEAMS_NOT_FOUND')

        try:
            life_at_insider = self.driver.find_element(By.XPATH,
                                                       '/html/body/div[1]/section[4]/div/div/div/div[3]/div/div')
        except:
            life_at_insider = None
        self.assertFalse(life_at_insider is None, 'LIFE_AT_INSIDER_BLOCK_NOT_FOUND')

        logging.info(f"{self._testMethodName} - Career page loaded successfully.")



    def test_3_list_the_qa_positions(self):
        self.driver.get('https://useinsider.com/careers/quality-assurance/')
        self.driver.find_element(By.XPATH, '//*[@id="page-head"]/div/div/div[1]/div/div/a').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.select2-selection__arrow'))
        )
        self.driver.find_element(By.CSS_SELECTOR, '.select2-selection__arrow').click()
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(self.long_break_time)
        self.driver.find_element(By.XPATH, '//*[@id="select2-filter-by-department-container"]').click()
        time.sleep(self.long_break_time)
        self.driver.find_element(By.CSS_SELECTOR, '.select2-selection__arrow').click()
        time.sleep(self.long_break_time)
        self.driver.find_element(By.XPATH, "//li[contains(text(), 'Istanbul, Turkey')]").click()
        try:
            job_list = self.driver.find_element(By.XPATH, '//*[@id="jobs-list"]')
            logging.info(f"{self._testMethodName} - Listed QA Positions page loaded successfully.")

        except:
            job_list = None

        self.assertFalse(job_list is None, 'JOB_LIST_NOT_FOUND')
        time.sleep(5)

    def test_4_check_all_department_location(self):
        position_items = self.driver.find_elements(By.CSS_SELECTOR, '#jobs-list > .position-list-item')
        time.sleep(self.long_break_time)
        status = True
        for item in position_items:
            position_department = item.find_element(By.CLASS_NAME, 'position-department').text
            position_location = item.find_element(By.CLASS_NAME, 'position-location').text

            if position_department != "Quality Assurance" or position_location != "Istanbul, Turkey":
                status = False

        if status:
            logging.info(f"{self._testMethodName} - Checked all positions and locations successfully.")
        else:
            self.assertFalse(status is False, 'LOCATION_AND_DEPARTMENT_DO_NOT_MATCH')

    def test_5_check_form_redirect(self):
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(self.short_break_time)
        self.driver.find_element(By.XPATH, '//*[@id="jobs-list"]/div[1]/div/a').click()
        open_tabs_count = len(self.driver.window_handles) > 1
        if open_tabs_count:
            logging.info(f"{self._testMethodName} - Redirection application form successfully.")
        else:
            self.assertFalse(open_tabs_count is False, 'THE_FORM_DOES_NOT_REDIRECT')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(InsiderWebsiteTest)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if result.wasSuccessful():
        logging.info("All tests passed.")
        sys.exit(1)
    else:
        logging.error("Some tests failed.")
        sys.exit(0)


if __name__ == "__main__":
    run_tests()
