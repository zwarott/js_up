import os
import subprocess
from osgeo import ogr
import warnings

# Suppress GDAL warning about future exceptions
warnings.filterwarnings("ignore", category=FutureWarning, message=".*exceptions.*")


def export_working_dir(
    gpkg_path: str,
    output_dir: str,
    working_dir: str,
    exclude_layers: list,
    include_layers: list,
    export_empty_layers: bool,
    encoding: str,
) -> None:
    """
    Export specified layers from a GeoPackage to ESRI Shapefiles
    in a specified output directory.

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
    encoding : str
        Specify ESRI Shapefile encoding.

    Returns
    -------
    None
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Verify the GeoPackage file exists
    if not os.path.isfile(gpkg_path):
        print(f"❗️ GeoPackage file not found: {gpkg_path}")
        exit(1)

    # Print the full path of the GeoPackage
    print(
        f"💡 GeoPackage full path: {os.path.abspath(gpkg_path)}",
        end="\n\n",
    )

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
        print("❌ Failed to list layers in the GeoPackage.")
        print(e)
        exit(1)

    if not layers:
        print("❗️ No layers found in the GeoPackage.")
        exit(1)

    # Print each layer on a new line using unpacking
    print(" 💡 Found layers:")
    print(*layers, sep="\n")
    print("")

    # Set GDAL to use exceptions
    ogr.UseExceptions()

    # Open the GeoPackage
    gpkg_ds = ogr.Open(gpkg_path)
    if gpkg_ds is None:
        print(f"❌ Failed to open GeoPackage: {gpkg_path}")
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
                    print(f"❗️ Layer {layer_name} not found in GeoPackage.")
                    continue

                # Check if the layer is empty
                if layer.GetFeatureCount() == 0 and not export_empty_layers:
                    print(f"❗️ Skipping empty layer: {layer_name}", end="\n\n")
                    continue

                print(f"⭐️ Exporting layer: {layer_name}")

                # Get the EPSG code of the layer's spatial reference system (SRS)
                srs = layer.GetSpatialRef()
                epsg_code = (
                    srs.GetAttrValue("AUTHORITY", 1) if srs is not None else "Unknown"
                )
                print(f"💡 EPSG: {epsg_code}")

                # Export the layer to a shapefile with specified encoding
                shapefile_path = os.path.join(output_dir, f"{layer_name}.shp")

                driver_name = "ESRI Shapefile"
                driver = ogr.GetDriverByName(driver_name)
                if driver is None:
                    print("❗️ ESRI Shapefile driver is not available.")
                    exit(1)
                else:
                    print(f"💡 Format: {driver_name}")
                # Create the output shapefile
                if os.path.exists(shapefile_path):
                    driver.DeleteDataSource(shapefile_path)
                out_ds = driver.CreateDataSource(shapefile_path)
                if out_ds is None:
                    print(f"❌ Failed to create shapefile: {shapefile_path}")
                    continue

                out_layer = out_ds.CreateLayer(
                    layer_name,
                    srs=srs,
                    geom_type=layer.GetGeomType(),
                    options=[f"ENCODING={encoding}"],
                )

                if out_layer is None:
                    print(f"❌ Failed to create layer: {layer_name} in shapefile.")
                    continue

                else:
                    print(f"💡 Encoding: {encoding}")
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
                print(
                    "✅ Successfully exported!",
                    end="\n\n",
                )
            else:
                print(f"❗️ Skipping layer: {layer_name}", end="\n\n")
        else:
            print(f"❗️ Skipping layer: {layer_name}", end="\n\n")

    print("✅ Export completed.")
