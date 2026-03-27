#!/python

from pathlib import Path
import pytest

@pytest.mark.xfail
def test():
    file_path = f"{Path.home()}/Downloads/csvReport_1773259809905.csv"
    # suppress_from_spreadsheet.suppress(file_path)
