from evennia import Command
from custom import genderize
import re

# Takes a list and returns it in pair tuples.
# [a, b, c, d, e] -> [(a,b), (c,d)]
def pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

class CmdPose(Command):
    """
    strike a pose

    Usage:
      pose <pose text>
      pose's <pose text>

    Example:
      pose is standing by the wall, smiling.
       -> others will see:
      Tom is standing by the wall, smiling.

    Describe an action being taken. The pose text will
    automatically begin with your name.
    """

    key = "pose"
    aliases = ["."]
    locks = "cmd:all()"
    arg_regex = None

    

    def func(self):
        caller = self.caller
        args = "."+self.args.strip()
        c_msg = "You "
        o_msg = caller.name+" "
        quotes = []

        #Find and store quoted strings
        l = [m.start() for m in re.finditer(r'\"', args)]
        if len(l) % 2 != 0:
            caller.msg("Unmatched quotes")
            return
        for x in pairwise(l):
            q = args[x[0]+1:x[1]]
            quotes.append(q)


        #Remove quotes
        count = 0
        for quote in quotes:
            args = args.replace(quote, f"@{count}@")
            count = count + 1


        #Split
        arg_list = args.split(" ")

        #Verb substituion
        for word in arg_list:
            #Check for a marked verb we need to subtitute.
            if word[0] == ".":
                #Take out the period.
                word = word[1:]

                #Sometimes we'll have some punctuation at the end of the word.
                l = [m.start() for m in re.finditer(r'[^a-zA-Z]',word)]
                punct = ""
                if l:
                    #Verify the word ends with some punctuation.
                    if l[-1] == len(word)-1:
                        #Store the punctuation then remove it.
                        punct = word[l[-1]]
                        word = word[:-1] 

                #Convert the verb and readd the punctuation
                c_msg += f"{word}{punct} "
                o_msg += f"{word}s{punct} "
            else:
                c_msg += f"{word} "
                o_msg += f"{word} "

        #my substition
        c_msg = c_msg.replace("my", "your")
        o_msg = o_msg.replace("my", "%p")
        c_msg = c_msg.replace("I", "you")
        o_msg = o_msg.replace("I", "%s")


        #Fix capitals
        c_list = re.split('\. |! |\? ', c_msg)
        for item in c_list:
            if item:
                c_msg = c_msg.replace(item, item[0].upper()+item[1:])

        o_list = re.split('\. %?|! %?|\? %?', o_msg)
        for item in o_list:
            if item:
                o_msg = o_msg.replace(item, item[0].upper()+item[1:])

        #Reinsert quotes
        count = 0
        for quote in quotes:
            c_msg = c_msg.replace("@"+str(count)+"@", quote)
            o_msg = o_msg.replace("@"+str(count)+"@", quote)
            count = count + 1

        #Issue messages
        caller.msg(c_msg)
        for content in caller.location.contents:
            if content != caller:
                content.msg(genderize(o_msg.replace(content.name,"you"),caller.db.gender))
