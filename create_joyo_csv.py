from bs4 import BeautifulSoup
from pprint import pprint
import re
from helper_methods import *
from freq_data import freq_data
from jlpt_data import jlpt_data

with open("List of jōyō kanji - Wikipedia.htm", "r", encoding="utf8") as s:
    html = s.read()

soup = BeautifulSoup(html, "html.parser")

def kanji_table_search(tag):
    return tag.has_attr('class') and tag["class"] == "sortable wikitable jquery-tablesorter".split(" ")

kanji_table = soup.find(kanji_table_search)

kanji_chars = []



with open("joyo.csv", "w", encoding="utf8") as o:
    o.write("")
with open("joyo.csv", "a", encoding="utf8") as o:
    headers = "index,kanji,kanji_old,radical,strokes,grade,year,meanings,on,kun,frequency,jlpt\n"
    o.write(headers)
    for row in kanji_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) >= 9:
            index = cells[0].text
            kanji = strip_kanji(cells[1].text)
            kanji_old = strip_kanji(cells[2].text)
            radical = cells[3].text
            strokes = cells[4].text
            grade = cells[5].text
            year = cells[6].text
            meanings = comma2sep(cells[7].text)
                        
            cols = [remove_citations(col) for col in [index, kanji, kanji_old, radical, strokes, grade, year, meanings]]

            # Extract on and kun readings
            readings = parse_readings(index, cells[8].text)
            on = readings["on"]
            kun = readings["kun"]
            
            # Lookup frequency
            kanji = cols[1]
            frequency = "9999999"
            if kanji in freq_data:
                frequency = str(freq_data[kanji])
            
            # Lookup jlpt
            kanji = cols[1]
            jlpt = "0"
            if kanji in jlpt_data:
                jlpt = str(jlpt_data[kanji])
            
            cols = cols + [on, kun, frequency, jlpt]
            
            o.write(",".join(cols) + "\n")