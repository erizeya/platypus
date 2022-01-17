from evennia.commands.command import Command as BaseCommand
from evennia.utils.search import search_object
from typeclasses.npcs.frontdesk import FrontDesk
from typeclasses.exits import HotelDoor

class CmdAddHotelRoom(BaseCommand):

    key = "!add_hotel_room"
    locks = "cmd:perm_above(Helper)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        arg_list = self.args.strip().split(" ") 
        target_obj = arg_list[0]
        target_link = arg_list[1]
        help_str = "Usage !add_hotel_room <NPC> <Room>"

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
            caller.msg(f"Could not find exit {link}.")
            return

        if not type(obj) is FrontDesk:
            caller.msg(f"First argument must be an NPC\n{help_str}")
            return

        if not type(link) is HotelDoor:
            caller.msg(f"Second argument must be an bar\n{help_str}")
            return

        obj.db.rooms.append(link)

        caller.msg(f"Linked {obj} to {link}")
