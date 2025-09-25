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
    jvar_file, drop_file, create_file, load_file = create_tpt_files(
        table_name, csv_file_path
    )

    print(f"Loading {csv_file_path} to table {table_name}")

    # Run create table job first
    print("Step 1: Dropping table...")
    drop_success = run_tbuild(jvar_file, drop_file)

    if not drop_success:
        print(f"Failed to drop table {table_name}")
        return False

    # Run create table job first
    print("Step 2: Creating table...")
    create_success = run_tbuild(jvar_file, create_file)

    if not create_success:
        print(f"Failed to create table {table_name}")
        return False

    # Run load job second
    print("Step 3: Loading data...")
    load_success = run_tbuild(jvar_file, load_file)

    if load_success:
        print(f"Successfully loaded {table_name}")
    else:
        print(f"Failed to load data to {table_name}")

    return load_success
