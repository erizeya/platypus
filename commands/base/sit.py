from evennia import Command

class CmdSit(Command):
    """
    Sit on the ground or on an object. Sitting characters cannot move.
    
    Usage:
      sit[ [on/at] <furniture>]
    
    TODO:
      multiple support
    
    """
    key = "sit"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("You sit on the ground.")
            caller.location.msg_contents(f"{caller.name} sits on the ground.", exclude=caller)
            caller.db.sitting = True
        else:
            #Split out arguments to
            args = self.args.split(" ")
            target = None
            if args[1] == "on" and len(args) == 2:
                caller.msg("Sit on what?")
            elif args[1] == "at" and len(args) == 2:
                caller.msg("Sit at what?")
            elif (args[1] == "on" or args[1] == "at") and len(args) > 2:
                target = " ".join(args[2:])
            else:
                target = " ".join(args[1:])

            if target:
                #Find the object to sit on and confirm we can sit on it.

                obj = caller.multiple_search(target,location=caller.location)
                if obj and obj.db.furniture and obj.db.seating:
                    caller.msg(f"You sit on the {obj}.")
                    caller.location.msg_contents(f"{caller.name} sits on the {obj}.",exclude=caller)
                    obj.db.occupants.append(caller)
                    caller.db.occupying = obj
                    caller.db.sitting = True
                else:
                    caller.msg(f"You can't sit on {obj}")
            else:
                caller.msg("Usage: sit[ [on/at] <furniture>]")
