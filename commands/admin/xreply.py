from evennia import Command
from evennia.utils.search import search_object, search_channel
class CmdXreply(Command):
    """
    Sends a message to all online staff and administrators.
    """

    key = "xreply"
    locks = "cmd:perm(Staff)"
    help_category = "General"

    def func (self):
        caller = self.caller
        args = self.args.strip()
        arg_list = args.split(" ")
        target = arg_list[0]
        del arg_list[0]
        args = " ".join(arg_list)
        target = search_object(target, exact=True)
        if not target:
            caller.msg("Could not find target.")
            return
        target = target[0]
        channel = search_channel("MudInfo")[0]

        channel.msg(f"[|rXHELP|n] [{caller} to {target}]: {args}")
        target.msg(f"[|rXHELP|n] [{caller} to You]: {args}")

        return
