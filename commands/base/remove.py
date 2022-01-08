from evennia import Command
from custom import genderize

class CmdRemove(Command):
    """
    Remove a wearable object
    
    Usage:
      remove [item]
    """

    key = "remove"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        count = None

        if not self.args:
            caller.msg("What do you want to remove?")
        else:

            obj = caller.multiple_search(target_obj)
            if not obj:
                return

            #Check if the object is worn
            if not obj.db.wearing:
                caller.msg("You are not wearing your %s." % obj.name)

            #If checks pass, equip item
            else:
                #Make sure nothing is over the item
                if caller.db.worn[obj.db.coverage][-1].id != obj.id:
                    caller.msg(f"You are wearing something over your {obj.name}.")
                else:
                    caller.msg(f"You take off on your {obj.name}.")
                    caller.location.msg_contents(f"{caller.name} takes off their {obj.name}.",exclude=caller)
                    obj.db.wearing = False
                    caller.db.worn[obj.db.coverage].pop()
