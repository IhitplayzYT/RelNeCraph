import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from consts import STOPWORDS
from helper import help
from errors import ERRNO
import sys


stop_words,stemmer = None,None

def init_nltk():
    global stop_words,stemmer
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer()



def preproc(doc: str) -> str:
    doc = doc.lower()
    if not stop_words or not stemmer:
        init_nltk() 
    
    text = re.sub(r'[^a-z0-9\s\.,:;\?]','', doc)
    tokens = text.split()
    if not stop_words:
        print("Depenedency NLTK not found: Stopwords Not Found")
        sys.exit(ERRNO.E_HELP)
    tokens = [t for t in tokens if t not in stop_words]
    if not stemmer:
        print("Depenedency NLTK not found: Stemmer Not Found")
        sys.exit(ERRNO.E_HELP)
       
    tokens = [stemmer.stem(t) for t in tokens]

    return " ".join(tokens)

