"""Main application to load CSV files to Teradata tables using TPT."""

import sys
from pathlib import Path


from pytpt.templates import load_env_vars
from pytpt.csv_utils import (
    load_config,
    find_csv_files,
    get_table_mapping,
    match_csv_to_table,
)
from pytpt.tpt_runner import load_table


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

    # Filter CSV files to only those with table mappings
    mapped_files = []
    skipped_files = []

    for csv_file in csv_files:
        table_name = match_csv_to_table(csv_file, table_mapping)
        if table_name:
            mapped_files.append((csv_file, table_name))
        else:
            skipped_files.append(csv_file)

    if skipped_files:
        print(f"\nSkipping {len(skipped_files)} CSV files with no table mapping:")
        for skipped_file in skipped_files:
            print(f"  - {skipped_file.name} (no mapping found)")

    if not mapped_files:
        print("No CSV files have table mappings configured!")
        return

    print(f"\nProcessing {len(mapped_files)} CSV files with table mappings:")

    # Process each mapped CSV file
    success_count = 0
    for csv_file, table_name in mapped_files:
        csv_path = str(csv_file.absolute())

        print(f"\nProcessing: {csv_file.name} -> {table_name}")

        if load_table(table_name, csv_path):
            success_count += 1

    print(
        f"\nCompleted: {success_count}/{len(mapped_files)} mapped files loaded successfully"
    )


if __name__ == "__main__":
    main()
