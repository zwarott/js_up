import sqlite3


def init_save(working_copy: str) -> None:
    """
    Modify 'qgis_projects' table structure in GeoPackage file for initial save
    within QGIS environment. 'metadata' column will be converted to a string,
    whereas value of 'content' column will be is treated as BLOB data for
    compatibility with Kart commits.

    Parameters
    ----------
    working_copy : str
        The file path to the GeoPackage where 'qgis_projects' file will be modified.

    Returns
    -------
    None
        This function does not return any value. It modifies the GeoPackage in-place.

    """
    # Open the GeoPackage using SQLite3 to modify the table structure.
    conn = sqlite3.connect(working_copy)
    cursor = conn.cursor()

    # Step 1: Create a temporary column to hold the converted 'metadata' as a string.
    cursor.execute("ALTER TABLE qgis_projects ADD COLUMN metadata_temp TEXT;")

    # Step 2: Convert BLOB 'metadata' to a string and store it in the new 'metadata_temp' column.
    cursor.execute("UPDATE qgis_projects SET metadata_temp = CAST(metadata AS TEXT);")

    # Step 3: Drop the old 'metadata' BLOB column.
    cursor.execute("ALTER TABLE qgis_projects DROP COLUMN metadata;")

    # Step 4: Rename 'metadata_temp' back to 'metadata'.
    cursor.execute("ALTER TABLE qgis_projects RENAME COLUMN metadata_temp TO metadata;")

    # Step 5: Update content of 'content' column (as BLOB).
    cursor.execute("UPDATE qgis_projects SET content = CAST(content AS BLOB);")

    # Commit the changes and close the connection.
    conn.commit()
    conn.close()

    print("💡 Project is prepared for Kart commit.")


def next_save(working_copy: str) -> None:
    """
    Modify 'qgis_projects' table structure in GeoPackage file for next save within QGIS
    environment. There is a need to ensure that the content of 'content' column is treated
    as BLOB data for compatibility with Kart commits.

    Parameters
    ----------
    working_copy : str
        The file path to the GeoPackage where 'qgis_projects' file will be modified.

    Returns
    -------
    None
        This function does not return any value. It modifies the GeoPackage in-place.
    """

    # Open the GeoPackage using SQLite3 to modify the table structure.
    conn = sqlite3.connect(working_copy)
    cursor = conn.cursor()

    # Update content of 'content' column (as BLOB).
    cursor.execute("UPDATE qgis_projects SET content = CAST(content AS BLOB);")

    # Commit the changes and close the connection.
    conn.commit()
    conn.close()

    print("💡 Project is prepared for Kart commit.")
