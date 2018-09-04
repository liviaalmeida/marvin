from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from gensim.models import KeyedVectors
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