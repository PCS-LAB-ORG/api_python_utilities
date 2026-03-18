import csv


def list_to_csv(file_name, data_list=[], mode="w+", encoding="utf-8"):
    with open(
        file_name, data_list, mode=mode, newline="", encoding=encoding
    ) as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=data_list[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(data_list)
    print(f"Finished writing {len(data_list)} rows to {file_name}")
