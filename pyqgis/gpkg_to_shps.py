import os
import logging
from osgeo import ogr
from datetime import datetime


def gpkg_to_shps(input_gpkg: str, output_directory: str, encoding: str) -> None:
    """
    Export specified layers from a GeoPackage to ESRI Shapefiles
    to a specified output directory with a specified encoding.

    Parameters
    ----------
    input_gpkg : str
        Path to the input GeoPackage file.
    output_directory : str
        Path to the directory where the shapefiles will be saved.
    encoding : str
        Character encoding for the exported shapefiles.
    
    Returns
    -------
    None
    """
    
    # Enhanced logging setup with timestamp, level, and message
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()]
    )

    # Constants for layers to include and exclude
    EXCLUDE_LAYERS = {"layer_styles", "qgis_projects"}
    INCLUDE_LAYERS = {
        "ReseneUzemi_p", "UzemiPrvkyRP_p", "ZastaveneUzemi_p", "ZastavitelneUzemi_p", 
        "PlochyRZV_p", "UzemniRezervy_p", "KoridoryP_p", "KoridoryN_p", "Lokality_p", 
        "PlochyZmen_p", "PlochyPodm_p", "VpsVpoAs_p", "VpsVpoAs_l", "USES_p", 
        "SystemSidelniZelene_p", "SystemVerProstr_p", "PlochaVI_p", "Zpochybneno_p"
    }
    
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Open the GeoPackage file with update mode to handle transactions
    gpkg = ogr.Open(input_gpkg, update=1)
    if gpkg is None:
        logging.error(f"Failed to open GeoPackage: {input_gpkg}")
        raise Exception("GeoPackage could not be opened.")

    # Track the start time
    start_time = datetime.now()

    # Filter layers based on INCLUDE_LAYERS and EXCLUDE_LAYERS
    layers_to_export = [
        layer for layer in gpkg if (layer.GetName() in INCLUDE_LAYERS or layer.GetName().startswith(('X', 'x'))) 
        and layer.GetName() not in EXCLUDE_LAYERS
    ]

    # Start a transaction to prevent database locking issues
    gpkg.StartTransaction()

    try:
        # Process and export each layer
        for layer in layers_to_export:
            layer_name = layer.GetName()
            logging.info(f"\n\nProcessing layer: {layer_name}\n{'-'*40}\n")

            # Define the output shapefile path
            output_shapefile = os.path.join(output_directory, f"{layer_name}.shp")

            # Create the shapefile driver
            shapefile_driver = ogr.GetDriverByName("ESRI Shapefile")

            # Check if the shapefile already exists and delete if so
            if os.path.exists(output_shapefile):
                shapefile_driver.DeleteDataSource(output_shapefile)

            # Create the shapefile
            output_ds = shapefile_driver.CreateDataSource(output_shapefile)
            if output_ds is None:
                logging.error(f"Could not create shapefile: {output_shapefile}")
                continue

            # Create the layer in the shapefile
            output_layer = output_ds.CreateLayer(layer_name, layer.GetSpatialRef(), layer.GetGeomType(), options=[f"ENCODING={encoding}"])
            if output_layer is None:
                logging.error(f"Could not create layer in shapefile: {output_shapefile}")
                continue

            # Copy fields from GeoPackage layer to shapefile layer
            layer_defn = layer.GetLayerDefn()
            for j in range(layer_defn.GetFieldCount()):
                field_defn = layer_defn.GetFieldDefn(j)
                output_layer.CreateField(field_defn)

            # Copy features from GeoPackage layer to shapefile layer
            for feature in layer:
                geometry = feature.GetGeometryRef()
                if geometry is not None:
                    output_feature = ogr.Feature(output_layer.GetLayerDefn())
                    output_feature.SetGeometry(geometry.Clone())
                    output_feature.SetFrom(feature)
                    output_layer.CreateFeature(output_feature)
                    output_feature = None  # Free memory
                else:
                    logging.warning(f"Feature in layer '{layer_name}' has no geometry and will be skipped.")

            # Destroy the layer object and close the shapefile
            output_ds = None
            logging.info(f"Layer '{layer_name}' successfully exported to {output_shapefile}")
            
            # Adding another log to ensure the format matches your request with a timestamp
            logging.info('')

        # Commit the transaction
        gpkg.CommitTransaction()

    except Exception as e:
        # Rollback transaction in case of error
        gpkg.RollbackTransaction()
        logging.error(f"Transaction failed: {e}")
        raise

    finally:
        # Close the GeoPackage
        gpkg = None

    # Calculate the total duration
    end_time = datetime.now()
    duration = end_time - start_time

    logging.info(f"\n\nExport process completed.\n{'='*40}\n")
    logging.info(f"Total layers processed: {len(layers_to_export)}")
    logging.info(f"Total time taken: {duration}")
    logging.info(f"Output directory: {output_directory}")


# Define the input GeoPackage file, output directory and encoding
# MacOS path format: /path/to/output_directory
# Windows path format: H:/path/to/output_directory
# utf-8 x windows-1250
input_gpkg = "C:/Users/zvardon/Desktop/uprava/UP_prazdny.gpkg"
output_directory = "C:/Users/zvardon/Desktop/export_shp/Data"
encoding = "utf-8"

# Run the export function
gpkg_to_shps(input_gpkg, output_directory, encoding)