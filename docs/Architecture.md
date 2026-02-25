# Framework Architecture - Common Page Object Approach

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Gauge Specs                               │
│  (sp_login.spec, sp_EmployeeCreation.spec, sp_YourPage.spec)   │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Step Implementations                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ st_login.py  │  │st_Employee   │  │st_YourPage   │          │
│  │              │  │Creation.py   │  │.py           │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                  │
│                            │                                     │
└────────────────────────────┼─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Core Utilities                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  PageObjectManager (Singleton Pattern)                   │   │
│  │  - get_page(PageClass) → Returns single instance         │   │
│  │  - reset_page(PageClass)                                 │   │
│  │  - reset_all()                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ScreenshotUtils                                         │   │
│  │  - capture_step_screenshot(name)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  BasePage (Base Class)                                   │   │
│  │  - navigate_to(url)                                      │   │
│  │  - login(username, password)                             │   │
│  │  - get_title()                                           │   │
│  │  - Configuration methods                                 │   │
│  │  - Assertion methods                                     │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Page Object Classes                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  LoginPage   │  │ Employee     │  │  YourPage    │          │
│  │  (BasePage)  │  │ Creation     │  │  (BasePage)  │          │
│  │              │  │ (BasePage)   │  │              │          │
│  │ - username   │  │ - username   │  │ - locators   │          │
│  │ - password   │  │ - password   │  │              │          │
│  │ - login_btn  │  │ - login_btn  │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Flow Diagram

### Step Execution Flow

```
1. Gauge Spec
   │
   ├─> Step: "Login with Swag Labs"
   │
   ▼
2. Step Implementation (st_login.py)
   │
   ├─> @step("Login with Swag Labs")
   │   def login_with_swag_labs():
   │
   ▼
3. Get Page Object
   │
   ├─> page = PageObjectManager.get_page(LoginPage)
   │   │
   │   ├─> Check if LoginPage instance exists
   │   │   ├─> YES: Return existing instance
   │   │   └─> NO: Create new instance, store, return
   │
   ▼
4. Perform Actions
   │
   ├─> page.navigate_to(url)
   ├─> page.login(username, password)
   │
   ▼
5. Capture Screenshot (if needed)
   │
   ├─> capture_step_screenshot("Login_Success")
   │
   ▼
6. Log Results
   │
   ├─> log_complete("Login successful")
   │
   ▼
7. Return to Gauge
```

## Component Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                     PageObjectManager                            │
│                                                                  │
│  _instances = {                                                  │
│    'LoginPage': <LoginPage instance>,                           │
│    'EmployeeCreation': <EmployeeCreation instance>,             │
│    'YourPage': <YourPage instance>                              │
│  }                                                               │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐     │
│  │ get_page(LoginPage)                                    │     │
│  │   ├─> Returns: _instances['LoginPage']                │     │
│  │   └─> Creates if not exists                           │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                             │
                             │ manages
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Page Object Instances                         │
│                                                                  │
│  LoginPage instance          EmployeeCreation instance           │
│  ├─ username_input           ├─ username_input                  │
│  ├─ password_input           ├─ password_input                  │
│  ├─ login_button             ├─ login_button                    │
│  └─ (inherits BasePage)      └─ (inherits BasePage)             │
└─────────────────────────────────────────────────────────────────┘
```

## Before vs After

### Before (Inconsistent Approach)

```
st_login.py:
├─ LoginPage class
├─ capture_step_screenshot() function (duplicate)
└─ Steps create: login_page = LoginPage()

st_EmployeeCreation.py:
├─ EmployeeCreation class
├─ _employee_creation_page global variable
├─ get_employee_creation_page() function
├─ capture_step_screenshot() function (duplicate)
└─ Steps use: page = get_employee_creation_page()

Issues:
❌ Different patterns in each file
❌ Duplicate screenshot code
❌ Inconsistent page object management
❌ Hard to add new pages
```

### After (Common Approach)

```
core/PageObjectManager.py:
└─ Centralized singleton manager

core/ScreenshotUtils.py:
└─ Common screenshot function

st_login.py:
├─ LoginPage class
└─ Steps use: PageObjectManager.get_page(LoginPage)

st_EmployeeCreation.py:
├─ EmployeeCreation class
└─ Steps use: PageObjectManager.get_page(EmployeeCreation)

st_YourPage.py (future):
├─ YourPage class
└─ Steps use: PageObjectManager.get_page(YourPage)

Benefits:
✅ Same pattern everywhere
✅ No code duplication
✅ Easy to add new pages
✅ Centralized management
✅ Well documented
```

## Key Principles

1. **Single Responsibility**
   - PageObjectManager: Manages instances
   - ScreenshotUtils: Handles screenshots
   - BasePage: Provides common functionality
   - Page Classes: Define page-specific locators

2. **DRY (Don't Repeat Yourself)**
   - Screenshot code in one place
   - Page management in one place
   - Common actions in BasePage

3. **Consistency**
   - Same pattern in all step files
   - Same imports
   - Same usage

4. **Extensibility**
   - Template file for new pages
   - Clear documentation
   - Easy to follow pattern
