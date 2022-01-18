from evennia.commands.command import Command as BaseCommand

# Set your look place
#
# Usage:
#   @lp <look place message>
#
class CmdLp(BaseCommand):
    """
    Set your character's "look place", the text shown after your name in a room description.
        Usage:
            @lp
                Clears your look place message.
            @lp <text> 
                Sets your look place to the provided text.
        Example:
            @lp is leaning against the wall. will show "Character is leaning against the wall."
    """
    key = "@lp"
    aliases = ("@look_place")
    lock = "cmd:all()"
    help_category = "Meta"

    def func(self):
        if not self.args:
            self.caller.msg("@look_place message cleared.")
            self.caller.db.look_place = " is here."
        else:
            self.caller.db.look_place = self.args
        self.caller.msg(f"Other players now see: {self.caller}{self.caller.db.look_place}")

