"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds

from evennia import settings

from commands.base.wear import CmdWear
from commands.base.remove import CmdRemove
from commands.base.inventory import CmdInventory
from commands.base.sit import CmdSit
from commands.base.stand import CmdStand
from commands.base.to import CmdTo
from commands.base.hold import CmdHold
from commands.base.get import CmdGet
from commands.base.put import CmdPut
from commands.base.use import CmdUse
from commands.base.drop import CmdDrop
from commands.base.open import CmdOpen
from commands.base.close import CmdClose
from commands.base.look import CmdLook
from commands.base.give import CmdGive
from commands.base.push import CmdPush
from commands.base.eat import CmdEat 
from commands.base.drink import CmdDrink 
from commands.base.free import CmdFree
from commands.base.lower import CmdLower
from commands.base.pose import CmdPose
from commands.base.emote import CmdEmote
from commands.base.count import CmdCount
from commands.base.pay import CmdPay
from commands.base.stop import CmdStop
from commands.base.read import CmdRead
from commands.base.whisper import CmdWhisper
from commands.base.xhelp import CmdXhelp

from commands.meta.comms import CmdJoin, CmdLeave, CmdChannels, CmdLocal
from commands.meta.lp import CmdLp
from commands.meta.naked import CmdNaked
from commands.meta.pronouns import CmdPronouns

from commands.admin.pair import CmdPair
from commands.admin.link import CmdLink
from commands.admin.furniture import CmdFurniture
from commands.admin.dig import CmdDig
from commands.admin.doorside import CmdDoorside
from commands.admin.tunnel import CmdTunnel
from commands.admin.givemoney import CmdGivemoney
from commands.admin.set import CmdSet
from commands.admin.add_hotel_room import CmdAddHotelRoom
from commands.admin.comms import CmdChannelCreate, CmdCBoot, CmdCdesc, CmdCdestroy, CmdCemit, CmdClock, CmdCWho, CmdDelCom
from commands.admin.xreply import CmdXreply

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # Disable existing commands
        #
        self.remove(default_cmds.CmdWhisper())
        self.remove(default_cmds.CmdDig())
        self.remove(default_cmds.CmdTunnel())
        #
        # any commands you add below will overload the default ones.
        #
        self.add(CmdWear())
        self.add(CmdRemove())
        self.add(CmdInventory())
        self.add(CmdSit())
        self.add(CmdStand())
        self.add(CmdLp())
        self.add(CmdNaked())
        self.add(CmdTo())
        self.add(CmdHold())
        self.add(CmdLower())
        self.add(CmdPronouns())
        self.add(CmdGet())
        self.add(CmdPut())
        self.add(CmdUse())
        self.add(CmdDrop())
        self.add(CmdOpen())
        self.add(CmdClose())
        self.add(CmdPair())
        self.add(CmdLink())
        self.add(CmdLook())
        self.add(CmdGive())
        self.add(CmdEat())
        self.add(CmdDrink())
        self.add(CmdFurniture())
        self.add(CmdPush())
        self.add(CmdDig())
        self.add(CmdTunnel())
        self.add(CmdDoorside())
        self.add(CmdFree())
        self.add(CmdPose())
        self.add(CmdEmote())
        self.add(CmdCount())
        self.add(CmdGivemoney())
        self.add(CmdPay())
        self.add(CmdSet())
        self.add(CmdSet())
        self.add(CmdStop())
        self.add(CmdRead())
        self.add(CmdAddHotelRoom())
        self.add(CmdWhisper())
        self.add(CmdXhelp())
        self.add(CmdXreply())
        self.add(CmdLocal())

class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.remove(default_cmds.CmdAddCom())
        self.remove(default_cmds.CmdAllCom())
        self.remove(default_cmds.CmdCBoot())
        self.remove(default_cmds.CmdCdesc())
        self.remove(default_cmds.CmdCdestroy())
        self.remove(default_cmds.CmdCemit())
        self.remove(default_cmds.CmdChannels())
        self.remove(default_cmds.CmdClock())
        self.remove(default_cmds.CmdCWho())
        #
        # Add
        #
        self.add(CmdJoin())
        self.add(CmdLeave())
        self.add(CmdChannelCreate())
        self.add(CmdCBoot())
        self.add(CmdCdesc())
        self.add(CmdCdestroy())
        self.add(CmdCemit())
        self.add(CmdChannels())
        self.add(CmdClock())
        self.add(CmdCWho())
        self.add(CmdDelCom())


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
