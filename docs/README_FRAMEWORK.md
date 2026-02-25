# Robot-Based Test Automation Framework

## ✅ Architecture Overview

This framework uses a **robot-based approach** where:
1. **Spec files** map to **Step implementation files** by naming convention
2. **Test IDs (Tags)** automatically find their data across **all Excel sheets**
3. **Zero manual configuration** - framework discovers everything automatically

## Framework Structure

```
Spec File          Step Implementation       Robot Test Data Driver
─────────────────  ───────────────────────  ──────────────────────────────
sp_login.spec  →   st_login.py          →   TC001 → Auto-discovers sheet
                                             TC003 → Auto-discovers sheet
                                             TC006 → Auto-discovers sheet
```

## Robot Approach - How It Works

### Traditional Approach (NOT USED)
```python
# Manual configuration - needs updating for every new test
TEST_DATA_MAPPING = {
    'TC001': 'LoginData',
    'TC003': 'Login',
    # ... manual entries
}
```

### Robot Approach (CURRENT)
```python
# Automatic discovery - zero configuration!
def get_sheet_for_test_id(test_id):
    """Searches ALL sheets to find the Test ID"""
    for sheet in all_sheets:
        if test_id exists in sheet:
            return sheet
```

### Benefits

✅ **Zero Configuration**: No manual mapping needed  
✅ **Auto-Discovery**: Framework finds test data automatically  
✅ **Future-Proof**: Add new tests/sheets without code changes  
✅ **Scalable**: Works with unlimited test cases and sheets  
✅ **Intelligent**: Skips system sheets (Environment, Config)  

## File Naming Convention

| Component         | Naming Pattern      | Example           |
|-------------------|---------------------|-------------------|
| Spec File         | `sp_<module>.spec`  | `sp_login.spec`   |
| Step Impl         | `st_<module>.py`    | `st_login.py`     |
| Page Object       | `pg_<module>.py`    | `pg_login.py`     |
| Core Utilities    | `<utility>.py`      | `excel_reader.py` |

## Test Data Driver (core/test_data_driver.py)

**Robot approach** - automatically searches all sheets:

```python
def get_sheet_for_test_id(test_id):
    """
    Dynamically find which sheet contains the given Test ID.
    Searches all sheets in the Excel file.
    
    ROBOT APPROACH - no manual configuration needed!
    """
    excel = ExcelReader(test_data_file)
    all_sheets = excel.get_all_sheet_names()
    
    # Search through all sheets
    for sheet_name in all_sheets:
        # Skip system sheets
        if sheet_name.lower() in ['environment', 'config']:
            continue
        
        # Check if this sheet has the Test ID
        test_data = excel.get_test_data_by_id(sheet_name, test_id)
        if test_data:
            return sheet_name
    
    return default_sheet
```

### How It Works

1. **Scenario has tag**: `TC003`
2. **Robot searches**: All sheets in Excel file
3. **Finds TC003**: In "LoginData" sheet
4. **Returns**: "LoginData"
5. **Test executes**: With fetched data

## Excel Structure

### File: data/td_FrameworkData.xlsx

The framework automatically searches ALL sheets (except Environment, Config, Settings)

#### Sheet: LoginData
| TestID | ModuleName | Username        | Password     |
|--------|------------|-----------------|--------------|
| TC001  | Login      | standard_user   | secret_sauce |
| TC002  | Login      | locked_out_user | secret_sauce |
| TC003  | Login      | standard_user   | secret_sauce |

#### Sheet: Login
| TestID | ModuleName | Username      | Password     |
|--------|------------|---------------|--------------|
| TC006  | Login      | standard_user | secret_sauce |

#### Future Sheets (Auto-discovered!)
Just add new sheets with TestID column - framework finds them automatically!

## Implementation Flow

```
1. Spec File: sp_login.spec
   Scenario: Tags: TC003

2. Step Implementation: st_login.py
   - Extracts Test ID from tags: TC003
   - Calls robot: get_sheet_for_test_id('TC003')

3. Robot Test Data Driver
   - Searches: LoginData sheet → Found TC003!
   - Returns: 'LoginData' sheet

4. Excel Reader
   - Reads from 'LoginData' sheet
   - Finds row where TestID = TC003
   - Returns test data

5. Test Execution
   - Uses fetched data for login
```

## Key Files

### 1. core/test_data_driver.py
**Purpose**: Robot approach - automatic sheet discovery

