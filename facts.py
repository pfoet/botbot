from willie import module
import re
from random import choice
from random import shuffle

f= open('channel.log')

nick = re.compile('.{6}<.(.*?)> .*')
line = re.compile('.*?> (.*)')
#comment = re.compile('^---')
#quit_part = re.compile('^.{6}-!-')
fact_finder = re.compile('.*? ([^ ]*) (?:ist|find ich) (?:(?:der|die|das|und|ein|en|eh|ja|so|doch|blos|mit|nicht|kein|keine|eine|nix|aber|schon|da|dann|man|was|es|ne|halt|eigentlich|nen|zwar|auch|dein|wenigstens|etwas|irgendwie|ist|mal) )* ?([^ ]+) .*')
lines = [ orig.decode('utf-8','ignore') for orig in f.read().splitlines()]
#data   = [(nick.match(x).group(1),line.match(x).group(1)) for x in lines if (nick.match(x) and line.match(x))]
facts_list = [ (z.group(1).lower(),z.group(2)) for z in [fact_finder.match(x) for x in lines if(fact_finder.match(x))]]
facts_dict = { word:list(set([z for otherword,z in facts_list if otherword==word])) for word in set([ x for x,y in facts_list])}
print(facts_dict)
print(set([ y for x,y in facts_list]))
@module.rule('was ist (.*)')
def factfact(bot, trigger):
    try:
        if trigger.group(1).lower() in facts_dict:
            bot.say(trigger.group(1)+' ist '+','.join(facts_dict[trigger.group(1).lower()]))
#        bot.say(choice([line for nick,line in data if (trigger.group(1) in line)]))
    except IndexError:
        pass
