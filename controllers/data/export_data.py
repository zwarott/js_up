import os
import subprocess
from osgeo import ogr


def export_working_dir(
    gpkg_path: str,
    output_dir: str,
    working_dir: str,
    exclude_layers: list,
    include_layers: list,
    export_empty_layers: bool,
) -> None:
    """
    Export specified layers from a GeoPackage to shapefiles in a specified output directory.

    Parameters
    ----------
    gpkg_path : str
        Path to the input GeoPackage file.
    output_dir : str
        Path to the directory where the shapefiles will be saved.
    working_dir_path : str
        Path to the Kart repository directory.
    exclude_layers : list
        List of layer names to exclude from export.
    include_layers : list
        List of layer names to explicitly include in export.
    export_empty_layers : bool
        Whether to export empty layers (True or False).

    Returns
    -------
    None
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Verify the GeoPackage file exists
    if not os.path.isfile(gpkg_path):
        print(f"GeoPackage file not found: {gpkg_path}")
        exit(1)

    # Print the full path of the GeoPackage
    print(f"GeoPackage full path: {os.path.abspath(gpkg_path)}")

    # Print the contents of the directory containing the GeoPackage
    print(f"Contents of {os.path.dirname(gpkg_path)}:")
    print(os.listdir(os.path.dirname(gpkg_path)))

    # List all layers in the GeoPackage using Kart versioning
    try:
        result = subprocess.run(
            ["kart", "data", "ls"],
            capture_output=True,
            text=True,
            check=True,
            cwd=working_dir,
        )
        layers = result.stdout.strip().split()
    except subprocess.CalledProcessError as e:
        print("Failed to list layers in the GeoPackage.")
        print(e)
        exit(1)

    if not layers:
        print("No layers found in the GeoPackage.")
        exit(1)

    # Print each layer on a new line using unpacking
    print("Found layers:")
    print(*layers, sep="\n")

    # Set GDAL to use exceptions
    ogr.UseExceptions()

    # Open the GeoPackage
    gpkg_ds = ogr.Open(gpkg_path)
    if gpkg_ds is None:
        print(f"Failed to open GeoPackage: {gpkg_path}")
        exit(1)

    # Iterate through each layer
    for layer_name in layers:
        # Check if the layer is in the exclude list
        if layer_name not in exclude_layers:
            # Check if the layer is in the include list or starts with "X"
            if layer_name in include_layers or layer_name.startswith("X"):
                # Get the layer
                layer = gpkg_ds.GetLayerByName(layer_name)
                if layer is None:
                    print(f"Layer {layer_name} not found in GeoPackage.")
                    continue

                # Check if the layer is empty
                if layer.GetFeatureCount() == 0 and not export_empty_layers:
                    print(f"Skipping empty layer: {layer_name}")
                    continue

                # Export the layer to a shapefile with UTF-8 encoding
                shapefile_path = os.path.join(output_dir, f"{layer_name}.shp")
                print(f"Exporting layer: {layer_name} to {shapefile_path}")

                driver = ogr.GetDriverByName("ESRI Shapefile")
                if driver is None:
                    print("ESRI Shapefile driver is not available.")
                    exit(1)

                # Create the output shapefile
                if os.path.exists(shapefile_path):
                    driver.DeleteDataSource(shapefile_path)
                out_ds = driver.CreateDataSource(shapefile_path)
                if out_ds is None:
                    print(f"Failed to create shapefile: {shapefile_path}")
                    continue

                out_layer = out_ds.CreateLayer(
                    layer_name, srs=layer.GetSpatialRef(), geom_type=layer.GetGeomType()
                )
                if out_layer is None:
                    print(f"Failed to create layer: {layer_name} in shapefile.")
                    continue

                # Copy the layer's fields
                layer_defn = layer.GetLayerDefn()
                for i in range(layer_defn.GetFieldCount()):
                    field_defn = layer_defn.GetFieldDefn(i)
                    out_layer.CreateField(field_defn)

                # Copy the features
                for feature in layer:
                    out_layer.CreateFeature(feature)

                # Close the output shapefile
                out_ds = None
                print(f"Successfully exported {layer_name} to {shapefile_path}")
            else:
                print(f"Skipping layer: {layer_name}")
        else:
            print(f"Skipping layer: {layer_name}")

    print("Export completed.")
