import nltk
from nltk.stem.snowball import SnowballStemmer
import re
"""### Tokenizing the document and filtering the tokens"""
def tokenize(train_texts):
  filtered_tokens = []
  tokens = [word for sent in nltk.sent_tokenize(train_texts) for word in nltk.word_tokenize(sent)]
  for token in tokens:
    if re.search('[a-zA-Z]',token):
      filtered_tokens.append(token)
  return filtered_tokens


"""### Tokenizing and stemming using Snowball stemmer"""

def tokenize_stem(train_texts):
  tokens = tokenize(train_texts)
  stemmer = SnowballStemmer('english')
  stemmed_tokens = [stemmer.stem(token) for token in tokens]
  return stemmed_tokens



"""### Generating the vocab for problem statement"""
def generate_vocab(train_texts):
  vocab_tokenized = []
  vocab_stemmed = []
  total_words = []
  for text in train_texts:
    allwords_tokenized = tokenize(text)
    total_words.append(allwords_tokenized)
    vocab_tokenized.extend(allwords_tokenized)    
    allwords_stemmed = tokenize_stem(text)
    vocab_stemmed.extend(allwords_stemmed)
  return vocab_tokenized,vocab_stemmed,total_words

