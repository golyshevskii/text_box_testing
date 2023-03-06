from time import sleep
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# класс формы
class TextBox:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        
        # заполняемые элементы формы (извлекаем по id тега <input id="...">)
        self.full_name = (By.ID, 'userName')
        self.email = (By.ID, 'userEmail')
        self.current_address = (By.ID, 'currentAddress')
        self.permanent_address = (By.ID, 'permanentAddress')
        # кнопка подтверждения формы (извлекаем по id тега <button id="...">)
        self.submit_button = (By.ID, 'submit')
        
    # методы заполнения каждого поля формы
    def in_full_name(self, name):
        self.wait.until(EC.visibility_of_element_located(self.full_name)).send_keys(name)
        
    def in_email(self, email):
        self.wait.until(EC.visibility_of_element_located(self.email)).send_keys(email)
        
    def in_current_address(self, address):
        self.wait.until(EC.visibility_of_element_located(self.current_address)).send_keys(address)
        
    def in_permanent_address(self, address):
        self.wait.until(EC.visibility_of_element_located(self.permanent_address)).send_keys(address)
    
    # метод подтверждения формы
    def click_submit_button(self):
        self.wait.until(EC.element_to_be_clickable(self.submit_button)).click()
    
    # очистка формы
    def clear_form(self):
        self.wait.until(EC.visibility_of_element_located(self.full_name)).clear()
        self.wait.until(EC.visibility_of_element_located(self.email)).clear()
        self.wait.until(EC.visibility_of_element_located(self.current_address)).clear()
        self.wait.until(EC.visibility_of_element_located(self.permanent_address)).clear()


# класс тестирования формы
class TestForm:
    def __init__(self, driver):
        self.driver = driver
    
    # генератор данных для тестирования
    def test_data(self):
        data = ({'name': 'Slava Golyshevskii',
                 'email': 'python_poseur@gmail.com',
                 'current_address': 'Israel, Rostoma 64/4',
                 'permanent_address': 'Mars, Olympus'},
                 {'name': 'Slava 1234',
                 'email': '123456789@com',
                 'current_address': '',
                 'permanent_address': ''})
        for d in data:
            yield d

    # основной метод запуска тестирования формы
    def test_form_submission(self):
        print(f'test_form_submission > START: {datetime.now()}')
        try:
            # получаем форму
            self.driver.get('https://demoqa.com/text-box')
            # создаем экземплярчик формы
            form_page = TextBox(self.driver)

            # прогоняем тесты
            test_cnt = 0
            for test in self.test_data():
                try:
                    form_page.in_full_name(test['name'])
                    form_page.in_email(test['email'])
                    form_page.in_current_address(test['current_address'])
                    form_page.in_permanent_address(test['permanent_address'])

                    # подтвержаем данные в форме + спим (даем кнопке прогрузиться)
                    sleep(2)
                    form_page.click_submit_button()
                    # проверяем ответ формы
                    assert 'field-error' not in self.driver.page_source, f'TEST {test_cnt} -> ERROR!'
                    print(f'TEST {test_cnt} -> SUCCESS')
                except (Exception, WebDriverException) as ex:
                    print(ex)
                finally:
                    test_cnt += 1
                    # очищаем форму + спим (даем форме обновиться)
                    form_page.clear_form()
                    sleep(2)

        except (Exception, WebDriverException) as ex:
            print(f'test_form_submission > ERROR: {datetime.now()}\n{ex}')
        print(f'test_form_submission > END: {datetime.now()}')


if __name__ == "__main__":
    test = TestForm(webdriver.Chrome())
    test.test_form_submission()
