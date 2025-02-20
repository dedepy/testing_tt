import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import Login
import allure


@pytest.fixture(scope="module")
def login_instance():
    url = os.getenv('url')
    username = os.getenv('name')
    password = os.getenv('password')
    login = Login(url, username, password)
    yield login
    if login.driver:
        login.driver.quit()  # Закрываем WebDriver после всех тестов

# Тест инициализации драйвера
@allure.feature("WebDriver Initialization")
@allure.story("Проверка инициализации WebDriver")
def test_start_driver(login_instance):
    with allure.step("Инициализация WebDriver"):
        login_instance.start_driver()
        assert login_instance.driver is not None, "WebDriver не был инициализирован"

# Тест входа в систему
@allure.feature("Login Functionality")
@allure.story("Проверка успешного входа в систему")
def test_login_success(login_instance):
    with allure.step("Выполнение входа в систему"):
        login_instance.login(login_instance.username, login_instance.password)

        try:
            WebDriverWait(login_instance.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'react-burger-menu-btn'))
            )
            allure.attach(
                login_instance.driver.get_screenshot_as_png(),
                name="Скриншот после входа",
                attachment_type=allure.attachment_type.PNG
            )
            assert True, "Вход выполнен успешно"
        except Exception as e:
            pytest.fail(f"Ошибка при выполнении входа: {e}")

# Тест выхода из системы
@allure.feature("Logout Functionality")
@allure.story("Проверка успешного выхода из системы")
def test_logout_success(login_instance):
    with allure.step("Выполнение выхода из системы"):
        try:
            # Открываем меню
            menu_b = WebDriverWait(login_instance.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'react-burger-menu-btn'))
            )
            menu_b.click()

            # Кликаем по кнопке выхода
            logout_b = WebDriverWait(login_instance.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'logout_sidebar_link'))
            )
            logout_b.click()

            # Проверяем, что пользователь вышел из системы
            WebDriverWait(login_instance.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'login-button'))
            )
            allure.attach(
                login_instance.driver.get_screenshot_as_png(),
                name="Скрин после выхода",
                attachment_type=allure.attachment_type.PNG
            )
            assert True, "Выход выполнен успешно"
        except Exception as e:
            pytest.fail(f"Ошибка при выполнении выхода: {e}")