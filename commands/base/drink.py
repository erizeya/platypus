from evennia import Command

class CmdDrink(Command):
    """
    Eat a currently held food item
     Usage:
      drink <drinkable item>
    """
    key = "drink"
    help_category = "General"

    def func(self):
        caller = self.caller
        location = caller.location
        target_obj = self.args.strip()

        if not target_obj:
            caller.msg("Drink what?")
            return

        obj = caller.multiple_search(target_obj)
        if not obj:
            return

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
