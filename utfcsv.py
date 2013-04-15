import csv

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    """
    UTF8 CSV Reader from: http://stackoverflow.com/q/904041/2100287
    """
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]
