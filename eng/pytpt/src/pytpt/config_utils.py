"""Configuration utilities."""

from pathlib import Path
from hydra import compose, initialize_config_dir


def load_config():
    """Load configuration using Hydra."""
    config_dir = Path("conf").absolute()
    with initialize_config_dir(config_dir=str(config_dir), version_base=None):
        cfg = compose(config_name="config")
    return cfg
