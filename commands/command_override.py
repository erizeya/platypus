from evennia import default_cmds

class CmdAccess(default_cmds.CmdAccess):
    key = "!access"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"

class CmdCharCreate(default_cmds.CmdCharCreate):
    key = "!charcreate"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"

class CmdCharDelete(default_cmds.CmdCharDelete):
    key = "!chardelete"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"

class CmdColorTest(default_cmds.CmdColorTest):
    key = "$color"
    aliases = ""
    help_category = "System"
    locks = ""

class CmdHelp(default_cmds.CmdHelp):
    key = "help"
    aliases = ""
    help_category = "Help"
    locks = ""

class CmdIC(default_cmds.CmdIC):
    key = "!ic"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"

class CmdOption(default_cmds.CmdOption):
    key = "$options"
    aliases = ""
    help_category = "system"
    locks = ""

class CmdPassword(default_cmds.CmdPassword):
    key = "$password"
    aliases = ""
    help_category = "system"
    locks = ""

class CmdQuell(default_cmds.CmdQuell):
    key = "!quell"
    aliases = "unquell"
    help_category = "Admin"
    locks = "cmd:pperm(Staff)"
    auto_help = False

class CmdQuit(default_cmds.CmdQuit):
    key = "$quit"
    aliases = ""
    help_category = "system"
    locks = ""

class CmdSetDesc(default_cmds.CmdSetDesc):
    key = "!setdesc"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"

class CmdStyle(default_cmds.CmdStyle):
    key = "$style"
    aliases = ""
    help_category = "system"
    locks = ""

class CmdWho(default_cmds.CmdWho):
    key = "!who"
    aliases = ""
    help_category = "Admin"
    locks = "cmd:perm(Staff);"