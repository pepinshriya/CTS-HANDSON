# # # # from selenium import webdriver
# # # # from selenium.webdriver.common.by import By
# # # # from selenium.webdriver.chrome.service import Service
# # # # from webdriver_manager.chrome import ChromeDriverManager

# # # # service = Service(ChromeDriverManager().install())

# # # # driver = webdriver.Chrome(service=service)

# # # # driver.get(
# # # #     "https://www.lambdatest.com/selenium-playground/simple-form-demo"
# # # # )

# # # # # CSS Selector using ID
# # # # element1 = driver.find_element(
# # # #     By.CSS_SELECTOR,
# # # #     "#user-message"
# # # # )

# # # # # CSS Selector using attribute
# # # # element2 = driver.find_element(
# # # #     By.CSS_SELECTOR,
# # # #     "[name='user-message']"
# # # # )

# # # # # CSS Selector using parent-child
# # # # element3 = driver.find_element(
# # # #     By.CSS_SELECTOR,
# # # #     "div > input"
# # # # )

# # # # print(element1)
# # # # print(element2)
# # # # print(element3)

# # # # driver.quit()

# # # from selenium import webdriver
# # # from selenium.webdriver.common.by import By
# # # from selenium.webdriver.chrome.service import Service
# # # from webdriver_manager.chrome import ChromeDriverManager

# # # service = Service(ChromeDriverManager().install())

# # # driver = webdriver.Chrome(service=service)

# # # driver.get(
# # #     "https://www.lambdatest.com/selenium-playground/checkbox-demo"
# # # )

# # # # Locate using exact text
# # # label = driver.find_element(
# # #     By.XPATH,
# # #     "//label[text()='Option 1']"
# # # )

# # # print(label.text)

# # # # Locate all labels containing "Option"
# # # labels = driver.find_elements(
# # #     By.XPATH,
# # #     "//label[contains(text(),'Option')]"
# # # )

# # # for item in labels:
# # #     print(item.text)

# # # driver.quit()

# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from webdriver_manager.chrome import ChromeDriverManager

# # service = Service(ChromeDriverManager().install())

# # driver = webdriver.Chrome(service=service)

# # driver.get(
# #     "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo"
# # )

# # driver.find_element(
# #     By.ID,
# #     "autoclosable-btn-success"
# # ).click()

# # alert = WebDriverWait(driver, 10).until(
# #     EC.visibility_of_element_located(
# #         (By.CSS_SELECTOR, ".alert-success")
# #     )
# # )

# # assert "successfully" in alert.text.lower()

# # print(alert.text)

# # driver.quit()

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager

# service = Service(ChromeDriverManager().install())

# driver = webdriver.Chrome(service=service)

# driver.get(
#     "https://www.lambdatest.com/selenium-playground/bootstrap-alert-messages-demo"
# )

# button = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable(
#         (By.ID, "autoclosable-btn-success")
#     )
# )

# button.click()

# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://example.com")

wait = WebDriverWait(
    driver,
    timeout=10,
    poll_frequency=0.5,
    ignored_exceptions=[NoSuchElementException]
)

element = wait.until(
    lambda d: d.find_element(By.ID, "message")
)

print(element.text)

driver.quit()