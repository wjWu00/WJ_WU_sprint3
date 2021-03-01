import main

def test_excel():
    result = main.excel_table()
    assert len(result) == 36383  #excel file has 36383 rows


