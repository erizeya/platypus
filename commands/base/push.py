from evennia import Command
class CmdPush(Command):
    """
    Push a specific button or series of buttons on an object
    Usage:
        push <what> on <obj>
    """
    key = "push"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    err_msg = "Usage: push <what> on <obj>"
    help_category = "General"

    def func(self):
        args = self.args.strip()
        caller = self.caller 

        try:
            arg_list = args.split(" on ")
        except:
            caller.msg(err_msg)
            return

        what = arg_list[0]
        target_obj = arg_list[1]

        obj = caller.multiple_search(target_obj, location=[caller.location, caller])
        
        if not obj:
            return

        if not obj.location is caller.location and not obj == caller.db.l_hand and not obj == caller.db.r_hand:
            caller.msg("You can only push keys on something you're holding or in the same room as you.")
            return

        if not obj:
            return

        obj.on_push(caller, what)

