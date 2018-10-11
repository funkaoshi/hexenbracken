The Hexenbracken
============

NOTE 10/5/2018:
This version has been modified by Max Cantor and has been adapted for python3.
hex.py and hexmaps.py have been altered, and utfcsv.py is now obsolete. 
Additionally, there were some mistakes or omissions in the original instructions.
Check out my blog!: https://weirdwonderfulworlds.blogspot.com/

This python script will take a set of hex descriptions from a Google Doc and
turn them into a simple web site. Several example websites exist: [The
Hexenbracken][1] and [The Kraal][2], [The Colossal Wastes of Zhaar][3],
[Synthexia][4]. The source files that generate them are in this repository,
under the `hexmaps` folder.

Usage:
1. You need to create a jinja template. As long as you stick to the proper .csv
   format, you should be able to just copy the base.html template from the templates
   folder into a new template, the same name as the .csv file (and eventually the
   html page itself):
   
   cp templates/base.html templates/[NAME].html

2. Then you can run the following through in unix bash (I used git bash):

   python -Xutf8 hex.py hexmaps/[NAME].csv title > [NAME].html
   
   The -Xutf8 has to do with the fact that I used Windows, if you use linux or 
   probably also mac I don't think that part is necessary. 

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
