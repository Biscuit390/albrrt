import random
import json
from re import match

RWFile = open("RecentWords.json")
WAFile = open("WordAssociations.json")
try:
    Recents = json.loads(RWFile)
    Associations = json.loads(WAFile)
except:
    print("Failed to load files")
    Recents = []
    Associations = {}

#Add words to the list of recently used words, as well as add associations.
def read(WordString):
    print("Reading words...")
    global Recents
    global Associations
    
    Words = WordString.split(" ")
    for I in range(0,len(Words)-1):
        W = Words[I]
        Recents.append(W)
        T = list(W)
        print("Removing punctuation...")
        for C in range(0,len(T)-1):
            if not T[C].isalpha():
                T.pop(C)
                print(T[C])
        if not (W in Associations):
            Associations[W] = []
        Associations[W].append(Words[I+1])

    print(Associations)
    
def trim():
    global Associations
    global Recents
    pass
