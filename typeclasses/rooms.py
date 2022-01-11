"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from typeclasses.npc import Npc
from typeclasses.characters import Character
from collections import defaultdict
from evennia.utils.utils import (
    class_from_module,
    variable_from_module,
    lazy_property,
    make_iter,
    is_iter,
    list_to_string,
    to_str,
)


class Room(DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    pass

    def return_appearance(self, looker, **kwargs):
        """
        This formats a description. It is the hook a 'look' command
        should call.
        Args:
            looker (Object): Object doing the looking.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).
        """
        if not looker:
            return ""
        # get and identify all objects
        visible = (con for con in self.contents if con != looker and con.access(looker, "view"))
        exits, users, things, furniture = [], [], defaultdict(list), []
        for con in visible:
            key = con.get_display_name(looker)
            if con.destination:
                exits.append("|u"+key+"|n")
            elif con.has_account or type(con) is Npc or type(con) is Character:
                users.insert(0, con)
            else:
                #split out furniture
                if(con.db.furniture):
                    furniture.append(con)
                else:
                    # things can be pluralized
                    things[key].append(con)
        # get description, build string
        string = "|c%s|n\n" % self.get_display_name(looker)
        desc = self.db.desc
        if desc:
            string += "%s" % desc

            #Attach furniture to desc
            if len(furniture) > 0:
                for furniture_item in furniture:
                    #search each furniture for occupants
                    if furniture_item.db.occupants:
                        occupant_list = []
                        for occupant in furniture_item.db.occupants:
                            if occupant in users:
                                users.remove(occupant)
                            occupant_list.append(f"|c{occupant.name}|n")
                        if len(occupant_list) == 1:
                            string += " "+list_to_string(occupant_list)
                            string += f" is {furniture_item.db.occupant_pose} |w{furniture_item.name}|n {furniture_item.db.position}"
                        else:
                            string += " "+list_to_string(occupant_list)
                            string += f" are {furniture_item.db.occupant_pose} |w{furniture_item.name}|n {furniture_item.db.position}"
                    else:
                        string += " There is a |w"+furniture_item.name+"|n "+furniture_item.db.position
        if exits:
            string += " You can go " + list_to_string(exits)+"."
        if users or things:
            # handle pluralization of things (never pluralize users)
            thing_strings = []
            for key, itemlist in sorted(things.items()):
                nitem = len(itemlist)
                if nitem == 1:
                    key, _ = itemlist[0].get_numbered_name(nitem, looker, key=key)
                else:
                    key = [item.get_numbered_name(nitem, looker, key=key)[1] for item in itemlist][
                        0
                    ]
                thing_strings.append("|Y"+key+"|n")

            if len(thing_strings) > 0:
                string += "\nScattered about you see " + list_to_string(thing_strings)

            for user in users:
                if users.index(user) == 0:
                    string += "\n"
                string += f"|c{user}|n{user.db.look_place} "

        return string

