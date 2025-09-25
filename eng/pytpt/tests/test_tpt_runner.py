"""Tests for tpt_runner module."""

import tempfile
from pathlib import Path

from pytpt.tpt_runner import run_tbuild, load_table


def test_run_tbuild_with_invalid_files():
    """Test run_tbuild with non-existent files (should return False)."""
    jvar_file = Path("/nonexistent/file.jvar")
    tpt_file = Path("/nonexistent/file.tpt")

    result = run_tbuild(jvar_file, tpt_file)
    assert result is False


def test_run_tbuild_with_valid_files():
    """Test run_tbuild with actual files (may fail but shouldn't crash)."""
    # Create temporary files with valid content
    jvar_content = """DDLTdpId='test'
, DDLUserName='test'
, DDLUserPassword='test'"""

    tpt_content = """DEFINE JOB test_job
DESCRIPTION 'Test job' (
  STEP test_step (
    APPLY ('select 1;')
    TO OPERATOR ($DDL);
  );
);"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jvar", delete=False) as jvar_f:
        jvar_f.write(jvar_content)
        jvar_file = Path(jvar_f.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".tpt", delete=False) as tpt_f:
        tpt_f.write(tpt_content)
        tpt_file = Path(tpt_f.name)

    try:
        # This will likely fail (no real database connection) but shouldn't crash
        result = run_tbuild(jvar_file, tpt_file)
        assert isinstance(result, bool)
    finally:
        jvar_file.unlink()
        tpt_file.unlink()


def test_load_table():
    """Test load_table function."""
    # Create a test CSV file
    csv_content = "id,name,value\n1,test1,100\n2,test2,200"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        csv_path = f.name

    try:
        table_name = "TEST_TABLE"

        # This will likely fail (no real database connection) but shouldn't crash
        result = load_table(table_name, csv_path)
        assert isinstance(result, bool)

        # Check that TPT files were created in render_tmp directory
        output_dir = Path("render_tmp")
        jvar_file = output_dir / f"{table_name}.jvar"
        tpt_file = output_dir / f"{table_name}.tpt"

        # Files should exist (created by create_tpt_files)
        assert jvar_file.exists()
        assert tpt_file.exists()

        # Check content
        jvar_content = jvar_file.read_text()
        assert table_name in jvar_content
        assert csv_path in jvar_content

        tpt_content = tpt_file.read_text()
        assert table_name in tpt_content

    finally:
        Path(csv_path).unlink()
        # Cleanup generated files if they exist
        output_dir = Path("render_tmp")
        for generated_file in [
            output_dir / f"{table_name}.jvar",
            output_dir / f"{table_name}.tpt",
        ]:
            if generated_file.exists():
                generated_file.unlink()


def test_load_table_creates_files():
    """Test that load_table creates the expected TPT files."""
    csv_content = "id,name\n1,test"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(csv_content)
        csv_path = f.name

    try:
        table_name = "FILE_CREATION_TEST"

        # Run load_table (may fail but should create files)
        load_table(table_name, csv_path)

        # Verify files were created
        output_dir = Path("render_tmp")
        jvar_file = output_dir / f"{table_name}.jvar"
        tpt_file = output_dir / f"{table_name}.tpt"

        assert jvar_file.exists(), f"Expected {jvar_file} to be created"
        assert tpt_file.exists(), f"Expected {tpt_file} to be created"

        # Verify file content structure
        jvar_content = jvar_file.read_text()
        assert "DDLTdpId=" in jvar_content
        assert "LoadTargetTable=" in jvar_content
        assert table_name in jvar_content

        tpt_content = tpt_file.read_text()
        assert "DEFINE JOB" in tpt_content
        assert table_name in tpt_content

    finally:
        Path(csv_path).unlink()
        # Cleanup
        output_dir = Path("render_tmp")
        for generated_file in [
            output_dir / f"{table_name}.jvar",
            output_dir / f"{table_name}.tpt",
        ]:
            if generated_file.exists():
                generated_file.unlink()
