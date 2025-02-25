import os
from qgis.core import QgsProject, QgsMapLayer, QgsVectorFileWriter


def toc_to_shps(output_directory: str, encoding: str) -> None:
    """
    Export specified layers from a GeoPackage to ESRI Shapefiles
    to a specified output directory.

    Parameters
    ----------
    output_directory: str
        Path to the directory where the shapefiles will be saved.
    encoding : str
        Character encoding for the exported shapefiles.
    
    Returns
    -------
    None
    """
    # Check if the output directory exists; if not, attempt to create it
    try:
        if not os.path.exists(output_directory):
            print(f"Directory {output_directory} does not exist. Creating it...")
            os.makedirs(output_directory)
        elif not os.access(output_directory, os.W_OK):
            print(f"Error: Directory {output_directory} is not writable.")
            return

    except Exception as e:
        print(f"Error creating directory {output_directory}: {e}")
        return

    # Get the list of all layers in the TOC (Table of Contents)
    layers = list(QgsProject.instance().mapLayers().values())

    # Check if there are no layers in the TOC
    if not layers:
        print("No layers found in the TOC.")
    else:
        # Iterate over each layer
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer:  # Ensure it is a vector layer
                # Construct the file path for the shapefile
                layer_name = layer.name()
                output_path = os.path.join(output_directory, f"{layer_name}.shp")

                try:
                    # Set up the parameters for the export
                    result, error_message = QgsVectorFileWriter.writeAsVectorFormat(
                        layer,
                        output_path,
                        encoding,
                        driverName="ESRI Shapefile"
                    )

                    # Check if the export was successful
                    if result == QgsVectorFileWriter.NoError:
                        print(f"Layer {layer_name} exported successfully to {output_path}")
                    else:
                        print(f"Error exporting {layer_name}: {error_message} (Code: {result})")

                except Exception as e:
                    print(f"Exception occurred while exporting {layer_name}: {e}")

        print("Export completed!")

# Define the output directory and ecnoding
# MacOS path format: /path/to/output_directory
# Windows path format: H:/path/to/output_directory
# utf-8 x windows-1250
output_directory = "/Users/zwarott/Desktop/stazena_uap"
encoding = "windows-1250"

toc_to_shps(output_directory, encoding)