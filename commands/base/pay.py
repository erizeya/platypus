from evennia import Command

class CmdPay(Command):
    """
    Help File
    """

    key = "pay"
    #aliases = ("a1", "a2")
    locks = "cmd:all()"
    help_category = "General"

    def func (self):
        caller = self.caller
        args = self.args.strip()

        if not args:
            caller.msg("Usage: pay <target> <amount>")
            return

        if caller.db.currency == 0:
            caller.msg("You don't have any money on you.")
            return

        arg_list = args.split(" ")
        target = caller.multiple_search(arg_list[0],location=caller.location)
        amount = arg_list[1]

        if not target:
            return

        if caller.db.currency - int(amount) < 0:
            caller.msg("You don't have that much money on you.")
            return


        caller.db.currency -= int(amount)
        target.db.currency += int(amount)
    
        caller.msg(f"You pass {amount} money to {target}.")
        target.msg(f"{caller} passes {amount} money to you.")

        return
