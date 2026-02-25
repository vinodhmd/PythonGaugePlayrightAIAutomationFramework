# ReportLogger Utility - Usage Guide

## Overview
The `ReportLogger` utility provides reusable methods for logging execution steps and data to Gauge reports in a clean, consistent, and maintainable way.

## Benefits
✅ **Cleaner Code**: Reduce repetitive logging code  
✅ **Consistency**: Standardized formatting across all steps  
✅ **Maintainability**: Easy to update logging format in one place  
✅ **Readability**: Clear, descriptive method names  

## Location
`core/report_logger.py`

## Quick Start

### Import the Utility
```python
from core.report_logger import ReportLogger, log_step, log_complete
```

### Basic Usage
```python
@step("My Test Step")
def my_test_step():
    # Start logging
    log_step("My Test Step")
    
    # Log information
    ReportLogger.log_info("Browser", "Chrome")
    ReportLogger.log_url("https://example.com")
    
    # Perform actions
    # ... your test code ...
    
    # Complete logging
    log_complete("Step completed successfully")
```

## Available Methods

### 1. **Step Header & Footer**

#### `log_step(step_name, icon="📍")`
Quick method to log a step header with formatting.

```python
log_step("Login to Application")
# Output:
# ════════════════════════════════════════════════════════════
# 📍 EXECUTION STEP: Login to Application
# ────────────────────────────────────────────────────────────
```

#### `log_complete(message)` / `log_failed(message)`
Quick methods to log step completion or failure.

```python
log_complete("Login successful")
# Output:
# ✅ Login successful
# ════════════════════════════════════════════════════════════
```

#### `ReportLogger.log_step_header(step_name, icon="📍")`
Full method for step header.

#### `ReportLogger.log_step_footer(success=True, message=None)`
Full method for step footer.

---

### 2. **Data Source Logging**

#### `ReportLogger.log_data_source(file_name, sheet_name, row_number=None, test_id=None)`
Log Excel data source information.

```python
ReportLogger.log_data_source("testdata.xlsx", "LoginData", row_number=2)
# Output:
#    📄 Excel File: testdata.xlsx
#    📑 Sheet Name: LoginData
#    📌 Row Number: 2
#    ────────────────────────────────────────────────────────────
```

---

### 3. **Test Data Logging**

#### `ReportLogger.log_test_data(test_data, mask_passwords=True)`
Log test data dictionary with automatic password masking.

```python
test_data = {"Username": "admin", "Password": "secret123"}
ReportLogger.log_test_data(test_data)
# Output:
#    📊 Test Data Retrieved:
#       • Username: admin
#       • Password: *********
#    ────────────────────────────────────────────────────────────
```

---

### 4. **Actions Logging**

#### `ReportLogger.log_actions(actions_list)`
Log a list of actions performed.

```python
actions = [
    "Fill username input",
    "Fill password input",
    "Click login button"
]
ReportLogger.log_actions(actions)
# Output:
#    🎯 Actions performed:
#       1. Fill username input
#       2. Fill password input
#       3. Click login button
#    ────────────────────────────────────────────────────────────
```

---

### 5. **Verification Logging**

#### `ReportLogger.log_verification(expected, actual, passed=None)`
Log verification results with expected vs actual comparison.

```python
ReportLogger.log_verification("Swag Labs", "Swag Labs", passed=True)
# Output:
#    🎯 Expected: Swag Labs
#    📋 Actual: Swag Labs
#    ────────────────────────────────────────────────────────────
#    ✅ VERIFICATION PASSED
```

---

### 6. **Credentials Logging**

#### `ReportLogger.log_credentials(username, password=None)`
Log credentials with automatic password masking.

```python
ReportLogger.log_credentials("admin", "secret123")
# Output:
#    👤 Username: admin
#    🔑 Password: *********
```

---

### 7. **URL & Browser Info**

#### `ReportLogger.log_url(url, label="Target URL")`
```python
ReportLogger.log_url("https://example.com")
# Output: 🌐 Target URL: https://example.com
```

#### `ReportLogger.log_browser_info(browser_type, headless)`
```python
ReportLogger.log_browser_info("chromium", False)
# Output:
#    🔧 Browser: chromium
#    👁️ Headless Mode: False
```

---

### 8. **General Logging**

