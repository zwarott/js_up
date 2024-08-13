import os
import subprocess


def list_shp(shp_dir):
    """
    Lists all shapefiles in the given directory.

    Parameters
    ----------
    shp_dir : str
        The path to the directory containing shapefiles.

    Returns
    -------
    list of str
        A list of shapefile paths.
    """
    return [
        os.path.join(shp_dir, filename)
        for filename in os.listdir(shp_dir)
        if filename.endswith(".shp")
    ]


def import_shp_dir(shp_dir, kart_repo):
    """
    Imports shapefiles into a KART working copy.

    Parameters
    ----------
    shp_dir : str
        The path to the directory containing shapefiles.
    repo_dir : str
        The path to the KART repository.

    Returns
    -------
    None
    """
    # Save the current working directory
    original_cwd = os.getcwd()

    try:
        # Change the working directory to the KART repository
        os.chdir(kart_repo)

        # Import each shapefile into KART working copy
        for shp in list_shp(shp_dir):
            try:
                result = subprocess.run(
                    ["kart", "import", shp],
                    capture_output=True,
                    text=True,
                )
                if result.returncode == 0:
                    print(f"✅ Successfully imported {shp}")
                else:
                    print(f"❌ Failed to import {shp}")
                    print(result.stderr)
            except Exception as e:
                print(f"❗️ Error importing {shp}: {e}")
    finally:
        # Restore the original working directory
        os.chdir(original_cwd)
