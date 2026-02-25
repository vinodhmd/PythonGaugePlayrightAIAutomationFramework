# Automatic Test Data Loading - User Guide

## Overview

The framework now **automatically loads test data** based on scenario tags! You no longer need to manually read Excel files in your step implementations.

## How It Works

### 1. Tag Your Spec

```gherkin
# Employee Creation Web Application

## Employee Creation Payday Application
Tags: PAY001, regression, smoke

* Payroll login to load the url
* Payroll login with credentials
```

### 2. Add Data to Excel

In `data/td_FrameworkData.xlsx`, add a row with matching tag:

| Tags   | ModuleName           | Url                        | Username | Password        |
|--------|---------------------|----------------------------|----------|-----------------|
| PAY001 | Payroll Application | http://qa.payday.internal  | vinodh   | Welcome@payday  |

### 3. Access Data in Steps

The framework **automatically**:
- Reads the tag from your spec (`PAY001`)
- Finds the matching row in Excel
- Loads all data into `TestDataManager`
- Makes it available throughout the scenario

```python
from core.TestDataManager import TestDataManager

@step("Payroll login with credentials")
def payroll_login_with_credentials():
    # Data is already loaded! Just access it:
    username = TestDataManager.get_value('Username')
    password = TestDataManager.get_value('Password')
    url = TestDataManager.get_value('Url')
    
    # Use the data
    page.login(username, password)
```

## TestDataManager API

### Check if Data Exists

```python
if TestDataManager.has_test_data():
    # Data is available
    pass
```

### Get Specific Values

```python
# Get a value with optional default
username = TestDataManager.get_value('Username')
url = TestDataManager.get_value('Url', 'http://default.com')
```

### Get All Data

```python
# Get the complete test data dictionary
test_data = TestDataManager.get_test_data()
# Returns: {'Tags': 'PAY001', 'Username': 'vinodh', ...}
```

### Get Metadata

```python
# Get the test ID (tag)
test_id = TestDataManager.get_test_id()  # Returns: 'PAY001'

# Get the sheet name where data was found
sheet = TestDataManager.get_test_sheet()  # Returns: 'EmployeeCreation'
```

## Complete Example

### Spec File: `sp_EmployeeCreation.spec`

```gherkin
# Employee Creation Web Application

## Employee Creation Payday Application
Tags: PAY001, regression

* Payroll login to load the url
* Payroll login with credentials
* Create new employee
* Verify employee created
```

### Excel Data: `td_FrameworkData.xlsx` → `EmployeeCreation` sheet

| Tags   | Url                       | Username | Password        | EmployeeName | Department |
|--------|---------------------------|----------|-----------------|--------------|------------|
| PAY001 | http://qa.payday.internal | vinodh   | Welcome@payday  | John Doe     | IT         |

### Step Implementation: `st_EmployeeCreation.py`

```python
from core.TestDataManager import TestDataManager
from core.PageObjectManager import PageObjectManager

@step("Payroll login to load the url")
def payroll_login_to_load_the_url():
    # Get URL from auto-loaded data
    url = TestDataManager.get_value('Url')
    
    page = PageObjectManager.get_page(EmployeeCreation)
    page.navigate_to(url)

@step("Payroll login with credentials")
def payroll_login_with_credentials():
    # Get credentials from auto-loaded data
    username = TestDataManager.get_value('Username')
    password = TestDataManager.get_value('Password')
    
    page = PageObjectManager.get_page(EmployeeCreation)
    page.login(username, password)

@step("Create new employee")
def create_new_employee():
    # Get employee data from auto-loaded data
    employee_name = TestDataManager.get_value('EmployeeName')
    department = TestDataManager.get_value('Department')
    
    page = PageObjectManager.get_page(EmployeeCreation)
    page.create_employee(employee_name, department)
```

## Benefits

✅ **No Manual Excel Reading** - Data loads automatically
✅ **Tag-Based Mapping** - Just add tags to your spec
✅ **Global Access** - Available in all steps of the scenario
✅ **Clean Code** - No boilerplate Excel reading code
✅ **Flexible** - Add any columns you need in Excel
✅ **Automatic Cleanup** - Data cleared after each scenario

## How Data Loading Works

### 1. Before Scenario (Automatic)

```
Gauge Spec with Tag: PAY001
         ↓
hooks.py @before_scenario
         ↓
TestDataManager.load_test_data()
         ↓
Searches all sheets for "PAY001" in "Tags" column
         ↓
Finds: EmployeeCreation sheet, Row 3
         ↓
Loads: {'Tags': 'PAY001', 'Url': '...', 'Username': '...', ...}
         ↓
Stores in: data_store.scenario['test_data']
```

### 2. During Steps (Your Code)

```python
# Simply access the data
username = TestDataManager.get_value('Username')
```

### 3. After Scenario (Automatic)

```
hooks.py @after_scenario
         ↓
TestDataManager.clear()
         ↓
Data cleared for next scenario
```

## Multiple Tags

If your spec has multiple tags:

```gherkin
Tags: PAY001, TC005, regression
```

The framework uses the **first tag** that matches a row in Excel. Priority order:
1. PAY001 (checked first)
2. TC005 (checked if PAY001 not found)
3. regression (checked if others not found)

## No Tag Scenarios

If a scenario has no matching tag:

```python
if not TestDataManager.has_test_data():
    # Fall back to configuration or hardcoded values
    url = BasePage.get_app_url()
```

## Adding New Test Data

### Step 1: Add Tag to Spec

```gherkin
Tags: PAY002
```

### Step 2: Add Row to Excel

Open `data/td_FrameworkData.xlsx`, go to appropriate sheet, add:

| Tags   | Url                  | Username | Password |
|--------|---------------------|----------|----------|
| PAY002 | http://staging.com  | admin    | pass123  |

### Step 3: Run Test

That's it! The framework automatically finds and loads the data.

## Debugging

### Check What Data Was Loaded

The framework logs this automatically:

```
📋 Test Data Auto-Loaded: PAY001 from EmployeeCreation sheet
   Available data keys: Tags, ModuleName, Url, Username, Password
```

### Manually Check in Steps

```python
test_data = TestDataManager.get_test_data()
print(f"Loaded data: {test_data}")
```

## Best Practices

1. **Use Descriptive Tags**: `PAY001`, `EMP_CREATE_001`, not just `TC1`
2. **Keep Tags Unique**: Each tag should appear only once across all sheets
3. **Add All Needed Columns**: Add any data columns your tests need
4. **Document Tags**: Keep a list of what each tag represents
5. **Check Data Exists**: Always check `has_test_data()` before accessing

## Migration from Old Approach

### Old Way (Manual)

```python
@step("Login with credentials")
def login():
    # Manual Excel reading
    test_data_file = BasePage.get_test_data_file()
    test_id = BasePage.get_test_id_from_tags()
    test_data_sheet = get_sheet_for_test_id(test_id)
    excel = ExcelReader(test_data_file)
    test_data = excel.get_test_data_by_id(test_data_sheet, test_id, columns)
    excel.close()
    
    username = test_data['Username']
    password = test_data['Password']
```

### New Way (Automatic)

```python
@step("Login with credentials")
def login():
    # Data already loaded!
    username = TestDataManager.get_value('Username')
    password = TestDataManager.get_value('Password')
```

**Result**: ~10 lines reduced to 2 lines! 🎉
