# Screenshot Capture for Failed Test Scenarios

## Overview
The framework now captures screenshots automatically when test scenarios or steps fail, and these screenshots are properly embedded in the Gauge HTML report.

## What Was Fixed

### Previous Issue
- Screenshots were being saved to files but not appearing in the Gauge HTML report
- The `@screenshot` decorator was not properly returning screenshot bytes

### Solution Implemented
1. **Enhanced `@screenshot` decorator** in `hooks.py`:
   - Now properly returns screenshot bytes for Gauge to embed in HTML reports
   - Uses `full_page=True` to capture the entire page
   - Added error handling to prevent crashes

2. **Added `@after_step` hook**:
   - Captures screenshots immediately when a step fails
   - Saves screenshots with descriptive names including scenario and step info
   - Adds failure messages to the Gauge report

3. **Enhanced `@after_scenario` hook**:
   - Captures screenshots when scenarios fail
   - Saves both to file and returns bytes for the report
   - Provides clear failure messages

## How It Works

### Automatic Screenshot Capture
Screenshots are automatically captured in these situations:

1. **Step Failure**: When any step fails
   - Screenshot saved as: `failed_step_{scenario_name}_{step_name}.png`
   - Location: `reports/screenshots/`

2. **Scenario Failure**: When a scenario fails
   - Screenshot saved as: `failed_{scenario_name}.png`
   - Location: `reports/screenshots/`

### Screenshot in Reports
- Screenshots appear inline in the Gauge HTML report
- Full-page screenshots capture the entire browser viewport
- Screenshots are embedded as base64 images in the HTML

## Configuration

Ensure your configuration has screenshot enabled:

```properties
# In env/default/default.properties or gauge.properties
screenshot_on_failure = true
```

## Testing the Feature

### Create a Failing Test
To test screenshot capture, create a scenario that will fail:

```gherkin
## Test Screenshot on Failure
Tags: test, screenshot
* Navigate to the application
* Login with credentials "invalid_user" and "wrong_password"
* verify the title of the page
```

### Run the Test
```bash
python build.py --skip-install
```

### Check the Results
1. **HTML Report**: Open `reports/html-report/index.html`
   - Failed scenarios will show embedded screenshots
   - Screenshots appear at the point of failure

2. **Screenshot Files**: Check `reports/screenshots/`
   - Files are saved with descriptive names
   - Useful for debugging and archiving

## File Locations

### Modified Files
- `step_impl/hooks.py`: Enhanced screenshot capture hooks
  - `@screenshot` decorator: Returns bytes for Gauge report
  - `@after_step`: Captures on step failure
  - `@after_scenario`: Captures on scenario failure

### Screenshot Storage
- **Directory**: `reports/screenshots/`
- **Naming Convention**: 
  - Step failures: `failed_step_{scenario}_{step}.png`
  - Scenario failures: `failed_{scenario}.png`

## Benefits

1. **Visual Debugging**: See exactly what the browser looked like when the test failed
2. **Better Reports**: Screenshots embedded directly in HTML reports
3. **Automatic Archiving**: Screenshots are included in report archives
4. **No Manual Intervention**: Completely automatic on failure

## Example Output

When a test fails, you'll see in the Gauge report:

```
❌ Step Failed - Screenshot captured: reports/screenshots/failed_step_Login_verify_title.png
```

And the screenshot will be displayed inline in the HTML report.

## Troubleshooting

### Screenshots Not Appearing in Report
1. Verify `screenshot_on_failure = true` in properties
2. Check that the browser page is still active when failure occurs
3. Look for error messages in the console output

### Screenshot Files Not Saved
1. Check that `reports/screenshots/` directory exists
2. Verify write permissions on the reports folder
3. Check for disk space issues

## Advanced Usage

### Manual Screenshot Capture
You can also capture screenshots manually in your step implementations:

```python
from core.playwright_driver import PlaywrightDriver

# Capture and save to file
screenshot_path = PlaywrightDriver.take_screenshot("my_custom_screenshot")

# Or capture bytes for Gauge report
from getgauge.python import Screenshots
page = PlaywrightDriver.get_page()
screenshot_bytes = page.screenshot()
Screenshots.capture_screenshot_bytes(screenshot_bytes)
```

## Notes

- Screenshots are captured using Playwright's `page.screenshot()` method
- Full-page screenshots may be large for long pages
- Screenshots are automatically cleaned up when reports are archived
- The `@screenshot` decorator is called by Gauge automatically on failures
