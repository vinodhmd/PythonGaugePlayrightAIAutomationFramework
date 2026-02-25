import yaml
import subprocess
import os
import sys

# Resolve config path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add project root to sys.path to allow importing from core
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from core.report_merger import GaugeReportMerger
from env_loader import load_env_context

config_path = os.path.join(script_dir, "yl_parallelexecution.yml")

# Load Excel Environment
excel_env = load_env_context()
os.environ.update(excel_env)

with open(config_path) as f:
    config = yaml.safe_load(f)["execution"]

base_cmd = ["gauge", "run"]

if config.get("parallel"):
    base_cmd += ["--parallel", "-n", str(config.get('nodes', 2))]

if config.get("include_tags"):
    # Normalize tags: split by ; and flatten
    raw_tags = config['include_tags']
    normalized_tags = []
    for tag_entry in raw_tags:
        normalized_tags.extend(tag_entry.split(';'))
    # Join with | for OR logic (Gauge Tag Expression)
    tag_expr = " | ".join(normalized_tags)
    base_cmd.append(f"--tags={tag_expr}")

if config.get("exclude_tags"):
    raw_excludes = config['exclude_tags']
    normalized_excludes = []
    for tag_entry in raw_excludes:
        normalized_excludes.extend(tag_entry.split(';'))
    # Exclude tags logic: !tag1 & !tag2
    exclude_expr = " & ".join([f"!{tag}" for tag in normalized_excludes])
    base_cmd.append(f"--tags={tag_expr} & {exclude_expr}" if config.get("include_tags") else f"--tags={exclude_expr}")

base_cmd += [f"--env={config['env']}", "specs/"]

browsers = config.get("browsers", [])
if not browsers:
    # No browsers specified, run once with default/env config
    subprocess.run(base_cmd, check=True)
else:
    # Run for each browser concurrently
    processes = []
    print(f"Starting execution for browsers: {browsers}")
    
    for browser in browsers:
        env = os.environ.copy()
        env["BROWSER"] = browser
        env["GAUGE_REPORTS_DIR"] = f"reports/{browser}"
        print(f"Launching run for BROWSER={browser} with command: {' '.join(base_cmd)}")
        p = subprocess.Popen(base_cmd, env=env)
        processes.append(p)
    
    # Wait for all to complete
    exit_codes = [p.wait() for p in processes]
    
    # Generate Consolidated Report
    print("\ngenerating Consolidated Report...")
    merger = GaugeReportMerger(browsers)
    merger.merge_reports()
    
    if any(code != 0 for code in exit_codes):
        sys.exit(1)

