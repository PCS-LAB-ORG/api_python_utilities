"""Naval Fate.

Usage:
  xlsx_writer.py --input_file=<input_file>
  xlsx_writer.py -h | --help

Options:
  -h --help     Show this screen.
  --input_file=<input_file>  File to be converted.
  # --speed=<kn>  Speed in knots [default: 10]

"""

import csv
import xlsxwriter
from docopt import docopt


def csv_to_xlsx(input_file: str) -> xlsxwriter.Workbook:

    # 1. Load CSV data
    with open(input_file, "r", encoding="utf-8") as f:
        data = list(csv.reader(f))

    # 2. Setup Workbook
    # workbook = xlsxwriter.Workbook('output.xlsx')
    output_file = f"{input_file[:-3]}xlsx"
    with xlsxwriter.Workbook(output_file) as workbook:

        worksheet = workbook.add_worksheet()

        # 3. Add Table (Formatting)
        # data[0] are headers, data[1:] is the body
        header_row = [{"header": h} for h in data[0]]
        worksheet.add_table(
            0,
            0,
            len(data) - 1,
            len(data[0]) - 1,
            {"data": data[1:], "columns": header_row, "style": "Table Style Medium 9"},
        )

        # 4. Auto-adjust Column Widths
        worksheet.autofit()
        worksheet.freeze_panes(top_row=0)
    return workbook


if __name__ == "__main__":
    arguments = docopt(doc=__doc__, version="Naval Fate 2.0")
    csv_to_xlsx(arguments["--input_file"])


"""
Goals:
- add csv to an existing csv or xlsx if the headers match
- remove duplicates
- add new csv to a separate sheet in the same workbook
"""
