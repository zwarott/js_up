import os
from osgeo import gdal
import warnings

# Suppress GDAL warning about future exceptions
warnings.filterwarnings("ignore", category=FutureWarning, message=".*exceptions.*")


def is_24bit_raster(raster_path: str) -> bool:
    """
    Check if a raster is 24-bit.

    Parameters
    ----------
    raster_path : str
        The path to the raster file.

    Returns
    -------
    bool
        True if the raster is 24-bit, False otherwise.
    """
    try:
        dataset = gdal.Open(raster_path)
        if dataset is None:
            print(f"Could not open {raster_path}")
            return False

        # Check if the raster has 3 bands
        if dataset.RasterCount != 3:
            return False

        # Check if each band is 8 bits (Byte data type)
        for i in range(1, 4):  # Bands are 1-based in GDAL
            band = dataset.GetRasterBand(i)
            if band.DataType != gdal.GDT_Byte:
                return False

        return True

    except Exception as e:
        print(f"Error checking raster {raster_path}: {e}")
        return False


def check_24bit_depth(target_dir: str) -> None:
    """
    Check if all rasters in a target directory are 24-bit.

    Parameters
    ----------
    directory : str
        The path to the target directory.

    Returns
    -------
    list
        A list of tuples containing the file name and a boolean indicating if it's 24-bit.
    """
    results = []
    for filename in os.listdir(target_dir):
        if filename.lower().endswith((".tif", ".tiff", ".png", ".bmp")):
            file_path = os.path.join(target_dir, filename)
            is_24bit = is_24bit_raster(file_path)
            results.append((filename, is_24bit))

    for filename, is_24bit in results:
        status = "is 24-bit" if is_24bit else "is not 24-bit"
        print(f"{filename}: {status}")
