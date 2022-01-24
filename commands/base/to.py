from evennia import Command
from custom import is_valid_cardinal

class CmdTo(Command):
    """
    Direct a message to a specific player or group of players
    
    Usage:
      to <character>
    """

    key = "to"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args
        args_l = args.strip().split(" ")
        target = args_l[0]

        if is_valid_cardinal(target):
            target = " ".join(args_l[:2])
            speech = " ".join(args_l[2:])
        else:
            speech = " ".join(args_l[1:])

        if not target or not speech:
            caller.msg("Usage: to <target> <message>")
            return

        target = caller.multiple_search(target, location=[caller, caller.location])

        if not target:
            return
        
        if not target.location is caller.location and  not target == caller.db.l_hand and not target == caller.db.r_hand:
            caller.msg("You can only direct speech to something you're holding or in the same room as you.")
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_pre_say(speech, to=True)
        caller.at_say(speech, msg_self=True, receivers=target, to=True)
