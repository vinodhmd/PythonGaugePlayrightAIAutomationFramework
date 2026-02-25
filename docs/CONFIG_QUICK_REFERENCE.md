# Gauge Configuration Quick Reference

## 🚀 Quick Start

### Run Tests
```bash
# All tests
gauge run specs

# Specific spec
gauge run specs/login.spec

# With tags
gauge run --tags "smoketesting" specs

# Exclude tags
gauge run --tags "!uattesting" specs

# Parallel execution (4 streams)
gauge run -p -n 4 specs
```

### Build Script
```bash
# Full build
python build.py

# Skip install
python build.py --skip-install

# Skip clean
python build.py --skip-clean
```

---

## ⚙️ Configuration Files

| File | Purpose |
|------|---------|
| `manifest.json` | Project settings & plugins |
| `env/default/default.properties` | Custom app properties |
| `env/default/gauge.properties` | Gauge settings |
| `core/config_reader.py` | Configuration reader |

---

## 🌐 Common Properties

### Application
```properties
APP_URL = https://www.saucedemo.com/
```

### Browser
```properties
BROWSER = chromium          # chromium, firefox, webkit
HEADLESS = false            # true/false
SLOW_MO = 0                 # milliseconds
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
```

### Timeouts (milliseconds)
```properties
DEFAULT_TIMEOUT = 30000
NAVIGATION_TIMEOUT = 60000
ACTION_TIMEOUT = 10000
```

### Screenshots & Tracing
```properties
SCREENSHOT_ON_FAILURE = true
ENABLE_TRACING = false
TRACE_DIR = reports/traces
```

### Test Data
```properties
TEST_DATA_FILE = testdata.xlsx
TEST_DATA_SHEET = LoginData
```

### Other
```properties
RETRY_COUNT = 0
LOG_LEVEL = INFO           # DEBUG, INFO, WARNING, ERROR
```

---

## 📊 Gauge Properties

```properties
gauge_reports_dir = reports
gauge_clear_state_level = scenario
screenshot_on_failure = true
enable_multithreading = false
# gauge_parallel_streams = 4
```

---

## 🏷️ Tags Usage

### In Spec File
```gherkin
## Login Test
Tags: smoketesting, regression, TC001
* Navigate to application
* Login with credentials
```

### Run by Tags
```bash
# Single tag
gauge run --tags "smoketesting" specs

# Multiple tags (OR)
gauge run --tags "smoketesting | regression" specs

# Multiple tags (AND)
gauge run --tags "smoketesting & regression" specs

# Exclude tags
gauge run --tags "!uattesting" specs

# Complex
gauge run --tags "(smoketesting | regression) & !slow" specs
```

---

## 🌍 Environments

### Create Environment
```bash
mkdir env/qa
# Create env/qa/default.properties
# Create env/qa/gauge.properties
```

### Run with Environment
```bash
gauge run --env qa specs
```

### Example: QA Environment
```properties
# env/qa/default.properties
APP_URL = https://qa.example.com
HEADLESS = true
TEST_DATA_FILE = testdata_qa.xlsx
```

---

## 🔧 ConfigReader Usage

```python
from core.config_reader import ConfigReader

# Application
url = ConfigReader.get_app_url()

# Browser
browser = ConfigReader.get_browser_type()
headless = ConfigReader.is_headless()

# Timeouts
timeout = ConfigReader.get_default_timeout()

# Test Data
file = ConfigReader.get_test_data_file()
sheet = ConfigReader.get_test_data_sheet()

# Screenshots
enabled = ConfigReader.screenshot_on_failure()
```

---

## 🔍 Debugging

### Enable Verbose Output
```bash
gauge run -v specs        # Verbose
gauge run -vv specs       # Very verbose
```

### Enable Tracing
```properties
ENABLE_TRACING = true
```

View trace:
```bash
npx playwright show-trace reports/traces/scenario_name.zip
```

### Enable Debug Logging
```properties
LOG_LEVEL = DEBUG
HEADLESS = false
SLOW_MO = 100
```

---

## 🎯 Common Scenarios

### Local Development
```properties
HEADLESS = false
SLOW_MO = 100
LOG_LEVEL = DEBUG
SCREENSHOT_ON_FAILURE = true
```

### CI/CD Pipeline
```properties
HEADLESS = true
SLOW_MO = 0
LOG_LEVEL = INFO
SCREENSHOT_ON_FAILURE = true
RETRY_COUNT = 2
```

### Performance Testing
```properties
HEADLESS = true
SCREENSHOT_ON_FAILURE = false
DEFAULT_TIMEOUT = 60000
NAVIGATION_TIMEOUT = 120000
```

---

## 📦 Plugins

### Install Plugin
```bash
gauge install html-report
gauge install xml-report
gauge install json-report
gauge install spectacle
```

### Update Plugin
```bash
gauge update html-report
```

### List Plugins
```bash
gauge list
```

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests timeout | Increase `DEFAULT_TIMEOUT` |
| No screenshots | Set `SCREENSHOT_ON_FAILURE = true` |
| Browser not launching | Run `python -m playwright install` |
| Config not loading | Check property names in `ConfigReader` |

---

## 📚 Full Documentation

See `docs/GAUGE_CONFIGURATION.md` for complete details.
