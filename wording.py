import random
import json

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
def read():
    pass
