"""Simple TPT execution functions."""

import re
import subprocess
from pathlib import Path
from typing import Dict, Optional

from .logging_config import get_logger

logger = get_logger(__name__)


def parse_tpt_metrics(output: str) -> Dict[str, Optional[int]]:
    """
    Parse TPT output to extract key metrics.

    Args:
        output: TPT stdout/stderr output

    Returns:
        Dictionary with parsed metrics
    """
    metrics = {"rows_sent": None, "rows_applied": None}

    # Pattern to match: $LOAD: Total Rows Sent To RDBMS: 1234
    rows_sent_pattern = r"\$LOAD:\s*Total Rows Sent To RDBMS:\s*(\d+)"
    rows_applied_pattern = r"\$LOAD:\s*Total Rows Applied:\s*(\d+)"

    # Search for rows sent
    sent_match = re.search(rows_sent_pattern, output, re.IGNORECASE)
    if sent_match:
        metrics["rows_sent"] = int(sent_match.group(1))

    # Search for rows applied
    applied_match = re.search(rows_applied_pattern, output, re.IGNORECASE)
    if applied_match:
        metrics["rows_applied"] = int(applied_match.group(1))

    return metrics


def run_tbuild(
    jvar_file: Path, tpt_file: Path, operation_type: str = "unknown"
) -> bool:
    """Run tbuild command with jobvars and TPT script."""
    cmd = ["tbuild", "-f", str(tpt_file), "-v", str(jvar_file)]

    logger.info(f"Starting {operation_type} operation: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    success = result.returncode == 0

    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Extract table name from jvar file for log naming
    table_name = "unknown"
    try:
        table_name = (
            jvar_file.stem.replace("_", "").replace("JVAR", "").replace("jvar", "")
        )
        if not table_name:
            table_name = jvar_file.stem
    except:
        table_name = "unknown"

    # Save complete TPT output to files
    stdout_log_file = logs_dir / f"tpt_{table_name}_{operation_type}_stdout.log"
    stderr_log_file = logs_dir / f"tpt_{table_name}_{operation_type}_stderr.log"
    combined_log_file = logs_dir / f"tpt_{table_name}_{operation_type}_combined.log"

    # Write stdout
    if result.stdout:
        with open(stdout_log_file, "w", encoding="utf-8") as f:
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Return Code: {result.returncode}\n")
            f.write(f"Operation: {operation_type}\n")
            f.write("=" * 80 + "\n")
            f.write(result.stdout)

    # Write stderr
    if result.stderr:
        with open(stderr_log_file, "w", encoding="utf-8") as f:
            f.write(f"Command: {' '.join(cmd)}\n")
            f.write(f"Return Code: {result.returncode}\n")
            f.write(f"Operation: {operation_type}\n")
            f.write("=" * 80 + "\n")
            f.write(result.stderr)

    # Write combined output
    with open(combined_log_file, "w", encoding="utf-8") as f:
        f.write(f"Command: {' '.join(cmd)}\n")
        f.write(f"Return Code: {result.returncode}\n")
        f.write(f"Operation: {operation_type}\n")
        f.write(f"Success: {success}\n")
        f.write("=" * 80 + "\n")
        if result.stdout:
            f.write("STDOUT:\n")
            f.write(result.stdout)
            f.write("\n" + "=" * 80 + "\n")
        if result.stderr:
            f.write("STDERR:\n")
            f.write(result.stderr)
            f.write("\n" + "=" * 80 + "\n")

    # Log the result
    if success:
        logger.success(f"{operation_type} operation completed successfully")
        logger.info(f"Complete TPT output saved to: {combined_log_file}")
    else:
        logger.error(
            f"{operation_type} operation failed with return code {result.returncode}"
        )
        logger.error(f"Error details saved to: {combined_log_file}")

    # Parse metrics if it's a load operation
    if operation_type.lower() == "load" and result.stdout:
        metrics = parse_tpt_metrics(result.stdout)
        if metrics["rows_sent"] is not None:
            logger.info(f"Rows sent to RDBMS: {metrics['rows_sent']:,}")
        if metrics["rows_applied"] is not None:
            logger.info(f"Rows applied: {metrics['rows_applied']:,}")

    # Log errors if any
    if result.stderr:
        logger.warning(f"TPT stderr output: {result.stderr}")

    # Log full output to debug level (for troubleshooting)
    if result.stdout:
        logger.debug(f"TPT stdout: {result.stdout}")

    return success


def load_table(
    table_name: str,
    csv_file_path: str,
) -> bool:
    """Load a single CSV file to a table using TPT."""
    from .templates import create_tpt_files

    logger.info(f"Starting table load process: {csv_file_path} -> {table_name}")

    # Create TPT files
    jvar_file, drop_file, create_file, load_file = create_tpt_files(
        table_name, csv_file_path
    )

    # Step 1: Drop table
    logger.info(f"Step 1/3: Dropping table {table_name}")
    drop_success = run_tbuild(jvar_file, drop_file, "drop")

    if not drop_success:
        logger.error(f"Failed to drop table {table_name}")
        return False

    # Step 2: Create table
    logger.info(f"Step 2/3: Creating table {table_name}")
    create_success = run_tbuild(jvar_file, create_file, "create")

    if not create_success:
        logger.error(f"Failed to create table {table_name}")
        return False

    # Step 3: Load data
    logger.info(f"Step 3/3: Loading data into {table_name}")
    load_success = run_tbuild(jvar_file, load_file, "load")

    if load_success:
        logger.success(f"Successfully completed table load: {table_name}")
    else:
        logger.error(f"Failed to load data to {table_name}")

    return load_success
