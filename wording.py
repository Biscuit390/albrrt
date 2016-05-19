import random
import json
from re import sub
from random import randint,choice,shuffle

Recents = []
FWWords = {}
Starters = []
BWWords = {}
FWFile,WAFile,SWFile,BWFile = None,None,None,None
        

def getWords():
    global FWFile
    global WAFile
    global SWFile
    global RWFile
    global Recents
    global FWWords
    global BWWords
    global Starters
    RWFile = open("RecentWords.json","r+")
    FWFile = open("FWWords.json","r+")
    SWFile = open("StartingWords.json","r+")
    BWFile = open("BWWords.json","r+")
    print("read")
    Recents = json.loads(RWFile.read())
    print("1")
    FWWords = json.loads(FWFile.read())
    print("2")
    Starters = json.loads(SWFile.read())
    print("3")
    BWWords = json.loads(BWFile.read())
    RWFile.close()
    FWFile.close()
    SWFile.close()
    BWFile.close()
    #print("Failed to load files")

#Add words to the list of recently used words, as well as add FWWords.
def read(WordString):
    print("Reading words...")
    if passcensor(WordString):
        global Recents
        global FWWords
        global BWWords
        global Starters
        sub('[^\.\w]', '', WordString)
        TW = WordString.lower().split("\n")
        Words = []
        for x in TW:
            for y in x.split(" "):
                Words.append(y)
        for I in range(0,len(Words)):
            W = Words[I]
            if W != '':
                Recents.append(W)
                T = list(W)
                
                if not (W in FWWords):
                    FWWords[W] = []
                    BWWords[W] = []
                
                if not W[-1] in (".","?","\n","!"):
                    try:
                        FWWords[W].append(Words[I+1])
                    except BaseException as e:
                        print(e)
                        
                try:
                    BWWords[W].append(Words[I-1])
                except BaseException as e:
                    print(e)
                #Recents.append(removeperiod(W))
                try:
                   if I == 0:
                       Starters.append(W)
                   elif Words[I-1][-1] in (".","?","\n","!","\""):
                       Starters.append(W)
                except:
                    print("hurr")
        #print(FWWords)
        #print(Starters)
        trim()
    else:
        print("a bad word")
    
def trim():
    global FWWords
    global Recents
    global Starters
    global BWWords
##    try:
##        while Recents[40000]:
##            Recents.pop(0)
##    except:
##        pass
##    for A in FWWords:
##        try:
##            while FWWords[A][40]:
##                FWWords[A].pop(0)
##        except:
##            pass
##    for A in BWWords:
##        try:
##            while BWWords[A][40]:
##                BWWords[A].pop(0)
##        except:
##            pass
##    try:
##        while Starters[1000]:
##            Starters.pop(0)
##    except:
##        pass
    for x in Recents:
        if not passcensor(x):
            Recents.pop(Recents.index(x))
    print(len(Recents),len(FWWords),len(Starters))
##def removeperiod(word):
##    T = list(word)
##    for x in T:
##        if x == ".":
##            T.pop(T.index(x))
##    s = []
##    for x in T:
##        s += x
##    return s

def writesentence(word):
    word = word.lower()
    writing = []
    writing.append(word)
    wtw = randint(1,35)
    for I in range(0,wtw):
        gotword = False
        try:
            shuffle(FWWords[writing[I]])
            for newword in FWWords[writing[I]]:
                if newword in Recents:
                    gotword = True
                    break
                    
            if not gotword:
                raise IndexError
        except IndexError as e:
            newword = choice(Recents)
            print(e)
        except KeyError as e:
            newword = choice(Recents)
            print(e)
        writing.append(newword)
    written = ""
    for x in writing:
        #print(x)
        written +=str(x)+" "
    #print(written)
    return written

def save():
    try:
        global FWFile
        global RWFile
        global SWFile
        global BWFile
        RWFile = open("RecentWords.json","r+")
        FWFile = open("FWWords.json","r+")
        SWFile = open("StartingWords.json","r+")
        BWFile = open("BWWords.json","r+")
        print(1)
        RWFile.truncate()
        print("A")
        FWFile.truncate()
        print("B")
        SWFile.truncate()
        print("C")
        BWFile.truncate()
        print(2)
        RWFile.write(json.dumps(Recents))
        FWFile.write(json.dumps(FWWords))
        SWFile.write(json.dumps(Starters))
        BWFile.write(json.dumps(BWWords))
        print(3)
        FWFile.close()
        RWFile.close()
        SWFile.close()
        BWFile.close()
    except BaseException as e:
        print(e)

def randomthought():
    try:
        return writesentence(choice(Starters))
    except IndexError:
        return writesentence(choice(Recents))


def passcensor(words):
    didpass = True
    Bad = ['fuck','porn','yiff','pee','defecate','autis','bitch','anal','douche','shit','gay','daddy','dick','tit','cis','cunt','sjw','cum','sex','dildo','penis','nigg','bugger']
    for x in Bad:
        if x in words.lower():
            didpass = False
            print("A bad word")
            break
    return didpass
