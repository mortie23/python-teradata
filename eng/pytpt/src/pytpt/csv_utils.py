"""Simple CSV discovery functions."""

from pathlib import Path
from .config_utils import load_config as _load_config


def load_config():
    """Load configuration using Hydra."""
    return _load_config()


def find_csv_files(
    data_dir: str,
) -> list[Path]:
    """Find all CSV files in data directory."""
    data_path = Path(data_dir)
    return list(data_path.glob("*.csv"))


def get_table_mapping():
    """Get CSV to table name mapping from config."""
    cfg = load_config()
    return dict(cfg.tables)


def match_csv_to_table(
    csv_file: Path,
    table_mapping: dict,
) -> str:
    """Match CSV filename to table name."""
    csv_name = csv_file.stem  # filename without extension
    return table_mapping.get(csv_name, csv_name.upper())
