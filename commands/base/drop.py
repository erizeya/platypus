from evennia import Command

class CmdDrop(Command):
    """
    Lets you drop an object from your inventory into the
    location you are currently in.
    
    Usage:
      drop <obj>
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Drop what?")
            return

        #Detect if we're looking for multiple
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        #Remove the item from hands if held
        if caller.db.l_hand == obj:
            caller.db.l_hand = None
        elif caller.db.r_hand == obj:
            caller.db.r_hand = None

        success = obj.move_to(caller.location, quiet=True)

        if not success:
            caller.msg("This couldn't be dropped.")
        else:
            caller.msg(f"You drop {obj.name}.")
            caller.location.msg_contents(f"{caller.name} drops {obj.name}", exclude=caller)
            # Call the object script's at_drop() method.
            obj.at_drop(caller)
