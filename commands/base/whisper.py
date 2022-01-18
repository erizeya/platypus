from evennia import Command

class CmdWhisper(Command):
    """
    Say something to someone else in the same room as you privately. Note that other players will be able to see you whispering to whoever you whisper to, but not what you say.
    
    Usage:
      whisper <target> <message>
    """

    key = "whisper"
    locks = "cmd:all()"

    def func(self):
        help_msg = "Usage: whisper <target> <message>"
        caller = self.caller
        args = self.args.strip()
        arg_list = args.split(" ")
        
        #Find target
        target = arg_list[0]
        del arg_list[0]
        target = caller.search(target)
        if not target:
            caller.msg(help_msg)
            return

        #Deliver message
        msg = " ".join(arg_list)

        # If the speech is empty, abort the command
        if not msg:
            caller.msg(help_msg)
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_pre_say(msg, to=True)

        # no need for self-message if we are whispering to ourselves (for some reason)
        #msg_self = None if caller is lhs else True

        caller.at_say(speech, msg_self=True, receivers=target, whisper=True)