```python
def get_sheet_for_test_id(test_id):
    """Automatically finds which sheet has the Test ID"""
    # Searches all sheets dynamically
    # No manual configuration needed!
```

### 2. step_impl/st_login.py
**Purpose**: Step implementations for login spec

```python
@step("Login with Swag Labs")
def login_with_swag_labs():
    # Get Test ID from tags
    test_id = get_test_id_from_tags()  # TC003
    
    # Robot finds the sheet automatically
    sheet = get_sheet_for_test_id(test_id)  # LoginData (auto-discovered)
    
    # Fetch data
    test_data = excel.get_test_data_by_id(sheet, test_id)
    
    # Execute test
    login_page.login(test_data['Username'], test_data['Password'])
```

## Test Results

✅ **TC001**: PASSED - Auto-discovered in LoginData sheet  
✅ **TC003**: PASSED - Auto-discovered in LoginData sheet  
✅ **TC006**: PASSED - Auto-discovered in Login sheet  

## Usage

### Running Tests

```bash
# Run specific test by tag
gauge run --tags "TC003" specs/sp_login.spec

# Run multiple tests
gauge run --tags "TC001 | TC003 | TC006" specs/

# Run all login tests
gauge run specs/sp_login.spec
```

### Adding New Test Cases (Zero Configuration!)

**Step 1**: Add data to ANY Excel sheet
```
Sheet: NewModuleData
| TestID | ModuleName | Data1 | Data2 |
|--------|------------|-------|-------|
| TC007  | NewModule  | value | value |
```

**Step 2**: Add scenario to spec
```markdown
## New Test
Tags: TC007
* Navigate to the application
* Login with Swag Labs
```

**Step 3**: Run test
```bash
gauge run --tags "TC007" specs/sp_login.spec
```

**That's it!** The robot automatically:
- Searches all sheets
- Finds TC007 in NewModuleData
- Fetches the data
- Runs the test

### Adding New Modules

**Step 1**: Create spec file: `specs/sp_employee.spec`
```markdown
# Employee Specification

## Create Employee
Tags: TC101
* Navigate to employee page
* Create employee
```

**Step 2**: Create step implementation: `step_impl/st_employee.py`
```python
from core.test_data_driver import get_sheet_for_test_id

@step("Create employee")
def create_employee():
    test_id = get_test_id_from_tags()
    sheet = get_sheet_for_test_id(test_id)  # Auto-discovers!
    # ... implementation
```

**Step 3**: Add Excel sheet: `EmployeeData` (or any name!)
| TestID | Name     | Department |
|--------|----------|------------|
| TC101  | John Doe | IT         |

**No configuration needed!** Robot finds it automatically.

## Robot Approach Benefits

✅ **Zero Configuration**: No manual TEST_DATA_MAPPING  
✅ **Auto-Discovery**: Searches all sheets automatically  
✅ **Future-Proof**: Add tests/sheets without code changes  
✅ **Scalable**: Unlimited test cases and sheets  
✅ **Intelligent**: Skips system sheets automatically  
✅ **Maintainable**: No mapping file to update  
✅ **Flexible**: Test data can be in any sheet  

## Demo Script

Run the demo to see robot approach in action:

```bash
python demo_robot_approach.py
```

Output shows:
- Dynamic sheet discovery for each Test ID
- All Test IDs discovered across all sheets
- Benefits of robot approach

## Error Handling

### Test ID Not Found in Any Sheet
Framework falls back to default sheet from config

### Multiple Sheets Have Same Test ID
Returns the first sheet found (searches in sheet order)

### Sheet Has No TestID Column
Skips that sheet and continues searching

## Files Modified (NoneType Fixes)

✅ **core/config_reader.py** - Fixed `.lower()` calls  
✅ **core/env_config_reader.py** - Fixed `.lower()` calls  
✅ **core/report_logger.py** - Fixed `.lower()` calls  

## Summary

This framework uses a **robot-based approach** where:
- **Naming convention** maps specs to step implementations
- **Robot Test Data Driver** automatically finds test data
- **Tags drive data** - Test ID triggers auto-discovery
- **Zero configuration** - no manual mapping needed
- **Future-proof** - add tests/sheets without code changes

---

**Status**: ✅ COMPLETE AND TESTED  
**Approach**: Robot-based with automatic discovery  
**Tests Passing**: TC001, TC003, TC006  
**Configuration Needed**: ZERO!
