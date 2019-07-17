#!/usr/bin/env python3

from pathlib import Path 
import re
import sys
import jieba

class Utterance():
    def __init__(self, username, ts, content):
        self.username = username
        self.ts = ts
        self.content = content
    def words(self):
        return jieba.cut(self.content)

datadir = "wechat_pilot"
pathlist = Path(datadir).glob("*.txt")
turnregex = re.compile(r'(?P<username>[^\s]+?)'
                       r'(?P<ts>\d{1,2}:\d\d.M)')
users = set()
datadir = "wechat"


for x in pathlist:
    utterances = list()
    print(x)
    with open(x, 'r', encoding='utf-8', errors='ignore') as f:
        #for line in f:
        #    print(line)
        try:
            buf = f.read()
        except UnicodeDecodeError as e:
            # this is an error that may be from improper encoding 
            print(e, file=sys.stderr)
        #print(buf)
        matches = list(turnregex.finditer(buf))
        #matches = list(re.findall(r'.*', buf))
        for i, match in enumerate(matches):
            #print(match)
            contentstart = match.end()
            contentend = matches[i+1].start()\
              if i+1 < len(matches)\
              else len(buf)
            username = match.group('username')
            ts = match.group('ts')
            content = buf[contentstart:contentend]
            users.add(username)
            u = Utterance(username, ts, content)
            utterances.append(u)
            
print(users)
for u in utterances:
    print(u.username, ":", " ".join(u.words()))
