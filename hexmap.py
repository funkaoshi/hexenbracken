import collections
import operator
import re


def make_histogram(d):
    histogram = [(l, len(i)) for l, i in d.items()]
    histogram = sorted(histogram, key=operator.itemgetter(1))
    return histogram


class Hex(object):
    """
    Data we store about a hex.
    """

    def __init__(self, location, settlement, author, description, url, themes):
        self.location = location  # e.g. 0121
        self.author = author
        self.description = description or "-"

        # The settlement / feature inside this hex. TODO: should be a list
        self.settlement = settlement.upper().strip()

        # A list of optional themes that describe this hex.
        self.themes = [t.upper().strip() for t in themes.split(",")]

        # A link to social media or blog post about this hex.
        self.url = url


class HexMap(object):
    def __init__(self, csvfile):
        """
        Expects a neatly formated CSV file and generates a data structure
        storing descriptions and information about the area described. The
        expected fields, in order, are:

            0  1  2       3        4        5              6       7
            X, Y, UNUSED, Hex Key, Terrain, Settlement(s), UNUSED, Author, ...

                8            9    10
            ... Description, URL, Themes
        """
        self.hexes = collections.defaultdict(list)
        self.themes = collections.defaultdict(list)
        self.settlements = {}
        for h in csvfile:
            h = Hex(h[3], h[5], h[7], h[8], h[9], h[10])
            if not h.location.isdigit() or not h.author:
                # skip empty / junky hexes
                continue
            if h.settlement:
                # take each comma separated list of settlements and add them to
                # our settlement lookup.
                for settlement in h.settlement.split(","):
                    self.settlements[settlement.strip()] = h.location
            for t in h.themes:
                self.themes[t].append(h.location)
            self.hexes[h.location].append(h)

        # Yank out all the authors
        self.authors = [
            d.author for l, details in self.hexes.items() for d in details if d.author
        ]
        self.author_histogram = collections.Counter(self.authors)

        # Yank out all references
        self.references = collections.defaultdict(set)
        for l, details in self.hexes.items():
            for d in details:
                # Look for [[XXYY]] style references to specific hexes.
                for m in re.finditer(r"\[\[(\d\d\d\d)\]\]", d.description):
                    if l != m.group(1):
                        self.references[m.group(1)].add(l)
                # Look for [[SETTLEMENT]], [[PERSON's]]
                for m in re.finditer(r"\[\[([\w]+?)(?:'s|S)?\]\]", d.description):
                    settlement = m.group(1).upper().strip()
                    if not settlement.isdigit() and settlement in self.settlements:
                        location = self.settlements[settlement]
                        if l != location:
                            self.references[location].add(l)

    @property
    def reference_histogram(self):
        return make_histogram(self.references)

    @property
    def themes_histogram(self):
        return make_histogram(self.themes)
