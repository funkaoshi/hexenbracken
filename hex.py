import argparse
import csv
import jinja2
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', dest='fmt', default='html',
                    help="Format of output: html or text")
args = parser.parse_args(sys.argv[1:])

def process(description):
    # Try to normalize references to hexes. Damn it people.
    description = re.sub(r"(\d\d) (\d\d)", r"\1\2", description)      # XX YY
    description = re.sub(r"\[(\d\d\d\d)\]", r"Hex \1", description)   # [XXYY]
    if args.fmt == 'html':
        description = re.sub(r"(\d\d\d\d)", r"<a href='#\1'>\1</a>", description)
    else:
        # Generate Markdown link?
        # description = re.sub(r"(\d\d\d\d)", r"[\1](#\1)", description)
        pass 
    # Who doesn't capitalize the first word in a sentance?
    description = description.capitalize()
    return description

# UTF8 CSV Reader
# from: http://stackoverflow.com/q/904041/2100287
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

# Read CSV dump of Google Docs hex map descriptions.
csvhexmap = unicode_csv_reader(open('hexmap.csv', 'rb'))

# Load hexes from CSV dump.
hexes = {}
for h in csvhexmap:
    location = h[3]
    if not location.isdigit():
        continue
    description = process(h[6]) or '-'.encode('utf-8')
    if location in hexes:
        hexes[location]['descriptions'].append(description)
    else:
        hexes[location] = {'terrain': h[4], 'descriptions': [description,]}

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
template = env.get_template('hexenbracken.html' if args.fmt == 'html' else 'text.txt')

print template.render(hexes=sorted(hexes.items())).encode('utf-8')