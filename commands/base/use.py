from evennia import Command

class CmdUse(Command):
    """
    Use an interactive object
    
      Usage:
          use <object>
    """
    key = "use"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args

        if not args:
            caller.msg("What do you want to use?")
            return
        
        target = caller.multiple_search(args.strip(), location=caller.location)
        if not target:
            return

        if not (caller.db.l_hand == None or caller.db.r_hand == None):
            caller.msg(f"How do you expect to use the {target} with both your hands full?")
            return

        if not target:
            return

        target.on_use(caller)
