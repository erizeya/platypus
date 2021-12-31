from typeclasses.objects import Object
from evennia.utils import evmenu
from evennia.utils.utils import list_to_string
from evennia import default_cmds
from evennia import create_object
from commands.furniturecommands import FurnitureCmdSet

class Furniture(Object):
    """
    This typeclass describes a wearable object.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        self.cmdset.add(FurnitureCmdSet, permanent=True)
        self.locks.add("puppet:superuser()")

        #Item specific traits
        self.db.furniture = True
        self.db.seating = True
        self.db.desc = "This is a piece of furniture."
        self.db.occupant_pose = "sitting on the"
        self.db.position = "against the wall."
        self.db.occupants = []
        self.db.container = False

class Container(Object):
    def at_object_creation(self):
        super().at_object_creation();
        self.db.container = True
        self.db.prep = "in"
        self.db.open = True

    def return_appearance(self, looker):
        text = f"|c{self.get_display_name(looker)}|n"

        if self.db.desc:
            text += "\n"+self.db.desc

        if self.db.open:
            text += "\nInside the chest you see: "
            items = []
            for content in self.contents:
                items.append(content.get_display_name(looker))

            text += list_to_string(items)
        else:
            text += f"\nThe {self} is closed."

        return text

class Bar(Furniture):
    def at_object_creation(self):
        super().at_object_creation();
        self.db.container = True
        self.db.seating = False
        self.db.wares = {"Tea":50, "Rice":25}

    
    def on_use(self, user):
        evmenu.EvMenu(user, "typeclasses.furniture", startnode="menunode_bar", cmd_on_exit=None, obj=self)

def menunode_bar(caller, raw_string):
    #Generate menu
    obj = caller.ndb._evmenu.obj
    wares = list(obj.db.wares.keys())

    if not wares:
        text += f"This {obj.name} doesn't have enough supplies to make anything."
        return

    text = f"Menu for the {obj.name}"

    options = []

    def _bar_action(caller, raw_string):
        selection = int(raw_string)-1
        new = create_object("typeclasses.consumable."+wares[selection], key="new drink")
        new.reset_name()
        new.move_to(caller, silent=True)
        if caller.db.r_hand == None:
            caller.db.r_hand = new
            caller.msg(f"You prepare {new} at the {obj.name}.")
        elif caller.db.l_hand == None:
            caller.db.l_hand = new
            caller.msg(f"You prepare {new} at the {obj.name}.")
        else:
            caller.msg(f"You prepare {new} and set it on the {obj.name}.")
        return None
    
    for ware in wares:
        options.append({"desc":f"{ware}.....{obj.db.wares[ware]}c", "goto": "menunode_exit", "exec":_bar_action})

    return text, options 

def menunode_exit(caller, raw_string, **kwargs):
    return None, None
