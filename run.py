from controllers.data.export_data import export_working_dir
from controllers.data.inspect_data import shp_overview

from controllers.layout.convert_layout import raster_to_24bit
from controllers.layout.inspect_layout import check_24bit_depth

from controllers.repo.repo_init import init_with_import
from controllers.repo.import_data import import_shp_dir

from aux_data.gpkg_layers import EXCLUDE_LAYERS, INCLUDE_LAYERS
from config import (
    MUNICIPALITIES,
    DEFAULT_REPO,
    REPO_DIR,
    WORKING_COPY,
    OUTPUT_DATA_DIR,
    OUTPUT_LAYOUT_DIR,
    MUN_CODE,
    NEW_OR_CHANGE,
    CHANGE_NUMBER,
    GPKG_TO_IMPORT,
    SHP_DIR_TO_IMPORT,
    ENCODING,
)

# Create a dictionary to map function names to their corresponding
# function calls and parameters
function_map = {
    "export_working_dir": {
        "func": export_working_dir,
        "params": {
            "gpkg_path": WORKING_COPY,
            "output_dir": OUTPUT_DATA_DIR,
            "working_dir": REPO_DIR,
            "exclude_layers": EXCLUDE_LAYERS,
            "include_layers": INCLUDE_LAYERS,
            "export_empty_layers": False,
            "encoding": ENCODING,
        },
    },
    "shp_overview": {
        "func": shp_overview,
        "params": {
            "data_dir": OUTPUT_DATA_DIR,
        },
    },
    "init_with_import": {
        "func": init_with_import,
        "params": {
            "default_repo": DEFAULT_REPO,
            "municipalities": MUNICIPALITIES,
            "mun_code": MUN_CODE,
            "new_or_change": NEW_OR_CHANGE,
            "change_number": CHANGE_NUMBER,
            "gpkg_to_import": GPKG_TO_IMPORT,
        },
    },
    "import_shp_dir": {
        "func": import_shp_dir,
        "params": {
            "shp_dir": SHP_DIR_TO_IMPORT,
            "repo_dir": REPO_DIR,
        },
    },
    "raster_to_24bit": {
        "func": raster_to_24bit,
        "params": {
            "raster_dir": OUTPUT_LAYOUT_DIR,
        },
    },
    "check_24bit_depth": {
        "func": check_24bit_depth,
        "params": {
            "raster_dir": OUTPUT_LAYOUT_DIR,
        },
    },
}


# Function to execute a user-selected function from the function_map
def execute_function(function_name):
    if function_name in function_map:
        func = function_map[function_name]["func"]
        params = function_map[function_name]["params"]
        func(**params)
    else:
        print(f"❌ Function {function_name} not found in function map.")


# Example usage
# execute_function("export_working_dir")
execute_function("init_with_import")
# execute_function("raster_to_24bit")
# execute_function("check_24bit_depth")
# execute_function("shp_overview")
# execute_function("import_shp_dir")
