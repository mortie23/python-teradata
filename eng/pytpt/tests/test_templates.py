"""Tests for templates module."""

import tempfile
from pathlib import Path

from pytpt.templates import (
    load_env_vars,
    get_credentials,
    render_template,
    write_file,
    create_tpt_files,
)


def test_load_env_vars():
    """Test load_env_vars function."""
    # Should not raise an exception
    load_env_vars()


def test_get_credentials():
    """Test get_credentials function."""
    credentials = get_credentials()

    # Check all required keys are present
    required_keys = [
        "ddl_username",
        "ddl_password",
        "target_username",
        "target_password",
        "ddl_host",
        "target_host",
        "ddl_logon_mech",
        "target_logon_mech",
        "working_database",
    ]

    for key in required_keys:
        assert key in credentials
        assert isinstance(credentials[key], str)


def test_render_template():
    """Test render_template function."""
    # Create a simple test template
    template_content = "Hello {{name}}, your value is {{value}}!"

    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(template_content)
        template_path = Path(f.name)

    try:
        result = render_template(template_path, name="World", value=42)
        assert result == "Hello World, your value is 42!"
    finally:
        template_path.unlink()


def test_write_file():
    """Test write_file function."""
    content = "Test file content"

    with tempfile.TemporaryDirectory() as temp_dir:
        output_path = Path(temp_dir) / "subdir" / "test.txt"

        write_file(content, output_path)

        assert output_path.exists()
        assert output_path.read_text() == content


def test_create_tpt_files():
    """Test create_tpt_files function."""
    table_name = "TEST_TABLE"
    csv_file_path = "/path/to/test.csv"

    try:
        jvar_file, tpt_file = create_tpt_files(table_name, csv_file_path)

        # Check files were created
        assert jvar_file.exists()
        assert tpt_file.exists()

        # Check file names
        assert jvar_file.name == f"{table_name}.jvar"
        assert tpt_file.name == f"{table_name}.tpt"

        # Check content contains expected values
        jvar_content = jvar_file.read_text()
        assert table_name in jvar_content
        assert csv_file_path in jvar_content

        tpt_content = tpt_file.read_text()
        assert table_name in tpt_content

    finally:
        # Cleanup
        if "jvar_file" in locals() and jvar_file.exists():
            jvar_file.unlink()
        if "tpt_file" in locals() and tpt_file.exists():
            tpt_file.unlink()
