from evennia import Command
from evennia.utils.search import search_channel
class CmdXhelp(Command):
    """
    Sends a message to all online staff and administrators.
    """

    key = "xhelp"
    locks = "cmd:all()"
    help_category = "Help"

    def func (self):
        caller = self.caller
        args = self.args.strip()

        channel = search_channel("MudInfo")[0]

        channel.msg(f"[|rXHELP|n] {caller}@{caller.location.id}: {args}", header="header", senders="sender")
        caller.msg("Your xhelp has been sent.")

        return
