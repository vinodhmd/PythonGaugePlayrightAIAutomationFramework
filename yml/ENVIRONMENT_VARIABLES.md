# Environment Variables Documentation

This document describes all environment variables used in the GaugeFramework YAML execution packages and Python runners.

---

## 📋 Table of Contents

1. [Configuration Files Overview](#configuration-files-overview)
2. [Environment Variables](#environment-variables)
3. [YAML Configuration Files](#yaml-configuration-files)
4. [How Environment Variables are Loaded](#how-environment-variables-are-loaded)

---

## Configuration Files Overview

### Python Runner Scripts
- **`parallelgauge_runner.py`** - Executes tests in parallel across multiple browsers
- **`bulkgauge_runner.py`** - Executes tests with tag-based filtering
- **`env_loader.py`** - Loads environment variables from Excel configuration

### YAML Configuration Files
- **`yl_parallelexecution.yml`** - Configuration for parallel browser execution
- **`yl_bulkexecution.yml`** - Configuration for bulk tag-based execution
- **`yl_execution.yml`** - Configuration for standard execution with tags

---

## Environment Variables

### Core Environment Variables

#### 1. `TEST_DATA_FILE`
- **Source**: `env/default/default.properties`
- **Purpose**: Specifies the Excel file containing test data and environment configuration
- **Default**: `td_FrameworkData.xlsx`
- **Used By**: 
  - `env_loader.py` - To locate the Excel file with Environment sheet
  - `Core_basePage.py` - For test data file discovery
  - `TestDataManager.py` - For test data retrieval
- **Example**: 
  ```properties
  TEST_DATA_FILE=td_FrameworkData.xlsx
  ```

#### 2. `BROWSER`
- **Source**: 
  - Excel Environment sheet (for single browser execution)
  - Set dynamically by `parallelgauge_runner.py` (for multi-browser execution)
- **Purpose**: Specifies which browser to use for test execution
- **Valid Values**: `chrome`, `firefox`, `edge`, `webkit`
- **Used By**: 
  - `Core_basePage.py` - To launch the appropriate browser
  - `parallelgauge_runner.py` - Sets this for each browser in parallel execution
- **Example**:
  ```python
  env["BROWSER"] = "chrome"
  ```

#### 3. `GAUGE_REPORTS_DIR`
- **Source**: Set by `parallelgauge_runner.py` for multi-browser execution
- **Purpose**: Specifies the directory where Gauge reports should be generated
- **Default**: `reports/`
- **Used By**: 
  - `Core_basePage.py` - For screenshot storage
  - `ScreenshotUtils.py` - For screenshot capture
  - `WebElementHelper.py` - For element screenshots
- **Example**:
  ```python
  env["GAUGE_REPORTS_DIR"] = "reports/chrome"
  ```

### Excel-Loaded Environment Variables

All variables defined in the **Environment sheet** of the test data Excel file are loaded into the environment by `env_loader.py`. Common variables include:

#### Application Configuration
- `APP_URL` - Base URL of the application under test
- `APP_TIMEOUT` - Default timeout for operations (in seconds)
- `HEADLESS` - Run browser in headless mode (`true`/`false`)
- `SLOW_MO` - Slow down browser operations (in milliseconds)

#### Credentials
- `USERNAME` - Default username for login
- `PASSWORD` - Default password for login

#### Test Data Configuration
- `TEST_DATA_SHEET` - Name of the sheet containing test data
- `ENVIRONMENT` - Current environment (e.g., `Default`, `UAT`, `PROD`)

---

## YAML Configuration Files

### 1. `yl_parallelexecution.yml`

Configures parallel execution across multiple browsers.

```yaml
execution:
  env: Default                    # Gauge environment to use
  browsers:                       # List of browsers for parallel execution
    - chrome
    - edge
  parallel: true                  # Enable parallel execution
  nodes: 2                        # Number of parallel nodes per browser
  
  include_tags:                   # Tags to include (OR logic)
    - smoke
    - regression
  
  exclude_tags:                   # Tags to exclude (AND NOT logic)
    - wip
    - skip
```

**Environment Variables Set**:
- `BROWSER` - Set for each browser in the list
- `GAUGE_REPORTS_DIR` - Set to `reports/{browser}` for each browser

### 2. `yl_bulkexecution.yml`

Configures bulk execution with tag filtering.

```yaml
execution:
  env: Default                    # Gauge environment to use
  parallel: false                 # Sequential execution
  
  include_tags:                   # Tags to include (semicolon-separated)
    - TC001;TC002;TC003
    - PAY001
  
  exclude_tags:                   # Tags to exclude
    - wip
```

### 3. `yl_execution.yml`

Configures standard execution with parallel threads.

```yaml
execution:
  env: Default                    # Gauge environment to use
  parallel: true                  # Enable parallel execution
  threads: 4                      # Number of parallel threads
  
  include_tags:                   # Tags to include
    - TC001;TC002;TC003;TC004
    - PAY001
  
  exclude_tags:                   # Tags to exclude (empty = none)

reporting:
  html: true                      # Generate HTML reports
  allure: false                   # Generate Allure reports
```

---

## How Environment Variables are Loaded

### Loading Sequence

1. **Properties File** (`env/default/default.properties`)
   - Gauge loads all properties from this file
   - `TEST_DATA_FILE` is read to determine which Excel file to use

2. **Excel Environment Sheet** (`env_loader.py`)
   ```python
   excel_env = load_env_context()
   os.environ.update(excel_env)
   ```
   - Reads the Environment sheet from the Excel file
   - Loads all key-value pairs as environment variables
   - Overwrites any existing environment variables

3. **Runner-Specific Variables** (e.g., `parallelgauge_runner.py`)
   ```python
   env = os.environ.copy()
   env["BROWSER"] = browser
   env["GAUGE_REPORTS_DIR"] = f"reports/{browser}"
   ```
   - Sets execution-specific variables
   - Used for parallel browser execution

### Access in Code

Environment variables can be accessed in Python code using:

```python
import os

# Direct access
browser = os.getenv('BROWSER', 'chrome')

# Using BasePage helper
browser = BasePage._get_config('BROWSER')
```

---

## YAML Configuration Parameters

### Execution Section

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `env` | string | Gauge environment name (maps to `env/{name}/` folder) | `default` |
| `parallel` | boolean | Enable parallel execution | `false` |
| `threads` | integer | Number of parallel threads (for single browser) | `1` |
| `nodes` | integer | Number of parallel nodes (for multi-browser) | `2` |
| `browsers` | list | List of browsers for parallel execution | `[]` |
| `include_tags` | list | Tags to include (OR logic, semicolon-separated) | `[]` |
| `exclude_tags` | list | Tags to exclude (AND NOT logic) | `[]` |

### Tag Expression Logic

**Include Tags** (OR logic):
```yaml
include_tags:
  - smoke;regression
  - critical
```
Translates to: `(smoke | regression | critical)`

**Exclude Tags** (AND NOT logic):
```yaml
exclude_tags:
  - wip
  - skip
```
Translates to: `!wip & !skip`

**Combined**:
```
--tags=(smoke | regression | critical) & !wip & !skip
```

---

## Examples

### Example 1: Run Tests on Chrome and Edge in Parallel

```bash
python yml/parallelgauge_runner.py
```

Uses `yl_parallelexecution.yml`:
- Loads environment variables from Excel
- Runs tests on both Chrome and Edge simultaneously
- Each browser gets its own report directory

### Example 2: Run Specific Tags in Bulk

```bash
python yml/bulkgauge_runner.py
```

Uses `yl_bulkexecution.yml`:
- Loads environment variables from Excel
- Runs tests matching `TC001`, `TC002`, `TC003`, or `PAY001`
- Excludes tests tagged with `wip`

### Example 3: Custom Environment

Modify the `env` parameter in YAML:
```yaml
execution:
  env: UAT  # Uses env/UAT/default.properties
```

---

## Best Practices

1. **Centralize Configuration**: Store all environment-specific values in the Excel Environment sheet
2. **Use Descriptive Names**: Use clear, uppercase names for environment variables
3. **Document Custom Variables**: Add any custom variables to this documentation
4. **Version Control**: Keep YAML files in version control, exclude `.properties` files with sensitive data
5. **Environment Separation**: Use different `env` values for different environments (Default, UAT, PROD)

---

## Troubleshooting

### Issue: Environment variables not loaded
**Solution**: Ensure `env_loader.load_env_context()` is called before Gauge execution

### Issue: Wrong browser launched
**Solution**: Check `BROWSER` value in Excel Environment sheet or YAML configuration

### Issue: Reports not in expected directory
**Solution**: Verify `GAUGE_REPORTS_DIR` is set correctly for parallel execution

---

*Last Updated: 2026-01-13*
