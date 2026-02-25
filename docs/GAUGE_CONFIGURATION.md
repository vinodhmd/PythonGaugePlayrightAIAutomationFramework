# Gauge Framework Configuration Guide

## Overview
This guide covers all configuration options for the Gauge automation framework, including environment properties, manifest settings, and execution parameters.

---

## Table of Contents
1. [Project Structure](#project-structure)
2. [Manifest Configuration](#manifest-configuration)
3. [Environment Properties](#environment-properties)
4. [Gauge Properties](#gauge-properties)
5. [Configuration Reader](#configuration-reader)
6. [Running Tests](#running-tests)
7. [Environment-Specific Configuration](#environment-specific-configuration)
8. [Best Practices](#best-practices)

---

## Project Structure

```
GaugeFramework/
├── env/
│   └── default/
│       ├── default.properties    # Custom environment properties
│       └── gauge.properties      # Gauge-specific properties
├── manifest.json                 # Gauge project manifest
├── specs/                        # Test specifications
├── step_impl/                    # Step implementations
├── core/                         # Core utilities
│   └── config_reader.py         # Configuration reader
├── data/                         # Test data files
└── reports/                      # Test reports
```

---

## Manifest Configuration

**File**: `manifest.json`

The manifest file defines the Gauge project settings.

```json
{
    "Language": "python",
    "Plugins": [
        "html-report",
        "screenshot"
    ]
}
```

### Available Plugins
- **html-report**: Generates HTML test reports
- **screenshot**: Enables screenshot capture
- **xml-report**: Generates XML reports (JUnit format)
- **json-report**: Generates JSON reports
- **spectacle**: Generates documentation from specs

### Adding Plugins
```bash
gauge install <plugin-name>
```

Example:
```bash
gauge install xml-report
gauge install json-report
```

---

## Environment Properties

### Location
- **Default**: `env/default/default.properties`
- **Custom**: `env/<environment-name>/default.properties`

### Configuration Categories

#### 1. **Application Configuration**

```properties
# Application URL
APP_URL = https://www.saucedemo.com/
```

#### 2. **Browser Configuration**

```properties
# Browser type: chromium, firefox, webkit
BROWSER = chromium

# Run browser in headless mode
HEADLESS = false

# Slow down operations (milliseconds)
SLOW_MO = 0

# Viewport dimensions
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
```

**Browser Options**:
- `chromium` - Chrome/Edge browser
- `firefox` - Firefox browser
- `webkit` - Safari browser

#### 3. **Timeout Configuration**

```properties
# Default timeout for all operations (milliseconds)
DEFAULT_TIMEOUT = 30000

# Navigation timeout (milliseconds)
NAVIGATION_TIMEOUT = 60000

# Action timeout (milliseconds)
ACTION_TIMEOUT = 10000
```

**Timeout Values**:
- `DEFAULT_TIMEOUT`: General operations (30 seconds)
- `NAVIGATION_TIMEOUT`: Page navigation (60 seconds)
- `ACTION_TIMEOUT`: Element interactions (10 seconds)

#### 4. **Screenshots & Tracing**

```properties
# Capture screenshots on test failure
SCREENSHOT_ON_FAILURE = true

# Enable Playwright tracing
ENABLE_TRACING = false

# Trace files directory
TRACE_DIR = reports/traces
```

**Tracing**:
- When enabled, creates `.zip` files with detailed execution traces
- View traces using: `npx playwright show-trace <trace-file.zip>`

#### 5. **Test Data Configuration**

```properties
# Excel test data file
TEST_DATA_FILE = testdata.xlsx

# Default sheet name
TEST_DATA_SHEET = LoginData
```

**Multiple Data Files**:
```properties
# You can specify different files for different environments
TEST_DATA_FILE = testdata_qa.xlsx    # QA environment
TEST_DATA_FILE = testdata_prod.xlsx  # Production environment
```

#### 6. **Retry Configuration**

```properties
# Number of retries for failed tests
RETRY_COUNT = 0
```

#### 7. **Logging Configuration**

```properties
# Log level: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL = INFO
```

---

## Gauge Properties

**File**: `env/default/gauge.properties`

Gauge-specific settings for test execution.

```properties
# Gauge internal properties
gauge_reports_dir = reports
gauge_clear_state_level = scenario

# Screenshot settings
screenshot_on_failure = true

# Parallel execution
enable_multithreading = false

# Number of parallel streams (if multithreading enabled)
# gauge_parallel_streams = 4
```

### Key Properties

#### `gauge_reports_dir`
Directory where reports are generated.
```properties
gauge_reports_dir = reports
```

#### `gauge_clear_state_level`
When to clear test state:
- `suite` - Clear after entire test suite
- `spec` - Clear after each specification
- `scenario` - Clear after each scenario (recommended)

```properties
gauge_clear_state_level = scenario
```

#### `screenshot_on_failure`
Automatically capture screenshots on failure.
```properties
screenshot_on_failure = true
```

#### `enable_multithreading`
Enable parallel test execution.
```properties
enable_multithreading = true
gauge_parallel_streams = 4
```

---

## Configuration Reader

**File**: `core/config_reader.py`

The `ConfigReader` class provides methods to access configuration values.

### Usage

```python
from core.config_reader import ConfigReader

# Application
app_url = ConfigReader.get_app_url()

# Browser
browser = ConfigReader.get_browser_type()
headless = ConfigReader.is_headless()

# Timeouts
timeout = ConfigReader.get_default_timeout()

# Test Data
data_file = ConfigReader.get_test_data_file()
data_sheet = ConfigReader.get_test_data_sheet()

# Screenshots
screenshot_enabled = ConfigReader.screenshot_on_failure()
```

### Available Methods

| Method | Returns | Default |
|--------|---------|---------|
| `get_app_url()` | Application URL | - |
| `get_browser_type()` | Browser name | `chromium` |
| `is_headless()` | Boolean | `true` |
| `get_slow_mo()` | Integer (ms) | `0` |
| `get_viewport_width()` | Integer | `1920` |
| `get_viewport_height()` | Integer | `1080` |
| `get_default_timeout()` | Integer (ms) | `30000` |
| `get_navigation_timeout()` | Integer (ms) | `60000` |
| `get_action_timeout()` | Integer (ms) | `10000` |
| `screenshot_on_failure()` | Boolean | `true` |
| `is_tracing_enabled()` | Boolean | `false` |
| `get_trace_dir()` | String | `reports/traces` |
| `get_test_data_file()` | String | `testdata.xlsx` |
| `get_test_data_sheet()` | String | `LoginData` |
| `get_retry_count()` | Integer | `0` |
| `get_log_level()` | String | `INFO` |

---

## Running Tests

### Basic Execution

```bash
# Run all specs
gauge run specs

# Run specific spec
gauge run specs/login.spec

# Run with tags
gauge run --tags "smoketesting" specs

# Run excluding tags
gauge run --tags "!uattesting" specs
```

### With Environment

```bash
# Use specific environment
gauge run --env qa specs

# Multiple environments
gauge run --env qa,staging specs
```

### Parallel Execution

```bash
# Run in parallel (4 streams)
gauge run -p -n 4 specs

# Parallel with specific tags
gauge run -p -n 4 --tags "regression" specs
```

### Verbose Output

```bash
# Verbose mode
gauge run -v specs

# Very verbose (debug)
gauge run -vv specs
```

### Using Build Script

```bash
# Full build (clean, install, run)
python build.py

# Skip dependency installation
python build.py --skip-install

# Skip clean step
python build.py --skip-clean

# Skip both
python build.py --skip-install --skip-clean
```

---

## Environment-Specific Configuration

### Creating New Environment

1. **Create directory**:
   ```bash
   mkdir env/qa
   ```

2. **Create properties files**:
   ```
   env/qa/default.properties
   env/qa/gauge.properties
   ```

3. **Configure environment-specific values**:
   ```properties
   # env/qa/default.properties
   APP_URL = https://qa.saucedemo.com/
   BROWSER = chromium
   HEADLESS = true
   TEST_DATA_FILE = testdata_qa.xlsx
   ```

4. **Run with environment**:
   ```bash
   gauge run --env qa specs
   ```

### Example Environments

#### Development
```properties
# env/dev/default.properties
APP_URL = http://localhost:3000
HEADLESS = false
SLOW_MO = 100
LOG_LEVEL = DEBUG
```

#### QA
```properties
# env/qa/default.properties
APP_URL = https://qa.example.com
HEADLESS = true
SCREENSHOT_ON_FAILURE = true
ENABLE_TRACING = true
```

#### Production
```properties
# env/prod/default.properties
APP_URL = https://example.com
HEADLESS = true
SCREENSHOT_ON_FAILURE = true
RETRY_COUNT = 2
```

---

## Best Practices

### 1. **Environment Separation**
- Keep separate configurations for dev, qa, staging, prod
- Never hardcode environment-specific values in code

### 2. **Sensitive Data**
- Don't commit sensitive data (passwords, API keys) to version control
- Use environment variables or secure vaults
- Add `env/*/default.properties` to `.gitignore` if needed

### 3. **Timeouts**
- Set realistic timeouts based on application performance
- Use longer timeouts for slower environments
- Adjust timeouts for CI/CD pipelines

### 4. **Screenshots**
- Always enable `screenshot_on_failure` for debugging
- Disable in local development if not needed
- Enable tracing for complex debugging scenarios

### 5. **Parallel Execution**
- Test parallel execution locally before using in CI/CD
- Ensure tests are independent and thread-safe
- Start with fewer streams and increase gradually

### 6. **Test Data**
- Use separate test data files for each environment
- Keep test data in version control
- Document test data requirements

### 7. **Browser Configuration**
- Use headless mode in CI/CD pipelines
- Use headed mode for local debugging
- Test on multiple browsers (chromium, firefox, webkit)

---

## Configuration Examples

### Example 1: Local Development
```properties
# env/default/default.properties
APP_URL = https://www.saucedemo.com/
BROWSER = chromium
HEADLESS = false
SLOW_MO = 100
SCREENSHOT_ON_FAILURE = true
ENABLE_TRACING = false
TEST_DATA_FILE = testdata.xlsx
LOG_LEVEL = DEBUG
```

### Example 2: CI/CD Pipeline
```properties
# env/ci/default.properties
APP_URL = https://qa.saucedemo.com/
BROWSER = chromium
HEADLESS = true
SLOW_MO = 0
SCREENSHOT_ON_FAILURE = true
ENABLE_TRACING = false
TEST_DATA_FILE = testdata_ci.xlsx
LOG_LEVEL = INFO
RETRY_COUNT = 2
```

### Example 3: Performance Testing
```properties
# env/perf/default.properties
APP_URL = https://perf.saucedemo.com/
BROWSER = chromium
HEADLESS = true
SLOW_MO = 0
SCREENSHOT_ON_FAILURE = false
ENABLE_TRACING = false
DEFAULT_TIMEOUT = 60000
NAVIGATION_TIMEOUT = 120000
```

---

## Troubleshooting

### Issue: Tests timing out
**Solution**: Increase timeout values
```properties
DEFAULT_TIMEOUT = 60000
NAVIGATION_TIMEOUT = 120000
```

### Issue: Screenshots not captured
**Solution**: Verify screenshot settings
```properties
SCREENSHOT_ON_FAILURE = true
# Also check gauge.properties
screenshot_on_failure = true
```

### Issue: Browser not launching
**Solution**: Check browser installation
```bash
# Install Playwright browsers
python -m playwright install
```

### Issue: Configuration not loading
**Solution**: Verify environment variable names match `ConfigReader` methods

---

## Summary

The Gauge framework configuration is managed through:
1. **manifest.json** - Project and plugin settings
2. **env/*/default.properties** - Custom application properties
3. **env/*/gauge.properties** - Gauge-specific settings
4. **core/config_reader.py** - Configuration access layer

Use environment-specific configurations to manage different test environments effectively! 🚀
