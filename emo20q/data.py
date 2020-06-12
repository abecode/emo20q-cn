#!/usr/bin/env python3
#!/usr/bin/python

import os
import re
import sys

class Tournament():
    def games(self):
        return self._games
    def __add__(self,other):
        t = Tournament()
        t._games = []
        t._games.extend(self.games())
        t._games.extend(other.games())
        return t


class HumanHumanTournament(Tournament):
    """A set of emo20q games played by two humans"""

    def __init__(self, annotationFile=None):
#        self.base = Base()
        if not annotationFile:
            import os
            annotationFile = os.path.dirname(__file__) + "/../wechat_pilot/emo20q_glossing_final_anonymous.txt"
        f = open(annotationFile, 'r', encoding="utf-8")
        try:
            self._games = [m for m in self.readGames(f)]
            #for m in self.readGames(f):
            #    print(m.turns[0])
        finally:
            f.close()

    def readGames(self,fh):
        games = []
        while True:
            line = fh.readline()
            #print(line)
            if not line:
                break
            game = Game()
            turns = []
            if re.match("match:\d+", line):
                m = re.match("match:\d+, ?answerer:(?P<answerer>.+?), ?questioner:(?P<questioner>.+?), ?start:\"(?P<start>.+?)\"", line)
                # note game/match records do not all have level
                game.answerer = m.group('answerer')
                game.questioner = m.group('questioner')
                game.start = m.group('start')
                turns = [turn for turn in game.readTurns(fh)]
                line = fh.readline()
                m = re.match(r"end:\"(?P<end>.+?)\", ?emotion:(?P<emotion>.+?), ?questions:(?P<questions>.+?), ?outcome:(?P<outcome>.+?)(, ?.*)", line)
                game._end = m.group('end');
                game._emotion = m.group('emotion');
                game._questions = m.group('questions');
                game._outcome = m.group('outcome');
                game._turns = turns
                #print(game._emotion)
                yield(game)


    def printStats(self):
        print("there are {0:d} games".format(len(t.games)))
        #sum up the turns
        sumTurns = 0
        for m_idx,m in enumerate(t.games):
            assert isinstance(m,Game)
            assert type(m._turns) == list
            print("  In game {0:d} there are {1:d} turns.".format(m_idx,len(m.turns)))
            for tn_idx,tn in enumerate(m.turns()):
                assert isinstance(tn,Turn)
                #further tests
                sumTurns = sumTurns + len(m.turns())

        print("In all, there are {0:d} turns.".format(sumTurns))


class Game(object):
    """An emo20q game instance"""

    def turns(self):
        return self._turns
    def emotion(self):
        return self._emotion



    def readTurns(self,fh):
        while True:
            turn = Turn()
            question = ""
            answer   = ""
            qgloss   = ""
            agloss   = ""
            while True:
                line = fh.readline()
                #print("question: "+line)
                if not line:
                    break
                if re.match("end:", line):
                    fh.seek(fh.tell() - len(line.encode("utf-8")),
                            os.SEEK_SET)
                    return
                if re.match("^ *$", line):
                    continue
                elif re.match("gloss:", line):
                    m = re.match("gloss:{(.*)}", line)
                    qgloss = m.group(1)
                    break
                else:
                    question += line

            while True:
                line = fh.readline()
                #print("answer: "+line)
                if not line:
                    break
                if re.match("end:", line):
                    fh.seek(fh.tell() - len(line.encode("utf-8")),
                            os.SEEK_SET)
                    break
                if re.match("-", line):
                    continue
                elif re.match("gloss:", line):
                    m = re.match("gloss:{(.*)}", line)
                    agloss = m.group(1)
                    break
                else:
                    answer += line

            turn.q = question.strip()
            turn.qgloss = qgloss.strip()
            turn.a = answer.strip()
            turn.agloss = agloss.strip()
            #ignore non-yes-no questions and their answers
            if "non-yes-no" in turn.agloss: continue
            if "non-yes-no" in turn.qgloss: continue
            yield turn

