from evennia import Command
from typeclasses.exits import Exit
from typeclasses.npcs.frontdesk import FrontDesk

class CmdSet(Command):
    """
    Set a property on an object

    Syntax:
        !set <target> <property> <value>

    Supported properties:
        Exits:
            pre_desc
            post_desc
        Hotel Front Desk NPC:
            price_per_duration
            duration
            duration_text
    """

    key = "!set"
    locks = "cmd:perm_above(Helper)"
    help_category = "Building"

    def func (self):
        caller = self.caller
        args = self.args.strip()
        help_msg = "Usage: !set <target> <property> <value>\nSee help !set for more information."
        supported_properties = ["pre_desc", "post_desc", "price_per_duration", "duration", "duration_text"]

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

        #Check error checking
        if prop in ["pre_desc", "post_desc"]:
            if not type(target) is Exit:
                caller.msg(f"Error: {prop} can only be set on exits.")
                return
        elif prop in ["price_per_duration", "duration", "duration_text"]:
            if not type(target) is FrontDesk:
                caller.msg(f"Error: {prop} can only be set on front desk NPCs.")
                return
            if prop in ["price_per_duration", "duration"] and not val.isnumeric():
                caller.msg(f"Error: {prop} must be set with a numeric value")
                return
                
        #Set the property
        if prop == "pre_desc":
            target.db.pre_desc = val+" "
            caller.msg(f"Set: {prop} is now \"{target.db.pre_desc}\".")
            return
        elif prop == "post_desc":
            target.db.post_desc = " "+val
            caller.msg(f"Set: {prop} is now \"{target.db.post_desc}\".")
            return
        elif prop == "price_per_duration":
            target.db.price_per_duration = int(val)
            caller.msg(f"Set: {prop} is now \"{target.db.price_per_duration}\".")
            return
        elif prop == "duration":
            target.db.duration = int(val)
            caller.msg(f"Set: {prop} is now \"{target.db.duration}\".")
            return
        elif prop == "duration_text":
            target.db.duration_text = val
            caller.msg(f"Set: {prop} is now \"{target.db.duration_text}\".")
            return                               
        else:
            caller.msg(f"!set: error. target={target} prop={prop} value={val}")
            caller.msg(help_msg)
            return

