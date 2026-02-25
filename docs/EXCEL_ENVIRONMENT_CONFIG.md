# Excel-Based Environment Configuration

## Overview

The Gauge Framework now supports **Excel-based environment configuration**, allowing you to manage all environment settings (APP_URL, browser settings, timeouts, etc.) in a centralized Excel file instead of scattered properties files.

## Benefits

✅ **Centralized Configuration** - All settings in one Excel file  
✅ **Easy to Edit** - No need to edit multiple property files  
✅ **Version Control Friendly** - Track configuration changes in Git  
✅ **Environment Management** - Easily switch between DEV, QA, UAT, PROD  
✅ **Backward Compatible** - Still supports environment variables as fallback  

## Configuration File

**Location:** `data/td_FrameworkData.xlsx`  
**Sheet Name:** `Environment`

### Excel Structure

| Property | Value | Description |
|----------|-------|-------------|
| APP_URL | https://www.saucedemo.com/ | Application URL to test |
| BROWSER | chromium | Browser type: chromium, firefox, webkit |
| HEADLESS | false | Run browser in headless mode: true/false |
| ... | ... | ... |

## Setup Instructions

### 1. Create Environment Configuration Sheet

Run the setup script to create the Environment configuration sheet:

```bash
python setup_env_config.py
```

This will create/update the `Environment` sheet in `data/td_FrameworkData.xlsx` with all default configuration properties.

### 2. View Current Configuration

To view all current configuration settings:

```bash
python view_env_config.py
```

This displays all configuration values loaded from Excel.

### 3. Edit Configuration

1. Open `data/td_FrameworkData.xlsx` in Excel
2. Navigate to the `Environment` sheet
3. Edit values in the **Value** column
4. Save the file

**Example: Change APP_URL**
- Find the `APP_URL` row
- Change the value from `https://www.saucedemo.com/` to your desired URL
- Save the file

## Available Configuration Properties

### Application Configuration
- `APP_URL` - Application URL to test
- `APP_NAME` - Application name for reporting
- `ENVIRONMENT` - Current environment (DEV, QA, UAT, PROD)

### Browser Configuration
- `BROWSER` - Browser type: chromium, firefox, webkit
- `HEADLESS` - Run in headless mode: true/false
- `SLOW_MO` - Slow motion delay in milliseconds
- `VIEWPORT_WIDTH` - Browser viewport width in pixels
- `VIEWPORT_HEIGHT` - Browser viewport height in pixels

### Timeout Configuration
- `DEFAULT_TIMEOUT` - Default timeout in milliseconds
- `NAVIGATION_TIMEOUT` - Navigation timeout in milliseconds
- `ACTION_TIMEOUT` - Action timeout in milliseconds

### Screenshots & Tracing
- `SCREENSHOT_ON_FAILURE` - Capture screenshot on test failure
- `ENABLE_TRACING` - Enable Playwright tracing
- `TRACE_DIR` - Directory to store trace files

### Test Data Configuration
- `TEST_DATA_FILE` - Test data Excel file name
- `TEST_DATA_SHEET` - Test data sheet name
- `BASE_PATH` - Base path for data files

### Retry Configuration
- `RETRY_COUNT` - Number of retries for failed tests

### Logging Configuration
- `LOG_LEVEL` - Logging level: DEBUG, INFO, WARNING, ERROR

## How It Works

### Configuration Priority

The framework uses a **dual-source configuration** approach:

1. **Environment Variables** (Highest Priority)
   - If an environment variable is set, it takes precedence
   - Useful for CI/CD pipelines or temporary overrides

2. **Excel Configuration** (Default)
   - If no environment variable is set, reads from Excel
   - Primary source for configuration management

### Code Usage

```python
from core.config_reader import ConfigReader

# Get configuration values
app_url = ConfigReader.get_app_url()
browser = ConfigReader.get_browser_type()
is_headless = ConfigReader.is_headless()
```

The `ConfigReader` automatically handles the dual-source lookup.

## Examples

### Example 1: Change Application URL

**Before:**
```
APP_URL = https://www.saucedemo.com/
```

**Steps:**
1. Open `data/td_FrameworkData.xlsx`
2. Go to `Environment` sheet
3. Find `APP_URL` row
4. Change value to `https://your-app-url.com/`
5. Save file

**Result:** All tests will now use the new URL

### Example 2: Switch to Firefox Browser

**Before:**
```
BROWSER = chromium
```

**Steps:**
1. Open `data/td_FrameworkData.xlsx`
2. Go to `Environment` sheet
3. Find `BROWSER` row
4. Change value to `firefox`
5. Save file

**Result:** Tests will run in Firefox instead of Chrome

### Example 3: Enable Headless Mode

**Before:**
```
HEADLESS = false
```

**Steps:**
1. Open `data/td_FrameworkData.xlsx`
2. Go to `Environment` sheet
3. Find `HEADLESS` row
4. Change value to `true`
5. Save file

**Result:** Browser will run in headless mode (no UI)

## Environment-Specific Configuration

You can maintain multiple Excel files for different environments:

```
data/
├── td_FrameworkData_DEV.xlsx    # Development settings
├── td_FrameworkData_QA.xlsx     # QA settings
├── td_FrameworkData_UAT.xlsx    # UAT settings
└── td_FrameworkData_PROD.xlsx   # Production settings
```

Set the environment variable to switch:

```bash
# Windows PowerShell
$env:ENV_CONFIG_FILE = "data/td_FrameworkData_UAT.xlsx"

# Linux/Mac
export ENV_CONFIG_FILE="data/td_FrameworkData_UAT.xlsx"
```

## Troubleshooting

### Configuration Not Loading

**Problem:** Changes in Excel are not reflected in tests

**Solution:**
1. Ensure you saved the Excel file after making changes
2. Close and reopen Excel if file is locked
3. Run `python view_env_config.py` to verify configuration

### File Not Found Error

**Problem:** `FileNotFoundError: Environment config file not found`

**Solution:**
1. Run `python setup_env_config.py` to create the configuration file
2. Verify the file exists at `data/td_FrameworkData.xlsx`

### Invalid Values

**Problem:** Tests fail due to invalid configuration values

**Solution:**
1. Check the `Description` column in Excel for valid value formats
2. Ensure boolean values are `true` or `false` (lowercase)
3. Ensure numeric values don't have extra spaces or characters

## Migration from Properties Files

If you're migrating from the old properties-based configuration:

1. Run `python setup_env_config.py` to create Excel configuration
2. Copy values from your old properties files to Excel
3. Test with `python view_env_config.py`
4. Run tests to verify: `gauge run specs`

The framework maintains **backward compatibility**, so environment variables will still work as overrides.

## Best Practices

1. **Version Control** - Commit the Excel configuration file to Git
2. **Documentation** - Use the Description column to document each property
3. **Validation** - Run `view_env_config.py` after making changes
4. **Backup** - Keep backup copies before major changes
5. **Environment Separation** - Use separate files for different environments

## Related Files

- `core/env_config_reader.py` - Excel configuration reader
- `core/config_reader.py` - Dual-source configuration manager
- `setup_env_config.py` - Setup script to create configuration
- `view_env_config.py` - View current configuration
- `data/td_FrameworkData.xlsx` - Configuration Excel file

## Support

For issues or questions about Excel-based configuration:
1. Check this documentation
2. Run `python view_env_config.py` to debug
3. Verify Excel file structure matches expected format
