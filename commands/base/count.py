from evennia import Command

class CmdCount(Command):
    """
    Count how much money you have on you.

    Usage:
        count
    """

    key = "count"
    #aliases = ("a1", "a2")
    locks = "cmd:all()"

    def func (self):
        caller = self.caller
        funds = caller.db.currency

        if funds == None or funds == 0: 
            caller.msg(f"You don't have any money to count.")
        else:
            caller.msg(f"You pull out and count {funds} money on your person.")
            caller.location.msg_contents(f"{caller} pulls out a wad of money and counts it.",exclude=caller)

        return
