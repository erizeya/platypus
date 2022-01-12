from evennia import Command

class CmdSet(Command):
    """
    Set a property on an object

    Syntax:
        !set <target> <property> <value>

    Supported properties:
        pre_desc
        post_desc 
    """

    key = "!set"
    #aliases = ("a1", "a2")
    locks = "cmd:all()"
    help_category = "Admin"

    def func (self):
        caller = self.caller
        args = self.args.strip()
        help_msg = "Usage: !set <target> <property> <value>\nSee help !set for more information."
        supported_properties = ["pre_desc", "post_desc"]

        if not args:
            caller.msg(help_msg)
            return

        arg_list = args.split(" ")
        
        #Extract target then discard
        target = caller.multiple_search(arg_list[0],location=caller.location)
        if not target:
            caller.msg(help_msg)
            return
        del arg_list[0]

        #Extract property then discard
        prop = arg_list[0]
        if not prop in supported_properties:
            caller.msg("Unsupported property.")
            caller.msg(help_msg)
            return
        del arg_list[0]

        #Everything else is the value
        val = " ".join(arg_list)

        #Set the property
        if prop == "pre_desc":
            target.db.pre_desc = val+" "
            return
        elif prop == "post_desc":
            target.db.post_desc = " "+val
            return
        else:
            caller.msg(f"!set: error. target={target} prop={prop} value={val}")
            caller.msg(help_msg)
            return

