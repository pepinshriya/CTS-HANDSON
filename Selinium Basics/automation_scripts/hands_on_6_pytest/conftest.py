# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# @pytest.fixture(scope="session")
# def driver():

#     service = Service(
#         ChromeDriverManager().install()
#     )

#     driver = webdriver.Chrome(service=service)

#     yield driver

#     driver.quit()

import pytest
from selenium import webdriver


@pytest.fixture(scope="session")
def base_url():

    return "https://www.lambdatest.com/selenium-playground/"

@pytest.fixture(scope="function")
def driver(request):

    driver = webdriver.Chrome()

    # Make the driver available to the hook
    request.node.driver = driver

    yield driver

    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        driver = getattr(item, "driver", None)

        if driver:
            test_name = item.name
            driver.save_screenshot(
                f"{test_name}_failure.png"
            )
