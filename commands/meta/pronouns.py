from evennia.commands.command import Command as BaseCommand

# Change your preferred pronouns
#
# Usage:
#   @pronouns <pronoun number>
#
class CmdPronouns(BaseCommand):
    key = "@pronouns"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        help_msg = "Usage: @pronouns [type]\nValid options:\n\tfeminine\n\tmasculine\n\tspivak"
        if not self.args:
            caller.msg(help_msg)
            return
        else:
            arg = self.args.split(" ")[1].strip()
            if arg == "feminine":
                caller.db.gender = 1
            elif arg == "masculine":
                caller.db.gender = 2
            elif arg == "spivak":
                caller.db.gender = 0
            else:
                caller.msg(help_msg)
