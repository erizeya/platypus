from evennia import Command
from custom import genderize

class CmdHold(Command):
    key = "hold"
    locks = "cmd:all()"

    """
    Takes an item that is currently in inventory and puts it into a free hand.
    
    Usage:
      hold <item>
          Puts item in the right hand, left if right is not free.
      hold[-left/-right] <item>
          Puts an item specifically into the left or right hand.
    """

    def func(self):
        caller = self.caller
        count = None
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Hold what?")
            return

        #Split out left/right arg.
        arg_list = self.args.split(" ")
        target_hand = None
        if arg_list[0].strip() == "-left":
            target_hand = "left"
            target_obj = " ".join(arg_list[1:])
        elif arg_list[0].strip() == "-right":
            target_hand = "right"
            target_obj = " ".join(arg_list[1:])

        #Search for object
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        #Case for wearing item
        if obj.db.wearing:
            caller.msg("You cannot hold something you're wearing.")

        #Case for both hands full
        elif caller.db.r_hand == obj or caller.db.l_hand == obj:
            caller.msg(f"You are already holding {obj}.")

        #Case for target_handed left hand but its full
        elif target_hand == "left" and not caller.db.l_hand == None:
            caller.msg("Your left hand is full")
        #Case for target_handed right hand but its full
        elif target_hand == "right" and not caller.db.r_hand == None:
            caller.msg("Your right hand is full.")

        #Case for empty right hand
        elif caller.db.r_hand == None and not target_hand == "left":
            caller.db.r_hand = obj
            caller.msg(f"You take your {obj} into your right hand")
            caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} in %p left hand",caller.db.gender), exclude=caller)

        #Case for empty left hand
        elif caller.db.l_hand == None and not target_hand == "right":
            caller.db.l_hand = obj
            caller.msg(f"You take your {obj} into your left hand")
            caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} in %p right hand",caller.db.gender), exclude=caller)

        else:
            caller.msg("Your hands are full.")
