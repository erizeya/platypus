from typeclasses.characters import Character
from evennia.utils import delay
from evennia.utils.utils import list_to_string
from evennia import create_object
import re

class Npc(Character):
    def at_post_unpuppet(self, account, session=None, **kwargs):
        pass

    def at_object_creation(self):
        super().at_object_creation()
        self.db.link = None

    def at_heard_say(self, message, from_obj):
        
        res = ""
        link = self.db.link

        #Populate menu items
        items = []
        for ware in link.db.wares:
            items.append(ware.lower())

        #Check if menu item is being asked for
        for item in items:
            pattern = r'{}\b'.format(item)
            pattern = re.compile(pattern)
            if re.search(pattern, message.lower()):
                res += f"Yeah. I can get you {item}, that'll be {link.db.wares[item.title()]} money."
                delay(2, self.serve, target=from_obj, item=item, amount=link.db.wares[item.title()])
                return res

        #Respond to hi
        if re.search(r"hi\b", message.lower()) or re.search(r"hey\b",message.lower()) or re.search(r"sup\b", message.lower()):
            res += "Hey there. "

        #Specific Responses
        if re.search(r"drink\b", message.lower()):
            res += "You want a drink? Check out the menu and tell me what you'd like."
        elif re.search(r"food\b", message.lower()) or re.search(r"eat", message.lower()):
            res += "You want a bite to eat? Take a look at the menu and let me know what sounds good."
        elif re.search(r"menu\b", message.lower()) and self.db.link:
            res += f"I can get you {list_to_string(items)}."
        elif link:
            res += "Let me know what I can get for you."

        return  res

    def respond(self, **kwargs):
        say = kwargs["say"]
        self.execute_cmd(f"say {say}")

    def serve(self, **kwargs):
        target = kwargs["target"]
        item = kwargs["item"].title()
        amount = int(kwargs["amount"])
        
        #Check target has enough funds
        if target.db.currency-amount < 0:
            self.execute_cmd(f"say Ah, actually. It doesn't look like you have enough money...")
            return

        #Deduct money from character
        target.db.currency -= amount
        target.msg(f"You pass some money to {self}")
        target.location.msg_contents(f"{target} passes some money to {self}.",exclude=target)

        #Check hands
        if self.db.l_hand or self.db.r_hand:
            self.execute_cmd(f"fh")

        new = create_object("typeclasses.consumable."+item, key="new drink")
        new.reset_name()
        self.execute_cmd(f"emote whips up a {new} at the {self.db.link}.")
        new.move_to(self, silent=True)
        self.db.r_hand = new
        self.execute_cmd(f"to {target} Here you go!")
        self.execute_cmd(f"give first {item} to {target}") 

    def msg(self, text=None, from_obj=None, **kwargs):
        "Custom msg() method reacting to say."

        if from_obj != self:
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
                        #self.execute_cmd(f"to {from_obj} {response}")
    
        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        super().msg(text=text, from_obj=from_obj, **kwargs)
