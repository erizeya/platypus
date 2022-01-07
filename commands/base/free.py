from evennia import Command as BaseCommand
from custom import genderize

class CmdFree(BaseCommand):
    """
    Causes you to put everything in your hands back into your inventory.

    Usage:
        free/freehands/fh:
            Lowers items in right and left hands into the inventory.
    """

    key = "free"
    aliases = ("freehands", "fh")
    locks = "cmd:all()"

    def func (self):
        caller = self.caller

        if not (caller.db.r_hand and caller.db.l_hand):
            caller.msg("You are not holding anything.")
            return
        if caller.db.r_hand:
            caller.msg(f"You put your {caller.db.r_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.r_hand} away.", caller.db.gender), exclude=caller)
            caller.db.r_hand = None
        if caller.db.l_hand:
            caller.msg(f"You put your {caller.db.l_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.l_hand} away.", caller.db.gender), exclude=caller)
            caller.db.l_hand = None

        return
