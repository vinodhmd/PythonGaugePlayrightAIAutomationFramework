
# Dynamic Configuration Discovery

## Overview

The framework has been updated to remove the hardcoded dependency on `td_FrameworkData.xlsx`. The configuration file is now discovered dynamically or specified via environment variables.

## Discovery Logic

The `BasePage` class (`core/Core_basePage.py`) determines the configuration file using the following priority:

1.  **Environment Variable**: Checks `ENV_CONFIG_FILE`. If set, tries to find this file in the project root.
2.  **Legacy Default**: Checks if `data/td_FrameworkData.xlsx` exists. If it does, it uses it (preserving backward compatibility).
3.  **Automatic Discovery**: Scans the `data/` directory for any Excel file (`.xlsx`) that contains a sheet named **'Environment'**. The first matching file found is used as the valid configuration.

## How to Name Your Config File

You can now rename your configuration file to anything (e.g., `ProjectA_Config.xlsx`, `UAT_Data.xlsx`) as long as:
1.  It is placed in the `data/` directory.
2.  It contains an **'Environment'** sheet.

## TEST_DATA_FILE Configuration

Once the configuration file is loaded (the "Bootstrap file"), the framework looks for the `TEST_DATA_FILE` key in the 'Environment' sheet.
This key specifies the name of the file containing the actual test data (which can be the same file or a different one).

### Example Environment Sheet

| Key | Value |
| :--- | :--- |
| **TEST_DATA_FILE** | **td_EmployyeCreationData.xlsx** |
| APP_URL | https://example.com |
| BROWSER | chromium |

If `TEST_DATA_FILE` is set to the filename of the config file itself, then the config file serves as both Environment and Test Data source.
