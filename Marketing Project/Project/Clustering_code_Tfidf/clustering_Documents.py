""### Import Statements"""

import os
import random
import nltk
import re
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle
from sklearn.externals import joblib

from dependencies import Get_stopwords as g
from dependencies import Load_data as d
from dependencies import Data_processing as da
from dependencies import Vector as v
from dependencies import Elbow as e


"""### Downloading extra dependencies from NLTK"""

#nltk.download('punkt')
#nltk.download('stopwords')


"""### Getting stopwords customized to your problem statement"""

#Use this function to create custom list of stop_words for your Project

path = r'C:\Users\devda\Desktop\Document-Clustering-TFIDF-master\Git Clustering\Stopwords\stopwords_not_to_be_used.txt' #Add the path to stopwords_not_to_be_used.txt file
stop_words,customized_stopwords = g.get_stopwords(path)


"""### Loading the Data"""

path = r'C:\Users\devda\Desktop\Document-Clustering-TFIDF-master\Git Clustering\Articles' #Add the path to Articles folder
seed = 137 #Seed value
train_texts = d.load_data(path,seed)


"""### Tokenizing the document and filtering the tokens"""

vocab_tokenized,vocab_stemmed,total_words = da.generate_vocab(train_texts)


"""### Calculating Tf-idf matrix"""

'''
Attributes in TfidVectorizer are data dependent. 
Use 'stop_words = customized_stopwords' if you want to use your own set of stopwords else leave it as it is.
Functions available for tokenizer -> 1)tokenize  2) tokenize_stem  3) Remove the attribute to use default function
''' 

tfidf_matrix = v.tfid_vector_train(train_texts)
print(tfidf_matrix.shape)

"""### Clustering Using K - Means"""

#Code For Elbow Method
e.elbow_curve(start = 1,end = 10,tfidf_matrix= tfidf_matrix)

'''
#Uncomment the below code after getting appropriate k value from the graph

K_value =   4   #Write the optimum K-value after seeing the Elbow Graph
km = KMeans(n_clusters = K_value, n_init = 2000, max_iter = 6000, precompute_distances = 'auto' )
clusters = km.fit_transform(tfidf_matrix)

#filename = 'finalized_model.sav'
pickle.dump(km,open('model4.sav','wb'))
#joblib.dump(km, 'model2.sav')



#loaded_model = pickle.load(open('model3.sav', 'rb'))
#result = loaded_model.predict(tfidf_matrix)
#print(result)

#clusters = list(clusters)
#print(clusters)

'''





