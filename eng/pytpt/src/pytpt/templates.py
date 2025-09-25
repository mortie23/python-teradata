"""Simple template processing functions."""

import os
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv
from .config_utils import load_config


def load_env_vars():
    """Load environment variables from .env file."""
    load_dotenv()


def get_credentials():
    """Get credentials from environment variables and config."""
    config = load_config()

    return {
        "ddl_username": os.getenv("DDL_USERNAME", "mortch"),
        "ddl_password": os.getenv("DDL_PASSWORD", ""),
        "target_username": os.getenv("TARGET_USERNAME", "mortch"),
        "target_password": os.getenv("TARGET_PASSWORD", ""),
        "ddl_host": config.database.ddl_host,
        "target_host": config.database.target_host,
        "ddl_logon_mech": config.database.ddl_logmech,
        "target_logon_mech": config.database.target_logmech,
        "working_database": config.database.working_database,
    }


def render_template(
    template_path: Path,
    **kwargs,
) -> str:
    """Render a Jinja template with provided variables."""
    with open(template_path, "r") as f:
        template_content = f.read()

    template = Template(template_content)
    return template.render(**kwargs)


def write_file(
    content: str,
    output_path: Path,
) -> None:
    """Write content to a file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(content)


def read_ddl_file(table_name: str) -> str:
    """Read DDL content for a table."""
    ddl_path = Path("ddl") / f"{table_name.lower()}.sql"
    if ddl_path.exists():
        with open(ddl_path, "r") as f:
            return f.read().strip()
    return ""


def create_tpt_files(
    table_name: str,
    csv_file_path: str,
) -> tuple[Path, Path, Path, Path]:
    """Create TPT jobvars and script files for create and load jobs."""
    # Get template paths
    scripts_dir = Path("scripts")
    jobvars_template = scripts_dir / "jobvars-template.jvar"
    create_template = scripts_dir / "create-table.tpt"
    load_template = scripts_dir / "load-table.tpt"

    # Get credentials
    credentials = get_credentials()

    # Read DDL for the table
    ddl_content = read_ddl_file(table_name)

    # Template variables
    template_vars = {
        **credentials,
        "table_name": table_name,
        "csv_file_path": csv_file_path,
        "ddl_content": ddl_content,
    }

    # Render templates
    jobvars_content = render_template(jobvars_template, **template_vars)
    create_content = render_template(create_template, **template_vars)
    load_content = render_template(load_template, **template_vars)

    # Output paths (in .gitignore directory)
    output_dir = Path(".gitignore")
    jobvars_output = output_dir / f"{table_name}.jvar"
    create_output = output_dir / f"{table_name}_create.tpt"
    load_output = output_dir / f"{table_name}_load.tpt"

    # Write files
    write_file(jobvars_content, jobvars_output)
    write_file(create_content, create_output)
    write_file(load_content, load_output)

    return jobvars_output, create_output, load_output
