import argparse
import os
import re
import string
import sys

import jinja2

import utfcsv
import hexmap as hm

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--format', dest='fmt', default='html',
                    help="Format of output: html or text")
parser.add_argument('CSV', help="The CSV file with the hex descriptions.")
parser.add_argument('Title', help="The title of this hex map.")
args = parser.parse_args(sys.argv[1:])

if args.fmt == 'html':
    template_name = os.path.basename(args.CSV)[:-3] + 'html'
elif args.fmt == 'text':
    template_name = 'text.txt'


# Read CSV dump of Google Docs hex map descriptions and create hexmap of
# the data.
with open(args.CSV, 'rb') as csvfile:
    hexmap = hm.HexMap(utfcsv.unicode_csv_reader(csvfile))


if args.fmt == 'stats':
    print 'Most referenced Hexes:'
    for l, count in hexmap.reference_histogram[-10:]:
        print "\t%s mentioned %d times" % (l, count)
    print 'Themes found in hexes:'
    for l, count in hexmap.themes_histogram:
        print "\t%s mentioned %d times" % (l, count)
    exit(0)


# Output Data to Template

def settlementlink(m):
    # Look up settlement in settlement map and create link if the settlement
    # exists.
    settlement = m.group(1).upper().strip()
    if settlement in hexmap.settlements:
        return u"<a href='#{hex}' class='city-link'>{settlement}</a>".format(
                settlement=settlement, hex=hexmap.settlements[settlement])
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
    if h in hexmap.references:
        return u', '.join("<a class='hex-link' href='#%s'>%s</a>" % (l, l)
                          for l in sorted(hexmap.references[h]))
    return u''

def coordinates(location):
    return int(location[:2]), int(location[2:])

last_hex = sorted(hexmap.hexes.keys())[-1]
max_x, max_y = coordinates(last_hex)

def nw(location):
    x, y = coordinates(location)
    if x % 2 == 1:
        y -= 1
    x -= 1
    return '' if x <= 0 or y <= 0 else "%02d%02d" % (x, y)

def ne(location):
    x, y = coordinates(location)
    if x % 2 == 1:
        y -= 1
    x += 1
    return '' if x >= max_x or y <= 0 else "%02d%02d" % (x, y)

def se(location):
    x, y = coordinates(location)
    if x % 2 == 0:
        y += 1
    x += 1
    return '' if x >= max_x or y >= max_y else "%02d%02d" % (x, y)

def sw(location):
    x, y = coordinates(location)
    if x % 2 ==1:
        y += 1
    x -= 1
    return '' if x <= 0 or y >= max_y else "%02d%02d" % (x, y)


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
env.filters['nw'] = nw
env.filters['ne'] = ne
env.filters['sw'] = sw
env.filters['se'] = se

template = env.get_template(template_name)

context = {
    'hexes': sorted(hexmap.hexes.items()),
    'authors': u", ".join("%s (%s)" % (author, count)
                          for author, count in hexmap.author_histogram.most_common()),
    'references': hexmap.references,
    'title': args.Title
}

print template.render(**context).encode('utf-8')
