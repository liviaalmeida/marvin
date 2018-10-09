from flask_restplus import Namespace, Resource, Api, reqparse
from flask import make_response
from werkzeug.datastructures import FileStorage
from io import StringIO
import csv

from sklearn.cluster import KMeans
from gensim.models import KeyedVectors, Word2Vec
import numpy as np

model = KeyedVectors.load('models/model.model', mmap='r')

def getVocab(text):
    vocab = set()
    for phrase in text:
        for word in phrase.split(' '):
            if word.isalpha():
                vocab.add(word)
    return vocab

def sentence2Vec(sentence):
    global model
    wordsVec = [model.word_vec(word) for word in sentence.split(' ') if word in model.vocab]
    sumVec = np.zeros(300)
    for vec in wordsVec:
        sumVec += vec
    return sumVec/len(wordsVec) if len(wordsVec) else sumVec

def cluster(text, numCluster):
    kmeans = KMeans(n_clusters=numCluster, init='k-means++')
    senVecs = [sentence2Vec(sentence) for sentence in text]
    data = kmeans.fit_predict(senVecs)
    return sorted([[sentence, clu] for sentence, clu in zip(text, data)], key=lambda x: x[1])

api = Namespace('clus', description='Cluster your text')

parser = api.parser()
parser.add_argument('file', location='files', type=FileStorage, required=True)
parser.add_argument('numClusters', location='form', type=int, required=True)

@api.route('')
# @api.expect(parser, validate=True)
@api.doc(parser=parser)
class Clustering(Resource):
    def post(self):
        args = parser.parse_args()

        csvfile = args['file']
        content = StringIO(csvfile.stream.read().decode('utf-8'), newline=None)
        reader = csv.reader(content)
        text = [' '.join(line) for line in reader]

        numClusters = args['numClusters'] if args['numClusters'] else 3

        clusters = cluster(text, numClusters)
        
        outputStream = StringIO()
        writer = csv.writer(outputStream)
        writer.writerows(clusters)

        output = make_response(outputStream.getvalue())
        output.headers['Content-Disposition'] = 'attachment; filename=output.csv'
        output.headers['Content-type'] = 'text/csv'

        return output