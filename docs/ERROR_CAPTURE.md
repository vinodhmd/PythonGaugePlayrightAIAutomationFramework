# Error Capture and Logging System

## ✅ Enhanced Error Capture Implemented

The framework now captures comprehensive error information when tests fail, including:
- Error messages
- Stack traces
- Test context (step, scenario, spec, tags)
- Screenshots
- Timestamps

## Error Capture Features

### 1. Console Output
When a step fails, detailed error information is displayed in the console:

```
======================================================================
❌ STEP FAILED: Login with test data from row "2"
   Scenario: Login with Excel Data - Row Based
   Spec: Swag Labs Login Web Application
   Tags: TC002, smoketesting
   Time: 2026-01-02 11:28:52
   Error: Element not found: #invalid-selector
======================================================================
   📝 Error logged to: C:\Vinodh\GaugeFramework\logs\execution_errors.log
   📸 Screenshot captured: reports/screenshots/failed_step_Login_with_Excel_Data_*.png
```

### 2. Error Log File
All errors are logged to `logs/execution_errors.log`:

```
======================================================================
EXECUTION ERROR - 2026-01-02 11:28:52
======================================================================
Step: Login with test data from row "2"
Scenario: Login with Excel Data - Row Based
Spec: Swag Labs Login Web Application
Tags: TC002, smoketesting
Error: Element not found: #invalid-selector
----------------------------------------------------------------------
Stack Trace:
Traceback (most recent call last):
  File "step_impl/st_login.py", line 102, in login_with_excel_data
    login_page.login(test_data['Username'], test_data['Password'])
  ...
======================================================================
```

### 3. Screenshot Capture
- Automatically captures screenshot when step fails
- Saved to: `reports/screenshots/failed_step_<scenario>_<step>.png`
- Attached to Gauge HTML report

### 4. Gauge HTML Report
- Error details visible in HTML report
- Screenshots embedded
- Stack trace available
- Located at: `reports/html-report/index.html`

## Error Information Captured

| Information | Description | Location |
|-------------|-------------|----------|
| Step Text | The step that failed | Console + Log |
| Scenario Name | Which scenario failed | Console + Log |
| Spec Name | Which spec file | Console + Log |
| Tags | Test case tags | Console + Log |
| Error Message | Actual error message | Console + Log |
| Stack Trace | Full Python stack trace | Log file only |
| Timestamp | When error occurred | Console + Log |
| Screenshot | Visual state at failure | File + HTML report |

## Error Log Location

```
GaugeFramework/
├── logs/
│   └── execution_errors.log  ← All errors logged here
├── reports/
│   ├── screenshots/          ← Failure screenshots
│   └── html-report/          ← Gauge HTML report
```

## Viewing Errors

### 1. During Execution
Errors are displayed in console in real-time

### 2. After Execution
```bash
# View error log
type logs\execution_errors.log

# View latest error
Get-Content logs\execution_errors.log -Tail 50

# Open HTML report
start reports\html-report\index.html
```

### 3. In CI/CD
- Error log file can be archived as artifact
- Screenshots available for debugging
- HTML report can be published

## Error Log Format

Each error entry contains:
1. **Header**: Timestamp and separator
2. **Context**: Step, Scenario, Spec, Tags
3. **Error**: Error message
4. **Stack Trace**: Full Python traceback
5. **Footer**: Separator

## Hooks Configuration

Error capture is configured in `step_impl/hooks.py`:

```python
@after_step
def capture_on_step_failure(context: ExecutionContext):
    """Capture screenshot and error details when step fails"""
    if context.step.is_failing:
        # 1. Extract error information
        # 2. Log to console
        # 3. Write to error log file
        # 4. Capture screenshot
```

## Benefits

✅ **Comprehensive Logging**: All error details captured  
✅ **Easy Debugging**: Stack traces and screenshots available  
✅ **Historical Record**: Error log persists across runs  
✅ **CI/CD Friendly**: Log files can be archived  
✅ **Visual Context**: Screenshots show exact failure state  
✅ **Structured Format**: Easy to parse and analyze  

## Error Log Retention

- Error log is **appended** (not overwritten)
- Each run adds new entries
- Manual cleanup recommended periodically
- Or implement log rotation if needed

## Example Error Entry

```
======================================================================
EXECUTION ERROR - 2026-01-02 11:28:52
======================================================================
Step: verify the title of the page
Scenario: Swag Labs Login with Excel Data
Spec: Swag Labs Login Web Application
Tags: TC003, uattesting
Error: Expected title 'Swag Labs' but got 'Swag Lab'
----------------------------------------------------------------------
Stack Trace:
Traceback (most recent call last):
  File "step_impl/st_login.py", line 157, in verify_the_title_of_the_page
    assert actual_title == expected_title
AssertionError: Expected title 'Swag Labs' but got 'Swag Lab'
======================================================================
```

## Troubleshooting

### Error log not created
- Check `logs/` directory exists
- Verify write permissions
- Check console for error messages

### Screenshots not captured
- Verify `SCREENSHOT_ON_FAILURE=true` in config
- Check browser is still running
- Verify `reports/screenshots/` directory

### Missing stack trace
- Stack trace only in log file, not console
- Check `logs/execution_errors.log`

---

**Status**: ✅ ERROR CAPTURE ACTIVE  
**Log File**: `logs/execution_errors.log`  
**Screenshots**: `reports/screenshots/`  
**HTML Report**: `reports/html-report/index.html`
