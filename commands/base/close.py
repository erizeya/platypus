from evennia import Command


class CmdClose(Command):
    """
    Close objects such as doors and bags
      Usage:
        close <object>
    """

    key = "close"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()

        obj = caller.multiple_search(target_obj, location=caller.location)
        if not obj:
            return

        if not (obj.db.door or obj.db.container):
            caller.msg(f"It doesn't look like the {obj} is something you can close.")
            return
        if(not obj.db.open):
            caller.msg(f"The {obj} is already closed.")
            return

        #Close the door or container
        obj.db.open = False

        #Close the other side too if this is a door
        if obj.db.door:
            obj.db.pair.db.open = False

        caller.msg(f"You close the {obj}")
        return
