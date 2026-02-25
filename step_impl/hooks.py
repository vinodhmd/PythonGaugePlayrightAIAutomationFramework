from getgauge.python import before_suite, after_suite, before_scenario, after_scenario, after_step, screenshot, ExecutionContext, data_store
from core.Core_basePage import BasePage
from core.TestDataManager import TestDataManager
from core.ReportLogger import ReportLogger
import os
import zipfile
import shutil
from datetime import datetime

def archive_reports():
    """Archive existing reports before new test execution"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    reports_dir = os.path.join(project_root, "reports")
    archive_dir = os.path.join(reports_dir, "archives")
    # Create archive directory if it doesn't exist
    os.makedirs(archive_dir, exist_ok=True)
    # Folders to archive
    # Dynamically find folders to archive (everything in reports except archives)
    folders_to_archive = []
    if os.path.exists(reports_dir):
        for item in os.listdir(reports_dir):
            if item == 'archives':
                continue
            item_path = os.path.join(reports_dir, item)
            # Archive both files and folders in reports dir (usually html-report, screenshots, etc)
            folders_to_archive.append(item_path)
    
    # Also add .gauge from project root
    folders_to_archive.append(os.path.join(project_root, ".gauge"))

    # Check if there are any existing reports to archive
    has_content = any(os.path.exists(f) for f in folders_to_archive)
    
    if not has_content:
        print("No existing reports to archive.")
        return
    
    # Create timestamped archive name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"reports_archive_{timestamp}.zip"
    archive_path = os.path.join(archive_dir, archive_name)
    
    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item_path in folders_to_archive:
                if os.path.exists(item_path):
                    if os.path.isdir(item_path):
                        folder_name = os.path.basename(item_path)
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                arcname = os.path.join(
                                    folder_name,
                                    os.path.relpath(file_path, item_path)
                                )
                                zipf.write(file_path, arcname)
                    else:
                        # Archive individual files in reports dir
                        zipf.write(item_path, os.path.basename(item_path))
                        
        print(f"Reports archived: {archive_path}")
        
        # Clean up archived items (except .gauge)
        for item_path in folders_to_archive:
            if os.path.exists(item_path) and item_path != os.path.join(project_root, ".gauge"):
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Cleaned directory: {item_path}")
                else:
                    os.remove(item_path)
                    print(f"Cleaned file: {item_path}")

    except Exception as e:
        print(f"Warning: Could not archive reports: {e}")

@before_suite
def init_driver():
    # Archive existing reports before running new tests
    archive_reports()
    BasePage.initialize()

@after_suite
def close_driver():
    BasePage.close()

@before_scenario
def init_context(context: ExecutionContext):
    # Store scenario tags in data_store for access in steps
    data_store.scenario['tags'] = context.scenario.tags
    data_store.scenario['name'] = context.scenario.name
    # Store specification file name (e.g., sp_login.spec)
    spec_file_name = context.specification.file_name if hasattr(context.specification, 'file_name') else ''
    data_store.scenario['spec_file'] = spec_file_name
    
    # Create browser context
    BasePage.create_context()
    BasePage.start_tracing()
    
    # Automatically load test data based on scenario tags
    test_data = TestDataManager.load_test_data()
    if test_data:
        test_id = TestDataManager.get_test_id()
        test_sheet = TestDataManager.get_test_sheet()
        ReportLogger.log_custom(f"📋 Test Data Auto-Loaded: {test_id} from {test_sheet} sheet")
        ReportLogger.log_custom(f"   Available data keys: {', '.join(test_data.keys())}")

@after_step
def capture_on_step_failure(context: ExecutionContext):
    """Capture screenshot and error details immediately when a step fails"""
    if context.step.is_failing:
        from getgauge.python import Messages
        import traceback
        # Log error details
        error_info = {
            'step': context.step.text,
            'scenario': context.scenario.name,
            'spec': context.specification.name,
            'tags': context.scenario.tags,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # Get error message if available
        try:
            error_msg = str(context.step.error_message) if hasattr(context.step, 'error_message') else "Unknown error"
            error_info['error'] = error_msg
        except:
            error_info['error'] = "Error details not available"
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            logs_dir = os.path.join(project_root, "logs")
            os.makedirs(logs_dir, exist_ok=True)
            error_log_path = os.path.join(logs_dir, "execution_errors.log")
            with open(error_log_path, 'a', encoding='utf-8') as f:
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"EXECUTION ERROR - {error_info['timestamp']}\n")
                f.write("=" * 70 + "\n")
                f.write(f"Step: {error_info['step']}\n")
                f.write(f"Scenario: {error_info['scenario']}\n")
                f.write(f"Spec: {error_info['spec']}\n")
                f.write(f"Tags: {', '.join(error_info['tags'])}\n")
                f.write(f"Error: {error_info['error']}\n")
                f.write("-" * 70 + "\n")
                f.write(f"Stack Trace:\n{traceback.format_exc()}\n")
                f.write("=" * 70 + "\n\n")
        except Exception as log_error:
            Messages.write_message(f"   ⚠️ Failed to write error log: {str(log_error)}")
        try:
            page = BasePage.get_page()
            if page and BasePage.screenshot_on_failure():
                step_name = context.step.text.replace(" ", "_")[:50]
                scenario_name = context.scenario.name.replace(" ", "_")[:30]
                screenshot_path = BasePage.take_screenshot(f"failed_step_{scenario_name}_{step_name}")
                relative_path = f"../screenshots/{os.path.basename(screenshot_path)}"
                Messages.write_message(f"📸 Screenshot captured: ![{step_name}]({relative_path})")
        except Exception as e:
            Messages.write_message(f"   ⚠️ Failed to capture step screenshot: {str(e)}")


@after_scenario
def close_context(context: ExecutionContext):
    # Take screenshot on failure and attach to report
    if context.scenario.is_failing:
        try:
            if BasePage.get_page() and BasePage.screenshot_on_failure():
                scenario_name = context.scenario.name.replace(" ", "_")
                screenshot_path = BasePage.take_screenshot(f"failed_{scenario_name}")
                # Also capture screenshot bytes for Gauge report
                screenshot_bytes = BasePage.get_page().screenshot()
                # Write to Gauge messages with Markdown link
                relative_path = f"../screenshots/{os.path.basename(screenshot_path)}"
                from getgauge.python import Messages
                Messages.write_message(f"❌ Scenario Failed - Screenshot: ![{scenario_name}]({relative_path})")
        except Exception as e:
            from getgauge.python import Messages
            Messages.write_message(f"⚠️ Failed to capture screenshot: {str(e)}")
    # Stop tracing if enabled
    if BasePage.is_tracing_enabled():
        scenario_name = context.scenario.name.replace(" ", "_")
        BasePage.stop_tracing(scenario_name)
    # Close browser context
    BasePage.close_context()
    # Clear test data for next scenario
    TestDataManager.clear()

@screenshot
def take_screenshot_on_failure():
    """Custom screenshot function for Gauge to capture browser screenshots on failure"""
    try:
        if BasePage.get_page():
            return BasePage.get_page().screenshot(full_page=True)
        else:
            print("Screenshot failed: No active page instance")
    except Exception as e:
        print(f"Screenshot capture error: {str(e)}")
    return b""