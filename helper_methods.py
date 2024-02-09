import re



# アイ、あわ-れ、あわ-れむai, awa-re, awa-remu
# 18,囲,圍,囗,7,5,,surround,イ、かこ-む、かこ-うi, kako-mu, kako-u
# 19,医,醫,酉,7,3,,doctor,イi
# 37,遺,,辵,15,6,,bequeath,イ、（ユイ）i, (yui)
t1 = "アイ、あわ-れ、あわ-れむai, awa-re, awa-remu"
t2 = "イ、かこ-む、かこ-うi, kako-mu, kako-u"
t3 = "イi"
t4 = "イ、（ユイ）i, (yui)"

def list_kanji(text):
    return re.findall(r"[一-龯]{1}", text)


def strip_kanji(text):
    return re.sub(r"[^一-龯]+", "", text)


def remove_citations(text):
    return re.sub(r"\[\d+\]", "", text)

    
def merge_parentheses(text):
    text = re.sub(r"、[ 　]*（", "（", text)
    return re.sub(r",[ 　]*\(", "(", text)


def comma2sep(text, sep="|"):
    return re.sub(r"[ 　]*[,、][ 　]*", sep, text)


def separate_en_jp(index, text):
    matches = list(re.finditer(r"[ぁ-～][(A-Za-zĀ-ſ]", text))
    if len(matches) != 1:
        message = f"Found no boundary between jp text and en text:\nLine {index}: {text}"
        print(message)
    else:
        boundary = (matches[0].span()[0]) + 1
        return { "jp" : text[:boundary], "en" : text[boundary:] }

def parse_readings(index, text, sep="|", show_romaji=False):
    text = remove_citations(text)
    text = merge_parentheses(text)
    text = comma2sep(text)
    readings = separate_en_jp(index, text)
    kun_readings = []
    on_readings = []
    jp = readings["jp"].split(sep)
    en = readings["en"].split(sep)
    for jp_word, en_word in zip(jp, en):
        group = f"{jp_word}|{en_word}" if show_romaji else jp_word
        if re.match(r"[ぁ-ゖ]", jp_word) != None:
            kun_readings.append(group)
        else:
            on_readings.append(group)
    return { "kun" : sep.join(kun_readings), "on" : sep.join(on_readings) }

# for test in [t1, t2, t3, t4]:
#     print(test)
#     test = merge_parentheses(test)
#     test = comma2sep(test)
#     test = parse_readings(test)
#     print(test)
#     print("-----------------------")