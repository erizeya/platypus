"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit
from evennia.utils import interactive
from evennia.utils import delay
import random
import time

#TODO: Verify door is still open when moving through it.

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
        self.db.pre_desc = ""
        self.db.post_desc = ""

    @interactive
    def at_traverse(self, traveller, target_loc):
        if not self.db.open and self.db.open is False:
            traveller.msg(f"{self} is closed.")
            return
        else:
            traveller.msg(f"You head towards the {self}.")
            traveller.ndb.moving = True
            yield 3
            if traveller.ndb.moving:
                super(Exit, self).at_traverse(traveller, target_loc)

    def return_appearance(self, looker):
        #Exit name
        text = f"|c{self.get_display_name(looker)}|n"

        #Door description
        if(self.db.desc):
            text += "\n"+self.db.desc

        if(self.db.see_thru and self.db.open):
            text += f"\n\nTo the {self} you see...\n"
            text += self.destination.return_appearance(looker)

        return text

class LockingDoor(Exit):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.code = 1234
        self.db.programming = False
        self.db.front = False
        self.db.door = True


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

class HotelDoor(Exit):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.code = 123456
        self.db.front = False
        self.db.expire = None
        self.db.renter = None
        self.db.door = True

    def on_push(self, caller, args):
        pair = self.db.pair
        mode = "unlock"
        
        #Check if room is expired and scramble code if true.
        if self.db.renter != None and self.db.expire < int(time.time()):
            self.db.code = random.randint(11111,99999)
            self.db.renter = None

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

        #function: push <code> on door
        if args != "unlock":
            try:
                code = int(args)
            except:
                self.location.msg_contents(f"The door beeps angrily.")
                return
        else:
            code = None

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

class AffiliatedDoor(Exit):
    
    def at_object_creation(self):
        super().at_object_creation()
        self.db.affiliation = ""
        self.db.front = False
        self.db.door = True

 
    def on_push(self, caller, args):
        pair = self.db.pair

        #function: push lock on exit
        if args == "lock":
            #Check error conditions
            if self.db.open:
                self.location.msg_contents(f"The {self} beeps angrily and the \"door open\" light flashes three times.")
                return
            elif self.db.locked:
                self.location.msg_contents(f"The {self} doesn't do anything. It must already be locked.")
                return

            #All checks pass, unlock the door
            self.db.locked = True
            pair.db.locked = True
            self.location.msg_contents(f"The {self} beeps happily and a lock clicks into place.")
            pair.location.msg_contents(f"The sound a lock clicking into place comes from {pair}.")
            return

        #function: push unlock on door
        elif args == "unlock":
            if self.db.affiliation in caller.db.affiliations:
                    delay(20, self.close_and_lock, caller)
                    self.location.msg_contents(f"The {self} beeps happily and unlocks.")
                    pair.location.msg_contents(f"The {pair} beeps happily and unlocks.")
                    self.db.locked = False
                    pair.db.locked = False
            else:
                    self.location.msg_contents(f"The {self} buzzes angrily and the \"unauthorized\" light blinks.")
                    pair.location.msg_contents(f"The {pair} buzzes angrily and the \"unauthorized\" light blinks.")
        else:
            self.location.msg_contents(f"Nothing happens.")
            return
    
    def close_and_lock(self, caller):
        pair = self.db.pair
        if self.db.open and not self.db.locked:
            self.db.open = False
            pair.db.open = False
            self.db.locked = True
            pair.db.locked = True
            self.location.msg_contents(f"The {self} closes automatically and locks.")
            pair.location.msg_contents(f"The {pair} closes automatically and locks.")
        elif not self.db.locked:
            self.db.locked = True
            pair.db.locked = True
            self.location.msg_contents(f"The {self} beeps as it automatically locks.")
            pair.location.msg_contents(f"The sound a lock clicking into place comes from {pair}.")