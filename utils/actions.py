
import allure
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.action_chains import ActionChains 





def switch_to_account(driver, account_index):
    """
    Переключение на указанный аккаунт.
    """
    wait = WebDriverWait(driver, 20)
    with allure.step(f"Переключение на аккаунт {account_index}"):
        menu = (AppiumBy.ACCESSIBILITY_ID, "Open navigation menu")
        account = (AppiumBy.XPATH, f"//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[{account_index}]")
        wait.until(EC.element_to_be_clickable(menu)).click()
        wait.until(EC.element_to_be_clickable(account)).click()
        allure.attach(driver.get_screenshot_as_png(), name=f"switch_account_{account_index}", attachment_type=allure.attachment_type.PNG)
    
    with allure.step("Открыть Telegram и кликнуть по строке поиска"):
        search_button = (AppiumBy.ACCESSIBILITY_ID, "Search")
        time.sleep(5)
        wait.until(EC.element_to_be_clickable(search_button)).click()
        allure.attach(driver.get_screenshot_as_png(), name="open_search", attachment_type=allure.attachment_type.PNG)

def double_tap(driver, element):
    """
    Выполняет двойной быстрый тап на элементе через прямое касание.
    """
    with allure.step("Выполнение двойного тапа"):
        try:
            # Получаем размеры элемента
            rect = element.rect
            center_x = rect['x'] + rect['width'] // 2
            center_y = rect['y'] + rect['height'] // 2

            # Выполняем два быстрых тапа
            driver.execute_script("mobile: clickGesture", {"x": center_x, "y": center_y})
            time.sleep(0.1)  # Пауза между тапами
            driver.execute_script("mobile: clickGesture", {"x": center_x, "y": center_y})

            print("Двойной тап выполнен.")
        except Exception as e:
            print(f"Ошибка при выполнении двойного тапа: {e}")
def like_post(driver):
    """
    Ставит лайк на пост, используя двойной быстрый тап.
    """
    try:
        wait = WebDriverWait(driver, 20)

        # Поиск элемента поста
        post_element = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, '//android.view.ViewGroup[contains(@text, "Reactions:")]')
            )
        )

        # Выполнение двойного тапа
        double_tap(driver, post_element)
    except TimeoutException:
        print("Элемент для лайка не найден.")
    except Exception as e:
        print(f"Ошибка при установке лайка: {e}")




def subscribe_to_channel(driver, link):
    """
    Подписка на канал по ссылке.
    """
    wait = WebDriverWait(driver, 20)

    with allure.step(f"Ввод ссылки {link} и переход"):
        search_field = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        search_box = wait.until(EC.presence_of_element_located(search_field))
        search_box.send_keys(link)
        allure.attach(driver.get_screenshot_as_png(), name="input_link", attachment_type=allure.attachment_type.PNG)

    with allure.step("Клик по первому результату"):
        first_result = (AppiumBy.XPATH, "//android.view.ViewGroup[1]")
        wait.until(EC.element_to_be_clickable(first_result)).click()
        allure.attach(driver.get_screenshot_as_png(), name="click_first_result", attachment_type=allure.attachment_type.PNG)

    with allure.step("проматать вниз"):
        try:
            down_button = (AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="Go to bottom"]/android.widget.ImageView[2]')
            wait.until(EC.element_to_be_clickable(down_button)).click()
        except TimeoutException:
            print("скролл не имеет смысла")
        
    with allure.step("Ставим лайк на пост, если это возможно"):
        like_post(driver)  # Установка лайка

            
            
    with allure.step("Проверка и нажатие кнопки 'Join'"):
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
            allure.attach(driver.get_screenshot_as_png(), name="join_channel", attachment_type=allure.attachment_type.PNG)
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="join_failed", attachment_type=allure.attachment_type.PNG)
            print("Кнопка 'Join' не найдена. Возможно, подписка уже выполнена.")
            
        with allure.step("возвращение"):
            back_button = (AppiumBy.ACCESSIBILITY_ID, "Go back")
            wait.until(EC.element_to_be_clickable(back_button)).click()
            allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
            
        with allure.step("Очистить поиск или открыть строку поиска"):
        # Попытка найти либо "Clear All", либо "Search"
            clear_button = (AppiumBy.ACCESSIBILITY_ID, "Clear All")
            search_button = (AppiumBy.ACCESSIBILITY_ID, "Search")
# androidx.recyclerview.widget.RecyclerView androidx.recyclerview.widget.RecyclerView
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


def click_ready(driver):
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
        driver.press_keycode(4)
        allure.attach(driver.get_screenshot_as_png(), name="click_result", attachment_type=allure.attachment_type.PNG)
        
