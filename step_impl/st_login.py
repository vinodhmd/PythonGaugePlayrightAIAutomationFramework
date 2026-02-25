from getgauge.python import step
from core.Core_basePage import BasePage
from core.ReportLogger import ReportLogger, log_step, log_complete, log_failed
from core.PageObjectManager import PageObjectManager
from core.ScreenshotUtils import capture_step_screenshot
from core.TestDataManager import TestDataManager
from locators.Objectlocators import Objectlocators

class LoginPage(BasePage):
    """
    Page Object Model for Swag Labs Login Page.
    Defines specific object mappings for this page.
    """
    username_input = Objectlocators.USERNAME_INPUT
    password_input = Objectlocators.PASSWORD_INPUT
    login_button = Objectlocators.LOGIN_BUTTON

@step("Navigate to the application")
def navigate_to_app():
    app_url = PageObjectManager.get_page(LoginPage).get_app_url()
    ReportLogger.log_browser_info(PageObjectManager.get_page(LoginPage).get_browser_type(), PageObjectManager.get_page(LoginPage).is_headless())
    PageObjectManager.get_page(LoginPage).navigate_to(app_url)

@step("Login with credentials <username> and <password>")
def login(username, password):
    PageObjectManager.get_page(LoginPage).login(username, password)

@step("Login with test data from row <row_number>")
def login_with_excel_data(row_number):
    test_data_file = PageObjectManager.get_page(LoginPage).get_test_data_file()
    test_data_sheet = PageObjectManager.get_page(LoginPage).get_test_data_sheet()
    log_step("Login with Excel Data (Row-Based)")
    ReportLogger.log_data_source(test_data_file, test_data_sheet, row_number=row_number)
    excel = TestDataManager(test_data_file)
    test_data = excel.get_row_data(test_data_sheet, int(row_number))
    excel.close()
    ReportLogger.log_test_data(test_data)
    PageObjectManager.get_page(LoginPage).login(test_data['Username'], test_data['Password'])

@step("Login with Swag Labs")
def login_with_swag_labs():
    try:
        if not TestDataManager.has_test_data():
            raise ValueError("No test data found for this scenario. Check if scenario has valid tags (e.g., TC001)")
        test_data = TestDataManager.get_test_data()
        test_id = TestDataManager.get_test_id()
        test_sheet = TestDataManager.get_test_sheet()
        log_step("Login with Swag Labs")
        app_url = TestDataManager.get_value('Url', BasePage.get_app_url())
        browser = BasePage.get_browser_type()
        headless = BasePage.is_headless()
        mapping = f"{test_id} -> {test_sheet} sheet"
        ReportLogger.log_test_context(
            url=app_url,
            browser=browser,
            headless=headless,
            file_name=BasePage.get_test_data_file(),
            sheet_name=test_sheet,
            test_id=test_id,
            mapping=mapping
        )        
        ReportLogger.log_test_data(test_data)
        username = TestDataManager.get_value('Username')
        password = TestDataManager.get_value('Password')
        if not username or not password:
            raise ValueError(f"Username or Password missing in test data for {test_id}")
        page = PageObjectManager.get_page(LoginPage)
        page.login(username, password)
        log_complete(f"Login completed for {test_id}")
        capture_step_screenshot("Login_Success")
    except Exception as e:
        log_failed(f"Login failed: {str(e)}")
        capture_step_screenshot("Error_Login")
        raise

@step("verify the title of the page")
def verify_the_title_of_the_page():
    """Verify that the page title matches expected value 'Swag Labs'."""
    try:
        actual_title = PageObjectManager.get_page(LoginPage).get_title()
        expected_title = "Swag Labs"
        log_step("Verify Page Title")
        passed = actual_title == expected_title
        ReportLogger.log_verification(expected_title, actual_title, passed)
        capture_step_screenshot("Verify_Page_Title")
        if passed:
            log_complete("Title verification passed")
        else:
            log_failed(f"Title verification failed: Expected '{expected_title}' but got '{actual_title}'")
        assert actual_title == expected_title, f"Expected title '{expected_title}' but got '{actual_title}'"
    except Exception as e:
        log_failed(f"Error in verify_the_title_of_the_page: {str(e)}")
        capture_step_screenshot("Error_verify_the_title_of_the_page")
        assert False, f"Error in verify_the_title_of_the_page: {str(e)}"