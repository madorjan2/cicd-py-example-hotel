import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import pytest

USERNAME = 'fidep36710@nexxterp.com'
PASSWORD = 'Asdf1234'

TEST_ADDRESS = 'Masik utca harmadik szam'
class TestHootel(object):
    def setup_method(self):
        
        URL = 'http://hotel-v3.progmasters.hu/'
        options = Options()
        options.add_experimental_option("detach", True)
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(URL)
        self.driver.set_window_size(1920, 1080)

    def teardown_method(self):
        self.driver.quit()

    @pytest.mark.parametrize("email, password", [('hiwasi1765@wisnick.com', 'tesztelek2021'), ('', '')])
    @allure.title("Hootel Login")
    @allure.description("A belépés tesztelése")
    @allure.severity(allure.severity_level.TRIVIAL)
    @allure.tag("login")
    def test_login(self, email, password):
        login_btn = self.driver.find_element(By.XPATH, '//a[@class="nav-link"]')
        login_btn.click()

        email_input = self.driver.find_element(By.ID, 'email')
        email_input.send_keys(email)

        password_input = self.driver.find_element(By.ID, 'password')
        password_input.send_keys(password)

        submit_btn = self.driver.find_element(By.NAME, 'submit')
        submit_btn.click()
        time.sleep(1)

        logout_btn = self.driver.find_element(By.ID, 'logout-link')

        assert logout_btn.text == "Kilépés"

    def test_hotel_list(self):
        hotel_list_btn = self.driver.find_element(By.XPATH, '//button[@class="btn btn-outline-primary btn-block"]')
        hotel_list_btn.click()
        time.sleep(1)

        hotel_list = self.driver.find_elements(By.XPATH, '//h4[@style="cursor: pointer"]')
        assert len(hotel_list) == 10

    def test_checkboxes(self):

        self.driver.find_element(By.XPATH, '//button[text()=" Megnézem a teljes listát "]').click()
    
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, 'redstar')))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@type="checkbox"]')))
    
        button_clear_checkbox = self.driver.find_element(By.ID, 'redstar')
        checkboxes = self.driver.find_elements(By.XPATH, '//input[@type="checkbox"]')
    
        for checkbox in checkboxes:
            checkbox.click()
    
        button_clear_checkbox.click()

        for checkbox in checkboxes:
            assert not checkbox.is_selected()

    def test_description_length(self):

        self.driver.find_element(By.XPATH, '//button[text()=" Megnézem a teljes listát "]').click()

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'h4'))).click()

        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        time.sleep(0.2)  # f dynamic loading of content...

        both_ps = self.driver.find_elements(By.XPATH, '//p[@class="card-text"]')
        description = both_ps[1].text

        assert len(description) >= 500

    def login(self):
        self.driver.find_element(By.XPATH, '//a[text()="Bejelentkezés"]').click()

        self.driver.find_element(By.ID, 'email').send_keys(USERNAME)
        self.driver.find_element(By.ID, 'password').send_keys(PASSWORD)
        self.driver.find_element(By.NAME, 'submit').click()
    def test_name_in_profile(self):
        self.login()
        a_profile = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'profile')))
        assert 'Profilom (Adorján)' == a_profile.text

    def test_email_in_profile(self):
        self.login()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'profile'))).click()
        assert WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//input[@placeholder="{USERNAME}"]'))).is_displayed()

    def test_editing_address(self):
        self.login()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'profile'))).click()
        input_address = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//strong[text()="Cím"]/../../input')))
        orig_address = input_address.get_property('placeholder')[1:]
        self.driver.find_element(By.NAME, 'submit').click()
        input_new_address = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'address')))
        input_new_address.click()
        input_new_address.clear()
        input_new_address.send_keys(TEST_ADDRESS)
        self.driver.find_element(By.NAME, 'submit').click()
        assert WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//strong[text()="Cím"]/../../input'))).get_property('placeholder')[1:] == TEST_ADDRESS

        self.driver.find_element(By.NAME, 'submit').click()
        input_new_address = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'address')))
        input_new_address.click()
        input_new_address.clear()
        input_new_address.send_keys(orig_address)
        self.driver.find_element(By.NAME, 'submit').click()
        assert WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//strong[text()="Cím"]/../../input'))).get_property('placeholder')[
               1:] == orig_address

'''

    driver.find_element(By.ID, 'user-bookings').click()

    button_past_bookings = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Korábbi foglalásaim")]')))

    all_current_bookings = driver.find_elements(By.XPATH, '//*[contains(text(), "Szállás neve")]')
    button_past_bookings.click()
    all_past_bookings = driver.find_elements(By.XPATH, '//*[contains(text(), "Szállás neve")]')

    if len(all_current_bookings) + len(all_past_bookings) > 0:
        print('User has at least one current or past booking.')
    else:
        print('User does not have any current or past booking.')

    driver.quit()
'''