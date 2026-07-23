from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class DropdownPage(BasePage):

    DAY_DROPDOWN = (
        By.ID,
        "select-demo"
    )

    def select_day(self, day_name):

        dropdown = self.driver.find_element(
            *self.DAY_DROPDOWN
        )

        Select(dropdown).select_by_visible_text(
            day_name
        )