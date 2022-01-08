from evennia import Command

class CmdTo(Command):
    """
    Direct a message to a specific player or group of players
    
    Usage:
      to <character>
    """

    key = "to"
    locks = "cmd:all()"

    def func(self):
        """Run the whisper command"""

        caller = self.caller
        args = self.args

        args_l = args.strip().split(" ")
        lhs = args_l[0]
        rhs = " ".join(args_l[1:])

        if not lhs or not rhs:
            caller.msg("Usage: to <target> <message>")
            return

        target = caller.search(lhs)
        speech = rhs

        # If the speech is empty, abort the command
        if not speech or not lhs:
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_pre_say(speech, to=True)

        # no need for self-message if we are whispering to ourselves (for some reason)
        #msg_self = None if caller is lhs else True

        caller.at_say(speech, msg_self=True, receivers=target, to=True)
