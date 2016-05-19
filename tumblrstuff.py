from tumblpy import Tumblpy,TumblpyError
from time import sleep
from random import randint,choice,shuffle
from importlib import reload
import wording
import string
import json
import re

others = json.loads(open('other.json').read())
keys = json.loads(open('keys.json').read())
t = Tumblpy(keys["YOUR_CONSUMER_KEY"], keys["YOUR_CONSUMER_SECRET"],keys['YOUR_API_KEY'],keys['YOUR_API_SECRET'])
Names = others['names']

Reblogged = []
others['names'] = lastreblogged = ""
lrbcount = 0
LA = ""
Testing = False

def getreblogged():
    RFile = open("RepliedPosts.json","r+")
    Reblogged = json.loads(RFile.read())
    RFile.close()
    return Reblogged

def setreblogged(Reblogged):
    RFile = open("RepliedPosts.json","r+")
    RFile.truncate()
    RFile.write(json.dumps(Reblogged))
    RFile.close()
    
def getsubmissions():
    try:
        x = t.get('blog/'+others['botblog']+'/posts/submission',params = {"filter" : "text"})['posts']
        x.reverse()
        return x
    except IndexError as e:
        print("ER",e)

##def gettagged():
##    Reblogged = getreblogged()
##    rt = []
##    try:
##        tagged = t.get('tagged',params = {'tag' : ''+others['botblog']+'','filter' : 'text'})
##        for post in tagged:
##            d = open("debug.txt",'r+',encoding = 'utf-8')
##            d.write(str(post))
##            if not post['reblog_key'] in Reblogged:
##                try:
##                    if wording.passcensor(post['reblog']['comment']):
##                        rt.append(post)
##                except:
##                    raise
##    except BaseException as e:
##        raise
##
##    #print(tagged)
##    #print(rt)
##    return rt

    
def getAR():
    Reblogged = getreblogged()
    print("T")
    try:
        x = []
        tT = t.get('blog/'+others['yourblog']+'/posts/text',params = {"filter" : "text"})['posts']
        for p in tT:#
            if not p['reblog_key'] in Reblogged and "a_r" in p['tags'] and wording.passcensor(p['body']):
                x.append(p)

    except TumblpyError as e:
        print("ER",e)
    return x

##def respondtags():
##    print("RT")
##    didreply = False
##    try:
##        tagged = gettagged()
##        for post in tagged:
##            try:
##                #print(post['comment'])
##                wording.read(post['body'])
##                comment = wording.writesentence(post['reblog']['comment'].split(' ')[randint(0,len(post['reblog']['comment']))])
##                parameters = {"id" : str(post['id']),
##                              "reblog_key" : post['reblog']['reblog_key'], 
##                              "state" : "published",
##                              "answer" : comment,
##                              "tags" : "crikey, reply,"+addtags(comment),
##                              "filter" : "text"
##                               }
##                t.post("blog/'+others['botblog']+'/post/reblog",params=parameters)
##                setreblogged(getreblogged().append(post['reblog']['reblog_key']))
##                didreply = true
##                break
##            except:
##                pass
##    except BaseException as e:
##        #print("ER:",e)
##        raise
##    return didreply

def answer():
    global Names
    global LA
    global ErrorState
    submissions = getsubmissions()
    didreply = False
    namefail = False
    x = 0
    for z in submissions:
        try:
            #print("i:",z['id'])
            #print("q:",z['question'])
            print("Q:",z['asking_name'])
            if wording.passcensor(z['question']):
                if LA != z['asking_name']:
                    #re.sub(unwanted,'',z['question'])
                    if not z['question'][-1] in (".","?",",","!"):
                        wording.read(z['question']+".")
                    else:
                        wording.read(z['question'])
                    LA = z['asking_name']
                    
                    try:
                        name = Names[z['asking_name']]
                    except KeyError:
                        name = z['asking_name']
                    if not 'crab' in z['question'].lower():
                        post = "hi "+name+",\n"+wording.writesentence(z['question'].split(" ")[randint(0,len(z['question'].split(" ")))-1])
                    else:
                        post = "hi "+name+",\n"+"crab "*randint(1,20)
                    #print("a:",post)
                    parameters = {"id" : str(z['id']),
                                  "state" : "published",
                                  "answer" : post,
                                  "tags" : "crikey, answer, "+str(z['asking_name'])+","+addtags(post),
                                  "filter" : "text"
                                   }
                    #print("p:",parameters)
                    print("r:",t.post("blog/'+others['botblog']+'/post/edit",params=parameters))
                    didreply = True
                    break
                else:
                    namefail = True
            else:
                t.post("blog/"+others['botblog']+"/post/delete",params = {'id' : z['id']})
            ErrorState = 0
        
        except IndexError as e:
            x = 0
            LA = ""
            print("ER",e)
        except TumblpyError as e:
            print("ER",e)
    if not didreply and namefail:
        LA = ""
        didreply = answer()
    return didreply

