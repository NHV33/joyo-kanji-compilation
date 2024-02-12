import csv

kanji = []

with open('joyo.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        kanji.append(row['kanji'])
        line_count += 1
        if line_count % 100 == 0:
            print(f'Processed {line_count} lines.')

with open('kanji_string.txt', 'w', encoding='utf8') as o:
    o.write("".join(kanji))
