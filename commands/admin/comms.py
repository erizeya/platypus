# in for example mygame/commands/commands.py

from evennia import default_cmds

class CmdChannelCreate(default_cmds.CmdChannelCreate):
    """
    create a new channel

    Usage:
        +create <new channel>[;alias;alias...] = description

    Creates a new channel owned by you.
    """
    key = "+create"
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"

class CmdCBoot(default_cmds.CmdCBoot):
    key = "+boot"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Staff);"

class CmdCdesc(default_cmds.CmdCdesc):
    key = "+desc"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"

class CmdCdestroy(default_cmds.CmdCdestroy):
    key = "+destroy"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"

class CmdCemit(default_cmds.CmdCemit):
    key = "+emit"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"

class CmdClock(default_cmds.CmdClock):
    key = "+lock"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"

class CmdCWho(default_cmds.CmdCWho):
    key = "+who"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Staff);"

class CmdDelCom(default_cmds.CmdDelCom):
    key = "+delete"
    aliases = ""
    help_category = "Comms (Admin)"
    locks = "cmd:perm(Admin);"