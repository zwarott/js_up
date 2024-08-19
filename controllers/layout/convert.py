import os
from osgeo import gdal


def raster_to_24bit(raster_dir: str) -> None:
    """
    Convert raster files in a folder to 24-bit depth by excluding the alpha channel.

    Parameters
    ----------
    raster_dir : str
        Path to the folder containing the raster files.

    Returns
    -------
    None
    """
    # Ensure the folder exists
    if not os.path.isdir(raster_dir):
        print(f"Folder does not exist: {raster_dir}")
        return

    # Create a temporary directory for intermediate files
    temp_dir = os.path.join(raster_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # Supported raster file extensions
    raster_extensions = (".png", ".tif", ".bmp")

    # Process each raster file in the folder
    raster_files = [f for f in os.listdir(raster_dir) if f.endswith(raster_extensions)]

    if not raster_files:
        print("No PNG, TIF, or BMP files found in the folder.")
        return

    for raster_file in raster_files:
        raster_file_path = os.path.join(raster_dir, raster_file)
        temp_file_path = os.path.join(temp_dir, raster_file)

        # Convert raster file to 24-bit depth by excluding the alpha channel
        print(f"Converting {raster_file_path} to 24-bit depth...")

        try:
            result = gdal.Translate(
                temp_file_path,
                raster_file_path,
                bandList=[1, 2, 3],
                outputType=gdal.GDT_Byte,
                outputSRS="EPSG:5514",
            )

            # Check if the conversion was successful
            if result is not None:
                print(f"Successfully converted {raster_file_path} to {temp_file_path}")
                os.replace(temp_file_path, raster_file_path)
            else:
                print(f"Failed to convert {raster_file_path}")
                if os.path.exists(temp_file_path):
                    os.remove(
                        temp_file_path
                    )  # Remove the temporary file if conversion failed
        except Exception as e:
            print(f"An error occurred during conversion of {raster_file_path}: {e}")
            if os.path.exists(temp_file_path):
                os.remove(
                    temp_file_path
                )  # Remove the temporary file if conversion failed

    # Clean up the temporary directory
    try:
        os.rmdir(temp_dir)
    except OSError:
        pass

    print("Conversion process completed.")
