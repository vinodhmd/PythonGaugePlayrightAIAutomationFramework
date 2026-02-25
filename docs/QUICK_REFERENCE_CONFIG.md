# Quick Reference: Excel Environment Configuration

## Setup (One-Time)

```bash
python setup_env_config.py
```

## View Configuration

```bash
python view_env_config.py
```

## Edit Configuration

1. Open `data/td_FrameworkData.xlsx`
2. Go to `Environment` sheet
3. Edit values in **Value** column
4. Save file

## Common Configuration Changes

### Change Application URL
```
Property: APP_URL
Value: https://your-app-url.com/
```

### Switch Browser
```
Property: BROWSER
Value: chromium | firefox | webkit
```

### Enable/Disable Headless Mode
```
Property: HEADLESS
Value: true | false
```

### Change Environment
```
Property: ENVIRONMENT
Value: DEV | QA | UAT | PROD
```

### Adjust Timeouts
```
Property: DEFAULT_TIMEOUT
Value: 30000 (milliseconds)

Property: NAVIGATION_TIMEOUT
Value: 60000 (milliseconds)
```

## Configuration Priority

1. **Environment Variables** (Highest - overrides Excel)
2. **Excel Configuration** (Default - primary source)

## Files

| File | Purpose |
|------|---------|
| `data/td_FrameworkData.xlsx` | Configuration storage |
| `core/env_config_reader.py` | Excel reader |
| `core/config_reader.py` | Dual-source config manager |
| `setup_env_config.py` | Setup script |
| `view_env_config.py` | View script |

## Example: Override via Environment Variable

```powershell
# Windows PowerShell
$env:APP_URL = "https://staging.example.com/"
gauge run specs

# Linux/Mac
export APP_URL="https://staging.example.com/"
gauge run specs
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Changes not reflected | Save Excel file and verify with `view_env_config.py` |
| File not found | Run `setup_env_config.py` |
| Invalid value | Check Description column for valid formats |

## Full Documentation

See [`docs/EXCEL_ENVIRONMENT_CONFIG.md`](EXCEL_ENVIRONMENT_CONFIG.md) for complete details.