#### `ReportLogger.log_info(key, value, mask_password=False)`
```python
ReportLogger.log_info("Timeout", "30000")
# Output: 🔧 Timeout: 30000
```

#### `ReportLogger.log_success(message)`
```python
ReportLogger.log_success("Data loaded successfully")
# Output: ✅ Data loaded successfully
```

#### `ReportLogger.log_error(message)`
```python
ReportLogger.log_error("Connection timeout")
# Output: ❌ ERROR: Connection timeout
```

#### `ReportLogger.log_warning(message)`
```python
ReportLogger.log_warning("Deprecated method used")
# Output: ⚠️ WARNING: Deprecated method used
```

#### `ReportLogger.log_custom(message, icon="ℹ️")`
```python
ReportLogger.log_custom("Custom message", "🚀")
# Output: 🚀 Custom message
```

---

### 9. **Utility Methods**

#### `ReportLogger.log_separator()`
```python
ReportLogger.log_separator()
# Output: ────────────────────────────────────────────────────────────
```

#### `ReportLogger.log_section(title)`
```python
ReportLogger.log_section("Database Connection")
# Output: 📌 Database Connection
```

#### `ReportLogger.log_timestamp(label="Timestamp")`
```python
ReportLogger.log_timestamp()
# Output: 🕐 Timestamp: 2025-12-31 12:45:30
```

---

## Complete Example

### Before (Old Way)
```python
@step("Login with credentials <username> and <password>")
def login(username, password):
    Messages.write_message("═" * 60)
    Messages.write_message("📍 EXECUTION STEP: Login with Credentials")
    Messages.write_message("─" * 60)
    Messages.write_message(f"   👤 Username: {username}")
    Messages.write_message(f"   🔑 Password: {'*' * len(password)}")
    Messages.write_message("─" * 60)
    Messages.write_message("   🎯 Actions performed:")
    Messages.write_message("      1. Fill username input")
    Messages.write_message("      2. Fill password input")
    Messages.write_message("      3. Click login button")
    Messages.write_message("─" * 60)
    
    login_page = LoginPage()
    login_page.login(username, password)
    
    Messages.write_message("   ✅ Login completed successfully")
    Messages.write_message("═" * 60)
```

### After (New Way with ReportLogger)
```python
@step("Login with credentials <username> and <password>")
def login(username, password):
    log_step("Login with Credentials")
    ReportLogger.log_credentials(username, password)
    ReportLogger.log_separator()
    
    actions = [
        "Fill username input",
        "Fill password input",
        "Click login button"
    ]
    ReportLogger.log_actions(actions)
    
    login_page = LoginPage()
    login_page.login(username, password)
    
    log_complete("Login completed successfully")
```

**Result**: Same output, but **50% less code** and much cleaner! 🎉

---

## Best Practices

1. **Use Quick Methods**: Use `log_step()` and `log_complete()` for simple cases
2. **Consistent Icons**: Stick to the default icons for consistency
3. **Mask Sensitive Data**: Always use password masking for credentials
4. **Group Related Logs**: Use separators to group related information
5. **Clear Messages**: Write descriptive messages that explain what's happening

---

## Customization

You can extend the `ReportLogger` class with your own methods:

```python
# In core/report_logger.py
@staticmethod
def log_api_request(method, endpoint, status_code):
    """Log API request details"""
    Messages.write_message(f"   🌐 API {method}: {endpoint}")
    Messages.write_message(f"   📊 Status Code: {status_code}")
```

Then use it:
```python
ReportLogger.log_api_request("POST", "/api/login", 200)
```

---

## Migration Guide

To migrate existing steps:

1. **Import the utility**:
   ```python
   from core.report_logger import ReportLogger, log_step, log_complete
   ```

2. **Replace header blocks** with `log_step()`
3. **Replace footer blocks** with `log_complete()`
4. **Use specific methods** for data, actions, verifications, etc.
5. **Test** to ensure output looks correct

---

## Summary

The `ReportLogger` utility makes your test code:
- ✅ **Cleaner** - Less boilerplate code
- ✅ **Consistent** - Standardized formatting
- ✅ **Maintainable** - Easy to update
- ✅ **Readable** - Clear intent

Start using it in your new steps and gradually migrate existing ones! 🚀
