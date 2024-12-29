import os
import time
from qgis.core import QgsProject, QgsLayoutExporter


def export_layouts(output_dir, output_format, include_world_file=False):
    """
    Export all layouts in the QGIS project to the specified file format and optionally include world files.

    Parameters:
    -----------
    output_dir : str
        The directory where the files will be saved.
    output_format : str
        The output file format ('PNG', 'TIF', 'BMP').
    include_world_file : bool
        Whether to include a world file (for georeferencing).
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Validate the output format
    supported_formats = ["PNG", "TIF", "BMP"]
    if output_format.upper() not in supported_formats:
        raise ValueError(
            f"Unsupported format '{output_format}'. Supported formats: {', '.join(supported_formats)}"
        )

    # Get the current project and layout manager
    project = QgsProject.instance()
    layout_manager = project.layoutManager()

    # Record the start time of the entire export process
    total_start_time = time.time()
    print(f"\nStarting the layout export process to {output_format}...\n")

    # Map output format to world file extensions
    world_file_extensions = {
        "PNG": "pgw",
        "TIF": "tfw",
        "BMP": "bpw",
    }

    # Iterate over all layouts in the project
    for layout in layout_manager.layouts():
        layout_name = layout.name()
        print(f"\n--- Starting export for layout: {layout_name} ---")

        try:
            # Record the start time for this layout
            layout_start_time = time.time()

            # Define the output path for each layout
            output_file_extension = output_format.lower()
            output_path = os.path.join(
                output_dir, f"{layout_name}.{output_file_extension}"
            )

            # Set up image export settings
            export_settings = QgsLayoutExporter.ImageExportSettings()
            export_settings.dpi = 300  # High-resolution export

            # Export the layout
            exporter = QgsLayoutExporter(layout)
            result = exporter.exportToImage(output_path, export_settings)

            if result == QgsLayoutExporter.Success:
                # Optionally write the world file
                if include_world_file:
                    world_file_extension = world_file_extensions[output_format.upper()]
                    write_world_file(output_path, layout, world_file_extension)

                layout_duration = time.time() - layout_start_time
                print(
                    f"Exported '{layout_name}' to {output_path} in {layout_duration:.2f} seconds"
                )
            else:
                print(f"Failed to export '{layout_name}' to {output_format}.")

        except Exception as e:
            print(f"Error exporting layout '{layout_name}': {e}")

        print(f"--- Finished export for layout: {layout_name} ---\n")

    # Calculate and print the total duration for the export process
    total_duration = time.time() - total_start_time
    print(
        f"\n=== All layouts exported as {output_format} in {total_duration:.2f} seconds ===\n"
    )


def write_world_file(output_path, layout, world_file_extension):
    """
    Create a world file for georeferencing the exported layout.

    Parameters:
    -----------
    output_path : str
        The path of the exported file.
    layout : QgsLayout
        The QGIS layout object.
    world_file_extension : str
        The extension of the world file (e.g., 'pgw', 'tfw').
    """
    dpi = 300  # Resolution of 300 DPI
    page = layout.pageCollection().pages()[0]
    layout_width_mm = page.pageSize().width()
    layout_height_mm = page.pageSize().height()

    map_item = layout.referenceMap()  # Get the main map item
    if map_item is None:
        print(
            f"No reference map found for layout '{layout.name()}'. Skipping world file creation."
        )
        return

    extent = map_item.extent()
    width_m = extent.width()
    height_m = extent.height()

    # Calculate pixel size in meters
    pixel_size_x = width_m / (layout_width_mm / 25.4 * dpi)
    pixel_size_y = height_m / (layout_height_mm / 25.4 * dpi)

    # World file content
    world_file_content = [
        f"{pixel_size_x:.10f}",
        "0.0",
        "0.0",
        f"-{pixel_size_y:.10f}",
        f"{extent.xMinimum():.10f}",
        f"{extent.yMaximum():.10f}",
    ]

    # Write the world file
    world_file_path = output_path.rsplit(".", 1)[0] + f".{world_file_extension}"
    with open(world_file_path, "w") as wf:
        wf.write("\n".join(world_file_content))
    print(
        f"World file created for '{output_path}' with extension '.{world_file_extension}'"
    )


# Example usage
output_directory = "/Users/zwarott/Desktop/vykresy_export"
export_layouts(output_directory, "TIF", include_world_file=True)
