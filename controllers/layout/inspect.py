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


def check_dpi(raster_dir):
    """
    Check the DPI (resolution) of all raster files in the specified directory using GDAL.

    Parameters:
    -----------
    raster_dir : str
        Path to the directory containing raster files.
    """
    supported_formats = (".png", ".tif", ".tiff", ".bmp")

    if not os.path.exists(raster_dir):
        print(f"Directory '{raster_dir}' does not exist.")
        return

    print(f"Checking DPI for raster files in directory: {raster_dir}\n")

    for file_name in os.listdir(raster_dir):
        file_path = os.path.join(raster_dir, file_name)

        if os.path.isfile(file_path) and file_name.lower().endswith(supported_formats):
            try:
                dataset = gdal.Open(file_path)
                if dataset is None:
                    print(f"Unable to open '{file_name}'. Skipping.")
                    continue

                metadata = dataset.GetMetadata()
                x_dpi = metadata.get("TIFFTAG_XRESOLUTION")
                y_dpi = metadata.get("TIFFTAG_YRESOLUTION")

                print(f"File: {file_name}")
                if x_dpi and y_dpi:
                    print(f" - DPI: {x_dpi} x {y_dpi}")
                else:
                    print(" - DPI information not available in metadata.")

            except Exception as e:
                print(f"Error processing '{file_name}': {e}")
        else:
            print(f"Skipped: {file_name} (not a supported raster format)")
