# # # from selenium import webdriver
# # # from selenium.webdriver.chrome.service import Service
# # # from webdriver_manager.chrome import ChromeDriverManager

# # # service = Service(ChromeDriverManager().install())

# # # options = webdriver.ChromeOptions()
# # # options.add_argument("--headless")

# # # driver = webdriver.Chrome(
# # #     service=service,
# # #     options=options
# # # )

# # # driver.get("https://www.lambdatest.com/selenium-playground/")

# # # print(driver.title)

# # # driver.quit()


# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager

# # service = Service(ChromeDriverManager().install())

# # driver = webdriver.Chrome(service=service)

# # driver.get("https://www.lambdatest.com/selenium-playground/")

# # driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

# # assert "simple-form-demo" in driver.current_url

# # print("Navigation Successful")

# # # driver.back()

# # # driver.quit()

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

# service = Service(ChromeDriverManager().install())

# driver = webdriver.Chrome(service=service)

# driver.get("https://www.lambdatest.com/selenium-playground/")

# driver.execute_script('window.open("https://www.google.com");')

# print("Window Handles:")
# print(driver.window_handles)

# driver.switch_to.window(driver.window_handles[1])


# print("Current Title:")
# print(driver.title)

# driver.switch_to.window(driver.window_handles[0])

# driver.save_screenshot("playground_screenshot.png")

# driver.quit()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://www.lambdatest.com/selenium-playground/")

print("Before Resize:")
print(driver.get_window_size())

driver.set_window_size(1280, 800)

print("After Resize:")
print(driver.get_window_size())

driver.quit()