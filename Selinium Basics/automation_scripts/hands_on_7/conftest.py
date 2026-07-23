import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


@pytest.fixture
def driver():

    driver = webdriver.Chrome(
        service=Service(
            ChromeDriverManager().install()
        )
    )

    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="session")
def base_url():

    return "https://www.lambdatest.com/selenium-playground/"