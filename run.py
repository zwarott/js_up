from controllers.data.export_data import export_working_dir
from controllers.data.inspect_data import shp_overview

from controllers.layout.convert_layout import raster_to_24bit
from controllers.layout.inspect_layout import check_24bit_depth

from controllers.repo.repo_init import init_with_import
from controllers.repo.import_data import import_shp_dir

from aux_data.gpkg_layers import EXCLUDE_LAYERS, INCLUDE_LAYERS
from config import (
    MUNICIPALITIES,
    DEFAULT_PATH,
    repo_dir,
    working_copy,
    output_data_dir,
    output_layout_dir,
    mun_code,
    new_or_change,
    change_number,
    gpkg_to_import,
    shp_dir_to_import,
    encoding,
)

# Create a dictionary to map function names to their corresponding
# function calls and parameters
function_map = {
    "export_working_dir": {
        "func": export_working_dir,
        "params": {
            "gpkg_path": working_copy,
            "output_dir": output_data_dir,
            "working_dir": repo_dir,
            "exclude_layers": EXCLUDE_LAYERS,
            "include_layers": INCLUDE_LAYERS,
            "export_empty_layers": False,
            "encoding": encoding,
        },
    },
    "shp_overview": {
        "func": shp_overview,
        "params": {
            "data_dir": output_data_dir,
        },
    },
    "init_with_import": {
        "func": init_with_import,
        "params": {
            "default_path": DEFAULT_PATH,
            "municipalities": MUNICIPALITIES,
            "mun_code": mun_code,
            "new_or_change": new_or_change,
            "change_number": change_number,
            "gpkg_to_import": gpkg_to_import,
        },
    },
    "import_shp_dir": {
        "func": import_shp_dir,
        "params": {
            "shp_dir": shp_dir_to_import,
            "repo_dir": repo_dir,
        },
    },
    "raster_to_24bit": {
        "func": raster_to_24bit,
        "params": {
            "raster_dir": output_layout_dir,
        },
    },
    "check_24bit_depth": {
        "func": check_24bit_depth,
        "params": {
            "raster_dir": output_layout_dir,
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
# execute_function("init_with_import")
# execute_function("raster_to_24bit")
# execute_function("check_24bit_depth")
# execute_function("shp_overview")
execute_function("import_shp_dir")
