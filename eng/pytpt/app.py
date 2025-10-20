"""Main application to load CSV files to Teradata tables using TPT."""

import sys
from pathlib import Path

from pytpt.logging_config import setup_logging, get_logger
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
    # Load configuration first (before logging setup)
    cfg = load_config()

    # Setup logging with config values
    log_dir = cfg.logging.get("dir", "logs")
    log_file = cfg.logging.get("file", "pytpt.log")
    log_level = cfg.logging.get("level", "INFO")
    setup_logging(log_dir=log_dir, log_file=log_file, log_level=log_level)

    logger = get_logger(__name__)
    logger.info("Starting CSV to Teradata loading process...")

    try:
        # Load environment variables
        load_env_vars()
        logger.info("Environment variables loaded")
        logger.info("Configuration loaded")

        # Get data directory and table mapping
        data_dir = cfg.data.dir
        table_mapping = get_table_mapping()

        logger.info(f"Looking for CSV files in: {data_dir}")
        logger.debug(f"Table mapping: {table_mapping}")

        # Find CSV files
        csv_files = find_csv_files(data_dir)

        if not csv_files:
            logger.warning("No CSV files found!")
            return

        logger.info(f"Found {len(csv_files)} CSV files")

        # Filter CSV files to only those with table mappings
        mapped_files = []
        skipped_files = []

        for csv_file in csv_files:
            table_name = match_csv_to_table(csv_file, table_mapping)
            if table_name:
                mapped_files.append((csv_file, table_name))
                logger.debug(f"Mapped: {csv_file.name} -> {table_name}")
            else:
                skipped_files.append(csv_file)

        if skipped_files:
            logger.warning(
                f"Skipping {len(skipped_files)} CSV files with no table mapping:"
            )
            for skipped_file in skipped_files:
                logger.warning(f"  - {skipped_file.name} (no mapping found)")

        if not mapped_files:
            logger.error("No CSV files have table mappings configured!")
            return

        logger.info(f"Processing {len(mapped_files)} CSV files with table mappings")

        # Process each mapped CSV file
        success_count = 0
        failed_files = []

        for csv_file, table_name in mapped_files:
            csv_path = str(csv_file.absolute())

            logger.info(f"Processing: {csv_file.name} -> {table_name}")

            if load_table(table_name, csv_path):
                success_count += 1
                logger.success(f"Successfully processed: {csv_file.name}")
            else:
                failed_files.append(csv_file.name)
                logger.error(f"Failed to process: {csv_file.name}")

        # Summary
        total_files = len(mapped_files)
        logger.info(
            f"Load process completed: {success_count}/{total_files} files loaded successfully"
        )

        if failed_files:
            logger.error(
                f"Failed files ({len(failed_files)}): {', '.join(failed_files)}"
            )

        if success_count == total_files:
            logger.success("All files loaded successfully!")
        elif success_count > 0:
            logger.warning(
                f"Partial success: {success_count} out of {total_files} files loaded"
            )
        else:
            logger.error("No files were loaded successfully")

    except Exception as e:
        logger.exception(f"Application failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
