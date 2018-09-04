#!flask/bin/python

import io
import csv
import preprocessing
import clustering
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)

def csvToText(csvfile):
	content = io.StringIO(csvfile.stream.read().decode('utf-8'), newline=None)
	reader = csv.reader(content)
	text = []
	for line in reader:
		text.append(line[0])
	return text


def defaultStopWords():
	try:
		with open('stopwords.txt', 'r') as f:
			return set([line.strip() for line in f.readlines()])
	except:
		return set()

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET'])
def home():
	return make_response(jsonify({'status': 'Success',
	'endpoints': {
		'/pre': {
			'file': 'The CSV file to be preprocessed',
			'removePunct': 'Remove all punctuation when value is True. Default value is False',
			'minWords': 'Minimum number of words in phrase. Default value is 1',
			'removeStop': 'Remove stop words when value is True. Default value is False',
			'stopWords': 'User can specify stop words to be removed. Must be lower and separated by ;'
		}
	}}), 200)

@app.route('/pre', methods=['GET'])
def get_pre():
	return make_response(jsonify({'error': 'Please use the POST method uploading a CSV file with key \'file\''}), 400)

@app.route('/pre', methods=['POST'])
def post_pre():
	if 'file' not in request.files:
		return make_response(jsonify({'error': 'No file uploaded. Please upload a CSV file with key \'file\''}), 400)
	
	csvfile = request.files['file']

	if csvfile.filename.split('.')[-1] != 'csv':
		return make_response(jsonify({'error': 'Extension not allowed. Must be a CSV file'}), 415)
	
	text = csvToText(csvfile)

	removePunct = False
	minWords = 1
	removeStop = False
	stopWords = []

	if 'removePunct' in request.form and request.form['removePunct'] == 'True':
		removePunct = True
	
	if 'minWords' in request.form:
		minWords = int(request.form['minWords'])
	
	if 'removeStop' in request.form and request.form['removeStop'] == 'True':
		removeStop = True
	
	if removeStop:
		stopWords = defaultStopWords()
		if 'stopWords' in request.form:
			userSW = set(request.form['stopWords'].split('\n'))
			stopWords = stopWords.union(userSW)
	
	text = preprocessing.process(text, minWords, removePunct, removeStop, stopWords)

	if 'removeDuplicates' in request.form and request.form['removeDuplicates'] == 'True':
		text = list(set(text))
	
	outputStream = io.StringIO()
	writer = csv.writer(outputStream)
	for line in text:
		writer.writerow([line])

	output = make_response(outputStream.getvalue())
	output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
	output.headers['Content-type'] = 'text/csv'
	
	return output

@app.route('/clus', methods=['GET'])
def get_clus():
	return make_response(jsonify({'error': 'Please use the POST method uploading a CSV file with key \'file\''}), 400)

@app.route('/clus', methods=['POST'])
def post_clus():
	if 'file' not in request.files:
		return make_response(jsonify({'error': 'No file uploaded. Please upload a CSV file with key \'file\''}), 400)
	
	csvfile = request.files['file']

	if csvfile.filename.split('.')[-1] != 'csv':
		return make_response(jsonify({'error': 'Extension not allowed. Must be a CSV file'}), 415)
	
	text = csvToText(csvfile)
	
	numClusters = 5

	if 'clusters' in request.form:
		numClusters = int(request.form['clusters'])

	clusters = clustering.cluster(text, numClusters)

	outputStream = io.StringIO()
	writer = csv.writer(outputStream)
	writer.writerows(clusters)

	output = make_response(outputStream.getvalue())
	output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
	output.headers['Content-type'] = 'text/csv'
	
	return output

if __name__ == '__main__':
	app.run(debug=True)