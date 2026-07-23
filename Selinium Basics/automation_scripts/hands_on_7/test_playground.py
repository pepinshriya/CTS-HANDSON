
from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from selenium.webdriver.support.ui import Select
from pages.input_form_page import InputFormPage


# def test_simple_form_submission(driver, base_url):

#     page = SimpleFormPage(driver)

#     page.navigate_to(
#         base_url + "simple-form-demo/"
#     )

#     page.enter_message(
#         "Hello Selenium"
#     )

#     page.click_submit()

#     assert page.get_displayed_message() == "Hello Selenium"


# def test_checkbox_submission(driver, base_url):
#     page = CheckboxPage(driver)

#     page.navigate_to(base_url + "checkbox-demo/")

#     page.check_option(0)

#     assert page.is_option_checked(0)


# def test_dropdown_selection(driver, base_url):
#     page = DropdownPage(driver)

#     page.navigate_to(base_url + "select-dropdown-demo/")

#     page.select_day("Wednesday")
    
#     page.select_day("Wednesday")

#     dropdown = Select(
#         page.driver.find_element(
#             *page.DAY_DROPDOWN
#         )
#     )

#     assert (
#         dropdown.first_selected_option.text
#         == "Wednesday"
#     )
# # Assertion to verify the selected day

def test_input_form_submit(
    driver,
    base_url
):

    page = InputFormPage(driver)

    page.navigate_to(
        base_url + "input-form-demo/"
    )

    page.fill_form(
        "Mahesh",
        "mahesh@example.com",
        "9876543210",
        "Chennai"
    )

    page.submit_form()

    assert (
        page.get_success_message()
        == "Thanks for contacting us"
    )