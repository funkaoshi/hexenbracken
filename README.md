The Hexenbracken
============

This python script will take a set of hex descriptions from a Google Doc and
turn them into a simple web site. Several example websites exist: [The
Hexenbracken][1] and [The Kraal][2], [The Colossal Wastes of Zhaar][3],
[Synthexia][4]. The source files that generate them are in this repository,
under the `hexmaps` folder.

Usage: `python hexmaps.py <input csv file> > <output html file>`

You can use the flag `-f text` to tell the generator to use a text template,
rather than an HTML one. The script currently assumes the HTML template used to
generate the page is named the same as the supplied CSV file, with a `.html`
extension. (e.g. If you try and generate an HTML page for `hexenbracken.csv` it
will look for the template `hexenbracken.html`.)

The input CSV files should be formated as follows:

    0  1  2       3        4        5              6       7       8            9    10
    X, Y, UNUSED, Hex Key, Terrain, Settlement(s), UNUSED, Author, Description, URL, Themes

The script till make settlements and references to other hexes into links. It 
finds referenced hexes by looking for `[[XXXX]]` in hex descriptions.


[1]: http://save.vs.totalpartykill.ca/grab-bag/hexenbracken/
[2]: http://save.vs.totalpartykill.ca/grab-bag/kraal/
[3]: /grab-bag/wastes/
[4]: /grab-bag/synthexia
