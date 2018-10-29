from flask_restplus import Namespace, Resource, Api, reqparse
from flask import make_response
from werkzeug.datastructures import FileStorage
from io import StringIO
import csv
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

api = Namespace('tfidf', description='Convert a collection of documents to a matrix of TF-IDF features')
parser = api.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True)
parser.add_argument('n_words', location='form', type=int, required=False)

def get_tfidf(text, n_words):
	vectorizer = TfidfVectorizer()
	response = vectorizer.fit_transform(text)	
	features = vectorizer.get_feature_names()
	tfidf = []
	
	for ind, sentence in enumerate(text):
		row = np.squeeze(response[ind].toarray())
		n_ids = np.argsort(row)[::-1][:n_words]
		n_features = [(features[i], row[i]) for i in n_ids if row[i] > 0] #retornar apenas os tfidfs maior que 0
		tfidf.append(n_features)
	return tfidf
	

@api.route('')
# @api.expect(parser, validate=True)
@api.doc(parser=parser)
class Tfidf(Resource):
	def post(self):
		args = parser.parse_args()
		n_words = args['n_words'] if args['n_words'] else 8
		
		csvfile = args['file']
		content = StringIO(csvfile.stream.read().decode('utf-8'), newline=None)
		reader = csv.reader(content)
		text = [' '.join(line) for line in reader]
		
		result = get_tfidf(text, n_words)
		
		outputStream = StringIO()
		writer = csv.writer(outputStream)
		for line in result:
			writer.writerow(line)
		output = make_response(outputStream.getvalue())
		output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
		output.headers['Content-type'] = 'text/csv'
		
		return output