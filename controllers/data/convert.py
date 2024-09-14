from osgeo import gdal, ogr


def int64_to_int32(gpkg_path):
    """
    Converts all fields of type Int64 (64-bit integer) to Int32 (32-bit integer) in all layers of a GeoPackage file.

    This function opens the specified GeoPackage, identifies fields with the `Int64` type in each layer, and creates new
    fields of type `Int32`. It then copies data from the `Int64` fields to the new `Int32` fields, handles potential
    overflow cases where `Int64` values exceed the `Int32` range, and finally deletes the original `Int64` fields,
    renaming the `Int32` fields to match the original field names.

    Parameters
    ----------
    gpkg_path : str
        The file path to the input GeoPackage (.gpkg) file.

    Raises
    ------
    RuntimeError
        If the GeoPackage file cannot be opened.

    Notes
    -----
    - The function checks for potential integer overflow when copying values from `Int64` to `Int32` fields. If a value
      exceeds the `Int32` range (`-2147483648` to `2147483647`), a warning is printed, and the value is skipped.
    - If a new `Int32` field already exists (i.e., it was created in a previous run), the field creation is skipped to
      avoid duplicate column names.

    Examples
    --------
    >>> int64_to_int32("path/to/geopackage.gpkg")
    Processing layer: Layer1
    Converting field field_name from Int64 to Int32.
    Conversion complete for all layers.
    """
    # Open GeoPackage file as a vector dataset and allow updates
    dataset = gdal.OpenEx(gpkg_path, gdal.OF_VECTOR | gdal.GA_Update)

    # Checks if the file was opened successfully
    if not dataset:
        print("Failed to open the GeoPackage file.")
        return  # Stops further execution

    # Iterate through each layers in the GeoPackage
    for layer_index in range(dataset.GetLayerCount()):
        layer = dataset.GetLayerByIndex(layer_index)
        layer_name = layer.GetName()
        print(f"💡 Processing layer: {layer_name}")

        # Get the layer definition (name, type etc.)
        layer_defn = layer.GetLayerDefn()

        # Identify fields with Int64 type
        fields_to_convert = []
        existing_fields = [
            layer_defn.GetFieldDefn(i).GetName()
            for i in range(layer_defn.GetFieldCount())
        ]

        for field_index in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(field_index)
            if field_defn.GetType() == ogr.OFTInteger64:  # Check for Int64 fields
                fields_to_convert.append(field_defn.GetName())

        # Convert each Int64 field to Int32
        for field_name in fields_to_convert:
            new_field_name = field_name + "_int32"

            # Check if the new field already exists - to avoid creating duplicate fields
            if new_field_name in existing_fields:
                print(f"❗️ Field {new_field_name} already exists. Skipping creation.")
                continue

            print(f"💡 Converting field {field_name} from Int64 to Int32.")

            # Create a new Int32 field with "_int32" suffix
            new_field_defn = ogr.FieldDefn(new_field_name, ogr.OFTInteger)
            layer.CreateField(new_field_defn)

            # Resets the reading of the layer to ensure that it starts iterating
            # over the features from the beginning
            layer.ResetReading()

            # Iterate over each feature to copy data from the old Int64 field to the new Int32 field
            # with "_int32" suffix
            feature = layer.GetNextFeature()
            while feature:
                # Retrieves the value of the old field
                old_value = feature.GetField(field_name)
                if old_value is not None:
                    # Handle overflow by checking if the value fits within the Int32 range
                    if -2147483648 <= old_value <= 2147483647:
                        feature.SetField(new_field_name, int(old_value))
                    else:
                        print(
                            f"❗️ Warning: Value {old_value} in field {field_name} exceeds Int32 range and will be skipped."
                        )
                    # The modified feature is updated in the layer
                    layer.SetFeature(feature)
                feature = layer.GetNextFeature()

            # Delete the old Int64 field after copying its data to the new Int32 field.
            layer.DeleteField(layer_defn.GetFieldIndex(field_name))

            # Rename the new Int32 field back to the original name
            # "Id_lokal_int32" is renamed to "Id_lokal"
            new_field_index = layer_defn.GetFieldIndex(new_field_name)
            layer.AlterFieldDefn(
                new_field_index,
                ogr.FieldDefn(field_name, ogr.OFTInteger),
                ogr.ALTER_NAME_FLAG,
            )

        # Sync layer to disk after processing
        layer = None

    # Close the GeoPackage dataset and release it from memory
    dataset = None
    print("✅ Conversion complete for all layers.")
