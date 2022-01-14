from evennia import Command

class CmdStop(Command):
    """
    Stops you from performing an action in progress.
        Syntax:
            stop <action>

        Supported actions:
            walk[ing]/moving
    """

    key = "stop"
    #aliases = ("a1", "a2")
    locks = "cmd:all()"
    help_category = "General"

    def func (self):
        caller = self.caller
        args = self.args.strip()

        if "walk" in args or "moving" in args:
            try:
                del caller.ndb.moving
                caller.msg("You stop moving.")
            except:
                caller.msg("You are not moving.")
        return
