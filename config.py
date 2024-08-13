# config.py

from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()


def get_env_variable(name: str, default: str | None = None) -> str:
    """Get an environment variable or raise an error if not found and no default is provided."""
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(
            f"Required environment variable '{name}' not set and no default value provided."
        )
    return value


def get_env_int(name: str, default: int | None = None) -> int:
    """Get an environment variable as an integer or raise an error if not found or not an integer."""
    value = get_env_variable(name, default=str(default))
    try:
        return int(value)
    except ValueError:
        raise ValueError(
            f"Environment variable '{name}' must be an integer, but got '{value}'."
        )


# File with municipality names and codes
MUNICIPALITIES = get_env_variable("MUNICIPALITIES")

# Define the path were spatial plans are stored
DEFAULT_REPO = get_env_variable("DEFAULT_REPO")

# Define the path where to run the `kart` command
KART_REPO = get_env_variable("KART_REPO")

# Define the path to your GeoPackage and the output directory
WORKING_COPY = get_env_variable("WORKING_COPY")

# Define the path to your output Data directory
OUTPUT_DATA_DIR = get_env_variable("OUTPUT_DATA_DIR")

# Define the path to maps directory
OUTPUT_LAYOUT_DIR = get_env_variable("OUTPUT_LAYOUT_DIR")

# Define code of desired municipality code
MUN_CODE = get_env_int("MUN_CODE")

# 0 for new spatial plan, 1 for change
NEW_OR_CHANGE = get_env_int("NEW_OR_CHANGE")

# Number of spatial plan change (when NEW_OR_CHANGE = 1 only)
CHANGE_NUMBER = get_env_int("CHANGE_NUMBER")

# Define the path to input GeoPackage for importing data to working directory
GPKG_TO_IMPORT = get_env_variable("GPKG_TO_IMPORT")

# Define the path to directory with input shapefiles
SHP_DIR_TO_IMPORT = get_env_variable("SHP_DIR_TO_IMPORT")

# Define ESRI Shapefile encoding (*.cpg)
ENCODING = get_env_variable("ENCODING")
