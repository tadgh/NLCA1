import re
sentence_split_regex = re.compile(r"(\.\.+\s?)(?=[A-Z])|([?!]+)|(\.\s)|(\.$)")
url_regex = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
secondary_url_regex = re.compile(r'[a-z]+\.(com|ca|edu|net|io|ly|gov|mil|int|cn|uk|de|jp|fr|au)', flags=re.IGNORECASE)
token_split_regex = re.compile(r"(\?+|!+|\.+|\'s?|.'[^s]|\s+)")