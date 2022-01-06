from evennia import Command


class CmdEat(Command):
    """
    Eat a currently held food item
     Usage: 
      eat <edible item>
    """
    key = "eat"
    help_category = "General"

    def func(self):
        caller = self.caller
        location = caller.location
        target_obj = self.args.strip()

        if not target_obj:
            caller.msg("Eat what?")
            return

        obj = caller.multiple_search(target_obj)
        if not obj:
            return

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
