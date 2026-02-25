from getgauge.python import step
from core.Core_basePage import BasePage
from core.ReportLogger import ReportLogger, log_step, log_complete, log_failed
from core.PageObjectManager import PageObjectManager
from core.ScreenshotUtils import capture_step_screenshot
from core.TestDataManager import TestDataManager
from locators.Objectlocators import Objectlocators
class EmployeeCreation(BasePage):
    """
    Page Object Model for Employee Creation (Payday) Page.
    Inherits from BasePage and maps standardized login locators to Payday specific locators.
    """
    username_input = Objectlocators.PAYROLL_USERNAME_INPUT
    password_input = Objectlocators.PAYROLL_PASSWORD_INPUT
    login_button = Objectlocators.PAYROLL_LOGIN_BUTTON

@step("Payroll login to load the url")
def payroll_login_to_load_the_url():
    try:
        if TestDataManager.has_test_data():
            app_url = TestDataManager.get_value('Url')
            if not app_url:
                app_url = BasePage.get_app_url()
        else:
            app_url = BasePage.get_app_url()
        ReportLogger.log_browser_info(BasePage.get_browser_type(), BasePage.is_headless())
        page = PageObjectManager.get_page(EmployeeCreation)
        page.navigate_to(app_url)
        log_complete(f"Navigated to: {app_url}")
    except Exception as e:
        log_failed(f"Navigation failed: {str(e)}")
        capture_step_screenshot("Error_Payroll_Navigation")
        raise

@step("Payroll login with credentials")
def payroll_login_with_credentials():
    try:
        if not TestDataManager.has_test_data():
            raise ValueError("No test data found for this scenario. Check if scenario has valid tags (e.g., PAY001)")
        test_data = TestDataManager.get_test_data()
        test_id = TestDataManager.get_test_id()
        test_sheet = TestDataManager.get_test_sheet()
        log_step("Login with Payday")
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
        page = PageObjectManager.get_page(EmployeeCreation)
        page.login(username, password)
        log_complete(f"Login completed for {test_id}")
        capture_step_screenshot("Payroll_Login_Success")
    except Exception as e:
        log_failed(f"Login failed: {str(e)}")
        capture_step_screenshot("Error_Payroll_Login")
        raise
