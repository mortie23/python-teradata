"""Simple template processing functions."""

import os
from pathlib import Path
from jinja2 import Template
from dotenv import load_dotenv


def load_env_vars():
    """Load environment variables from .env file."""
    load_dotenv()


def get_credentials():
    """Get credentials from environment variables."""
    return {
        "ddl_username": os.getenv("DDL_USERNAME", "mortch"),
        "ddl_password": os.getenv("DDL_PASSWORD", ""),
        "target_username": os.getenv("TARGET_USERNAME", "mortch"),
        "target_password": os.getenv("TARGET_PASSWORD", ""),
        "ddl_host": os.getenv("DDL_HOST", "tdvm"),
        "target_host": os.getenv("TARGET_HOST", "terprddb.edw.health"),
        "ddl_logon_mech": os.getenv("DDL_LOGON_MECH", "LDAP"),
        "target_logon_mech": os.getenv("TARGET_LOGON_MECH", "LDAP"),
        "working_database": os.getenv("WORKING_DATABASE", "python_db"),
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


def create_tpt_files(
    table_name: str,
    csv_file_path: str,
) -> tuple[Path, Path]:
    """Create TPT jobvars and script files for a table."""
    # Get template paths
    scripts_dir = Path("scripts")
    jobvars_template = scripts_dir / "jobvars-template.jvar"
    tpt_template = scripts_dir / "load-table.tpt"

    # Get credentials
    credentials = get_credentials()

    # Template variables
    template_vars = {
        **credentials,
        "table_name": table_name,
        "csv_file_path": csv_file_path,
    }

    # Render templates
    jobvars_content = render_template(jobvars_template, **template_vars)
    tpt_content = render_template(tpt_template, **template_vars)

    # Output paths (in .gitignore directory)
    output_dir = Path(".gitignore")
    jobvars_output = output_dir / f"{table_name}.jvar"
    tpt_output = output_dir / f"{table_name}.tpt"

    # Write files
    write_file(jobvars_content, jobvars_output)
    write_file(tpt_content, tpt_output)

    return jobvars_output, tpt_output
