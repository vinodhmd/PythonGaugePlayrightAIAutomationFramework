# Test Execution Steps - Login Specification

This document details the step-by-step execution flow for the login test scenarios defined in `specs/login.spec`.

---

## 📋 Test Suite Overview

| Property | Value |
|----------|-------|
| **Specification File** | `specs/login.spec` |
| **Step Implementation** | `step_impl/login_steps.py` |
| **Page Object** | `pages/login_page.py` |
| **Application URL** | https://www.saucedemo.com/ |
| **Test Data File** | `data/testdata.xlsx` |
| **Test Data Sheet** | `LoginData` |

---

## 🧪 Scenario 1: Successful Login with Credentials

**Tags:** `TC001`, `positive`, `credentials`

### Execution Steps:

| Step # | Spec Step | Implementation Function | Execution Flow |
|--------|-----------|------------------------|----------------|
| 1 | `Navigate to the application` | `navigate_to_app()` | 1. Creates `LoginPage` instance<br>2. Gets URL from `ConfigReader.get_app_url()`<br>3. Calls `page.goto(url)` via Playwright |
| 2 | `Login with credentials "standard_user" and "secret_sauce"` | `login(username, password)` | 1. Creates `LoginPage` instance<br>2. Fills username input: `input[name='user-name']`<br>3. Fills password input: `input[name='password']`<br>4. Clicks login button: `input[name='login-button']` |

### Detailed Execution Flow:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Step 1: Navigate to the application                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  login_steps.py::navigate_to_app()                                 │
│     │                                                               │
│     ├─► LoginPage() → BasePage.__init__()                          │
│     │       └─► PlaywrightDriver.get_page() → Returns active page  │
│     │                                                               │
│     └─► login_page.navigate_to(ConfigReader.get_app_url())         │
│             │                                                       │
│             ├─► ConfigReader.get_app_url()                         │
│             │       └─► os.getenv('APP_URL')                       │
│             │           └─► Returns: "https://www.saucedemo.com/"  │
│             │                                                       │
│             └─► base_page.navigate_to(url)                         │
│                     └─► self.page.goto(url) [Playwright]           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Step 2: Login with credentials "standard_user" and "secret_sauce"  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  login_steps.py::login("standard_user", "secret_sauce")            │
│     │                                                               │
│     ├─► LoginPage() → BasePage.__init__()                          │
│     │       └─► PlaywrightDriver.get_page() → Returns active page  │
│     │                                                               │
│     └─► login_page.login("standard_user", "secret_sauce")          │
│             │                                                       │
│             ├─► self.page.fill("input[name='user-name']",          │
│             │                  "standard_user")                     │
│             │                                                       │
│             ├─► self.page.fill("input[name='password']",           │
│             │                  "secret_sauce")                      │
│             │                                                       │
│             └─► self.page.click("input[name='login-button']")      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Scenario 2: Login with Excel Data - Row Based

**Tags:** `TC002`, `positive`, `data-driven`, `excel`

### Execution Steps:

| Step # | Spec Step | Implementation Function | Execution Flow |
|--------|-----------|------------------------|----------------|
| 1 | `Navigate to the application` | `navigate_to_app()` | Same as Scenario 1, Step 1 |
| 2 | `Login with test data from row "2"` | `login_with_excel_data(row_number)` | 1. Opens `data/testdata.xlsx`<br>2. Reads row 2 from `LoginData` sheet<br>3. Extracts `Username` and `Password` columns<br>4. Performs login with extracted data |

### Detailed Execution Flow:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Step 2: Login with test data from row "2"                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  login_steps.py::login_with_excel_data("2")                        │
│     │                                                               │
│     ├─► ExcelReader('testdata.xlsx')                               │
│     │       │                                                       │
│     │       ├─► data_folder = "GaugeFramework/data"                │
│     │       └─► load_workbook("data/testdata.xlsx")                │
│     │                                                               │
│     ├─► excel.get_row_data('LoginData', 2)                         │
│     │       │                                                       │
│     │       ├─► Get headers from row 1                             │
│     │       │   e.g. ['TestID', 'Username', 'Password', ...]       │
│     │       │                                                       │
│     │       ├─► Get values from row 2                              │
│     │       │   e.g. ['TC001', 'standard_user', 'secret_sauce']    │
│     │       │                                                       │
│     │       └─► Returns: {'TestID': 'TC001',                       │
│     │                     'Username': 'standard_user',             │
│     │                     'Password': 'secret_sauce', ...}         │
│     │                                                               │
│     ├─► excel.close()                                              │
│     │                                                               │
│     ├─► LoginPage() → BasePage.__init__()                          │
│     │       └─► PlaywrightDriver.get_page()                        │
│     │                                                               │
│     └─► login_page.login(test_data['Username'],                    │
│                          test_data['Password'])                    │
│             │                                                       │
│             ├─► self.page.fill(username_input, <username>)         │
│             ├─► self.page.fill(password_input, <password>)         │
│             └─► self.page.click(login_button)                      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Scenario 3: Login with Excel Data - Test ID Based

**Tags:** `TC003`, `positive`, `data-driven`, `excel`

### Execution Steps:

| Step # | Spec Step | Implementation Function | Execution Flow |
|--------|-----------|------------------------|----------------|
| 1 | `Navigate to the application` | `navigate_to_app()` | Same as Scenario 1, Step 1 |
| 2 | `Login with Swag Labs` | `login_with_swag_labs()` | 1. Gets test data file from config<br>2. Gets test data sheet from config<br>3. Reads row 2 from sheet<br>4. Performs login with data |
| 3 | `verify the title of the page` | `verify_the_title_of_the_page()` | 1. Gets page title using Playwright<br>2. Asserts title equals "Swag Labs" |

