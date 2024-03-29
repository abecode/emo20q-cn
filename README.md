# Emotion Twenty Questions in Chinese

Emotion Twenty Questions (emo20q) is a game for collecting language
about how people talk about emotions and an artificial intelligence
task to imitate this verbal behavior.

The Emotion Twenty Questions in Chinese (emo20q_cn) is a project to
play emo20q in Chinese.  

## Links

- this github repo (emo20q-cn): https://github.com/abecode/emo20q-cn
- the github pages: https://abecode.github.io/emo20q-cn/
- private repo (contains raw data that may have private info, available to students who have completed IRB training): https://github.com/abecode/emo20q-cn-private

## Getting Started

```
pip3 install -r requirements.txt
```

## Past Work

- [English EMO20Q](https://github.com/abecode/emotion-twenty-questions)
  - This is not very well organized.  I made it when I was in grad
    school before I was following good programming practices.  It was
    written in Python 2.7 originally.  I've updated it so it runs with
    Python 3 but haven't had rigorous testing (the old code had
    doctest but it should have a unit testing component)
	
	
## Current Work

- Human-human emo20q in Chinese collected from WeChat (raw files not available publicly due to private data)
	```
	./wechat_pilot/groupchat*txt
	```
- Annotations/glosses
	```
	./wechat_pilot/emo20q_glossing_final.txt # not available publically
	./wechat_pilot/emo20q_glossing_final_anonymous.txt
	```

- some scripts:
  
  - split dialogs into turns:
	``` .
	./split_wechat.py 
	```
  - extract the list of emotions that players chose:
	```
	./emo20q/data.py -e
	```
  - generate html ./docs directory from the annotation/gloss file
	```
	./emo20q/data.py -w docs
	```
	
## To Do's 

- Refactoring old emo20q code
  - separate dialog engine from emo20q implementation
  - add better testing.  I like doctest but probably better to use
    pytest

- Figure out Windows newline difference
  - using ```unix2dos wechat_pilot/emo20q_glossing_final.txt ```
    worked but it would be good to have a more convenient solution.

- IDEA: translate README to Chinese

- IDEA: study use of WeChat emojis

- ...

## Contributors and Maintainers

Because this repository is a public version of a more active private 
repository, many commits have been removed/squashed and thus we acknowledge 
contributions here.

- Shanshan Kong [@sskong85](https://github.com/sskong85) collected and annotated the data on WeChat
- Abe Kazemzadeh [@abecode](https://github.com/abecode) maintains the repository and is the point of contact with the [University of St. Thomas IRB](https://stthomas.edu/irb)
