import nltk
from sklearn.cluster import KMeans
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def tagText(text):
   return [TaggedDocument(nltk.word_tokenize(phrase), [i]) for i, phrase in enumerate(text)]


def cluster(text, numCluster):
   tagged = tagText(text)
   model = Doc2Vec(tagged)
   model.train(tagged, total_examples=model.corpus_count, epochs=20, start_alpha=0.002, end_alpha=-0.016)
   kmeans = KMeans(n_clusters=numCluster, init='k-means++', max_iter=200)
   X = kmeans.fit(model.docvecs.vectors_docs)
   labels = kmeans.labels_.tolist()
   l = kmeans.fit_predict(model.docvecs.vectors_docs)
   pca = PCA(n_components=2).fit(model.docvecs.vectors_docs)
   datapoint = pca.transform(model.docvecs.vectors_docs)
   
   plt.figure
   label1 = ["#3D5899", "#960200", "#46CE53", "#FFD046", "#EA31AC"]
   color = [label1[i] for i in labels]
   plt.scatter(datapoint[:, 0], datapoint[:, 1], c=color)