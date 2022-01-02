from evennia.commands.command import Command as BaseCommand
from evennia.utils.search import search_object

class CmdPair(BaseCommand):

    key = "!pair"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        arg_list = self.args.strip().split(" ") 
        target_obj = arg_list[0]
        target_link = arg_list[1]

        obj = caller.search(
            target_obj
        )

        if not obj:
            caller.msg(f"Count not find {target_obj}")
            return

        link = search_object(
            target_link,
            exact = True
        )[0]

        if not link:
            caller.msg(f"Count not find {target_link}")
            return

        if not (obj.db.door and link.db.door):
            caller.msg(f"Both objects need to be doors.")
            return

        caller.msg(f"Linking {obj} to {link}")

        obj.db.pair = link 
        link.db.pair = obj
