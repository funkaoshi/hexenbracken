all: build deploy

build: hexenbracken kraal wastes fallout synthexia kaltval barbarianbracken barbarian  marshes gongburg omega scorchedcoast

HEX=python hex.py

fetch:
	curl -L "https://docs.google.com/spreadsheets/d/1IWhom7MIVIscN2ZEqM3UVsypCJLqWQOm1B7le4br9RM/export?format=csv" -o hexmaps/barbarian.csv
	curl -L "https://docs.google.com/spreadsheets/d/15N4beAStRAkS1nqKJ7Dt3owjo1vT_MZXVveh5muYgbc/export?format=csv" -o hexmaps/barbarianbracken.csv
	curl -L "https://docs.google.com/spreadsheets/d/1uhrVrgJ0Udh53jGcbWo8TBcRxCtVlcecIUllyuSNvOg/export?format=csv" -o hexmaps/marshes.csv
	curl -L "https://docs.google.com/spreadsheets/d/1CCkTx5YoK3ilFBsVWpAcUEQaimVsvZ3br3n2_rtLakY/export?format=csv" -o hexmaps/gongburg.csv
	curl -L "https://docs.google.com/spreadsheets/d/1HoEw1wqErcRJX7h8B2xYoqnT69494IiyTw82YqzDYPM/export?format=csv" -o hexmaps/omega.csv☝🏾
	curl -L "https://docs.google.com/spreadsheets/d/1YMsXboEy1F6rjtxsdD9QuoUyrQ9ikXkFU5V2G1LbBVA/export?format=csv" -o hexmaps/misericorde.csv

# curl -L https://dl.dropboxusercontent.com/u/125469/Code/Kaltval.csv > kaltval.csv
# curl -L -L https://dl.dropboxusercontent.com/u/125469/Code/MacysMutants.csv > fallout.csv
# curl -L -L https://dl.dropboxusercontent.com/u/125469/Code/Synthexia.csv > synthexia.csv


hexenbracken:
	$(HEX) hexmaps/$@.csv "The Hexenbracken" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Hexenbracken" > ../s.vs.tpk/grab-bag/$@/$@.txt

kraal:
	$(HEX) hexmaps/$@.csv "The Kraal" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Kraal" > ../s.vs.tpk/grab-bag/$@/$@.txt

wastes:
	$(HEX) hexmaps/$@.csv "The Colossal Wastes of Zhaar." > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Colossal Wastes of Zhaar." > ../s.vs.tpk/grab-bag/$@/$@.txt

fallout:
	$(HEX) hexmaps/$@.csv "The Fallout" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Fallout" > ../s.vs.tpk/grab-bag/$@/$@.txt

synthexia:
	$(HEX) hexmaps/$@.csv "Synthexia" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "Synthexia" > ../s.vs.tpk/grab-bag/$@/$@.txt

kaltval:
	$(HEX) hexmaps/$@.csv "The Kaltval" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Kaltval" > ../s.vs.tpk/grab-bag/$@/$@.txt

barbarian:
	$(HEX) hexmaps/$@.csv "The Kingdom of Argeld" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Kingdom of Argeld" > ../s.vs.tpk/grab-bag/$@/$@.txt

barbarianbracken:
	$(HEX) hexmaps/$@.csv "The Barbarian Prince" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Barbarian Prince" > ../s.vs.tpk/grab-bag/$@/$@.txt

marshes:
	$(HEX) hexmaps/$@.csv "The Lavender Marshes" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Lavender Marshes" > ../s.vs.tpk/grab-bag/$@/$@.txt

gongburg:
	$(HEX) hexmaps/$@.csv "The Lavender Marshes" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Lavender Marshes" > ../s.vs.tpk/grab-bag/$@/$@.txt

omega:
	$(HEX) hexmaps/$@.csv "Partol Sector Omega" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "Partol Sector Omega" > ../s.vs.tpk/grab-bag/$@/$@.txt

scorchedcoast:
	$(HEX) hexmaps/$@.csv "The Scorched Coast" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "The Scorched Coast" > ../s.vs.tpk/grab-bag/$@/$@.txt

misericorde:
	curl -L "https://docs.google.com/spreadsheets/d/1YMsXboEy1F6rjtxsdD9QuoUyrQ9ikXkFU5V2G1LbBVA/export?format=csv" -o hexmaps/misericorde.csv
	$(HEX) hexmaps/$@.csv "Misericorde" > ../s.vs.tpk/grab-bag/$@/index.html
	$(HEX) -f text hexmaps/$@.csv "Misericorde" > ../s.vs.tpk/grab-bag/$@/$@.txt


deploy:
	cd ../s.vs.tpk; make


# curl -L https://dl.dropboxusercontent.com/u/125469/Code/Kaltval.csv > kaltval.csv
# curl -L -L https://dl.dropboxusercontent.com/u/125469/Code/MacysMutants.csv > fallout.csv
# curl -L -L https://dl.dropboxusercontent.com/u/125469/Code/Synthexia.csv > synthexia.csv
