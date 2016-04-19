from wording50k import *
import multiprocessing

corecount = 8 #use real processors, not logical
fiftykay = ""

def multi_randthought(proccount=corecount):
    global fiftykay
    wordsperproc = 51000/proccount
    print(wordsperproc)
    getWords()
    fiftykay += randomthought(wordsperproc)
    print(len(fiftykay))
    print(proccount)
    k50 = open("50k.txt","a+",errors="ignore")
    k50.write(fiftykay)

if __name__ == "__main__":
    k50 = open("50k.txt","w+",errors="ignore")
    k50.close()
    jobs = []
    for i in range(corecount):
        p = multiprocessing.Process(target=multi_randthought, args=[corecount])
        jobs.append(p)
        p.start()
    print("start")
    for proc in jobs:
        proc.join()
    print("join")
    #stillalive = True
    #while stillalive:
    #    stillalive = sum([x.is_alive() for x in jobs])
    #print("alive")
    #print(len(fiftykay))
    #k50.write(fiftykay)
    
