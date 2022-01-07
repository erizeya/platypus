from evennia.commands.command import Command as BaseCommand
from custom import genderize

class CmdLower(BaseCommand):
    """
    Lower a held item from being in-hand to inventory.

    Usage:
      lower <item>
          Lower the specific in-hand item and return it to the inventory.
      lower-left/lower-right
          Lower the item held in the left or right hand.
    """

    key = "lower"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Lower what?")
            return

        #Case for lower-left and lower-right
        if "-left" in self.args:
            caller.msg(f"You put your {caller.db.l_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.l_hand} away.", caller.db.gender), exclude=caller)
            caller.db.l_hand = None
            return
        if "-right" in self.args:
            caller.msg(f"You put your {caller.db.r_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.r_hand} away.", caller.db.gender), exclude=caller)
            caller.db.r_hand = None
            return

        #Search for the object
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        #Makre sure we're holding the object
        if caller.db.r_hand == obj:
            caller.db.r_hand = None
        elif caller.db.l_hand == obj:
            caller.db.l_hand = None
        else:
            caller.msg(f"You are not holding {self.args.strip()}.")
            return

        #Message player and room
        caller.msg(f"You put your {obj} away.")
        caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} away.",caller.db.gender), exclude=caller)

