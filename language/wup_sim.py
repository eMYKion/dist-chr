#THIS CODE IS NOT MINE I TOOK IT FROM alvas
#source: https://stackoverflow.com/questions/18871706/check-if-two-words-are-related-to-each-other

from nltk.corpus import wordnet as wn
from itertools import product

def wup_score(word1, word2):
    
    sem = [wn.synsets(word1), wn.synsets(word2)]

    maxscore = 0
    
    for i,j in list(product(sem[0], sem[1])):

        #Wu-Palmer Similarity
        score = i.wup_similarity(j)
        
        if(score == None):
            score = 0.0
        
        maxscore = score if maxscore < score else maxscore

    return maxscore
