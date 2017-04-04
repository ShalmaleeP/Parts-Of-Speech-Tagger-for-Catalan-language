from __future__ import division
from collections import defaultdict
import timeit
import codecs

start = timeit.default_timer()


file=codecs.open("catalan_corpus_train_tagged.txt",'r','UTF-8')
# file=open("sample_tagged",'r')
# file=codecs.open("sample_tagged",'r','UTF-8')
file_dat=file.read()
lines=file_dat.splitlines()
word_cnt=defaultdict(int)
tag_cnt=defaultdict(int)
wordwithtag_cnt=defaultdict(int)
start_tag=defaultdict(int)
last_tag=defaultdict(int)
tagfortrans=defaultdict(int)

file1=codecs.open("hmmmodel.txt",'w+','UTF-8')

# print "Line count:",len(lines)
for line in lines:
    words=line.split(" ")
    for word in words:
        word_len=len(word)
        tag=word[word_len-2:]
        wrd=word[:word_len-3]
        tag_cnt[tag] += 1
        word_cnt[wrd] += 1
        wordwithtag_cnt[word] += 1
    last_tag[tag] += 1
    # print wrd," tag=", tag

# print "Last tag:",last_tag

# print "TAGS:"
transition_prob=defaultdict()

for tag in tag_cnt:
    # print tag,"=",tag_cnt[tag]
    tagfortrans[tag] = tag_cnt[tag] - last_tag[tag]
    transition_prob[tag]=defaultdict(int)
    for tg in tag_cnt:
        transition_prob[tag][tg]=0

file1.write("%d\n"%len(tag_cnt))
file1.write("Start prob\n")

for line in lines:
    words = line.split(" ")
    prev = words[0]
    prev_len = len(prev)
    prev_tag = prev[prev_len - 2:]
    start_tag[prev_tag] += 1
    for word in words[1:]:
        word_len = len(word)
        tag = word[word_len - 2:]
        transition_prob[prev_tag][tag]+=1
        prev_tag = tag

# print tagfortrans

for tag in tag_cnt:
    prob=(start_tag[tag]+1)/(len(lines)+len(tag_cnt))
    file1.write("%s = %f\n"%(tag,prob))
    # print tag,"=",prob
file1.write("Transition prob\n")

for prev_tag in transition_prob:
    # print transition_prob[prev_tag]
    for tag in transition_prob[prev_tag]:
        # print tag,"|",prev_tag,"=",transition_prob[prev_tag][tag]
        prob = float((transition_prob[prev_tag][tag]+1)/(tagfortrans[prev_tag]+len(tag_cnt)))
        # print "P(", tag, "|",prev_tag,") = ", prob
        file1.write("P( %s | %s ) = %f\n"%(tag,prev_tag,prob))

# file1.write("probablity of tag given word\n")
#
# for word in wordwithtag_cnt:
#     prob1=float(wordwithtag_cnt[word]/word_cnt[word[:len(word)-3]])
#     print word[len(word)-2:],word[:len(word)-3],"=",prob1
#     file1.write("P( %s | %s ) = %f\n" % (word[len(word)-2:],word[:len(word)-3], prob1))
# for ln in wordwithtag_cnt:
#     print ln,"=>", wordwithtag_cnt[ln]

file1.write("probablity word given tag\n")

for word in wordwithtag_cnt:
    prob1=float(wordwithtag_cnt[word]/tag_cnt[word[len(word)-2:]])
    # print word[:len(word)-3],word[len(word)-2:],"=",prob1
    file1.write("P( %s | %s ) = %f\n" % (word[:len(word)-3], word[len(word)-2:], prob1))

stop = timeit.default_timer()

# print len(wordwithtag_cnt)

# print stop - start