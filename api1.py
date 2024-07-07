import re
import nltk
import time
from nltk.corpus import words, stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('words')
nltk.download('stopwords')

class StatementAnalyzer:
    def __init__(self):
        self.dictionary = set(words.words())
        self.profanity_list = {'bad', 'stupid', 'shit'} 
        self.stop_words = set(stopwords.words('english'))
    
    def find_incorrect_spellings(self, text):
        tokens = word_tokenize(text)
        misspelled = [word for word in tokens if word.lower() not in self.dictionary and word.isalpha()]
        return misspelled
    
    def find_profanity_words(self, text):
        tokens = word_tokenize(text)
        profanity = [word for word in tokens if word.lower() in self.profanity_list]
        return profanity
    
    def find_nouns(self, text):
        tokens = word_tokenize(text)
        tagged = pos_tag(tokens)
        nouns = [word for word, pos in tagged if pos in ('NN', 'NNS')]
        return sorted(nouns, key=len)
    
    def analyze(self, text):
        incorrect_spellings = self.find_incorrect_spellings(text)
        profanity_words = self.find_profanity_words(text)
        nouns = self.find_nouns(text)
        return {
            'incorrect_spellings': incorrect_spellings,
            'profanity_words': profanity_words,
            'nouns': nouns
        }

if __name__ == "__main__":
    st = time.time()
    analyzer = StatementAnalyzer()
    result = analyzer.analyze("This is a test with stupid and incorect spelling. logikal kowedle")
    et = time.time()
    print(result)
    print(f"total script runtime {(et-st)/60} minutes")
