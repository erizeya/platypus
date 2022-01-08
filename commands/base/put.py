from evennia import Command
from custom import genderize

class CmdPut(Command):
    """
    Put a held item into a container

      Usage:
          put <item> in <container>
    """

    key = "put"
    locks = "cmd:all()"

    def func(self):
        args = self.args
        caller = self.caller
        location = self.caller.location
        count = None
        error_msg = "Usage: put <object> in <container>"
        if not args:
            caller.msg(error_msg)
            return


        #Split args out
        args_list = args.strip().split(" ")
        try:
            split = args_list.index("in")
        except:
            caller.msg(error_msg)
            return 
        target_obj = " ".join(args_list[:split])
        target_container = " ".join(args_list[split+1:])
        if not target_obj or not target_container:
            caller.msg(error_msg)
            return 

        #verify container
        container = caller.multiple_search(target_container, location=caller.location)
        if not container:
            caller.msg(error_msg)
            return 

        #Ensure the container is really a container
        if not container.db.container:
            caller.msg(f"You can't take anything from the {container}")
            return

        #Ensure the container is open
        if not container.db.open:
            caller.msg(f"The {container} is closed.")
            return

        #find object in character's hand
        obj = caller.multiple_search(target_obj)
        if not obj:
            caller.msg(error_msg)
            return
        if not (caller.db.l_hand == obj or caller.db.r_hand == obj):
            caller.msg(f"You have to be holding your {obj} to put it {container.db.prep} the {container}.")
            return

        #remove object from character hands
        if caller.db.r_hand == obj:
            obj.move_to(container, quiet=True)
            caller.db.r_hand = None
        elif caller.db.l_hand == obj:
            obj.move_to(container, quiet=True)
            caller.db.l_hand = None

        caller.msg(f"You put your {obj} {container.db.prep} the {container}.")
        container.location.msg_contents(genderize(f"{caller} puts %p {obj} {container.db.prep} the {container}.", caller.db.gender), exclude=caller)
