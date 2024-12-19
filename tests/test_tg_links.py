import pytest
import allure
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.appium_driver import get_links_from_file
from selenium.common.exceptions import TimeoutException


@allure.feature("Telegram open")
@allure.story("Open Telegram")
def test_open_tg(driver):
    wait = WebDriverWait(driver, 20)  # Явное ожидание с таймаутом 20 секунд

    with allure.step("Открыть Telegram"):
        tg_icon = (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="Predicted app: Telegram"]')
        wait.until(EC.element_to_be_clickable(tg_icon)).click()
        allure.attach(driver.get_screenshot_as_png(), name="open_telegram", attachment_type=allure.attachment_type.PNG)

    with allure.step("Открыть Telegram и кликнуть по строке поиска"):
        search_button = (AppiumBy.ACCESSIBILITY_ID, "Search")
        time.sleep(5)
        wait.until(EC.element_to_be_clickable(search_button)).click()
        allure.attach(driver.get_screenshot_as_png(), name="open_search", attachment_type=allure.attachment_type.PNG)


    
@allure.feature("Telegram Links")
@allure.story("Open and interact with Telegram links")
@pytest.mark.parametrize("link", get_links_from_file())
def test_open_telegram_link(driver, link):
    """
    ввода ссылк и подписки на канал с Allure-шагами.
    """
    wait = WebDriverWait(driver, 20)  # Явное ожидание с таймаутом 20 секунд


    with allure.step(f"Ввести ссылку {link} и открыть"):
        search_field = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        search_box = wait.until(EC.presence_of_element_located(search_field))
        search_box.send_keys(link)
        allure.attach(driver.get_screenshot_as_png(), name="input_link", attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть по первому результату поиска"):
        first_result = (AppiumBy.XPATH, "//android.view.ViewGroup[1]")
        wait.until(EC.element_to_be_clickable(first_result)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)

    with allure.step("Проверить наличие кнопки 'Join' и кликнуть"):
        join_button = (AppiumBy.XPATH, '//android.view.View[@content-desc="JOIN"]')
        apply_tojoin_button = (AppiumBy.XPATH, '//android.view.View[@content-desc="APPLY TO JOIN GROUP"]')
        try:
            element = WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.element_to_be_clickable(join_button),
                    EC.element_to_be_clickable(apply_tojoin_button)
                )
            )
            element.click()
            print("Подписка выполнена.")
        except Exception:
            allure.attach(driver.get_screenshot_as_png(), name="join_button_missing", attachment_type=allure.attachment_type.PNG)
            print("Кнопка 'Join' не найдена. Возможно, подписка уже выполнена.")

    with allure.step("вернуться на главную"):
        back_buttton = (AppiumBy.ACCESSIBILITY_ID, "Go back")
        wait.until(EC.element_to_be_clickable(back_buttton)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
        
    with allure.step("Очистить поиск или открыть строку поиска"):
        # Попытка найти либо "Clear All", либо "Search"
        clear_button = (AppiumBy.ACCESSIBILITY_ID, "Clear All")
        search_button = (AppiumBy.ACCESSIBILITY_ID, "Search")

        try:
            # Ожидание любого из двух элементов
            element = WebDriverWait(driver, 10).until(
                EC.any_of(
                    EC.element_to_be_clickable(clear_button),
                    EC.element_to_be_clickable(search_button)
                )
            )
            element.click()  # Выполняем клик по найденному элементу
            allure.attach(driver.get_screenshot_as_png(), name="clear_or_search", attachment_type=allure.attachment_type.PNG)
            print("Нажата кнопка очистки или поиска.")
        except TimeoutException:
            print("Ни кнопка 'Clear All', ни 'Search' не найдены.")

@allure.feature("открыт основной канал")
@allure.story("нажать на участвовать")
def test_ready(driver):
    wait = WebDriverWait(driver, 20)  # Явное ожидание с таймаутом 20 секунд

    with allure.step(f"Ввести test и открыть"):
        search_field = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        search_box = wait.until(EC.presence_of_element_located(search_field))
        search_box.send_keys("test")
        allure.attach(driver.get_screenshot_as_png(), name="input_link", attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть по первому результату поиска"):
        first_result = (AppiumBy.XPATH, "//android.view.ViewGroup[1]")
        wait.until(EC.element_to_be_clickable(first_result)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)

    with allure.step("Кликнуть по участвовать"):
        ready_button = (AppiumBy.CLASS_NAME, "android.widget.Button")
        wait.until(EC.element_to_be_clickable(ready_button)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
    time.sleep(20)
    with allure.step("вернуться на главную"):
        back_buttton = (AppiumBy.ACCESSIBILITY_ID, "Go back")
        wait.until(EC.element_to_be_clickable(back_buttton)).click()
        wait.until(EC.element_to_be_clickable(back_buttton)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
    with allure.step("Нажать кнопку Home"):
        driver.press_keycode(3)  # Нажимаем кнопку Home (код 3)
        allure.attach(driver.get_screenshot_as_png(), name="home_pressed", attachment_type=allure.attachment_type.PNG)