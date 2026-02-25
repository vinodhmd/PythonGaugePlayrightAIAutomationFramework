import os
import shutil
import json
import webbrowser
from bs4 import BeautifulSoup

class GaugeReportMerger:
    def __init__(self, browser_reports=None):
        """
        Initialize merger with list of browser names.
        :param browser_reports: List of browsers, e.g., ['chrome', 'edge', 'firefox']
        """
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.reports_root = os.path.join(self.project_root, "reports")
        self.consolidated_dir = os.path.join(self.reports_root, "consolidated_report")
        self.browser_reports = browser_reports or ["chrome", "edge", "firefox"]

    def merge_reports(self):
        """Consolidate reports from different browsers into a single unified report."""
        print("Starting report consolidation...")
        # 1. Create consolidated directory structure
        if os.path.exists(self.consolidated_dir):
            shutil.rmtree(self.consolidated_dir)
        os.makedirs(self.consolidated_dir)
        # 2. Find a valid base report to use as a template (e.g., Chrome's)
        base_report_path = None
        for browser in self.browser_reports:
            report_path = os.path.join(self.reports_root, browser, "html-report")
            if os.path.exists(os.path.join(report_path, "index.html")):
                base_report_path = report_path
                break
        if not base_report_path:
            print("No valid base report found to merge.")
            return
        # 3. Copy ALL static assets (css, js, images, fonts) from the base report
        #    This ensures the Gauge report checks/structure remains valid.
        try:
            for item in os.listdir(base_report_path):
                s = os.path.join(base_report_path, item)
                d = os.path.join(self.consolidated_dir, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d)
                else:
                    shutil.copy2(s, d)
            # 4. Also copy screenshots from ALL browsers into the consolidated report
            consolidated_screenshots_dir = os.path.join(self.reports_root, "screenshots") # This might be legacy
            common_screenshots_dir = os.path.join(self.reports_root, "screenshots")
            os.makedirs(common_screenshots_dir, exist_ok=True)
            for browser in self.browser_reports:
                browser_screenshot_dir = os.path.join(self.reports_root, browser, "screenshots")
                if os.path.exists(browser_screenshot_dir):
                    for file in os.listdir(browser_screenshot_dir):
                        src = os.path.join(browser_screenshot_dir, file)
                        dst = os.path.join(common_screenshots_dir, file)
                        if not os.path.exists(dst):
                            shutil.copy2(src, dst)
        except Exception as e:
            print(f"Error copying base assets: {e}")
            return
        # 5. Parse and Merge Data
        # We will create a custom Dashboard that links to individual browser reports
        # OR attempt to merge the JSON data (Gauge stores data in js/search_index.js usually)
        # Merging Gauge spec details deeply is complex because of ID collisions.
        # BETTER APPROACH: Create a "Consolidated Dashboard" that serves as a landing page
        # showing pass/fail stats per browser and links to full individual reports.
        self.create_dashboard_html()

    def create_dashboard_html(self):
        """Create a custom HTML dashboard summarizing results from all browsers."""
        summary_data = []
        for browser in self.browser_reports:
            index_path = os.path.join(self.reports_root, browser, "html-report", "index.html")
            data = {
                "browser": browser.capitalize(),
                "status": "Not Run",
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "total": 0,
                "duration": "0s",
                "link": f"../{browser}/html-report/index.html"
            }
            if os.path.exists(index_path):
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f.read(), 'html.parser')
                        passed = soup.select_one(".scenario-stats.pass .value")
                        failed = soup.select_one(".scenario-stats.fail .value")
                        skipped = soup.select_one(".scenario-stats.skip .value")
                        p_val = int(passed.text) if passed else 0
                        f_val = int(failed.text) if failed else 0
                        s_val = int(skipped.text) if skipped else 0
                        data["passed"] = p_val
                        data["failed"] = f_val
                        data["skipped"] = s_val
                        data["total"] = p_val + f_val + s_val
                        if f_val > 0:
                            data["status"] = "Failed"
                        elif p_val > 0:
                            data["status"] = "Passed"
                        else:
                            data["status"] = "No Tests"
                        duration_label = soup.find("label", string=lambda x: x and "Total Time" in x)
                        if duration_label:
                            duration_val = duration_label.find_next("span")
                            if duration_val:
                                data["duration"] = duration_val.text.strip()
                except Exception as e:
                    print(f"Error parsing {browser} report: {e}")
            summary_data.append(data)
        # Generate HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Consolidated Test Execution Report</title>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; }}
                .container {{ max-width: 1000px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                h1 {{ text-align: center; color: #2c3e50; margin-bottom: 30px; }}
                .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
                .card {{ padding: 20px; border-radius: 8px; color: white; text-align: center; transition: transform 0.2s; }}
                .card:hover {{ transform: translateY(-5px); }}
                .card.chrome {{ background: linear-gradient(135deg, #4285F4, #34A853); }}
                .card.edge {{ background: linear-gradient(135deg, #0078D7, #00C4CC); }}
                .card.firefox {{ background: linear-gradient(135deg, #FF7139, #E0C845); }}
                .card h2 {{ margin: 0 0 10px 0; font-size: 1.5em; }}
                .stats {{ display: flex; justify-content: space-around; margin-top: 15px; font-weight: bold; }}
                .stat-item {{ display: flex; flex-direction: column; }}
                .stat-val {{ font-size: 1.2em; }}
                .status-badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; background: rgba(0,0,0,0.2); margin-top: 10px; }}
                .view-btn {{ display: block; margin-top: 15px; padding: 10px; background: rgba(255,255,255,0.2); color: white; text-decoration: none; border-radius: 4px; font-weight: bold; }}
                .view-btn:hover {{ background: rgba(255,255,255,0.3); }}
                .footer {{ text-align: center; margin-top: 20px; color: #888; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Consolidated Test Execution Report</h1>
                
                <div class="summary-grid">
        """
        for item in summary_data:
            icon = "🌐"
            if item['browser'] == 'Chrome': icon = "🔵"
            if item['browser'] == 'Firefox': icon = "🦊"
            if item['browser'] == 'Edge': icon = "🌊"
            html_content += f"""
            <div class="card {item['browser'].lower()}">
                <h2>{icon} {item['browser']}</h2>
                <div class="status-badge">{item['status']}</div>
                <div class="stats">
                    <div class="stat-item"><span class="stat-val">✔ {item['passed']}</span>Pass</div>
                    <div class="stat-item"><span class="stat-val">✘ {item['failed']}</span>Fail</div>
                    <div class="stat-item"><span class="stat-val">⏱ {item['duration']}</span>Time</div>
                </div>
                <a href="{item['link']}" class="view-btn" target="_blank">View Full Report ➜</a>
            </div>
            """ 
        html_content += """
                </div>
                <div class="footer">
                    Generated by Gauge Framework • <a href="#">Dashboard</a>
                </div>
            </div>
        </body>
        </html>
        """
        output_path = os.path.join(self.consolidated_dir, "dashboard.html")
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(html_content)
        print(f"Consolidated dashboard created at: {output_path}")
if __name__ == "__main__":
    merger = GaugeReportMerger()
    merger.merge_reports()