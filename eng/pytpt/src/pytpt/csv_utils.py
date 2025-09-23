"""Simple CSV discovery functions."""

from pathlib import Path
from hydra import compose, initialize_config_dir


def load_config():
    """Load configuration using Hydra."""
    config_dir = Path("conf").absolute()
    with initialize_config_dir(config_dir=str(config_dir), version_base=None):
        cfg = compose(config_name="config")
    return cfg


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
