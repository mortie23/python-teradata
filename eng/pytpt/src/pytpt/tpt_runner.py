"""Simple TPT execution functions."""

import subprocess
from pathlib import Path


def run_tbuild(
    jvar_file: Path,
    tpt_file: Path,
) -> bool:
    """Run tbuild command with jobvars and TPT script."""
    cmd = ["tbuild", "-f", str(tpt_file), "-v", str(jvar_file)]

    print(f"Running: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode == 0


def load_table(
    table_name: str,
    csv_file_path: str,
) -> bool:
    """Load a single CSV file to a table using TPT."""
    from .templates import create_tpt_files

    # Create TPT files
    jvar_file, tpt_file = create_tpt_files(table_name, csv_file_path)

    print(f"Loading {csv_file_path} to table {table_name}")

    # Run TPT
    success = run_tbuild(jvar_file, tpt_file)

    if success:
        print(f"Successfully loaded {table_name}")
    else:
        print(f"Failed to load {table_name}")

    return success
