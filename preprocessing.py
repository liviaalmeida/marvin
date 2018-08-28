"""
All emails are mapped to a EMAIL token.
All numbers are mapped to 0 token.
All urls are mapped to URL token.
HTML strings are removed.
All text between brackets are removed.
...
"""

import re
import nltk
import string


# ##### #
# Regex #
# ##### #
re_brackets = re.compile(r'\{.*\}')
re_html = re.compile(r'<(\/|\\)?.+?>', re.UNICODE)
re_numbers = re.compile(r'\d', re.UNICODE)
re_emails = re.compile(r'[^\s]+@[^\s]+', re.UNICODE)
re_url = re.compile(r'(http|https)://[^\s]+', re.UNICODE)

re_separateDots = re.compile(r'(?<=\.)(?=[^\s])', re.UNICODE)

re_quotes = re.compile(r'(?u)[‘’`′“”"\']', re.UNICODE)
re_hyphen = re.compile(r'[–-]')

re_trim = re.compile(r' +', re.UNICODE)


def cleanString(text, removePunct):
    """Apply all regex above to a given string."""

    text = text.lower()

    text = re_brackets.sub('', text)
    text = re_html.sub(' ', text)
    text = re_numbers.sub('0', text)
    text = re_emails.sub('EMAIL', text)
    text = re_url.sub('URL', text)

    text = re_separateDots.sub(' ', text)

    text = re_quotes.sub('', text)
    text = re_hyphen.sub('', text)
    text = re_trim.sub(' ', text)

    return text.strip()


def process(text, removePunct, minWords, removeStop, stopWords):

    text = [cleanString(phrase, removePunct) for phrase in text]
    tokensList = [nltk.word_tokenize(phrase) for phrase in text]
    if removePunct:
        tokensList = [[tk for tk in tokens if tk not in string.punctuation] for tokens in tokensList]
    if removeStop:
        tokensList = [[tk for tk in tokens if tk not in stopWords or tk != '...'] for tokens in tokensList]
    text = [' '.join(tokens) for tokens in tokensList if sum(tk.isalpha() for tk in tokens) >= minWords]

    return text