class Turn(object):
    """One of the question/answer pairs from and emo20q game"""

    def questionId(self):
        return self.qgloss
    def answerId(self):
        ans = "other"
        if "agloss" in self.__dict__:
            if self.agloss.find("yes") == 0 : ans = "yes"
            if self.agloss.find("no") == 0 : ans = "no"
        else:
            if self.a.lower().find("yes") == 0 : ans = "yes"
            if self.a.lower().find("no") == 0 : ans = "no"

        return ans

class Question(object):
    """Keeps track of question strings"""

    def __init__(self,q,gloss):
        self.q = q
        self.gloss = gloss

class Answer(object):
    """Keeps track of answer strings"""

    def __init__(self,a,gloss):
        self.a = a
        self.gloss = gloss



if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description="""study information contained in the gloss file """)
    parser.add_argument('-e', '--emotions',
                           action='store_true',
                           help='print list of emotions, from end: annotation')
    parser.add_argument('-w', '--webpage',
                           default=False,
                           help='generate a webpage rendering of the data')
    # can add new arguments to argparser  to implement new features
    # e.g     parser.add_argument('-p', '--players', ...

    args = parser.parse_args()
    if args.emotions:  # if -e or --emotion flag is used
        # read in tournament
        t = HumanHumanTournament()
        assert isinstance(t, Tournament) # t is Tournament class
        assert type(t.games() ) == list # games() returns a list
        for g in t.games():
            print(g.emotion())
    if args.webpage:  # if --html flag is used
        if not os.path.isdir(args.webpage):
            sys.exit(args.webpage + " must be a directory")
        from jinja2 import Template, Environment, BaseLoader
        import jieba
        basetemplate = Environment(loader=BaseLoader).from_string("""
        <html>
        <head>
        <title>{% block title %}{% endblock %}</title>
        </head>
        <body>
        {% block body %}{% endblock %}
        </body>
        </html>
        """)
        index =  Template("""
        <html>
        <head>
        <title> EMO20Q-CN Index </title>
        </head>
        <body>
        <h1>EMO20Q-CN Index</h1>
        <ul>
          {% for game in games %}
          <li>
            <a href="{{ loop.index0 }}.html">  Game:{{ loop.index0}} </a>, 
            Questioner: {{ game.questioner }}, Answerer: {{ game.answerer }}, 
            Emotion: 
              <a href="https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={{ game.emotion() }}">
                {{ game.emotion() }} </a>, 
            Turns: {{ game.turns() |length }}
          </li>
        {% endfor %}
        </ul>
        </body>
        </html>
        """)

        dialog =  Template("""
        <html>
        <head>
        <title> EMO20Q-CN Game/Dialog </title>
        </head>
        <body>
        <h1>EMO20Q-CN Game/Dialog</h1>
        <ul>
          {% for turn in turns %}
          <li> Turn {{ loop.index }}
            <ul>
              <li> Question: </li>
                {% for word in cut(turn.q) %}
                <a href="https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={{ word }}">
                {{ word }} 
                </a>
                {% endfor %}
              <li> Answer:  </li>
                {% for word in cut(turn.a) %}
                <a href="https://www.mdbg.net/chinese/dictionary?page=worddict&wdrst=0&wdqb={{ word }}">
                {{ word }} 
                </a>
                {% endfor %}
            </ul>
          </li>
        {% endfor %}
        </ul>
        </body>
        </html>
        """)

        # read in tournament
        t = HumanHumanTournament()
        assert isinstance(t, Tournament) # t is Tournament class
        assert type(t.games() ) == list # games() returns a list
        games = [g for g in t.games()]
        with open(os.path.join(args.webpage, "index.html"), "w") as f:
            print(index.render(games=games), file=f)

        for i, game in enumerate(games):
            with open(os.path.join(args.webpage, str(i)+".html"), "w") as f:
                print(dialog.render(turns=game.turns(), cut=jieba.cut), file=f)
            
    else:
        parser.print_help()
