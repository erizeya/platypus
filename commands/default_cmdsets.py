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
from commands.command import CmdWear
from commands.command import CmdRemove
from commands.command import CmdInventory
from commands.command import CmdSit
from commands.command import CmdStand
from commands.command import CmdTo
from commands.command import CmdHold
from commands.command import CmdLower
from commands.command import CmdGet
from commands.command import CmdPut
from commands.command import CmdUse
from commands.command import CmdDrop
from commands.command import CmdOpen
from commands.command import CmdClose
from commands.base.look import CmdLook
from commands.base.give import CmdGive
from commands.base.push import CmdPush
from commands.meta.lp import CmdLp
from commands.meta.naked import CmdNaked
from commands.meta.pronouns import CmdPronouns
from commands.admin.pair import CmdPair
from commands.admin.link import CmdLink
from commands.admin.furniture import CmdFurniture
from commands.admin.dig import _CmdDig
from commands.admin.dig import CmdDig


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
        self.add(CmdFurniture())
        self.add(CmdPush())
        self.add(_CmdDig())
        self.add(CmdDig())


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
