# Page Object Pattern - Common Approach Guide

## Overview

This framework uses a centralized approach for managing page objects across all test implementations. This ensures consistency, reduces code duplication, and makes it easy to add new pages.

## Core Components

### 1. PageObjectManager (`core/PageObjectManager.py`)

Centralized singleton manager for all page objects.

**Key Features:**
- Ensures only one instance of each page object exists
- Lazy initialization (creates instances only when needed)
- Easy to use across all step files

**Usage:**
```python
from core.PageObjectManager import PageObjectManager

# Get a page object instance
login_page = PageObjectManager.get_page(LoginPage)
employee_page = PageObjectManager.get_page(EmployeeCreation)

# Reset a specific page (if needed)
PageObjectManager.reset_page(LoginPage)

# Reset all pages (typically in hooks)
PageObjectManager.reset_all()
```

### 2. ScreenshotUtils (`core/ScreenshotUtils.py`)

Common screenshot capture functionality.

**Usage:**
```python
from core.ScreenshotUtils import capture_step_screenshot

# Capture a screenshot
capture_step_screenshot("Login_Success")
capture_step_screenshot("Error_Navigation")
```

### 3. BasePage (`core/Core_basePage.py`)

Base class for all page objects with common functionality:
- Browser interactions (navigate, get_title, etc.)
- Login actions
- Configuration management
- Assertions
- Screenshot capture

## Creating a New Page Object

### Step 1: Define Your Page Object Class

Create a new file in `step_impl/` (e.g., `st_Dashboard.py`):

```python
from getgauge.python import step, Messages, data_store
from core.Core_basePage import BasePage
from core.PageObjectManager import PageObjectManager
from core.ScreenshotUtils import capture_step_screenshot
from locators.Objectlocators import Objectlocators

class DashboardPage(BasePage):
    """
    Page Object Model for Dashboard Page.
    """
    # Define page-specific locators
    menu_button = Objectlocators.DASHBOARD_MENU
    user_profile = Objectlocators.USER_PROFILE
    logout_button = Objectlocators.LOGOUT_BUTTON
```

### Step 2: Implement Step Functions

```python
@step("Navigate to dashboard")
def navigate_to_dashboard():
    """Navigate to the dashboard page."""
    try:
        # Get page object using PageObjectManager
        page = PageObjectManager.get_page(DashboardPage)
        
        # Perform actions
        dashboard_url = BasePage.get_config('DASHBOARD_URL')
        page.navigate_to(dashboard_url)
        
        log_complete("Dashboard navigation successful")
        capture_step_screenshot("Dashboard_Loaded")
        
    except Exception as e:
        log_failed(f"Error: {str(e)}")
        capture_step_screenshot("Error_Dashboard")
        assert False, f"Error: {str(e)}"
```

### Step 3: Use in Gauge Specs

```gherkin
# Dashboard Tests
Tags: DASH001

## Verify Dashboard Access
* Navigate to dashboard
* Verify user profile is displayed
```

## Standard Pattern for All Step Files

### Required Imports

```python
from getgauge.python import step, Messages, data_store
from core.Core_basePage import BasePage, get_sheet_for_test_id
from core.ReportLogger import ReportLogger, log_step, log_complete, log_failed
from core.Excel_Reader import ExcelReader
from core.PageObjectManager import PageObjectManager
from core.ScreenshotUtils import capture_step_screenshot
from locators.Objectlocators import Objectlocators
```

### Page Object Access Pattern

**Always use PageObjectManager:**
```python
# ✅ CORRECT
page = PageObjectManager.get_page(YourPageClass)

# ❌ WRONG - Don't create instances directly
page = YourPageClass()
```

### Screenshot Pattern

**Use the common utility:**
```python
# ✅ CORRECT
from core.ScreenshotUtils import capture_step_screenshot
capture_step_screenshot("Step_Name")

# ❌ WRONG - Don't duplicate screenshot code
def capture_step_screenshot(step_name):
    # ... duplicate code
```

## Benefits of This Approach

1. **Consistency**: All page objects are managed the same way
2. **No Duplication**: Common code (screenshots, page management) is centralized
3. **Easy to Extend**: Adding new pages follows the same pattern
4. **Singleton Pattern**: Only one instance per page object, shared across steps
5. **Maintainability**: Changes to common functionality only need to be made once

## Example Files

- **Template**: `step_impl/st_Template.py` - Copy this to create new pages
- **Login Example**: `step_impl/st_login.py` - Swag Labs login implementation
- **Employee Example**: `step_impl/st_EmployeeCreation.py` - Payroll application implementation

## Hooks Integration

In `step_impl/hooks.py`, you can reset page objects between scenarios:

```python
from core.PageObjectManager import PageObjectManager

@after_scenario
def cleanup_page_objects(context):
    # Reset all page objects for the next scenario
    PageObjectManager.reset_all()
```

## Quick Reference

| Task | Code |
|------|------|
| Get page object | `page = PageObjectManager.get_page(PageClass)` |
| Take screenshot | `capture_step_screenshot("Name")` |
| Log step | `log_step("Message")` |
| Log completion | `log_complete("Message")` |
| Log failure | `log_failed("Message")` |
| Get test data | `BasePage.get_test_id_from_tags()` |
| Navigate | `page.navigate_to(url)` |
| Login | `page.login(username, password)` |

## Adding More Pages

1. Copy `st_Template.py` to `st_YourPage.py`
2. Define your page class with locators
3. Implement step functions using `PageObjectManager.get_page(YourPage)`
4. Use `capture_step_screenshot()` for screenshots
5. Follow the error handling pattern in the template

That's it! The framework handles the rest.
