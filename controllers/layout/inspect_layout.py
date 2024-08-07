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
            print(f"❗️ Could not open {raster_path}")
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
        print(f"❗️ Error checking raster {raster_path}: {e}")
        return False


def check_24bit_depth(raster_dir: str) -> None:
    """
    Check if all rasters in a raster directory are 24-bit.

    Parameters
    ----------
    raster_dir : str
        The path to the raster directory.

    Returns
    -------
    None
    """
    raster_files = [
        f
        for f in os.listdir(raster_dir)
        if f.lower().endswith((".tif", ".tiff", ".png", ".bmp"))
    ]

    if not raster_files:
        print(f"❗️ No raster files found in the directory '{raster_dir}'.")
        return

    results = [
        (filename, is_24bit_raster(os.path.join(raster_dir, filename)))
        for filename in raster_files
    ]

    for filename, is_24bit in results:
        status = "✅ is 24-bit" if is_24bit else "❌ is not 24-bit"
        print(f"{filename}: {status}")
