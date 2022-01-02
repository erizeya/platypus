from evennia.commands.command import Command as BaseCommand

# Set your look place
#
# Usage:
#   @lp <look place message>
#
class CmdLp(BaseCommand):
    key = "@lp"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("@look_place message cleared.")
            self.caller.db.look_place = " is here."
        else:
            self.caller.db.look_place = self.args
        self.caller.msg(f"Other players now see: {self.caller}{self.caller.db.look_place}")

