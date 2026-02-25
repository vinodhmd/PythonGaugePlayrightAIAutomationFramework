"""
Screenshot Utilities - Common screenshot capture functions
Provides reusable screenshot functionality for all step implementations
"""
from getgauge.python import Messages
from core.Core_basePage import BasePage
import os
from datetime import datetime

def capture_step_screenshot(step_name):
    """
    Capture screenshot and attach to Gauge report.    
    Args:
        step_name: Name/description of the step for the screenshot filename    
    Returns:
        str: Path to the saved screenshot file, or None if capture failed
    """
    try:
        page = BasePage.get_page()
        if page:
            # Create screenshots folder under reports
            base_report_dir = os.environ.get("GAUGE_REPORTS_DIR", "reports")
            screenshot_dir = os.path.join(base_report_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            safe_name = step_name.replace(" ", "_").replace("/", "_")[:50]
            screenshot_path = os.path.join(screenshot_dir, f"{safe_name}_{timestamp}.png")            # Take screenshot and save to file
            screenshot_bytes = page.screenshot(path=screenshot_path)
            # Attach screenshot to report using HTML
            Messages.write_message(f"   📷 Screenshot: {step_name}")
            Messages.write_message(f"<img src='../screenshots/{os.path.basename(screenshot_path)}' width='600' />")
            return screenshot_path
    except Exception as e:
        Messages.write_message(f"   [Screenshot capture failed: {str(e)}]")
    return None
