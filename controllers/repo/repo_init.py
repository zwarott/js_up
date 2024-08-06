import os
import subprocess
from unidecode import unidecode
import pandas as pd


def normalize_mun_name(mun_name: str) -> str:
    """
    Normalize municipality name to lowercase and replace special characters.
    Czech characters such as ě, š, č, ř, ž, ý, á, í, é, ú, ů are replaced
    as well.

    Parameters
    ----------
    mun_name: str
        Municipality name to be normalized.

    Returns
    -------
    str
        Normalized municipality name.
    """
    return unidecode(mun_name).replace(" ", "_").lower()


def init_with_import(
    default_repo: str,
    municipalities_csv: str,
    mun_code: int,
    new_or_change: int,
    change_number: int,
    gpkg_to_import: str,
) -> None:
    """
    Initialize a Kart repository with the given parameters and import data
    from GeoPackage into the working directory.

    Parameters
    ----------
    default_repo : str
        The default repository path with all spatial plans.
    municipalities_csv : str
        The path to the municipalities CSV file.
    mun_code : int
        The municipality code.
    new_or_change : int
        Indicator for new spatial plan (0) or change (1).
    change_number : int
        The change number (used if new_or_change is 1).
    gpkg_to_import : str
        The GeoPackage file to import.

    Returns
    -------
    None
    """
    try:
        # Load the municipalities CSV file
        df = pd.read_csv(municipalities_csv)

        # Validate MUN_CODE and get corresponding MUN_NAME
        if mun_code not in df["mun_code"].values:
            print("❗️ Input municipality code is not valid.")
            return
        else:
            # Extract municipality name from mun_name attribute and normalize it
            mun_name = df.loc[df["mun_code"] == mun_code, "mun_name"].values[0]
            mun_name = normalize_mun_name(mun_name)
            print(f"💡 Normalized municipality name: {mun_name}")

            # Repo name for new spatial plan
            if new_or_change == 0:
                spatial_plan = f"up_{mun_name}"
            # Repo name for change of the spatial plan
            else:
                spatial_plan = f"zmena_c{change_number}_up_{mun_name}"

            # Create the full path for the spatial plan repository
            spatial_plan_path = os.path.join(default_repo, spatial_plan)
            print(f"💡 Spatial plan path: {spatial_plan_path}")

            # Initialize the Kart repository
            init_command = (
                f"kart init {spatial_plan_path} --import GPKG:{gpkg_to_import}"
            )
            print(f"💡 Running command: {init_command}")
            subprocess.run(init_command, shell=True, check=True)

            # Create the folder structure with uppercase main folder and capitalized subfolders
            if new_or_change == 0:
                main_folder = f"DUP_{mun_code}"
            else:
                main_folder = f"DUP_{mun_code}_Z{change_number}"

            # Create output main folder
            main_folder_path = os.path.join(spatial_plan_path, main_folder)
            os.makedirs(main_folder_path, exist_ok=True)

            # Create output subfolders
            subfolders = ["Data", "Texty", "Vykresy"]
            for subfolder in subfolders:
                os.makedirs(os.path.join(main_folder_path, subfolder), exist_ok=True)

            print(
                f"✅ Repository {spatial_plan} created successfully with the required structure."
            )

    except ImportError as e:
        print(f"❗️ ImportError: {e}")
    except subprocess.CalledProcessError as e:
        print(f"❗️ Error during repository initialization: {e}")
    except Exception as e:
        print(f"❗️ An unexpected error occurred: {e}")
