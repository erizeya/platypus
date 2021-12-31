from typeclasses.characters import Character

class Npc(Character):
    """
    A NPC typeclass which extends the character class.
    """
    def at_heard_say(self, message, from_obj):
        """
        A simple listener and response. This makes it easy to change for
        subclasses of NPCs reacting differently to says.

        """
        # message will be on the form `<Person> says, "say_text"`
        # we want to get only say_text without the quotes and any spaces
        if "drink" in message:
            message = "You want a drink? Check out the menu and tell me what you'd like."
        elif "food" in message or "eat" in message:
            message = "You want a bite to eat? Take a look at the menu and let me know what sounds good."

        # we'll make use of this in .msg() below
        return  message

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
                        self.execute_cmd(f"to {from_obj} {response}")
    
        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        super().msg(text=text, from_obj=from_obj, **kwargs)
