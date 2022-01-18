from evennia.commands.command import Command as BaseCommand

# Set or display your nakeds
# 
# Usage:
#   @naked[s]
#       Display all nakeds as a lit
#   @naked[s] <location> = <description>
#       Set a specific naked 
#
class CmdNaked(BaseCommand):
    """
    Show or set your characters nudity messages.

    Usage:
        @naked
            Display your current naked messages.
        @naked <body_part> = <description>
            Will set the description of the selected body part.
    """
    key = "@naked"
    aliases = ["@nakeds"]
    lock = "cmd:all()"
    help_category = "Meta"


    def func(self):
        nakeds = ["head", "face", "upper_body", "hands", "lower_body", "feet"]
        if not self.args:
            for naked in nakeds:
                self.caller.msg(f"@naked {naked} = "+self.caller.db.naked[naked])
        else:
            arg_list = self.args.split("=")
            l_arg = arg_list[0].strip()
            r_arg = arg_list[1].strip()

            #Set object properties
            if l_arg in nakeds:
                self.caller.db.naked[l_arg] = r_arg
                self.caller.msg(f"@naked {l_arg} is now \"{r_arg}\"")
            else:
                self.caller.msg("Invalid naked location")
