import pytest
import time
import subprocess
from utils.appium_driver import get_driver

AVD_PATH = "/home/ham/Android/Sdk/emulator" # путь к эмулятору
AVD_LIST = ["Medium_Phone_API_35"] # список эмуляторов 
ADB_PATH = "/home/ham/Android/Sdk/platform-tools/adb" # путь к adb

def start_emulator(avd_name):
    """
    запуск эмулятора
    """
    print(f"запуск эмулятора {avd_name} XD")
    process = subprocess.Popen(
        [AVD_PATH + "/emulator", "-avd", avd_name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(30)
    if wait_emulator_ready():
        print(f"эмулятор {avd_name} запущен")
    else:
        print(f"Ошибка при запуске эмулятора {avd_name}")
        process.terminate()
        raise RuntimeError("ne gotov emulator")
    return process
    
def stop_emulator(process):
    """
    остановка эмулятора
    """
    print("stop_emulator")
    process.terminate()
    process.wait()
        
def wait_emulator_ready(timeout=180):
    """
    Ожидание, пока эмулятор не станет полностью готовым через ADB и Appium.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            result = subprocess.run(
                [ADB_PATH, "devices"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "emulator-" in result.stdout and "device" in result.stdout:
                print("Эмулятор зарегистрирован в ADB.")
                return True
            else:
                print("Ожидание готовности эмулятора...")
        except Exception as e:
            print(f"Ошибка при ожидании эмулятора: {e}")
        time.sleep(5)
    raise RuntimeError("Эмулятор не готов после ожидания.")
        
@pytest.fixture(params=AVD_LIST, scope="session")
def emulator(request):
    """
    последовательный запуск эмуляторов
    """
    avd_name = request.param
    process = start_emulator(avd_name)
    yield process
    stop_emulator(process)

# Фикстура для инициализации Appium-драйвера
@pytest.fixture(scope="session")
def driver(emulator):
    """
    Инициализирует Appium-драйвер и закрывает его после завершения тестов.
    """
    driver = get_driver()
    yield driver
    driver.quit()

def pytest_addoption(parser):
    """
    Регистрация пользовательского параметра --link для pytest.
    """
    parser.addoption("--link", action="store", default=None, help="Link to be processed in the test")

def get_links_from_file():
    """Считывает ссылки из файла links.txt."""
    with open("links.txt", "r") as file:
        links = [line.strip() for line in file if line.strip()]
    return links


@pytest.fixture
def link(request):
    """
    Фикстура для передачи параметра --link в тесты.
    """
    return request.config.getoption("--link")
