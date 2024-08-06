import os
from osgeo import ogr
import warnings

warnings.filterwarnings("ignore", category=FutureWarning, message=".*exceptions.*")


def get_cpg_encoding(cpg_file):
    """
    Reads the character encoding from a .cpg file.

    Parameters
    ----------
    cpg_file : str
        The path to the .cpg file.

    Returns
    -------
    str
        The encoding specified in the .cpg file. Returns 'Not specified' if the
        encoding cannot be read.

    Warnings
    --------
    Prints a warning message if unable to read the .cpg file.
    """
    try:
        with open(cpg_file, "r") as f:
            encoding = f.read().strip()
            return encoding
    except Exception as e:
        print(f"  Warning: Unable to read encoding from CPG file: {e}")
        return "Not specified"


def shp_overview(data_dir):
    """
    Prints an overview of all shapefiles in a directory, including EPSG code,
    encoding, feature count, and attributes.

    Parameters
    ----------
    data_dir : str
        The path to the directory containing shapefiles.

    Warnings
    --------
    Prints warning messages if unable to open a shapefile or read its details.

    Notes
    -----
    This function reads the encoding from .cpg files associated with the shapefiles.
    """
    for filename in os.listdir(data_dir):
        if filename.endswith(".shp"):
            filepath = os.path.join(data_dir, filename)
            try:
                datasource = ogr.Open(filepath)
                if datasource is None:
                    print(f"Failed to open {filename}")
                    continue

                layer = datasource.GetLayer()
                layer_defn = layer.GetLayerDefn()
                srs = layer.GetSpatialRef()

                # Get EPSG code
                epsg_code = "Unknown"
                if srs is not None:
                    srs.AutoIdentifyEPSG()
                    epsg_code = srs.GetAuthorityCode(None)
                    if epsg_code is None:
                        epsg_code = "Unknown"

                # Get encoding by reading the CPG file
                cpg_filename = os.path.splitext(filepath)[0] + ".cpg"
                encoding = get_cpg_encoding(cpg_filename)

                print(f" ⭐️ {filename}")
                print(f"  💡 EPSG: {epsg_code}")
                print(f"  💡 Encoding: {encoding}")
                print(f"  💡 Feature Count: {layer.GetFeatureCount()}")
                print("  💡 Attributes:")

                for i in range(layer_defn.GetFieldCount()):
                    field_defn = layer_defn.GetFieldDefn(i)
                    print(
                        f"     - {field_defn.GetName()} (Type: {field_defn.GetFieldTypeName(field_defn.GetType())})"
                    )

                print()
            except Exception as e:
                print(f"Error processing {filename}: {e}")
