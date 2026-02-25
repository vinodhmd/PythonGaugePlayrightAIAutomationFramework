"""
Template for creating new Page Object step implementations
Copy this file and customize for your new page
Example: st_Dashboard.py, st_Reports.py, st_Settings.py
"""
from getgauge.python import step, Messages, data_store
from core.Core_basePage import BasePage, get_sheet_for_test_id
from core.ReportLogger import ReportLogger, log_step, log_complete, log_failed
from core.TestDataManager import TestDataManager
from core.PageObjectManager import PageObjectManager
from core.ScreenshotUtils import capture_step_screenshot
from locators.Objectlocators import Objectlocators

class YourPageName(BasePage):
    """
    Page Object Model for [Your Page Description].
    Inherits from BasePage and defines specific locators for this page.
    """
    # Define your page-specific locators here
    # Example:
    # submit_button = Objectlocators.YOUR_SUBMIT_BUTTON
    # input_field = Objectlocators.YOUR_INPUT_FIELD
    pass
# ============================================================================
# STEP IMPLEMENTATIONS
# ============================================================================
@step("Your step description here")
def your_step_function():
    """
    Description of what this step does.
    """
    try:
        # Get the page object instance using PageObjectManager
        page = PageObjectManager.get_page(YourPageName)        
        # Perform your actions
        # page.navigate_to(url)
        # page.click(page.submit_button)
        # etc.
        # Log completion
        log_complete("Step completed successfully")
        # Optional: Capture screenshot
        # capture_step_screenshot("Your_Step_Name")
    except Exception as e:
        log_failed(f"Error in your_step_function: {str(e)}")
        capture_step_screenshot("Error_your_step_function")
        assert False, f"Error in your_step_function: {str(e)}"

@step("Another step with parameter <param>")
def another_step_with_parameter(param):
    """
    Step that accepts parameters from the spec file.    
    Args:
        param: Parameter passed from the Gauge spec
    """
    try:
        page = PageObjectManager.get_page(YourPageName)
        # Use the parameter
        log_step(f"Executing step with parameter: {param}")
        # Your logic here
        log_complete(f"Step completed with parameter: {param}")
    except Exception as e:
        log_failed(f"Error: {str(e)}")
        capture_step_screenshot(f"Error_{param}")
        assert False, f"Error: {str(e)}"

@step("Step with Excel data")
def step_with_excel_data():
    """
    Step that uses auto-loaded test data from Excel based on scenario tags.
    Data is automatically loaded in hooks - just access it!
    """
    try:
        # Check if test data is available
        if not TestDataManager.has_test_data():
            raise ValueError("No test data found for this scenario. Check if scenario has valid tags")        
        # Get test data (already loaded automatically in hooks)
        test_data = TestDataManager.get_test_data()
        test_id = TestDataManager.get_test_id()
        
        # Log context
        log_step(f"Processing test data for {test_id}")
        ReportLogger.log_test_data(test_data)
        # Get specific values from test data
        field_value = TestDataManager.get_value('FieldName')
        another_value = TestDataManager.get_value('AnotherField', 'default_value')
        # Get page object and perform actions with test data
        page = PageObjectManager.get_page(YourPageName)
        # Use test data
        # page.fill_field(field_value)
        # page.submit(another_value)
        log_complete(f"Completed processing for {test_id}")
    except Exception as e:
        log_failed(f"Error: {str(e)}")
        capture_step_screenshot("Error_excel_data")
        raise
