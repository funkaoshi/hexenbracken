import argparse
import collections
import csv
import jinja2
import re
import string
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', dest='fmt', default='html',
                    help="Format of output: html or text")
parser.add_argument('CSV', help="The CSV file with the hex descriptions.")
args = parser.parse_args(sys.argv[1:])


# UTF8 CSV Reader
# from: http://stackoverflow.com/q/904041/2100287
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

# Read CSV dump of Google Docs hex map descriptions.
csvhexmap = unicode_csv_reader(open(args.CSV, 'rb'))


# Load hexes from CSV dump.
hexes = collections.defaultdict(list)
settlements = {}
for h in csvhexmap:
    # X, Y, Extra, Hex Key, Terrain, Settlement(s), Extra, Author, Description
    location = h[3]
    if not location.isdigit():
        continue
    settlement = h[5].upper()
    if settlement:
        settlements[settlement] = location
    hexes[location].append({
        'settlement': settlement,
        'author': h[7],
        'description': h[8] or '-'.encode('utf-8'),
        'moreinfo': h[9]
    })


def settlementlink(m):
    # Look up settlement in settlement map and create link if the settlement
    # exists.
    settlement = m.group(1).upper()
    if settlement in settlements:
        return "<a href='#{hex}' class='city-link'>{settlement}</a>".format(
                settlement=settlement, hex=settlements[settlement])
    return settlement

def process(description):
    # Fix some poor grammar / punctuation
    description = description.strip()
    if description[-1] not in string.punctuation:
        description = description + '.'
    if description[0].islower():
        description = description.capitalize()
    # Add links were appropriate
    if args.fmt == 'html':
        description = re.sub(r"\[\[(\d\d\d\d)\]\]",
                             r"<a class='hex-link' href='#\1'>\1</a>",
                             description)
        description = re.sub(r"\[\[(.*?)\]\]", settlementlink, description)
    else:
        # Convert link short-hand to plain text.
        description = re.sub(r"\[\[(.*?)\]\]", r"\1", description)
    return description

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env.filters['process'] = process

template = env.get_template('hexenbracken.html' if args.fmt == 'html' else 'text.txt')

print template.render(hexes=sorted(hexes.items())).encode('utf-8')
