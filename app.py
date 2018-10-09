#!flask/bin/python
from flask import Flask
from apis import api

app = Flask(__name__)
api.init_app(app)

if __name__ == '__main__':
	app.run(debug=True)

# def csvToText(csvfile):
# 	content = io.StringIO(csvfile.stream.read().decode('utf-8'), newline=None)
# 	reader = csv.reader(content)
# 	text = []
# 	for line in reader:
# 		text.append(line[0])
# 	return text


# def defaultStopWords():
# 	try:
# 		with open('stopwords.txt', 'r') as f:
# 			return set([line.strip() for line in f.readlines()])
# 	except:
# 		return set()

# @app.errorhandler(404)
# def not_found(error):
# 	return make_response(jsonify({'error': 'Not found'}), 404)

# @app.route('/pre', methods=['POST'])
# def post_pre():

	
# 	outputStream = io.StringIO()
# 	writer = csv.writer(outputStream)
# 	for line in text:
# 		writer.writerow([line])

# 	output = make_response(outputStream.getvalue())
# 	output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
# 	output.headers['Content-type'] = 'text/csv'
	
# 	return output

# @app.route('/clus', methods=['POST'])
# def post_clus():
# 	if 'file' not in request.files:
# 		return make_response(jsonify({'error': 'No file uploaded. Please upload a CSV file with key \'file\''}), 400)
	
# 	csvfile = request.files['file']

# 	if csvfile.filename.split('.')[-1] != 'csv':
# 		return make_response(jsonify({'error': 'Extension not allowed. Must be a CSV file'}), 415)
	
# 	text = csvToText(csvfile)
	
# 	numClusters = 5

# 	if 'clusters' in request.form:
# 		numClusters = int(request.form['clusters'])

# 	clusters = clustering.cluster(text, numClusters)

# 	outputStream = io.StringIO()
# 	writer = csv.writer(outputStream)
# 	writer.writerows(clusters)

# 	output = make_response(outputStream.getvalue())
# 	output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
# 	output.headers['Content-type'] = 'text/csv'
	
# 	return output