import pytest
from utils.appium_driver import get_driver

# Фикстура для инициализации Appium-драйвера
@pytest.fixture(scope="session")
def driver():
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
