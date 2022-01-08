from evennia import Command


class CmdStand(Command):
    """
    Stand up from sitting

    Usage:
      stand
    """
    key = "stand"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        if caller.db.sitting:
            if caller.db.occupying:
                caller.db.occupying.db.occupants.remove(caller)
                caller.msg(f"You stand up from the {caller.db.occupying.name}.")
                caller.location.msg_contents(f"{caller.name} stands up from the {caller.db.occupying.name}.",exclude=caller)
                caller.db.occupying = None
            else:
                caller.msg("You stand up.")
                caller.location.msg_contents(f"{caller.name} stands up.",exclude=caller)
            caller.db.sitting = False
        else:
            caller.msg("You are not sitting.")
