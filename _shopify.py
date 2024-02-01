import csv
import _utils as u
import json as j
import os


def get_data(file_path: str, _from: str, _to: str, _group_by: str, _groups: str, codepage: str):
    """Get data from csv-file."""
    func_name = u.get_func_name()

    in_fields = _from.split(', ')  # лист входных csv-полей
    out_fields = _to.split(', ')  # лист выходных json-полей
    g = _groups.split(', ')  # лист групп для фильтрования товаров

    try:
        with (open(file_path, 'r', encoding=codepage) as csv_file):  # Открываем csv-файл
            csv_reader = csv.reader(csv_file)
            csv_header = next(csv_reader)  # Считываем заголовок (первую строку) файла
            # Создаем соответствие между именами полей и индексами
            field_indices = {field: csv_header.index(field) for field in in_fields}

            # Формирование списка словарей
            return [
                [
                    rec[field_indices[in_fields[i]]] for i in range(len(in_fields))
                ] for rec in csv_reader if rec[field_indices[_group_by]] in g
            ]
    except Exception as e:
        u.log_msg(func_name, True, e)


def write_data(rows: list, _groups: str, docs_path: str, images_path: str, noimage: str):
    """Convert 'aloha_db' list of rows to json-docs & write it to disc."""
    image_extension = ['jpg', 'png', 'jpeg', 'gif']
    for row in rows:
        if str(row[-1]) in _groups:  # INI ALOHA[groups]
            image_file = f"{images_path}/{str(row[1])}"  # INI [DATA]images

            # Check if image file exists
            for ext in image_extension:
                if os.path.exists(f"{image_file}.{ext}"):
                    image_file = f"{image_file}.{ext}"
                    break
            else:
                # Use default image if no matching image is found
                image_file = noimage  # INI [DATA]noimage

            item = {
                '_id': row[0],
                'Code': row[1],
                'Name': row[2],
                'Comment': row[3],
                'Price': row[4],
                'Group': f"{str(row[5]).upper()}",
                'Image': image_file
            }

            # Convert row to json
            json_doc = j.dumps(item, indent=2, ensure_ascii=False)

            # Write item json to file
            with open(f"{docs_path}/{item['Code']}.json", "w", encoding="utf-8") as file:
                file.write(json_doc)

