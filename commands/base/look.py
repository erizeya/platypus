from evennia.commands.command import Command as BaseCommand

# look at location or object
# 
# Usage:
#   look
#   look <obj>
#   look *<account>
# 
# Observes your location or objects in your vicinity.
class CmdLook(BaseCommand):

    key = "look"
    aliases = ["l", "ls"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "General"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        if not self.args:
            target = caller.location
            if not target:
                caller.msg("You have no location to look at!")
                return
        else:
            target = caller.multiple_search(self.args.strip(),mode="look")
            if not target:
                return
        desc = caller.at_look(target)
        # add the type=look to the outputfunc to make it
        # easy to separate this output in client.
        self.msg(text=(desc, {"type": "look"}), options=None)
