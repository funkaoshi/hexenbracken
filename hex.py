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
parser.add_argument('Template', help="The template to use to generate webpage.")
parser.add_argument('Title', help="The title of this hex map.")
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
    location = h[3].strip('*')
    if not location.isdigit() or not h[7]:
        # skip empty / junky hexes
        continue
    settlement = h[5].upper().strip()
    if settlement:
        settlements[settlement] = location
    hexes[location].append({
        'settlement': settlement,
        'author': h[7],
        'description': h[8] or '-'.encode('utf-8'),
        'moreinfo': h[9]
    })

# Yank out all the authors
authors = [d['author'] for l, details in hexes.iteritems() for d in details
           if d['author']]
author_histogram = collections.Counter(authors)


# Yank out all references
references = collections.defaultdict(set)
for l, details in hexes.iteritems():
    for d in details:
        for m in re.finditer(r"\[\[(\d\d\d\d)\]\]", d['description']):
            if l != m.group(1):
                references[m.group(1)].add(l)
        for m in re.finditer(r"\[\[(.*?)\]\]", d['description']):
            settlement = m.group(1).upper().strip()
            if not settlement.isdigit() and settlement in settlements:
                location = settlements[settlement]
                if l != location:
                    references[location].add(l)

def settlementlink(m):
    # Look up settlement in settlement map and create link if the settlement
    # exists.
    settlement = m.group(1).upper().strip()
    if settlement in settlements:
        return "<a href='#{hex}' class='city-link'>{settlement}</a>".format(
                settlement=settlement, hex=settlements[settlement])
    return settlement

def hex2link(text):
    # Add links were appropriate
    if args.fmt == 'html':
        text = re.sub(r"\[\[(\d\d\d\d)\]\]",
                      r"<a class='hex-link' href='#\1'>\1</a>",
                      text)
        text = re.sub(r"\[\[(.*?)\]\]", settlementlink, text)
    else:
        # Convert link short-hand to plain text.
        text = re.sub(r"\[\[(.*?)\]\]", r"\1", text)
    return text

def getreferences(h):
    # return references for this hex.
    if h in references:
        return ', '.join("<a class='hex-link' href='#%s'>%s</a>" % (l, l)
                         for l in sorted(references[h]))
    return ''

def process(description):
    # Fix some poor grammar / punctuation
    description = description.strip()
    if description[-1] not in string.punctuation:
        description = description + '.'
    if description[0].islower():
        description = description.capitalize()
    description = hex2link(description)
    return description

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
env.filters['process'] = process
env.filters['references'] = getreferences

template = env.get_template(args.Template)

context = {
    'hexes': sorted(hexes.items()),
    'authors': u", ".join("%s (%s)" % (author, count)
                          for author, count in author_histogram.most_common()),
    'references': references,
    'title': args.Title
}

print template.render(**context).encode('utf-8')
