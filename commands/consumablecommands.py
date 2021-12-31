
from evennia import Command
from evennia import CmdSet
from evennia import default_cmds

# Eat a currently held food item
#  Usage: 
#   eat
#
class CmdEat(Command):
    key = "eat"

    def func(self):
        caller = self.caller
        location = caller.location
        obj = self.obj

        obj.db.charges -= 1
        if obj.db.untouched:
            message = obj.db.messages["first_consume"]
            message = obj.db.messages["taste"]
            obj.db.untouched = False
        elif obj.db.charges < 1:
            message = obj.db.messages["last_consume"]
            obj.delete()
        else:
            message = obj.db.messages["consume"]
        caller.msg(message)
        return

# Eat a currently held food item
#  Usage: 
#   drink
#
class CmdDrink(Command):
    key = "drink"

    def func(self):
        caller = self.caller
        location = caller.location
        obj = self.obj

        if caller.db.l_hand == obj or caller.db.r_hand == obj:
            obj.db.charges -= 1
            if obj.db.untouched:
                message = obj.db.messages["first_consume"]
                message = obj.db.messages["taste"]
                obj.db.untouched = False
            elif obj.db.charges < 1:
                message = obj.db.messages["last_consume"]
                obj.delete()
            else:
                message = obj.db.messages["consume"]
            caller.msg(message)
            return
        else:
            caller.msg(f"You have to hold your {obj} to drink it.")

class FoodCmdSet(CmdSet):
    """
    For binding commands
    """
    key = "foodcmdset"

    def at_cmdset_creation(self):
        self.add(CmdEat())

class DrinkCmdSet(CmdSet):
    """
    For binding commands
    """
    key = "drinkcmdset"

    def at_cmdset_creation(self):
        self.add(CmdDrink())
