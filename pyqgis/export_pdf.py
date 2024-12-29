import os
import time
from qgis.core import QgsProject, QgsLayoutExporter


def export_layouts_to_pdf(output_dir):
    """
    Export all layouts in the QGIS project to PDFs in the specified output directory.

    Parameters:
    -----------
    output_dir : str: The directory where the PDFs will be saved.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Get the current project and layout manager
    project = QgsProject.instance()
    layout_manager = project.layoutManager()

    # Record the start time of the entire export process
    total_start_time = time.time()
    print("\nStarting the layout export process...\n")

    # Iterate over all layouts in the project
    for layout in layout_manager.layouts():
        layout_name = layout.name()
        print(f"\n--- Starting export for layout: {layout_name} ---")

        try:
            # Record the start time for this layout
            layout_start_time = time.time()

            # Define the output path for each layout
            output_path = os.path.join(output_dir, f"{layout_name}.pdf")

            # Export the layout as a PDF
            exporter = QgsLayoutExporter(layout)
            result = exporter.exportToPdf(
                output_path, QgsLayoutExporter.PdfExportSettings()
            )

            # Check export result
            if result == QgsLayoutExporter.Success:
                layout_duration = time.time() - layout_start_time
                print(
                    f"Successfully exported '{layout_name}' to {output_path} in {layout_duration:.2f} seconds"
                )
            else:
                print(
                    f"Warning: Export of '{layout_name}' completed with warnings (result code: {result})."
                )

        except Exception as e:
            # Handle any exceptions and continue with the next layout
            print(f"Error: Failed to export layout '{layout_name}'.")
            print(f"Details: {e}")

        print(f"--- Finished export for layout: {layout_name} ---\n")

    # Calculate and print the total duration for the export process
    total_duration = time.time() - total_start_time
    print(f"\n=== All layouts exported in {total_duration:.2f} seconds ===\n")


# Example usage
output_directory = "/Users/zwarott/Desktop/vykresy_export/"
export_layouts_to_pdf(output_directory)
