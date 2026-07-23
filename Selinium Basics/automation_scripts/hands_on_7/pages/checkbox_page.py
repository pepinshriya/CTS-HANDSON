from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckboxPage(BasePage):

    CHECKBOXES = (
        By.CSS_SELECTOR,
        "input[type='checkbox']"
    )

    def check_option(self, index):

        checkbox = self.driver.find_elements(
            *self.CHECKBOXES
        )[index]

        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, index):

        checkbox = self.driver.find_elements(
            *self.CHECKBOXES
        )[index]

        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, index):

        return self.driver.find_elements(
            *self.CHECKBOXES
        )[index].is_selected()