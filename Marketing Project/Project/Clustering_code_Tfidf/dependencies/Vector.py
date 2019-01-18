import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from dependencies import Data_processing as da

def tfid_vector_test(train_texts):
  tfidf_vectorizer = TfidfVectorizer(vocabulary = pickle.load(open("feature.pkl", "rb")) ,max_df = 0.85, min_df = 0.1, sublinear_tf = True, stop_words = 'english', use_idf = True, tokenizer = da.tokenize, ngram_range = (1,10))
  tfidf_matrix = tfidf_vectorizer.fit_transform(train_texts)
  return tfidf_matrix

def tfid_vector_train(train_texts):
  tfidf_vectorizer = TfidfVectorizer(max_df = 0.85, min_df = 0.1, sublinear_tf = True, stop_words = 'english', use_idf = True, tokenizer = da.tokenize, ngram_range = (1,10))
  tfidf_matrix = tfidf_vectorizer.fit_transform(train_texts)
  pickle.dump(tfidf_vectorizer.vocabulary_,open("feature.pkl","wb"))
  return tfidf_matrix
