from evennia import Command
class CmdDoorside(Command):
    """
    Admin commands for toggling which side of a door faces "out"
    
    Usage:
        !doorside <door>
    """
    key = "!doorside"
    locks = "cmd:perm_above(Helper)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        location = caller.location
        args = self.args.strip()

        obj = caller.multiple_search(args, location=caller.location)

        if not obj:
            return

        if not obj.db.door:
            caller.msg("!doorside can only be used on doors.")
            return

        if not obj.db.pair:
            caller.msg("!doorside can only be used on paired doors.")
            return
        
        pair = obj.db.pair

        if obj.db.front:
            pair.db.front = True
            obj.db.front = False
            caller.msg(f"The front of {obj} is now facing you.")
        else:
            pair.db.front = False
            obj.db.front = True
            caller.msg(f"The front of {obj} is now facing away from you.")

        return
