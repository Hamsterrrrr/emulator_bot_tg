from appium import webdriver
from appium.options.android import UiAutomator2Options

def get_driver():
    """
    Инициализирует и возвращает Appium-драйвер с обновлёнными опциями.
    """
    try:
        # Инициализация опций для Android-драйвера
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "emulator-5554"
        options.app_package = "org.telegram.messenger"
        options.app_activity = "org.telegram.ui.LaunchActivity"
        options.automation_name = "UiAutomator2"
        options.no_reset = True

        print("Инициализация драйвера с параметрами:", options.to_capabilities())

        # Подключение к Appium-серверу
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        return driver
    except Exception as e:
        print(f"Ошибка инициализации Appium-драйвера: {e}")
        return None

def get_links_from_file():
    """Считывает ссылки из файла links.txt."""
    with open("links.txt", "r") as file:
        links = [line.strip() for line in file if line.strip()]
    return links