"""Main application to load CSV files to Teradata tables using TPT."""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path("eng/pytdml/src")))

from pytdml.templates import load_env_vars
from pytdml.csv_utils import (
    load_config,
    find_csv_files,
    get_table_mapping,
    match_csv_to_table,
)
from pytdml.tpt_runner import load_table


def main():
    """Main function to load all CSV files."""
    print("Starting CSV to Teradata loading process...")

    # Load environment variables
    load_env_vars()

    # Load configuration
    cfg = load_config()

    # Get data directory and table mapping
    data_dir = cfg.data.dir
    table_mapping = get_table_mapping()

    print(f"Looking for CSV files in: {data_dir}")
    print(f"Table mapping: {table_mapping}")

    # Find CSV files
    csv_files = find_csv_files(data_dir)

    if not csv_files:
        print("No CSV files found!")
        return

    print(f"Found {len(csv_files)} CSV files")

    # Process each CSV file
    success_count = 0
    for csv_file in csv_files:
        table_name = match_csv_to_table(csv_file, table_mapping)
        csv_path = str(csv_file.absolute())

        print(f"\nProcessing: {csv_file.name} -> {table_name}")

        if load_table(table_name, csv_path):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(csv_files)} files loaded successfully")


if __name__ == "__main__":
    main()
