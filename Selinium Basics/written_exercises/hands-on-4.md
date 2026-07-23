"""
Step 24: Selenium Components

1. Selenium WebDriver
WebDriver is the programming interface that allows Python code to automate a web browser. It sends WebDriver commands to the browser driver, which performs actions such as opening web pages, locating elements, clicking buttons, entering text, and retrieving information from the browser.

2. Selenium Grid
Selenium Grid enables parallel execution of automated tests across multiple machines, operating systems, and browsers. It reduces execution time by distributing test cases to different browser nodes simultaneously.

3. Selenium IDE
Selenium IDE is a browser extension used for record-and-playback automation. It helps beginners learn Selenium concepts quickly and can generate starter automation scripts, although large-scale automation projects typically use Selenium WebDriver with programming languages.
"""


# Implicit wait applies globally to every find_element() call.
# It can slow down test execution because all element searches
# wait up to the specified time. Explicit waits are preferred
# because they wait only for specific conditions such as
# visibility or clickability of an element.