### Detailed Execution Flow:

```
┌─────────────────────────────────────────────────────────────────────┐
│ Step 2: Login with Swag Labs                                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  login_steps.py::login_with_swag_labs()                            │
│     │                                                               │
│     ├─► ConfigReader.get_test_data_file()                          │
│     │       └─► os.getenv('TEST_DATA_FILE', 'testdata.xlsx')       │
│     │           └─► Returns: "testdata.xlsx"                       │
│     │                                                               │
│     ├─► ExcelReader('testdata.xlsx')                               │
│     │       └─► load_workbook("data/testdata.xlsx")                │
│     │                                                               │
│     ├─► ConfigReader.get_test_data_sheet()                         │
│     │       └─► os.getenv('TEST_DATA_SHEET', 'LoginData')          │
│     │           └─► Returns: "LoginData"                           │
│     │                                                               │
│     ├─► excel.get_row_data('LoginData', 2)                         │
│     │       └─► Returns: {Username, Password, ...}                 │
│     │                                                               │
│     ├─► excel.close()                                              │
│     │                                                               │
│     └─► login_page.login(test_data['Username'],                    │
│                          test_data['Password'])                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Step 3: verify the title of the page                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  login_steps.py::verify_the_title_of_the_page()                    │
│     │                                                               │
│     ├─► LoginPage() → BasePage.__init__()                          │
│     │       └─► PlaywrightDriver.get_page()                        │
│     │                                                               │
│     ├─► login_page.get_title()                                     │
│     │       └─► self.page.title() [Playwright]                     │
│     │           └─► Returns: "Swag Labs"                           │
│     │                                                               │
│     └─► assert title == "Swag Labs"                                │
│             │                                                       │
│             ├─► PASS: Test continues                               │
│             └─► FAIL: AssertionError raised                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Framework Execution Flow (Hooks)

Before and after each scenario, the Gauge framework executes hooks:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     COMPLETE TEST EXECUTION FLOW                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  [BEFORE_SUITE]                                                    │
│     └─► PlaywrightDriver.initialize()                              │
│             ├─► Start Playwright                                   │
│             ├─► Get browser config (chromium/firefox/webkit)       │
│             ├─► Get headless setting (true/false)                  │
│             └─► Launch browser                                     │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ FOR EACH SCENARIO                                            │  │
│  ├──────────────────────────────────────────────────────────────┤  │
│  │                                                              │  │
│  │  [BEFORE_SCENARIO]                                          │  │
│  │     ├─► PlaywrightDriver.create_context()                   │  │
│  │     │       ├─► Set viewport (1920x1080)                    │  │
│  │     │       ├─► Set default timeout (30000ms)               │  │
│  │     │       ├─► Set navigation timeout (60000ms)            │  │
│  │     │       └─► Create new page                             │  │
│  │     │                                                        │  │
│  │     └─► PlaywrightDriver.start_tracing() (if enabled)       │  │
│  │                                                              │  │
│  │  [EXECUTE STEPS]                                            │  │
│  │     ├─► Step 1: Navigate to the application                 │  │
│  │     ├─► Step 2: Login with credentials/data                 │  │
│  │     └─► Step 3: Verify page (if applicable)                 │  │
│  │                                                              │  │
│  │  [AFTER_SCENARIO]                                           │  │
│  │     ├─► IF scenario failed AND screenshot_on_failure:       │  │
│  │     │       └─► PlaywrightDriver.take_screenshot()          │  │
│  │     │                                                        │  │
│  │     ├─► PlaywrightDriver.stop_tracing() (if enabled)        │  │
│  │     │                                                        │  │
│  │     └─► PlaywrightDriver.close_context()                    │  │
│  │             ├─► Close context                               │  │
│  │             └─► Reset page to None                          │  │
│  │                                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  [AFTER_SUITE]                                                     │
│     └─► PlaywrightDriver.close()                                   │
│             ├─► Close browser                                      │
│             └─► Stop Playwright                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 File Dependencies

```
GaugeFramework/
├── specs/
│   └── login.spec              ← Test specification (scenarios)
├── step_impl/
│   └── login_steps.py          ← Step implementations
├── pages/
│   ├── base_page.py            ← Base page with common methods
│   └── login_page.py           ← Login page object
├── core/
│   ├── playwright_driver.py    ← Browser management
│   ├── config_reader.py        ← Configuration reader
│   └── excel_reader.py         ← Excel data reader
├── data/
│   └── testdata.xlsx           ← Test data file
└── env/
    └── default/
        └── default.properties  ← Environment configuration
```

---

## ⚡ Quick Run Commands

```bash
# Run all scenarios in login.spec
gauge run specs/login.spec

# Run specific scenario by tag
gauge run --tags "TC001" specs/login.spec

# Run all positive tests
gauge run --tags "positive" specs/login.spec

# Run data-driven tests only
gauge run --tags "data-driven" specs/login.spec

# Run with verbose output
gauge run -v specs/login.spec

# Run in parallel
gauge run --parallel specs/login.spec
```

---

## 📊 Expected Test Data Format (testdata.xlsx)

The `LoginData` sheet should have the following structure:

| Row | TestID | Username | Password | ExpectedResult |
|-----|--------|----------|----------|----------------|
| 1 (Header) | TestID | Username | Password | ExpectedResult |
| 2 | TC001 | standard_user | secret_sauce | Success |
| 3 | TC002 | locked_out_user | secret_sauce | Locked |
| 4 | TC003 | problem_user | secret_sauce | Success |

---

*Document generated on: 2025-12-30*
