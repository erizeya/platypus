from typeclasses.furniture import Furniture
from evennia.utils import evmenu
from evennia import create_object


class Bar(Furniture):
    def at_object_creation(self):
        super().at_object_creation();
        self.db.container = True
        self.db.seating = False
        self.db.wares = {"Tea":50, "Rice":25}
        self.db.affiliation = ""
        
    def on_use(self, user):
        if self.db.affiliation in user.db.affiliations:
            evmenu.EvMenu(user, "typeclasses.bar", startnode="menunode_bar", cmd_on_exit=None, obj=self)
        else:
            user.msg("You don't seem to have the keys nessecary to unlock the bar.")

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
