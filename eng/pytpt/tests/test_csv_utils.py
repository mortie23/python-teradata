"""Tests for csv_utils module."""

import tempfile
from pathlib import Path

from pytpt.csv_utils import (
    load_config,
    find_csv_files,
    get_table_mapping,
    match_csv_to_table,
)


def test_load_config():
    """Test load_config function."""
    config = load_config()

    # Check config has expected attributes
    assert hasattr(config, "data")
    assert hasattr(config, "tables")
    assert hasattr(config.data, "dir")


def test_find_csv_files():
    """Test find_csv_files function."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test CSV files
        csv_files = ["game.csv", "player.csv", "team.csv"]
        for filename in csv_files:
            (Path(temp_dir) / filename).write_text("test,data\n1,2")

        # Create non-CSV file
        (Path(temp_dir) / "readme.txt").write_text("not a csv")

        result = find_csv_files(temp_dir)

        # Should find only CSV files
        assert len(result) == 3
        result_names = {f.name for f in result}
        assert result_names == set(csv_files)


def test_find_csv_files_empty_directory():
    """Test find_csv_files with empty directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        result = find_csv_files(temp_dir)
        assert result == []


def test_get_table_mapping():
    """Test get_table_mapping function."""
    table_mapping = get_table_mapping()

    # Should return a dictionary
    assert isinstance(table_mapping, dict)

    # Should have some table mappings (from config)
    assert len(table_mapping) > 0


def test_match_csv_to_table():
    """Test match_csv_to_table function."""
    # Test with mapping that exists
    csv_file = Path("/path/to/game.csv")
    table_mapping = {"game": "GAME_TABLE", "player": "PLAYER_TABLE"}

    result = match_csv_to_table(csv_file, table_mapping)
    assert result == "GAME_TABLE"


def test_match_csv_to_table_not_in_mapping():
    """Test match_csv_to_table when CSV not in mapping."""
    csv_file = Path("/path/to/unknown.csv")
    table_mapping = {"game": "GAME_TABLE"}

    result = match_csv_to_table(csv_file, table_mapping)
    assert result == "UNKNOWN"  # Should return uppercase stem


def test_match_csv_to_table_with_real_config():
    """Test match_csv_to_table with real configuration."""
    table_mapping = get_table_mapping()

    # Test with a CSV that should be in the config
    if "game" in table_mapping:
        csv_file = Path("/path/to/game.csv")
        result = match_csv_to_table(csv_file, table_mapping)
        assert result == table_mapping["game"]
