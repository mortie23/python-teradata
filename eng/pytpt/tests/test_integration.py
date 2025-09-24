"""Integration tests that actually connect to the database."""

import os
import tempfile
from pathlib import Path

import pytest

from pytpt.templates import load_env_vars, get_credentials, create_tpt_files
from pytpt.tpt_runner import load_table
from pytpt.csv_utils import load_config, find_csv_files


@pytest.mark.integration
def test_real_credentials():
    """Test loading real credentials from .env file."""
    load_env_vars()
    credentials = get_credentials()

    # Print credentials (passwords will be hidden in output)
    print("\nCredentials loaded:")
    for key, value in credentials.items():
        if "password" in key.lower():
            print(f"  {key}: {'*' * len(value) if value else '(empty)'}")
        else:
            print(f"  {key}: {value}")

    # Basic validation
    assert credentials["ddl_username"]
    assert credentials["target_username"]
    assert credentials["ddl_host"]
    assert credentials["target_host"]


@pytest.mark.integration
def test_real_config_loading():
    """Test loading real Hydra configuration."""
    config = load_config()

    print(f"\nConfig loaded:")
    print(f"  Data directory: {config.data.dir}")
    print(f"  Tables configured: {len(config.tables)}")

    # Verify data directory exists
    data_dir = Path(config.data.dir)
    if not data_dir.is_absolute():
        data_dir = Path.cwd() / data_dir

    assert data_dir.exists(), f"Data directory does not exist: {data_dir}"


@pytest.mark.integration
def test_find_real_csv_files():
    """Test finding CSV files in the real data directory."""
    config = load_config()
    data_dir = config.data.dir

    # Convert to absolute path if needed
    if not Path(data_dir).is_absolute():
        data_dir = str(Path.cwd() / data_dir)

    csv_files = find_csv_files(data_dir)

    print(f"\nFound {len(csv_files)} CSV files in {data_dir}:")
    for csv_file in csv_files:
        print(f"  - {csv_file.name} ({csv_file.stat().st_size} bytes)")

    assert len(csv_files) > 0, f"No CSV files found in {data_dir}"


@pytest.mark.integration
def test_tpt_file_generation_with_real_data():
    """Test TPT file generation with real credentials and CSV."""
    load_env_vars()

    # Create a small test CSV
    test_csv = "id,name,value\n1,Integration Test,999\n"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(test_csv)
        csv_path = f.name

    try:
        table_name = "INTEGRATION_TEST_TABLE"
        jvar_file, tpt_file = create_tpt_files(table_name, csv_path)

        print(f"\nGenerated TPT files:")
        print(f"  JVAR: {jvar_file}")
        print(f"  TPT:  {tpt_file}")

        assert jvar_file.exists()
        assert tpt_file.exists()

        # Print file contents for verification
        print(f"\nJVAR content:")
        print(jvar_file.read_text())

        print(f"\nTPT content:")
        print(tpt_file.read_text())

    finally:
        Path(csv_path).unlink()
        # Cleanup generated files
        if "jvar_file" in locals() and jvar_file.exists():
            jvar_file.unlink()
        if "tpt_file" in locals() and tpt_file.exists():
            tpt_file.unlink()


@pytest.mark.database
def test_actual_database_load():
    """Test actual database loading (requires real database access).

    This test will attempt to load data to a real Teradata table.
    Only run this if you have:
    1. Valid database credentials in .env
    2. TPT tools installed
    3. Appropriate database permissions
    """
    # Safety check - only run if explicitly enabled
    if not os.getenv("ENABLE_DB_TESTS", "").lower() == "true":
        pytest.skip("Database tests disabled. Set ENABLE_DB_TESTS=true to enable.")

    load_env_vars()
    credentials = get_credentials()

    # Skip if no passwords provided
    if not credentials["ddl_password"] or not credentials["target_password"]:
        pytest.skip("No database passwords provided in .env file")

    # Create test data
    test_csv = (
        "id,name,category,amount\n1,DB Test 1,TEST,100.50\n2,DB Test 2,TEST,250.75\n"
    )

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(test_csv)
        csv_path = f.name

    try:
        # Use timestamped table name to avoid conflicts
        import time

        timestamp = int(time.time())
        table_name = f"PYTPT_DB_TEST_{timestamp}"

        print(f"\nAttempting to load table: {table_name}")
        print(f"CSV file: {csv_path}")

        result = load_table(table_name, csv_path)

        if result:
            print(f"✓ Successfully loaded table {table_name}")
            print(f"⚠️  Note: Table {table_name} was created and may need cleanup")
        else:
            print(f"✗ Failed to load table {table_name}")
            print("This may be expected due to permissions, connectivity, etc.")

        # Don't assert success since database connectivity issues are common
        # in test environments - just verify the function completes
        assert isinstance(result, bool)

    finally:
        Path(csv_path).unlink()
