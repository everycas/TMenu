import dbf
import json as j
import _constants as c
import os


def get_data(aloha_db_path: str):
    """Aloha POS dbf-files to jsons """

    # Формирование листа элементов товаров из таблиц Aloha DB
    with dbf.Table(f'{aloha_db_path}/CAT.DBF', codepage=c.CODEPAGE) as table:
        cats = [(rec['ID'], rec['NAME'].rstrip()) for rec in table if rec['SALES'] == 'Y']

    with dbf.Table(f'{aloha_db_path}/CIT.DBF', codepage=c.CODEPAGE) as table:
        cits = [[rec['ITEMID'], rec['CATEGORY']] for rec in table if any(cat[0] == rec['CATEGORY'] for cat in cats)]
    categs = [cit + [cat[1]] for cit in cits for cat in cats if cit[1] == cat[0]]

    with dbf.Table(f'{aloha_db_path}/ITM.DBF', codepage=c.CODEPAGE) as table:
        itms = [
            [
                rec['ID'],
                rec['USERNUMBER'],
                rec['SHORTNAME'].rstrip().replace('\\n', ' '),
                rec['LONGNAME'].rstrip().replace('\\n', ' '),
                rec['PRICE']
            ] for rec in table if any(cit[0] == rec['ID'] for cit in categs)]
    rows = [itm + [cat[2]] for itm in itms for cat in categs if itm[0] == cat[0]]
    return sorted(rows, key=lambda x: x[0])[1:]  # сортировка по возраст. ID товара, [1:] - без позиции "Все меню"


def write_data(rows: list, aloha_groups: str, docs_path: str, images_path: str, noimage: str):
    """Convert 'aloha_db' list of rows to json-docs & write it to disc."""
    image_extension = ['jpg', 'png', 'jpeg', 'gif']
    for row in rows:
        if str(row[-1]) in aloha_groups:  # INI ALOHA[groups]
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
                'Code': str(row[1]),
                'Name': str(row[2]),
                'Comment': str(row[3]),
                'Price': str(round(row[4], 2)),
                'Group': f"{str(row[5]).upper()}",
                'Image': image_file
            }

            # Convert row to json
            json_doc = j.dumps(item, indent=2, ensure_ascii=False)

            # Write item json to file
            with open(f"{docs_path}/{item['Code']}{item['Name'].replace('/', ' ')}.json", "w", encoding="utf-8") as file:
                file.write(json_doc)


data_rows = get_data(c.ALOHA_DB)
write_data(data_rows, c.ALOHA_GROUPS, c.DOCS, c.IMAGES, c.NOIMAGE)





