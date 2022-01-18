from evennia import Command

class CmdGivemoney(Command):
    """
    Gives money to a player or NPC
        Usage:
            !givemoney <target> <amount>
    """

    key = "!givemoney"
    locks = "cmd:perm_above(Helper)"
    help_category = "Admin"

    def func (self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Usage: !givemoney <target> <amount>")

        arg_list = args.split(" ")
        who = caller.multiple_search(arg_list[0],location=caller.location)
        amount = arg_list[1]

        who.db.currency += int(amount)
        caller.msg(f"You just spawned {amount} currency on {who}.")
        who.msg(f"{caller} just spawned {amount} currency on you!")

        return
