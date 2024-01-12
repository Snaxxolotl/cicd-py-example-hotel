import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.relative_locator import locate_with
import allure
import pytest


class TestHootel(object):
    def setup_method(self):
        URL = 'http://hotel-v3.progmasters.hu/'
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.get(URL)
        self.browser.maximize_window()

    def teardown_method(self):
        self.browser.quit()

    @pytest.mark.parametrize("email, password", [('hiwasi1765@wisnick.com', 'tesztelek2021'), ('', '')])
    @allure.title("Hootel Login")
    @allure.description("A belépés tesztelése")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("login")
    def test_login(self, email, password):
        menu_toggle = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="navbar-toggler collapsed"]')))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email)

        password_input = self.browser.find_element(By.ID, 'password')
        password_input.send_keys(password)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()

        logout_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, 'logout-link')))

        assert logout_btn.text == "Kilépés"

    def test_hotel_list(self):
        hotel_list_btn = self.browser.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        time.sleep(1)

        hotel_list = self.browser.find_elements(By.XPATH, '//h4[@style="cursor: pointer"]')
        assert len(hotel_list) != 0
        assert len(hotel_list) == 10

    def test_hotel_checkboxes(self):
        hotel_list_btn = self.browser.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        time.sleep(1)

        checkboxes = self.browser.find_elements(By.XPATH, '//input[@type="checkbox"]')
        for index, checkbox in enumerate(checkboxes):
            checkboxes[index].click()
            assert checkboxes[index].is_selected()

        clear_checkboxes = self.browser.find_element(By.XPATH, '//span[@class="badge badge-secondary mr-2"]')
        clear_checkboxes.click()
        for index, _ in enumerate(checkboxes):
            assert not checkboxes[index].is_selected()

    def test_find_hotel(self):
        hotel_list_btn = self.browser.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        hotel_name = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//h4[text()="Mágikus szálló - szálloda"]')))
        assert hotel_name.text == 'Mágikus szálló - szálloda'
        hotel_btn = self.browser.find_element(locate_with(By.TAG_NAME, 'button').below(hotel_name))
        hotel_btn.click()
        desc = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, "//p[text()[contains(.,'AAAAAAAAAAAAAAAAAAAAAa')]]")))
        assert 'A' in desc.text

    def test_foglalas_tab(self):
        menu_toggle = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="navbar-toggler collapsed"]')))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        time.sleep(1)

        email_foglalassal = 'kadav78379@glalen.com'
        pw_foglalassal = '!-=#&'

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email_foglalassal)

        pw_input = self.browser.find_element(By.ID, 'password')
        pw_input.send_keys(pw_foglalassal)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()
        exit_btn = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'logout-link')))
        assert exit_btn.is_displayed()
        bookings_btn = self.browser.find_element(By.ID, 'user-bookings')
        bookings_btn.click()
        foglalasok = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'actual-tab')))
        assert foglalasok.text == 'Aktuális és későbbi foglalásaim'

    def test_aktualis_foglalsok(self):
        menu_toggle = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="navbar-toggler collapsed"]')))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        time.sleep(1)

        email_foglalassal = 'kadav78379@glalen.com'
        pw_foglalassal = '!-=#&'

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email_foglalassal)

        pw_input = self.browser.find_element(By.ID, 'password')
        pw_input.send_keys(pw_foglalassal)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()
        exit_btn = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'logout-link')))
        assert exit_btn.is_displayed()
        bookings_btn = self.browser.find_element(By.ID, 'user-bookings')
        bookings_btn.click()
        foglalasok = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'actual-tab')))
        assert foglalasok.text == 'Aktuális és későbbi foglalásaim'
        delete_btn = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//button[@class="btn btn-primary mr-4 "]')))
        assert delete_btn.is_displayed()

    def test_kesobbi_foglalsok(self):
        menu_toggle = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="navbar-toggler collapsed"]')))
        menu_toggle.click()
        login_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//a[@class="nav-link"]')))
        login_btn.click()

        time.sleep(1)

        email_foglalassal = 'kadav78379@glalen.com'
        pw_foglalassal = '!-=#&'

        email_input = self.browser.find_element(By.ID, 'email')
        email_input.send_keys(email_foglalassal)

        pw_input = self.browser.find_element(By.ID, 'password')
        pw_input.send_keys(pw_foglalassal)

        submit_btn = self.browser.find_element(By.NAME, 'submit')
        submit_btn.click()
        exit_btn = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'logout-link')))
        assert exit_btn.is_displayed()
        bookings_btn = self.browser.find_element(By.ID, 'user-bookings')
        bookings_btn.click()
        foglalasok = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.ID, 'actual-tab')))
        assert foglalasok.text == 'Aktuális és későbbi foglalásaim'
        korabbi_foglalasok_btn = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'Korábbi foglalásaim')))
        korabbi_foglalasok_btn.click()

        time.sleep(1)

        delete_btn = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@class="btn btn-primary mr-4 "]')))
        for index, _ in enumerate(delete_btn):
            if index+1 > len(delete_btn)-1:
                break
            else:
                assert delete_btn[index+1].is_displayed()