def reblogtagged():
    Reblogged = getreblogged()
    RFile = open("RepliedPosts.json","r+")
    Reblogged = json.loads(RFile.read())
    RFile.close()
    didreply = 0
    try:
        new = getAR()
        for n in new:
            #re.sub(unwanted,'',n['body'])
            #n['body'])
            wording.read(n['body'])
            comment = wording.writesentence(n['body'].split(" ")[randint(0,len(n['body'].split(" ")))-1])
            #print("b:",n['body'])
            #print("c:",comment)
            print(t.post("blog/'+others['botblog']+'/post/reblog",params={"id" : n['id'],
                                                             "reblog_key" : n['reblog_key'],
                                                             "comment" : comment,
                                                              "tags" : "crikey, reply, "+addtags(comment)
                                                                }))
            Reblogged.append(n['reblog_key'])
            didreply = 1
    except TumblpyError as e:
        print("ER",e)
    setreblogged(Reblogged)
    return didreply


def shitpost():
    try:
        thought = wording.randomthought()
        print(t.post("blog/"+others['botblog']+"/post",params={"type" : "text",
                                                    "tags" : "random thought, crikey,"+addtags(thought),
                                                    "body" : thought
                                                    }))
    except TumblpyError as e:
        print("ER",e.error_code, e)

def addtags(words):
    ts = ""
    tags = []
    Planes = {"f15","a-10","a10","f-22","f22","f-15","plane","airliner","boeing","lockheed","aircraft","fighter"}
    if any([x in words.lower() for x in Planes]):
        tags.append(u"\u2708")
    if 'crab' in words.lower():
        tags.append('crab')
    for x in tags:
        ts += x+", "
    return ts

def reblogfromothers():
    Reblogged = getreblogged()
    #chance = randint(0,100)
    robots = others['robots']
    shuffle(robots) 
    #print("R:",chance)
    didreply = 0
    if True: #0 <= chance <= 100:
        for bot in robots:
            try:
                botpost = t.get("blog/"+bot+"/posts/text",params = {"filter" : "text"})['posts'][0]
                print("b:",bot)
                #print("S:",botpost['body']+'\n')
                if wording.passcensor(botpost['body']) and not botpost['reblog_key'] in Reblogged and not 'dnr' in botpost['tags']:
                    #botpost['body'])
                    #re.sub(unwanted,'',botpost['body'])
                    comment = wording.writesentence(botpost['body'].split(" ")[randint(0,len(botpost['body'].split(" ")))-1])
                    #print("C:",comment)
                    t.post("blog/"+others['botblog']+"/post/reblog",params = {"id" : botpost['id'],
                                                                  "reblog_key": botpost['reblog_key'],
                                                                  "comment" : comment,
                                                                  "tags" : "crikey, reply, "+bot+", "+addtags(comment)
                                                                  })
                    Reblogged.append(botpost['reblog_key'])
                    setreblogged(Reblogged)
                    wording.read(botpost['body'])
                    didreply = 1
                    break
            except TumblpyError as e:
                print("ER",e)
            except IndexError as e:
                print("ER",e)
            except UnicodeEncodeError as e:
                print("ER",e)
    if not didreply:
        print("left posts with none replyable")
    return didreply

while True:
    try:
        reload(wording)
        wording.getWords()
        reblogtagged()
        if answer():
            pass
        #elif respondtags():
        #   pass
        elif reblogfromothers():
            pass
        else:
            shitpost()
        wording.trim()
        wording.save()
    except KeyboardInterrupt as e:
        raise
    except AttributeError as e:
        print("probably hit post limit or somehting")
    if Testing:
        sleep(10)
    else:
        sleep(345)

