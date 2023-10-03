#30.5.1 В написанном тесте (проверка таблицы питомцев) добавьте явные ожидания элементов страницы.

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password
import pytest

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('C:/Users/Наталья/Desktop/QAP/chromedriver.exe')

   # Переходим на страницу авторизации
   pytest.driver.set_window_size(1400, 1000)
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()

@pytest.fixture()
def test_show_my_pets():
   """ Авторизация на сайте, переход на страницу "Мои питомцы". """

   #Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'email')))

   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'pass')))

   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))

   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Установка явного ожидания
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]')))

   # Нажимаем на кнопку "Мои питомцы"
   pytest.driver.find_element(By.XPATH, '//*[@id="navbarNav"]/ul[1]/li[1]/a[1]').click()

# Проверяем, что мы оказались на странице "Мои питомцы"
   assert pytest.driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'