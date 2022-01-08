from evennia import Command
from custom import genderize

class CmdWear(Command):
    """
     Wear a wearable item such as clothing or armor.
    
     Usage:
      wear [item]
    """
    key = "wear"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        count = None

        if not self.args:
            caller.msg("What do you want to wear?")
        else:
            obj = caller.multiple_search(target_obj)
            if not obj:
                return
            #Check if the object is wearable
            if not obj.db.wearable:
                caller.msg(f"How are you expecting to wear your {obj.name}?")

            #Check if the object is already being worn
            elif obj.db.wearing:
                caller.msg(f"You are already wearing your {obj.name}")

            #If checks pass, equip item
            else:
                caller.msg("You put on your %s" % obj.name)
                caller.location.msg_contents(genderize(f"{caller.name} puts on %p {obj.name}",caller.db.gender),exclude=caller)
                obj.db.wearing = True
                caller.db.worn[obj.db.coverage].append(obj)

