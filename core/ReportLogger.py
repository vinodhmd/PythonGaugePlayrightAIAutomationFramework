from getgauge.python import Messages, data_store
from datetime import datetime

class ReportLogger:
    """
    Report Logger Class
    Handles all logging and reporting functionality for Gauge reports.
    formerly part of BasePage.
    """
    @staticmethod
    def log_step_header(step_name, icon="📍"):
        """Log a step header with formatting"""
        Messages.write_message("═" * 80)
        Messages.write_message(f"{icon} EXECUTION STEP: {step_name}")
    
    @staticmethod
    def log_step_footer(success=True, message=None):
        """Log a step footer with status"""
        if message:
            status_icon = "✅" if success else "❌"
            Messages.write_message(f"   {status_icon} {message}")
        Messages.write_message("═" * 80)
    
    @staticmethod
    def log_info(key, value, mask_password=False):
        """Log a key-value pair"""
        if mask_password and key and ('password' in key.lower() or 'pwd' in key.lower()):
            display_value = '*' * len(str(value)) if value else 'N/A'
        else:
            display_value = value
        Messages.write_message(f"   🔧 {key}: {display_value}")
    
    @staticmethod
    def log_data_source(file_name, sheet_name, row_number=None, test_id=None):
        """Log data source information"""
        Messages.write_message(f"   📄 Excel File: {file_name}")
        Messages.write_message(f"   📑 Sheet Name: {sheet_name}")
        if row_number:
            Messages.write_message(f"   📌 Row Number: {row_number}")
        if test_id:
            Messages.write_message(f"   🆔 Test ID: {test_id}")
    
    @staticmethod
    def log_test_data(test_data, mask_passwords=True):
        """Log test data dictionary"""
        Messages.write_message("   📊 Test Data Retrieved:")
        for key, value in test_data.items():
            if mask_passwords and key and 'password' in key.lower():
                Messages.write_message(f"      • {key}: {'*' * len(str(value)) if value else 'N/A'}")
            else:
                Messages.write_message(f"      • {key}: {value}")
    
    @staticmethod
    def log_actions(actions_list):
        """Log a list of actions performed"""
        Messages.write_message("   🎯 Actions performed:")
        for i, action in enumerate(actions_list, 1):
            Messages.write_message(f"      {i}. {action}")
    
    @staticmethod
    def log_verification(expected, actual, passed=None):
        """Log verification results"""
        Messages.write_message(f"   🎯 Expected: {expected}")
        Messages.write_message(f"   📋 Actual: {actual}")
        
        if passed is not None:
            if passed:
                Messages.write_message("   ✅ VERIFICATION PASSED")
            else:
                Messages.write_message(f"   ❌ VERIFICATION FAILED: Expected '{expected}' but got '{actual}'")
    
    @staticmethod
    def log_error(error_message):
        """Log an error message"""
        Messages.write_message(f"   ❌ ERROR: {error_message}")
    
    @staticmethod
    def log_warning(warning_message):
        """Log a warning message"""
        Messages.write_message(f"   ⚠️ WARNING: {warning_message}")
    
    @staticmethod
    def log_success(success_message):
        """Log a success message"""
        Messages.write_message(f"   ✅ {success_message}")
    
    @staticmethod
    def log_separator():
        """Log a separator line"""
        Messages.write_message("─" * 80)
    
    @staticmethod
    def log_section(title):
        """Log a section title"""
        Messages.write_message(f"\n   📌 {title}")
    
    @staticmethod
    def log_url(url, label="Target URL"):
        """Log a URL"""
        Messages.write_message(f"   🌐 {label}: {url}")
    
    @staticmethod
    def log_browser_info(browser_type, headless):
        """Log browser configuration"""
        Messages.write_message(f"   🔧 Browser: {browser_type}")
        Messages.write_message(f"   👁️ Headless Mode: {headless}")
    
    @staticmethod
    def log_credentials(username, password=None):
        """Log credentials (password is masked)"""
        Messages.write_message(f"   👤 Username: {username}")
        if password:
            Messages.write_message(f"   🔑 Password: {'*' * len(password)}")
    
    @staticmethod
    def log_custom(message, icon="ℹ️"):
        """Log a custom message with an icon"""
        Messages.write_message(f"   {icon} {message}")
    
    @staticmethod
    def log_timestamp(label="Timestamp"):
        """Log current timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Messages.write_message(f"   🕐 {label}: {timestamp}")

    @staticmethod
    def log_test_context(url, browser, headless, file_name, sheet_name, test_id=None, mapping=None):
        """Log consolidated test context"""
        Messages.write_message("═" * 80)
        Messages.write_message("   📝 TEST CONTEXT")
        Messages.write_message(f"   🌐 Target URL: {url}")
        Messages.write_message(f"   🔧 Browser: {browser}")
        Messages.write_message(f"   👁️ Headless Mode: {headless}")
        if mapping:
             Messages.write_message(f"   🗺️ Driver Mapping: {mapping}")
        Messages.write_message(f"   📄 Excel File: {file_name}")
        Messages.write_message(f"   📑 Sheet Name: {sheet_name}")
        if test_id:
            Messages.write_message(f"   🆔 Test ID: {test_id}")
        Messages.write_message("═" * 80)

# Helper functions for cleaner imports in steps
def log_step(step_name, icon="📍"):
    """Quick method to log step header"""
    ReportLogger.log_step_header(step_name, icon)

def log_complete(message="Step completed successfully"):
    """Quick method to log step completion"""
    ReportLogger.log_step_footer(success=True, message=message)

def log_failed(message="Step failed"):
    """Quick method to log step failure"""
    ReportLogger.log_step_footer(success=False, message=message)
