# Using td_FrameworkData.xlsx for All Configuration and Test Data

## Summary

Successfully consolidated all configuration and test data into a single Excel file: **`data/td_FrameworkData.xlsx`**

## What Was Done

### 1. Migrated Test Data
- Copied test data sheets from `td_Paydaytestdata_UAT.xlsx` to `td_FrameworkData.xlsx`
- Sheets migrated: `LoginData`, `Login`
- All formatting and data preserved

### 2. Updated Configuration
- Updated `TEST_DATA_FILE` in Excel Environment sheet to `td_FrameworkData.xlsx`
- Updated `env/default/default.properties` to use `td_FrameworkData.xlsx`

### 3. Fixed Code
- Removed module-level caching of test data file configuration
- Updated step implementations to dynamically load configuration

## File Structure

**`data/td_FrameworkData.xlsx`** now contains:

| Sheet | Purpose | Rows x Columns |
|-------|---------|----------------|
| Environment | Framework configuration (APP_URL, browser settings, etc.) | 20 x 3 |
| LoginData | Login test data | 4 x 4 |
| Login | Additional login test data | 2 x 4 |

## Configuration Sources

The framework now uses a **single Excel file** for:

1. **Environment Configuration** (Environment sheet)
   - APP_URL, BROWSER, HEADLESS, timeouts, etc.
   
2. **Test Data** (LoginData, Login sheets)
   - Username, Password, TestID, ModuleName

## Test Results

✅ **All tests passing!**

```
Specifications: 1 executed, 1 passed
Scenarios: 4 executed, 4 passed
Total time: 8.375s
```

All scenarios working:
1. ✅ Successful Login with Credentials
2. ✅ Login with Excel Data - Row Based
3. ✅ Swag Labs Login with Excel Data
4. ✅ Swag Labs Login with another Excel Data

## Benefits

✅ **Single Source of Truth** - All configuration and test data in one file  
✅ **Easy Management** - Edit one file instead of multiple  
✅ **Version Control** - Track all changes in one place  
✅ **Team Collaboration** - Share one file across team  
✅ **No Hardcoding** - All values configurable in Excel  

## Files Modified

1. **`data/td_FrameworkData.xlsx`**
   - Added LoginData and Login sheets
   - Updated TEST_DATA_FILE configuration

2. **`env/default/default.properties`**
   - Changed TEST_DATA_FILE from `testdata.xlsx` to `td_FrameworkData.xlsx`

3. **`step_impl/st_login.py`**
   - Removed module-level caching
   - Added dynamic configuration loading

## Scripts Created

1. **`migrate_test_data.py`** - Migrates test data sheets to td_FrameworkData.xlsx
2. **`update_config.py`** - Updates TEST_DATA_FILE configuration
3. **`check_config.py`** - Checks configuration values
4. **`debug_config.py`** - Debug configuration loading

## How to Use

### View All Configuration
```bash
python view_env_config.py
```

### Edit Configuration or Test Data
1. Open `data/td_FrameworkData.xlsx`
2. Navigate to desired sheet:
   - `Environment` - for framework configuration
   - `LoginData` or `Login` - for test data
3. Edit values
4. Save file

### Run Tests
```bash
gauge run specs
```

## Configuration Priority

1. **Environment Variables** (Highest - from env/default/default.properties or system)
2. **Excel Configuration** (Default - from td_FrameworkData.xlsx)
3. **Hardcoded Defaults** (Fallback - in code)

## Important Notes

- The `env/default/default.properties` file is loaded by Gauge and sets environment variables
- These environment variables override Excel configuration
- To use Excel configuration exclusively, comment out properties in default.properties
- Or, update default.properties to match Excel configuration

## Next Steps

### Optional: Remove Redundant Configuration

You can now comment out properties in `env/default/default.properties` to rely solely on Excel configuration:

```properties
# TEST_DATA_FILE = td_FrameworkData.xlsx  # Now managed in Excel
# TEST_DATA_SHEET = LoginData             # Now managed in Excel
```

This makes Excel the single source of truth.

### Add More Test Data

Simply add new sheets or rows to `td_FrameworkData.xlsx`:

1. Open `data/td_FrameworkData.xlsx`
2. Add new sheet or edit existing sheets
3. Update `TEST_DATA_SHEET` in Environment sheet if using a new sheet
4. Save and run tests

## Backup

A backup of the original file was created:
- `data/td_FrameworkData.backup.xlsx`

## Documentation

- **Full Guide**: `docs/EXCEL_ENVIRONMENT_CONFIG.md`
- **Quick Reference**: `docs/QUICK_REFERENCE_CONFIG.md`
- **Implementation Summary**: `docs/IMPLEMENTATION_SUMMARY_CONFIG.md`

---

**Status**: ✅ Complete and Tested  
**Date**: 2025-12-31  
**All Tests**: Passing
