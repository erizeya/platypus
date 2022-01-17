from evennia import Command

class CmdRead(Command):
    """
    Read an item that has text written on it.

        Usage: 
            read <item>
    """

    key = "read"
    #aliases = ("a1", "a2")
    locks = "cmd:all()"
    help_category = "General"

    def func (self):
        caller = self.caller
        args = self.args.strip()

        #find item
        obj = caller.multiple_search(args)

        if not obj:
            caller.msg(f"Unable to find {args}. Are you sure you're holding it?")
            return

        #check if item is in hand
        if caller.db.l_hand == obj or caller.db.r_hand == obj:
            caller.msg(f"The {obj} reads...")
            caller.msg(obj.db.text)
        else:
            caller.msg(f"You have to be holding something to read it.")
            return


        #display item contents
        return
