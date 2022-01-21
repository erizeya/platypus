from evennia.utils.search import search_channel
from django.conf import settings
from evennia import Command
from evennia import default_cmds
from evennia.utils.utils import make_iter, class_from_module

__all__ = ("CmdChannels")

_DEFAULT_WIDTH = settings.CLIENT_DEFAULT_WIDTH

CHANNEL_DEFAULT_TYPECLASS = class_from_module(
    settings.BASE_CHANNEL_TYPECLASS, fallback=settings.FALLBACK_CHANNEL_TYPECLASS)

class CmdJoin(Command):
    """
    Connect to a channel.
    """

    key = "+join"
    help_category = "Comms"
    locks = "cmd:not pperm(channel_banned)"

    def func(self):
        """Implement the command"""
        caller = self.caller
        args = self.args.strip()
        if not args:
            self.msg("Which channel do you want to connect to?")
            return


        channelname = args
        channel = search_channel(channelname)
        if not channel:
            caller.msg(f"Error joining channel \"{channelname}\".")
            return

        channel = channel[0]

        # Check permissions
        if not channel.access(caller, 'listen'):
            self.msg("%s: You are not allowed to listen to this channel." % channel.key)
            return

        # If not connected to the channel, try to connect
        if not channel.has_connection(caller):
            if not channel.connect(caller):
                self.msg("%s: You are not allowed to join this channel." % channel.key)
                return
            else:
                self.msg("You now are connected to the %s channel. " % channel.key.lower())
        else:
            self.msg("You already are connected to the %s channel. " % channel.key.lower())

class CmdLeave(Command):
    """
    Disconnect from a channel.
    """

    key = "+leave"
    help_category = "Comms"
    locks = "cmd:not pperm(channel_banned)"

    def func(self):
        """Implement the command"""
        caller = self.caller
        args = self.args.strip()
        if not args:
            self.msg("Which channel do you want to disconnect from?")
            return

        channelname = args
        channel = search_channel(channelname)
        if not channel:
            return

        channel = channel[0]

        # If connected to the channel, try to disconnect
        if channel.has_connection(caller):
            if not channel.disconnect(caller):
                self.msg("%s: You are not allowed to disconnect from this channel." % channel.key)
                return
            else:
                self.msg("You stop listening to the %s channel. " % channel.key.lower())
        else:
            self.msg("You are not connected to the %s channel. " % channel.key.lower())

class CmdChannels(default_cmds.CmdChannels):
    """
    list all channels available to you
    Usage:
      +channels

    Lists all channels available to you, whether you listen to them or not.
    Use 'comlist' to only view your current channel subscriptions.
    Use addcom/delcom to join and leave channels
    """
    key = "+channels"
    aliases = ""
    help_category = "Comms"
    locks = "cmd:not pperm(channel_banned)"

    # this is used by the COMMAND_DEFAULT_CLASS parent
    account_caller = True

    def func(self):
        """Implement function"""

        caller = self.caller

        # all channels we have available to listen to
        channels = [
            chan
            for chan in CHANNEL_DEFAULT_TYPECLASS.objects.get_all_channels()
            if chan.access(caller, "listen")
        ]
        if not channels:
            self.msg("No channels available.")
            return
        # all channel we are already subscribed to
        subs = CHANNEL_DEFAULT_TYPECLASS.objects.get_subscriptions(caller)

        if self.cmdstring == "comlist":
            #depricated
            pass
        else:
            # full listing (of channels caller is able to listen to)
            comtable = self.styled_table(
                "|wsub|n",
                "|wchannel|n",
                #"|wmy aliases|n",
                #"|wlocks|n",
                "|wdescription|n",
                maxwidth=_DEFAULT_WIDTH,
            )
            for chan in channels:
                clower = chan.key.lower()
                nicks = caller.nicks.get(category="channel", return_obj=True)
                nicks = nicks or []
                if chan not in subs:
                    substatus = "|rNo|n"
                elif caller in chan.mutelist:
                    substatus = "|rMuted|n"
                else:
                    substatus = "|gYes|n"
                comtable.add_row(
                    *[
                        substatus,
                        "%s"
                        % (
                            chan.key,
                            #chan.aliases.all() and "(%s)" % ",".join(chan.aliases.all()) or "",
                        ),
                        #"%s"
                        #% ",".join(
                        #    nick.db_key
                        #    for nick in make_iter(nicks)
                        #    if nick.value[3].lower() == clower
                        #),
                        #str(chan.locks),
                        chan.db.desc,
                    ]
                )
            #comtable.reformat_column(0, width=9)
            #comtable.reformat_column(3, width=14)
            self.msg(
                "\n|wAvailable channels|n (use |w+join|n and |w+leave|n"
                " to join and leave.):\n%s" % comtable
            )

class CmdLocal(Command):
    """
    list all channels available to you
    Usage:
      +local <message>

    Lists all channels available to you, whether you listen to them or not.
    Use 'comlist' to only view your current channel subscriptions.
    Use addcom/delcom to join and leave channels
    """
    key = "+local"
    aliases = ""
    help_category = "Comms"

    def func(self):
        caller = self.caller
        args = self.args.strip()
        channel = search_channel("MudInfo")[0]

        channel.msg(f"[|yOOC|n] {caller}@{caller.location.id}: {args}")
        caller.location.msg_contents(f"[|yOOC|n] {caller}: {args}")

        return  