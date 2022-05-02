import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
import nltk
import pandas as pd
DATA_FILE = "./data/yikyak.csv"

stemmer = SnowballStemmer("english")

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
# Tokenize and lemmatize
def preprocess(text):
    result=[]
    for token in gensim.utils.simple_preprocess(text) :
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

def main():
    yikyaks = pd.read_csv(DATA_FILE)["content"]
    data = []
    for yak in yikyaks:
        if not isinstance(yak, str):
            continue
        data.append(preprocess(yak))

    dictionary = gensim.corpora.Dictionary(data)
    bow_corpus = [dictionary.doc2bow(doc) for doc in data]
    
    # document_num = 1
    # bow_doc_x = bow_corpus[document_num]

    # for i in range(len(bow_doc_x)):
    #     print("Word {} (\"{}\") appears {} time.".format(bow_doc_x[i][0], 
    #                                                     dictionary[bow_doc_x[i][0]], 
    #                                                     bow_doc_x[i][1]))
    
    lda_model =  gensim.models.LdaMulticore(bow_corpus, 
                                   num_topics = 5, 
                                   id2word = dictionary,                                    
                                   passes = 30,
                                   workers = 3)
    
    for idx, topic in lda_model.print_topics(-1):
        print("Topic: {} \nWords: {}".format(idx, topic ))
        print("\n")
    
if __name__ == "__main__":
    main()