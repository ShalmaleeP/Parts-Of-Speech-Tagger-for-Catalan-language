from __future__ import division
from collections import defaultdict
import math

import timeit
import codecs

start = timeit.default_timer()

file=codecs.open("hmmmodel.txt",'r','UTF-8')
data=file.read()
lines=data.splitlines()

tagcount=int(lines[0])
# print "No of tags",tagcount

# print "Start prob"
# tag_list=defaultdict()
start_prob=defaultdict(float)
for line in lines[2:tagcount+2]:
    elems=line.split(" ")
    start_prob[elems[0]]=float(elems[2])
    # print line
    # print elems[0]," = ",start_prob[elems[0]]

vocab=defaultdict(int)


transition_prob=defaultdict()
abc=tagcount+tagcount*tagcount+3
# print lines[tagcount+tagcount*tagcount+3]
for line in lines[tagcount+3:tagcount+tagcount*tagcount+3]:
    elems=line.split(" ")
    prev=elems[3]
    cur=elems[1]
    if prev not in transition_prob:
        transition_prob[prev]=defaultdict(float)
    transition_prob[prev][cur]=float(elems[6])

# for prev_tag in transition_prob:
#     print prev_tag, " ", transition_prob[prev_tag]

wordgiventag=defaultdict(dict)

curpos=tagcount+tagcount*tagcount+4

for line in lines[curpos:]:
    words = line.split(" ")
    word = words[1]
    tag = words[3]
    wordgiventag[tag][word]=float(words[6])
    vocab[word]+=1


# print "Length",len(vocab)

tomod=codecs.open("catalan_corpus_dev_raw.txt",'r','UTF-8')
data1=tomod.read()
lines1=data1.splitlines()

f1 = codecs.open("hmmoutput.txt","w+","utf-8")

for line1 in lines1:
    words = line1.split(" ")
    startword = words[0]
    linedict = defaultdict(dict)
    back_pointer_array = defaultdict(dict)
    for tg in start_prob:
        linedict[tg] = {}
        if startword in vocab:
            if startword in wordgiventag[tg]:
                linedict[tg][1] = math.log(start_prob[tg]) + math.log(wordgiventag[tg][startword])
            else:
                linedict[tg][1] = math.log(start_prob[tg])+ float("-inf")
        else:
            linedict[tg][1] = math.log(start_prob[tg])
        back_pointer_array[tg][1] = u"start"

    for time_instance in range(2,len(words)+1):
        curr = time_instance - 1
        for tg in start_prob:
            maximum = float("-inf")
            for prev_tg in start_prob:
                if words[curr] in vocab:
                    if words[curr] in wordgiventag[tg]:
                        val = linedict[prev_tg][curr] + math.log(transition_prob[prev_tg][tg]) + math.log(wordgiventag[tg][words[curr]])
                    else:
                        val = linedict[prev_tg][curr] + math.log(transition_prob[prev_tg][tg]) + float("-inf")
                else:
                    val = linedict[prev_tg][curr] + math.log(transition_prob[prev_tg][tg])
                if val >= maximum:
                    maximum = val
                    linedict[tg][time_instance] = val
                    back_pointer_array[tg][time_instance] = prev_tg
    # print linedict
    # print back_pointer_array

    max3 = float("-inf")
    T = len(words)
    for x in linedict:
        if linedict[x][T] > max3:
            max3 = linedict[x][T]
            tail = x
    # print backpointer
    # print probability_array
    ctr = len(words)
    ans = []
    while ctr > 0:
        if ctr == len(words) :
            ans.append(words[ctr - 1] + u"/" + tail)
        else:
            ans.append(words[ctr - 1] + u"/" + tail + u" ")
        # print tail
        tail = back_pointer_array[tail][ctr]
        ctr -= 1
    for x in reversed(ans):
        f1.write(x)
    f1.write("\n")
f1.close()
# print("--- %s seconds ---" % (time.time() - start_time))
# f.close()

stop = timeit.default_timer()
# print stop-start
