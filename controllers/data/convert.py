from osgeo import gdal, ogr


def int64_to_int32(gpkg_path):
    # Open the GeoPackage for updating
    dataset = gdal.OpenEx(gpkg_path, gdal.OF_VECTOR | gdal.GA_Update)

    if not dataset:
        print("Failed to open the GeoPackage file.")
        return

    # Iterate through all layers in the GeoPackage
    for layer_index in range(dataset.GetLayerCount()):
        layer = dataset.GetLayerByIndex(layer_index)
        layer_name = layer.GetName()
        print(f"Processing layer: {layer_name}")

        # Get the layer definition
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

            # Check if the new field already exists
            if new_field_name in existing_fields:
                print(f"Field {new_field_name} already exists. Skipping creation.")
                continue

            print(f"Converting field {field_name} from Int64 to Int32.")

            # Create a new Int32 field
            new_field_defn = ogr.FieldDefn(new_field_name, ogr.OFTInteger)
            layer.CreateField(new_field_defn)

            # Ensure to reset the reading before iterating over features
            layer.ResetReading()

            # Iterate over each feature to copy data
            feature = layer.GetNextFeature()
            while feature:
                old_value = feature.GetField(field_name)
                if old_value is not None:
                    # Handle overflow by checking if the value fits within the Int32 range
                    if -2147483648 <= old_value <= 2147483647:
                        feature.SetField(new_field_name, int(old_value))
                    else:
                        print(
                            f"Warning: Value {old_value} in field {field_name} exceeds Int32 range and will be skipped."
                        )
                    layer.SetFeature(feature)
                feature = layer.GetNextFeature()

            # Delete the old Int64 field
            layer.DeleteField(layer_defn.GetFieldIndex(field_name))

            # Rename the new Int32 field back to the original name
            new_field_index = layer_defn.GetFieldIndex(new_field_name)
            layer.AlterFieldDefn(
                new_field_index,
                ogr.FieldDefn(field_name, ogr.OFTInteger),
                ogr.ALTER_NAME_FLAG,
            )

        # Sync layer to disk after processing
        layer = None

    # Close the dataset
    dataset = None
    print("Conversion complete for all layers.")
