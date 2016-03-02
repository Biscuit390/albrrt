import random
import json
from re import sub

try:
    Recents = json.loads(RWFile)
    Associations = json.loads(WAFile)
    Starters = json.loads(SWFile)
    RWFile = open("RecentWords.json","r+")
    WAFile = open("WordAssociations.json","r+")
    SWFile = open("StartingWords.json","r+")
except:
    print("Failed to load files")
    Recents = []
    Associations = {}
    Starters = []

#Add words to the list of recently used words, as well as add associations.
def read(WordString):
    print("Reading words...")
    global Recents
    global Associations

    sub('[^\.\w]', '', WordString)
    Words = WordString.lower().split(" ")
    for I in range(0,len(Words)-1):
        W = Words[I]
        if W != '':
            Recents.append(W)
            T = list(W)

            if not (W in Associations):
                Associations[W] = []

            if W[-1] != ".":
                Associations[W].append(Words[I+1])

            Recents.append(removeperiod(W))
            try:
               if I == 0:
                   Starters.append(W)
               elif Words[I-1][-1] == ".":
                   Starters.append(W)
            except:
                print("hurr")
    print(Associations)
    trim()
    
def trim():
    global Associations
    global Recents
    try:
        while Recents[5000]:
            Recents.pop(0)
    except:
        pass
    for A in Associations:
        print(A)
    
def removeperiod(word):
    T = list(word)
    for x in T:
        if x == ".":
            T.pop(T.index(x))
    return str(T)
