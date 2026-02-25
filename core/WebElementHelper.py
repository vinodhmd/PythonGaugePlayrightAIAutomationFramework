from playwright.sync_api import Page
import time
import os
from getgauge.python import Messages, data_store
# ============================================================================
# WEB ELEMENT HELPER CLASS
# ============================================================================
class WebElementHelper:
    """Unified helper for all web elements"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def _log_pass(self, action, selector, details=""):
        """Log pass message"""
        Messages.write_message(f"✓ PASS: {action} on '{selector}' {details}")
        if not hasattr(data_store.scenario, 'passed_steps'):
            data_store.scenario.passed_steps = []
        data_store.scenario.passed_steps.append(f"{action}: {selector}")
    
    def _log_fail(self, action, selector, error):
        """Log fail message with screenshot"""
        Messages.write_message(f"✗ FAIL: {action} on '{selector}'")
        Messages.write_message(f"✗ Error: {str(error)}")
        try:
            # Use GAUGE_REPORTS_DIR if set, otherwise default to 'reports'
            base_report_dir = os.environ.get("GAUGE_REPORTS_DIR", "reports")
            screenshot_dir = os.path.join(base_report_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"error_{action}_{int(time.time())}.png")
            self.page.screenshot(path=screenshot_path)
            Messages.write_message(f"✗ Screenshot: {screenshot_path}")
        except:
            pass
        if not hasattr(data_store.scenario, 'failed_steps'):
            data_store.scenario.failed_steps = []
        data_store.scenario.failed_steps.append(f"{action}: {selector}")
        raise AssertionError(f"{action} failed: {str(error)}")
    
    # ========== EDIT BOX ==========
    def editbox_enter_text(self, selector, text, clear=True):
        """Enter text in edit box"""
        try:
            element = self.page.locator(selector)
            element.wait_for(state='visible', timeout=10000)
            if clear:
                element.clear()
            element.fill(text)
            actual = element.input_value()
            if actual == text:
                self._log_pass("editbox_enter_text", selector, f"- Text: '{text}'")
            else:
                self._log_fail("editbox_enter_text", selector, f"Expected '{text}', got '{actual}'")
            return True
        except Exception as e:
            self._log_fail("editbox_enter_text", selector, e)
    
    def editbox_get_text(self, selector):
        """Get text from edit box"""
        try:
            element = self.page.locator(selector)
            text = element.input_value()
            self._log_pass("editbox_get_text", selector, f"- Value: '{text}'")
            return text
        except Exception as e:
            self._log_fail("editbox_get_text", selector, e)
    
    # ========== CHECKBOX ==========
    def checkbox_check(self, selector):
        """Check a checkbox"""
        try:
            element = self.page.locator(selector)
            element.check()
            is_checked = element.is_checked()
            if is_checked:
                self._log_pass("checkbox_check", selector, "- Checked successfully")
            else:
                self._log_fail("checkbox_check", selector, "Checkbox not checked")
            return True
        except Exception as e:
            self._log_fail("checkbox_check", selector, e)
    
    def checkbox_uncheck(self, selector):
        """Uncheck a checkbox"""
        try:
            element = self.page.locator(selector)
            element.uncheck()
            is_checked = element.is_checked()
            if not is_checked:
                self._log_pass("checkbox_uncheck", selector, "- Unchecked successfully")
            else:
                self._log_fail("checkbox_uncheck", selector, "Checkbox still checked")
            return True
        except Exception as e:
            self._log_fail("checkbox_uncheck", selector, e)
    
    def checkbox_is_checked(self, selector):
        """Check if checkbox is checked"""
        try:
            element = self.page.locator(selector)
            is_checked = element.is_checked()
            status = "checked" if is_checked else "unchecked"
            self._log_pass("checkbox_is_checked", selector, f"- Status: {status}")
            return is_checked
        except Exception as e:
            self._log_fail("checkbox_is_checked", selector, e)
    
    def checkbox_toggle(self, selector):
        """Toggle checkbox state"""
        try:
            element = self.page.locator(selector)
            current_state = element.is_checked()
            if current_state:
                element.uncheck()
            else:
                element.check()
            new_state = element.is_checked()
            self._log_pass("checkbox_toggle", selector, f"- {current_state} → {new_state}")
            return True
        except Exception as e:
            self._log_fail("checkbox_toggle", selector, e)
    
    # ========== RADIO BUTTON ==========
    def radio_select(self, selector):
        """Select a radio button"""
        try:
            element = self.page.locator(selector)
            element.check()
            is_checked = element.is_checked()
            if is_checked:
                self._log_pass("radio_select", selector, "- Selected successfully")
            else:
                self._log_fail("radio_select", selector, "Radio not selected")
            return True
        except Exception as e:
            self._log_fail("radio_select", selector, e)
    
    def radio_is_selected(self, selector):
        """Check if radio button is selected"""
        try:
            element = self.page.locator(selector)
            is_checked = element.is_checked()
            status = "selected" if is_checked else "not selected"
            self._log_pass("radio_is_selected", selector, f"- Status: {status}")
            return is_checked
        except Exception as e:
            self._log_fail("radio_is_selected", selector, e)
    
    def radio_get_selected_value(self, name):
        """Get selected radio button value from group"""
        try:
            selected = self.page.locator(f"input[name='{name}']:checked")
            value = selected.get_attribute('value')
            self._log_pass("radio_get_selected_value", name, f"- Value: '{value}'")
            return value
        except Exception as e:
            self._log_fail("radio_get_selected_value", name, e)
    
    # ========== DROPDOWN ==========
    def dropdown_select_by_value(self, selector, value):
        """Select dropdown option by value"""
        try:
            element = self.page.locator(selector)
            element.select_option(value=value)
            selected = element.input_value()
            if selected == value:
                self._log_pass("dropdown_select_by_value", selector, f"- Value: '{value}'")
            else:
                self._log_fail("dropdown_select_by_value", selector, f"Expected '{value}', got '{selected}'")
            return True
        except Exception as e:
            self._log_fail("dropdown_select_by_value", selector, e)
    
    def dropdown_select_by_label(self, selector, label):
        """Select dropdown option by label"""
        try:
            element = self.page.locator(selector)
            element.select_option(label=label)
            self._log_pass("dropdown_select_by_label", selector, f"- Label: '{label}'")
            return True
        except Exception as e:
            self._log_fail("dropdown_select_by_label", selector, e)
    
    def dropdown_select_by_index(self, selector, index):
        """Select dropdown option by index"""
        try:
            element = self.page.locator(selector)
            element.select_option(index=index)
            self._log_pass("dropdown_select_by_index", selector, f"- Index: {index}")
            return True
        except Exception as e:
            self._log_fail("dropdown_select_by_index", selector, e)
    
    def dropdown_get_selected_text(self, selector):
        """Get selected dropdown text"""
        try:
            element = self.page.locator(selector)
            selected_option = element.locator("option:checked")
            text = selected_option.inner_text()
            self._log_pass("dropdown_get_selected_text", selector, f"- Text: '{text}'")
            return text
        except Exception as e:
            self._log_fail("dropdown_get_selected_text", selector, e)
    
    def dropdown_get_all_options(self, selector):
        """Get all dropdown options"""
        try:
            element = self.page.locator(selector)
            options = element.locator("option").all_inner_texts()
            self._log_pass("dropdown_get_all_options", selector, f"- Count: {len(options)}")
            return options
        except Exception as e:
            self._log_fail("dropdown_get_all_options", selector, e)
    
    # ========== DATE/TIME PICKER ==========
    def datepicker_set_date(self, selector, date):
        """Set date (format: YYYY-MM-DD)"""
        try:
            element = self.page.locator(selector)
            element.fill(date)
            actual = element.input_value()
            if actual == date:
                self._log_pass("datepicker_set_date", selector, f"- Date: {date}")
            else:
                self._log_fail("datepicker_set_date", selector, f"Expected '{date}', got '{actual}'")
            return True
        except Exception as e:
            self._log_fail("datepicker_set_date", selector, e)
    
    def timepicker_set_time(self, selector, time_value):
        """Set time (format: HH:MM)"""
        try:
            element = self.page.locator(selector)
            element.fill(time_value)
            actual = element.input_value()
            if actual == time_value:
                self._log_pass("timepicker_set_time", selector, f"- Time: {time_value}")
            else:
                self._log_fail("timepicker_set_time", selector, f"Expected '{time_value}', got '{actual}'")
            return True
        except Exception as e:
            self._log_fail("timepicker_set_time", selector, e)
    
    def datetimepicker_set(self, selector, datetime_value):
        """Set datetime (format: YYYY-MM-DDTHH:MM)"""
        try:
            element = self.page.locator(selector)
            element.fill(datetime_value)
            actual = element.input_value()
            self._log_pass("datetimepicker_set", selector, f"- DateTime: {datetime_value}")
            return True
        except Exception as e:
            self._log_fail("datetimepicker_set", selector, e)
    
    # ========== FILE UPLOAD ==========
    def file_upload_single(self, selector, file_path):
        """Upload single file"""
        try:
            element = self.page.locator(selector)
            element.set_input_files(file_path)
            self._log_pass("file_upload_single", selector, f"- File: {file_path}")
            return True
        except Exception as e:
            self._log_fail("file_upload_single", selector, e)
    
    def file_upload_multiple(self, selector, file_paths):
        """Upload multiple files"""
        try:
            element = self.page.locator(selector)
            element.set_input_files(file_paths)
            self._log_pass("file_upload_multiple", selector, f"- Files: {len(file_paths)}")
            return True
        except Exception as e:
            self._log_fail("file_upload_multiple", selector, e)
    
    def file_clear_upload(self, selector):
        """Clear uploaded files"""
        try:
            element = self.page.locator(selector)
            element.set_input_files([])
            self._log_pass("file_clear_upload", selector, "- Cleared")
            return True
        except Exception as e:
            self._log_fail("file_clear_upload", selector, e)
    
    # ========== TABLE ==========
    def table_get_row_count(self, selector):
        """Get table row count"""
        try:
            rows = self.page.locator(f"{selector} tbody tr").count()
            self._log_pass("table_get_row_count", selector, f"- Rows: {rows}")
            return rows
        except Exception as e:
            self._log_fail("table_get_row_count", selector, e)
    
    def table_get_cell_text(self, selector, row, col):
        """Get table cell text (1-indexed)"""
        try:
            cell = self.page.locator(f"{selector} tbody tr:nth-child({row}) td:nth-child({col})")
            text = cell.inner_text()
            self._log_pass("table_get_cell_text", selector, f"- Row:{row}, Col:{col}, Text:'{text}'")
            return text
        except Exception as e:
            self._log_fail("table_get_cell_text", selector, e)
    
    def table_get_row_data(self, selector, row):
        """Get entire row data as list"""
        try:
            cells = self.page.locator(f"{selector} tbody tr:nth-child({row}) td").all_inner_texts()
            self._log_pass("table_get_row_data", selector, f"- Row:{row}, Cells:{len(cells)}")
            return cells
        except Exception as e:
            self._log_fail("table_get_row_data", selector, e)
    
    def table_get_column_data(self, selector, col):
        """Get entire column data as list"""
        try:
            cells = self.page.locator(f"{selector} tbody tr td:nth-child({col})").all_inner_texts()
            self._log_pass("table_get_column_data", selector, f"- Col:{col}, Cells:{len(cells)}")
            return cells
        except Exception as e:
            self._log_fail("table_get_column_data", selector, e)
    
    def table_click_cell(self, selector, row, col):
        """Click on table cell"""
        try:
            cell = self.page.locator(f"{selector} tbody tr:nth-child({row}) td:nth-child({col})")
            cell.click()
            self._log_pass("table_click_cell", selector, f"- Row:{row}, Col:{col}")
            return True
        except Exception as e:
            self._log_fail("table_click_cell", selector, e)
    
    def table_search_text(self, selector, search_text):
        """Search for text in table and return row number"""
        try:
            rows = self.page.locator(f"{selector} tbody tr").count()
            for i in range(1, rows + 1):
                row_text = " ".join(self.page.locator(f"{selector} tbody tr:nth-child({i})").all_inner_texts())
                if search_text in row_text:
                    self._log_pass("table_search_text", selector, f"- Found at row:{i}")
                    return i
            self._log_fail("table_search_text", selector, f"Text '{search_text}' not found")
        except Exception as e:
            self._log_fail("table_search_text", selector, e)
    
    # ========== IMAGE ==========
    def image_is_visible(self, selector):
        """Check if image is visible"""
        try:
            element = self.page.locator(selector)
            is_visible = element.is_visible()
            status = "visible" if is_visible else "not visible"
            self._log_pass("image_is_visible", selector, f"- Status: {status}")
            return is_visible
        except Exception as e:
            self._log_fail("image_is_visible", selector, e)
    
    def image_get_src(self, selector):
        """Get image src attribute"""
        try:
            element = self.page.locator(selector)
            src = element.get_attribute('src')
            self._log_pass("image_get_src", selector, f"- Src: {src}")
            return src
        except Exception as e:
            self._log_fail("image_get_src", selector, e)
    
    def image_get_alt_text(self, selector):
        """Get image alt text"""
        try:
            element = self.page.locator(selector)
            alt = element.get_attribute('alt')
            self._log_pass("image_get_alt_text", selector, f"- Alt: {alt}")
            return alt
        except Exception as e:
            self._log_fail("image_get_alt_text", selector, e)
    
    def image_click(self, selector):
        """Click on image"""
        try:
            element = self.page.locator(selector)
            element.click()
            self._log_pass("image_click", selector, "- Clicked")
            return True
        except Exception as e:
            self._log_fail("image_click", selector, e)
    
    # ========== LINK ==========
    def link_click(self, selector):
        """Click on link"""
        try:
            element = self.page.locator(selector)
            element.click()
            self._log_pass("link_click", selector, "- Clicked")
            return True
        except Exception as e:
            self._log_fail("link_click", selector, e)
    
    def link_get_href(self, selector):
        """Get link href"""
        try:
            element = self.page.locator(selector)
            href = element.get_attribute('href')
            self._log_pass("link_get_href", selector, f"- Href: {href}")
            return href
        except Exception as e:
            self._log_fail("link_get_href", selector, e)
    
    def link_get_text(self, selector):
        """Get link text"""
        try:
            element = self.page.locator(selector)
            text = element.inner_text()
            self._log_pass("link_get_text", selector, f"- Text: '{text}'")
            return text
        except Exception as e:
            self._log_fail("link_get_text", selector, e)
    
    def link_open_new_tab(self, selector):
        """Click link that opens in new tab"""
        try:
            with self.page.context.expect_page() as new_page_info:
                self.page.locator(selector).click()
            new_page = new_page_info.value
            self._log_pass("link_open_new_tab", selector, f"- New page URL: {new_page.url}")
            return new_page
        except Exception as e:
            self._log_fail("link_open_new_tab", selector, e)
    
    # ========== BUTTON ==========
    def button_click(self, selector):
        """Click button"""
        try:
            element = self.page.locator(selector)
            element.click()
            self._log_pass("button_click", selector, "- Clicked")
            return True
        except Exception as e:
            self._log_fail("button_click", selector, e)
    
    def button_double_click(self, selector):
        """Double click button"""
        try:
            element = self.page.locator(selector)
            element.dblclick()
            self._log_pass("button_double_click", selector, "- Double clicked")
            return True
        except Exception as e:
            self._log_fail("button_double_click", selector, e)
    
    def button_right_click(self, selector):
        """Right click button"""
        try:
            element = self.page.locator(selector)
            element.click(button='right')
            self._log_pass("button_right_click", selector, "- Right clicked")
            return True
        except Exception as e:
            self._log_fail("button_right_click", selector, e)
    
    def button_is_enabled(self, selector):
        """Check if button is enabled"""
        try:
            element = self.page.locator(selector)
            is_enabled = element.is_enabled()
            status = "enabled" if is_enabled else "disabled"
            self._log_pass("button_is_enabled", selector, f"- Status: {status}")
            return is_enabled
        except Exception as e:
            self._log_fail("button_is_enabled", selector, e)
    
    def button_get_text(self, selector):
        """Get button text"""
        try:
            element = self.page.locator(selector)
            text = element.inner_text()
            self._log_pass("button_get_text", selector, f"- Text: '{text}'")
            return text
        except Exception as e:
            self._log_fail("button_get_text", selector, e)
    
    def button_wait_and_click(self, selector, timeout=5000):
        """Wait for button and click"""
        try:
            element = self.page.locator(selector)
            element.wait_for(state='visible', timeout=timeout)
            element.click()
            self._log_pass("button_wait_and_click", selector, f"- Clicked after wait")
            return True
        except Exception as e:
            self._log_fail("button_wait_and_click", selector, e)
