from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time

# Инициализация драйвера
browser = webdriver.Chrome()

# Открытие веб-страницы
browser.get('https://www.aviasales.ru')

from_ = "Омск"
to_ = "Санкт-Петербург"
xpath_from = "/html/body/div[8]/div[3]/div/div/div/div[2]/form/span/div[1]/div/span/input"
xpath_to = '/html/body/div[8]/div[3]/div/div/div/div[2]/form/span/div[2]/div/span/input'
xpath_search = '/html/body/div[8]/div[3]/div/div/div/div[2]/form/div[3]/button'
xpath_date_first = '/html/body/div[8]/div[3]/div/div/div/div[2]/form/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[3]/div[3]/div[5]/div/div[1]'
xpath_date_second = '/html/body/div[8]/div[3]/div/div/div/div[2]/form/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div/div/div/div/div[2]/div[1]/div[3]/div[3]/div[7]/div/div[1]'

value_date_first = 'Fri Jun 14 2014'
value_date_second = 'Sun Jun 16 2014'

# Инициализация WebDriverWait
wait = WebDriverWait(browser, 10)

# Находим элементы на странице
button_from = wait.until(EC.presence_of_element_located((By.XPATH, xpath_from)))
button_to = wait.until(EC.presence_of_element_located((By.XPATH, xpath_to)))
button_search = wait.until(EC.presence_of_element_located((By.XPATH, xpath_search)))


# Функция для ввода значений в поля
def city_input(butt, value):
    butt.send_keys(Keys.CONTROL + 'a')
    butt.send_keys(Keys.DELETE)
    time.sleep(1)  # Добавляем неболь
    # шую задержку
    butt.send_keys(value)
    time.sleep(1)  # Добавляем небольшую задержку
    butt.send_keys(Keys.ENTER)


if __name__ == '__main__':
    # Вводим значения в поля
    city_input(button_from, from_)
    city_input(button_to, to_)


    dateFieldFirst = wait.until(EC.presence_of_element_located((By.XPATH, xpath_date_first)))
    dateFieldSecond = wait.until(EC.presence_of_element_located((By.XPATH, xpath_date_second)))

    # Нажимаем кнопку поиска
    button_search.click()

    # Задержка, чтобы увидеть результат (или можно использовать другое ожидание)
    time.sleep(10)

    # Закрываем браузер
    browser.quit()
