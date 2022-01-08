from evennia import Command


class CmdOpen(Command):

    """
    Open objects such as doors and bags

      Usage:
         open <object>
    """
    key = "open"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()

        obj = caller.multiple_search(target_obj, location=caller.location)
        if not obj:
            return

        if not (obj.db.door or obj.db.container):
            caller.msg(f"It doesn't look like the {obj} is something you can open.")
            return

        if(obj.db.open):
            caller.msg(f"The {obj} is already open.")
            return

        #Open the door
        if not obj.db.locked:
            obj.db.open = True
        else:
            caller.msg(f"The {obj} is locked.")
            return

        #Open the other side too if acting on a door
        if obj.db.door:
            obj.db.pair.db.open = True

        caller.msg(f"You open the {obj}")
        caller.location.msg_contents(f"{caller} opens the {obj}.",exclude=caller)
        return

