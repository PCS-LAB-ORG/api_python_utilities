import csv
from apu.utils import json_ops


def list_to_csv(file_name="", data_list=None, mode="w+", encoding="utf-8", keys=None):
    if not keys:
        keys = data_list[0].keys()
    with open(file=file_name, mode=mode, newline="", encoding=encoding) as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=keys)
        csv_writer.writeheader()
        csv_writer.writerows(data_list)
    print(f"Finished writing {len(data_list)} rows to {file_name}")


def obj_to_csv(
    file_name="", data_list=None, mode="w+", encoding="utf-8", flatten=False, keys=None
):
    """get vars of objects in list and flatten their heirarchy using dot notation"""
    list_of_dictionaries = []
    for obj in data_list:
        obj_vars = vars(obj)
        if flatten:
            obj_vars = json_ops.flatten_json(obj_vars)
        list_of_dictionaries.append(obj_vars)
    list_to_csv(file_name, list_of_dictionaries, mode, encoding, keys)


def read_csv(file_name: str):
    with open(file_name) as user_list:
        return csv.DictReader(user_list)
