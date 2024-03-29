from evennia.commands.command import Command as BaseCommand
from evennia.utils.search import search_object
from typeclasses.npcs.bartender import Bartender
from typeclasses.bar import Bar

class CmdLink(BaseCommand):
    """
    Links a bartender to a bar
        Usage:
            !link <NPC> <Bar>
        
        Notes:
            <Bar> must be a dbref such as "#123"
    """
    key = "!link"
    locks = "cmd:perm_above(Helper)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        arg_list = self.args.strip().split(" ") 
        target_obj = arg_list[0]
        target_link = arg_list[1]
        help_str = "Usage !link <NPC> <Bar>"

        obj = caller.search(
            target_obj
        )
        if not obj:
            caller.msg(f"Could not locate NPC {obj}.")
            return

        link = search_object(
            target_link,
            exact = True
        )[0]

        if not link:
            calle.msg(f"Could not locate bar {link}.")
            return

        if not type(obj) is Bartender:
            caller.msg(f"First argument must be an NPC\n{help_str}")
            return

        if not type(link) is Bar:
            caller.msg(f"Second argument must be an bar\n{help_str}")
            return

        obj.db.link = link

        caller.msg(f"Linked {obj} to {link}")
