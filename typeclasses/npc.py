from typeclasses.characters import Character
from evennia.utils import delay
import re

class Npc(Character):
    def at_post_unpuppet(self, account, session=None, **kwargs):
        pass

    def at_object_creation(self):
        super().at_object_creation()

    def at_heard_say(self, message, from_obj):
        
        res = None
        return  res

    def respond(self, **kwargs):
        say = kwargs["say"]
        self.execute_cmd(f"say npc respond called.")
        self.execute_cmd(f"say {say}")

    def ignore(self, **kwargs):
        caller = kwargs["caller"]
        self.execute_cmd(f"pose seem to ignore {caller}.")

    def msg(self, text=None, from_obj=None, **kwargs):
        "Custom msg() method reacting to say."

        if "subclass" in kwargs.keys():
            from_subclass = True
        else:
            from_subclass = False

        if from_obj != self and not from_subclass:
            # make sure to not repeat what we ourselves said or we'll create a loop
            try:
                say_text, is_say = text[0], text[1]['type'] == 'to'
            except Exception:
                is_say = False
            if is_say:
                #Check if directed
                if " [to You]: " in text[0]:
                    # First get the response (if any)
                    response = self.at_heard_say(say_text, from_obj)
                    # If there is a response
                    if response != None:
                        # speak ourselves, using the return
                        delay(1, self.respond, say=response)
                    else:
                        delay(1, self.ignore, caller=from_obj)
    
        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        super().msg(text=text, from_obj=from_obj, **kwargs)
