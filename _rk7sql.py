import _utils as u
import pyodbc as p
import json as j
import os


def write_new_rk7query(file_path: str, query: str):
    """If sql-file not exist in folder, create new file."""
    func_name = u.get_func_name()
    if not os.path.exists(file_path):
        with open(file_path, 'w') as ini_file:
            ini_file.write(query)
        u.log_msg(func_name, True, f"New '{file_path}' file created.")


def connect_server(server: str, db: str, user: str, psw: str) -> object:
    """Establish a connection to the SQL Server"""
    return p.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={db};UID={user};PWD={psw};')


def get_data(connection, query_file_path: str) -> list:
    """Get sql rows list, add to json-docs, and write as separate files to disc."""
    # Create a cursor from the connection
    cursor = connection.cursor()

    # Read SQL query from file
    with open(query_file_path, 'r') as file:
        query = file.read()

    # Execute the SQL query
    cursor.execute(query)

    # Fetch the results
    rows = cursor.fetchall()  # list

    # Close the cursor
    cursor.close()

    return rows


def write_data(rows: list, rk7groups: str, docs_path: str, images_path: str, noimage: str):
    """Convert 'rk7_db' list of rows to json-docs & write it to disc."""

    image_extension = ['jpg', 'png', 'jpeg', 'gif']

    for row in rows:
        if str(row.CATEGLIST_NAME) in rk7groups:  # rk7 groups string from ini
            image_file = f"{images_path}/{str(row.CODE)}"

            # Check if image file exists
            for ext in image_extension:
                if os.path.exists(f"{image_file}.{ext}"):
                    image_file = f"{image_file}.{ext}"
                    break
            else:
                # Use default image if no matching image is found
                image_file = noimage

            item = {
                '_id': row.SIFR,
                'Code': str(row.CODE),
                'Name': str(row.MENUITEMS_NAME),
                'Comment': str(row.COMMENT),
                'Price': str(round(row.VALUE, 2)),
                'Group': f"{str(row.CATEGLIST_NAME).upper()}",
                'Image': image_file
            }

            # Convert row to json
            json_doc = j.dumps(item, indent=2, ensure_ascii=False)

            # Write item json to file
            with open(f"{docs_path}/{item['Code']}.json", "w", encoding="utf-8") as file:
                file.write(json_doc)


def close_connection(connection: object):
    """Close the SQL Server connection"""
    connection.close()

