import pytest
import allure
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.appium_driver import get_links_from_file
from selenium.common.exceptions import TimeoutException
from utils import actions

@allure.feature("Telegram open")
@allure.story("Open Telegram")
def test_open_tg(driver):
    wait = WebDriverWait(driver, 20)  # Явное ожидание с таймаутом 20 секунд

    with allure.step("Открыть Telegram"):
        tg_icon = (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Predicted app: Telegram"]')
        wait.until(EC.element_to_be_clickable(tg_icon)).click()
        allure.attach(driver.get_screenshot_as_png(), name="open_telegram", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Переключение на второй аккаунт"):
        actions.switch_to_account(driver, 3)
        
    with allure.step("Открыть Telegram и кликнуть по строке поиска"):
        search_button = (AppiumBy.ACCESSIBILITY_ID, "Search")
        time.sleep(5)
        # wait.until(EC.element_to_be_clickable(search_button)).click()
        allure.attach(driver.get_screenshot_as_png(), name="open_search", attachment_type=allure.attachment_type.PNG)


    

@allure.feature("Telegram Links")
@allure.story("Подписка на каналы с переключением аккаунтов")
def test_subscribe_on_multiple_accounts(driver, link):
    """
    Подписка на каналы на двух аккаунтах.
    """
    links = get_links_from_file()  # Получаем все ссылки из файла

    # Действия для первого аккаунта
    with allure.step("Действия для первого аккаунта"):
        for link in links:
            actions.subscribe_to_channel(driver, link)# Подписка на каждую ссылку
        actions.click_ready(driver)
    # Переключение на второй аккаунт
    with allure.step("Переключение на второй аккаунт"):
        actions.switch_to_account(driver, 4)

    # Действия для второго аккаунта
    with allure.step("Действия для второго аккаунта"):
        for link in links:
            actions.subscribe_to_channel(driver, link)  # Подписка на каждую ссылку
        actions.click_ready(driver)
        


# @allure.feature("открыт основной канал")
# @allure.story("нажать на участвовать")
# def test_ready(driver):
#     wait = WebDriverWait(driver, 20)  # Явное ожидание с таймаутом 20 секунд

#     with allure.step(f"Ввести test и открыть"):
#         search_field = (AppiumBy.CLASS_NAME, "android.widget.EditText")
#         search_box = wait.until(EC.presence_of_element_located(search_field))
#         search_box.send_keys("test")
#         allure.attach(driver.get_screenshot_as_png(), name="input_link", attachment_type=allure.attachment_type.PNG)

#     with allure.step("Кликнуть по первому результату поиска"):
#         first_result = (AppiumBy.XPATH, "//android.view.ViewGroup[1]")
#         wait.until(EC.element_to_be_clickable(first_result)).click()
#         allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)

#     with allure.step("Кликнуть по участвовать"):
#         ready_button = (AppiumBy.CLASS_NAME, "android.widget.Button")
#         wait.until(EC.element_to_be_clickable(ready_button)).click()
#         allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
#     time.sleep(20)
#     with allure.step("вернуться на главную"):
#         back_buttton = (AppiumBy.ACCESSIBILITY_ID, "Go back")
#         wait.until(EC.element_to_be_clickable(back_buttton)).click()
#         driver.press_keycode(4)
#         allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
#     # with allure.step("Нажать кнопку Home"):
#     #     driver.press_keycode(3)  # Нажимаем кнопку Home (код 3)
#     #     allure.attach(driver.get_screenshot_as_png(), name="home_pressed", attachment_type=allure.attachment_type.PNG)
#     #//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]
#     #//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout[1]/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]
    
#     with allure.step("переход на след аккаунт"):
#         menu = (AppiumBy.ACCESSIBILITY_ID, "Open navigation menu")
#         second_account = (AppiumBy.XPATH, "//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]")
#         wait.until(EC.element_to_be_clickable(menu)).click()
#         wait.until(EC.element_to_be_clickable(second_account)).click()
#         allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)