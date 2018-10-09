from flask_restplus import Namespace, Resource, Api, reqparse
from flask import make_response
from werkzeug.datastructures import FileStorage
from io import StringIO
import csv

import re
import string
import nltk

re_brackets = re.compile(r'\{.*\}')
re_html = re.compile(r'<(\/|\\)?.+?>', re.UNICODE)
re_dates = re.compile(r'\d{1,2}[/-]\d{1,2}[/-]*[\d{2}\d{4}]*', re.UNICODE)

re_punct = re.compile(r'['+string.punctuation+'°'+r']+', re.UNICODE)

re_numbers = re.compile(r'\d', re.UNICODE)
re_emails = re.compile(r'[^\s]+@[^\s]+', re.UNICODE)
re_url = re.compile(r'(http|https)://[^\s]+', re.UNICODE)

re_quotes = re.compile(r'(?u)[‘’`′“”"\']', re.UNICODE)
re_hyphen = re.compile(r'\W[–-]|[–-]\W')

re_trim = re.compile(r' +', re.UNICODE)

def cleanString(sentence):
    """Apply all regex above to a given string."""

    sentence = sentence.lower()

    sentence = re_brackets.sub('', sentence)
    sentence = re_html.sub(' ', sentence)
    sentence = re_dates.sub('DATE', sentence)
    sentence = re_numbers.sub('0', sentence)
    sentence = re_emails.sub('EMAIL', sentence)
    sentence = re_url.sub('URL', sentence)

    sentence = re_quotes.sub('', sentence)
    sentence = re_hyphen.sub(' ', sentence)
    sentence = re_trim.sub(' ', sentence)

    return sentence.strip()


def process(text, minWords, removePunct, removeStop):

    with open('files/stopwords.txt') as f:
        stopWords = [line.strip() for line in f.readlines()]

    text = [cleanString(phrase) for phrase in text]
    tokensList = [nltk.wordpunct_tokenize(phrase) for phrase in text]
    for phrase in tokensList:
        while phrase.count('-'):
            i = phrase.index('-')
            if i == len(phrase)-1:
                break
            phrase[i-1] += phrase[i] + phrase[i+1]
            phrase.pop(i+1)
            phrase.pop(i)
    if removePunct:
        tokensList = [[tk for tk in tokens if re_punct.fullmatch(tk) == None] for tokens in tokensList]
    if removeStop:
        tokensList = [[tk for tk in tokens if tk not in stopWords] for tokens in tokensList]
    text = [' '.join(tokens) for tokens in tokensList if sum(tk.isalpha() for tk in tokens) >= minWords]

    return text


api = Namespace('pre', description='Preprocess your text')

parser = api.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True)
parser.add_argument('minWords', location='form', type=int)
parser.add_argument('removePunct', location='form', type=bool)
parser.add_argument('removeStop', location='form', type=bool)

@api.route('')
# @api.expect(parser, validate=True)
@api.doc(parser=parser)
class Preprocessor(Resource):
    def post(self):
        args = parser.parse_args()

        minWords = args['minWords'] if args['minWords'] else 1
        removePunct = True if args['removePunct'] else False
        removeStop = True if args['removeStop'] else False

        csvfile = args['file']
        content = StringIO(csvfile.stream.read().decode('utf-8'), newline=None)
        reader = csv.reader(content)
        text = [' '.join(line) for line in reader]

        text = process(text, minWords, removePunct, removeStop)
        
        outputStream = StringIO()
        writer = csv.writer(outputStream)
        for line in text:
            writer.writerow([line])

        output = make_response(outputStream.getvalue())
        output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
        output.headers['Content-type'] = 'text/csv'

        return output