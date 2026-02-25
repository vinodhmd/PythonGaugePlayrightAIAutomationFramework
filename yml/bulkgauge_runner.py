import subprocess
import os
from yaml_reader import load_execution_config
from env_loader import load_env_context

# Resolve config path relative to this script
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, "yl_bulkexecution.yml")

def run_gauge_with_tags():
    # Load Environment context from Excel
    excel_env = load_env_context()
    os.environ.update(excel_env)

    config = load_execution_config(config_path)

    execution = config.get("execution", {})
    include_tags = execution.get("include_tags", [])
    exclude_tags = execution.get("exclude_tags", [])
    parallel = execution.get("parallel", False)
    threads = execution.get("threads", 1)
    env = execution.get("env", "default")

    cmd = ["gauge", "run"]

    # Parallel execution
    if parallel:
        cmd.append("--parallel")
        cmd.append("-n")
        cmd.append(str(threads))

    # Construct Tag Expression
    # Format: (tag1 | tag2) & !tag3 & !tag4
    tag_expression_parts = []
    
    # Process includes (OR logic)
    if include_tags:
        # Flatten and split any semicolon separated tags
        flat_includes = []
        for tag in include_tags:
            flat_includes.extend(tag.split(';'))
        
        # Join with |
        if flat_includes:
            inc_str = " | ".join(flat_includes)
            tag_expression_parts.append(f"({inc_str})")
            
    # Process excludes (AND NOT logic)
    if exclude_tags:
        flat_excludes = []
        for tag in exclude_tags:
            flat_excludes.extend(tag.split(';'))
            
        for tag in flat_excludes:
            tag_expression_parts.append(f"!{tag}")
            
    # Combine everything with &
    if tag_expression_parts:
        final_tags = " & ".join(tag_expression_parts)
        cmd.append(f"--tags={final_tags}")

    # Environment
    cmd.append(f"--env={env}")

    # Specs folder
    cmd.append("specs/")

    print("Executing:", " ".join(cmd))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Gauge execution failed with exit code {e.returncode}")
        # We exit gracefully so it doesn't look like the runner script crashed
        exit(e.returncode)

if __name__ == "__main__":
    run_gauge_with_tags()
