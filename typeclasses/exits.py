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
        self.db.door = False
        self.db.open = True
        self.db.pair = None
        self.db.see_thru = True
        self.db.desc = ""
        self.db.locked = False

    def at_traverse(self, traveller, target_loc):
        if not self.db.open and self.db.open is False:
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

class LockingDoor(Exit):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.code = 1234
        self.db.programming = False
        self.db.front = False

    def on_push(self, caller, args):
        pair = self.db.pair
        mode = "unlock"
        #function: push lock on exit
        if args == "lock":
            #Check error conditions
            if self.db.open:
                self.location.msg_contents(f"The door beeps angrily and the \"door open\" light flashes three times.")
                return
            elif self.db.locked:
                self.location.msg_contents(f"The door doesn't do anything. It must already be locked.")
                return

            #All checks pass, unlock the door
            self.db.locked = True
            pair.db.locked = True
            self.location.msg_contents(f"The door beeps happily and a lock clicks into place.")
            return

        #function: push program <code> on door. Doors can only be programmed from outside.
        if "program " in args:
            if not self.db.front:
                caller.msg("The door doesn't do anything. You can only program the door from the front")
                return
            args = args.replace("program ", "")
            mode = "program"

        #function: push cancel on door
        if args == "cancel":
            if self.db.programming:
                self.db.programming = False
                self.location.msg_contents(f"The door beeps happily and the \"programming\" light stops blinking.")
            else:
                self.location.msg_contents(f"Nothing happens.")
            return
        
        #function: push <code> on door
        if args != "unlock":
            try:
                code = int(args)
            except:
                self.location.msg_contents(f"The door beeps angrily.")
                return
        else:
            code = None

        if self.db.programming:
            self.db.code = code
            self.location.msg_contents(f"The door beeps twice.")
            return

        # Let users on the inside of the door "push open/unlock on out" but require code from outside.
        if code == self.db.code or ((not self.db.front) and (args == "unlock" or args == "open")):
            if mode == "unlock":
                if self.db.locked:
                    self.location.msg_contents(f"The door beeps happily and unlocks.")
                    self.db.locked = False
                    pair.db.locked = False
                else:
                    self.location.msg_contents(f"Nothing happens.")
                return

            elif mode == "program":
                self.location.msg_contents(f"The door beeps happily and the \"programming\" light begins to blink.")
                self.db.programming = True
                return

        else:
            self.location.msg_contents(f"The door buzzes angrily.")
            return
