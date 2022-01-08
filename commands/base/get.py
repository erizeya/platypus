from evennia import Command

class CmdGet(Command):
    """
    Take an item from the ground
    
    Usage:
      get/grab/take <item> [ from <container>]
    """
    key = "get"
    aliases = ["grab", "take"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        args = self.args.strip()
        caller = self.caller
        location = self.caller.location
        error_msg = "Usage: take <object> from <container>"
        if not args:
            caller.msg(error_msg)
            return

        #Check for full hands
        if not (caller.db.l_hand == None or caller.db.r_hand == None):
            caller.msg(f"Your hands are full.")
            return

        #Determine if we're taking from a container
        if " from " in args:
            arg_list = args.split(" from ")
            container = caller.multiple_search(arg_list[1], location=caller.location)
            if not container:
                return
            #Make sure the container is actually a container
            if not container.db.container:
                caller.msg(f"You can't put stuff into the {container}.")
                return

            #Ensure the container is open
            if not container.db.open:
                caller.msg(f"The {container} is closed.")
                return

            obj = caller.multiple_search(arg_list[0], location=container)
            if not obj:
                return
        else:
            obj = caller.multiple_search(args, location=caller.location)
            if not obj:
                return
            container = None

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        #Grab the item and call the post-grab hook
        if caller.db.r_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.r_hand = obj
        elif caller.db.l_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.l_hand = obj

        if not container:
            caller.msg(f"You take the {obj}.")
            caller.location.msg_contents(f"{caller} takes a {obj} from the {container}.", exclude=caller)
        else:
            caller.msg(f"You take the {obj} from the {container}.")
            caller.location.msg_contents(f"{caller} takes a {obj} from the {container}.", exclude=caller)

        return
