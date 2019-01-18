import nltk
def get_stopwords(path):
  stopwords = nltk.corpus.stopwords.words('english')
  not_words = []
  with open(path,'r') as f:
    not_words.append(f.readlines())
  not_words = [word.replace('\n','') for words in not_words for word in words]
  not_words = set(not_words)
  stopwords = set(stopwords)
  customized_stopwords = list(stopwords - not_words)
  return stopwords,customized_stopwords

