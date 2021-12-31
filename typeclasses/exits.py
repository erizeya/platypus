"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit


class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """
    def at_object_creation(self):
        self.db.door = True
        self.db.open = True
        self.db.pair = None
        self.db.see_thru = True
        self.db.desc = ""

    def at_traverse(self, traveller, target_loc):
        if not self.db.open:
            traveller.msg(f"{self} is closed.")
            return
        else:
            super(Exit, self).at_traverse(traveller, target_loc)

    def return_appearance(self, looker):
        #Exit name
        text = f"|c{self.get_display_name(looker)}|n"

        #Door description
        if(self.db.desc):
            text += "\n"+self.db.desc

        if(self.db.see_thru and self.db.open):
            text += f"\n\nTo the door you see...\n"
            text += self.destination.return_appearance(looker)

        return text
