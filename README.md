# Gauge Automation Framework

A Python-based test automation framework using **Gauge** and **Playwright** for BDD-style specification testing.

---

## 📁 Project Structure

```
GaugeFramework/
├── core/                    # Core utilities and helpers
│   ├── config_reader.py     # Dual-source configuration reader
│   ├── env_config_reader.py # Excel-based environment config reader
│   ├── excel_reader.py      # Excel data reader for data-driven tests
│   ├── playwright_driver.py # Playwright browser driver management
│   └── assertions.py        # Custom assertion helpers
│
├── pages/                   # Page Object Model (POM) classes
│   ├── base_page.py         # Base page with common methods
│   └── login_page.py        # Login page object (example)
│
├── specs/                   # Gauge specification files (.spec)
│   └── login.spec           # Login test specifications (example)
│
├── step_impl/               # Step implementations for specs
│   ├── hooks.py             # Before/After hooks for test lifecycle
│   └── login_steps.py       # Login step implementations (example)
│
├── data/                    # Test data files
│   ├── td_FrameworkData.xlsx # Environment configuration and test data (primary)
│   └── execution_control.xlsx # Execution control configuration
│
├── env/                     # Environment configurations (legacy)
│   └── default/             # Default environment settings
│
├── docs/                    # Documentation
│   ├── EXECUTION_STEPS.md   # Detailed execution flow documentation
│   └── EXCEL_ENVIRONMENT_CONFIG.md # Excel config documentation
│
├── logs/                    # Test execution logs
├── reports/                 # Test reports and archives
├── setup_env_config.py      # Setup script for Excel configuration
├── view_env_config.py       # View current configuration
├── manifest.json            # Gauge project manifest
└── requirements.txt         # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

1. **Python 3.8+** installed
2. **Gauge** installed - [Download Gauge](https://docs.gauge.org/getting_started/installing-gauge.html)
3. **Gauge Python plugin** installed

### Installation Steps

```bash
# 1. Clone/Copy the framework to your local machine

# 2. Navigate to the project directory
cd GaugeFramework

# 3. Create a virtual environment
python -m venv .venv

# 4. Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 5. Install Python dependencies
pip install -r requirements.txt

# 6. Install Playwright browsers
playwright install

# 7. Install Gauge Python plugin (if not already installed)
gauge install python
```

---

## ▶️ Running Tests

### Run all specifications
```bash
gauge run specs/
```

### Run a specific specification
```bash
gauge run specs/login.spec
```

### Run with HTML reports
```bash
gauge run --env default specs/
```

---

## 📝 How to Add New Tests

### Step 1: Create a Specification File
Create a new `.spec` file in the `specs/` folder:

```markdown
# Feature Name
Tags: tagname

## Scenario Name
* Step description one
* Step description two
* Step description three
```

### Step 2: Create Page Object (if needed)
Add a new page class in `pages/`:

```python
from pages.base_page import BasePage

class NewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.element = page.locator("#element-id")
    
    def perform_action(self):
        self.element.click()
```

### Step 3: Implement Step Definitions
Add step implementations in `step_impl/`:

```python
from getgauge.python import step

@step("Step description one")
def step_implementation():
    # Your implementation here
    pass
```

---

## 📊 Data-Driven Testing

The framework supports Excel-based data-driven testing:

1. Add test data to `data/td_FrameworkData.xlsx` (LoginData or Login sheets)
2. Use `core/excel_reader.py` to read data in your steps
3. Control test execution via `data/execution_control.xlsx`

---

## ⚙️ Configuration

### Excel-Based Environment Configuration (Recommended)

The framework now supports **centralized configuration management** using Excel:

**Quick Setup:**
```bash
# 1. Create environment configuration sheet
python setup_env_config.py

# 2. View current configuration
python view_env_config.py

# 3. Edit configuration
# Open data/td_FrameworkData.xlsx -> Environment sheet
# Edit values in the 'Value' column
```

**Configuration File:** `data/td_FrameworkData.xlsx` (Sheet: `Environment`)

**Available Settings:**
- Application URL and environment (DEV, QA, UAT, PROD)
- Browser settings (type, headless mode, viewport)
- Timeouts (navigation, actions, default)
- Screenshots and tracing options
- Test data file locations
- Logging and retry configuration

**For detailed documentation, see:** [`docs/EXCEL_ENVIRONMENT_CONFIG.md`](docs/EXCEL_ENVIRONMENT_CONFIG.md)

### Legacy Configuration (Still Supported)

Environment-specific configurations can also be set via environment variables or stored in `env/default/`:
- `default.properties` - Environment variables and settings

---

## 📚 Documentation

For detailed execution flow and step-by-step guide, refer to:
- `docs/EXECUTION_STEPS.md`

---

## 👥 Team Guidelines

1. **Follow Page Object Model (POM)** - Keep page interactions in `pages/`
2. **Reusable Steps** - Create generic, reusable step implementations
3. **Meaningful Names** - Use descriptive names for specs and scenarios
4. **Data Separation** - Keep test data in `data/` folder, not hardcoded
5. **Clean Commits** - Don't commit `.gauge/`, `logs/`, `__pycache__/`, `.venv/`

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `gauge: command not found` | Install Gauge and add to PATH |
| `Module not found` | Activate virtual environment and run `pip install -r requirements.txt` |
| `Browser not found` | Run `playwright install` |

---

## 📄 License

Internal Use Only - [Your Organization]
