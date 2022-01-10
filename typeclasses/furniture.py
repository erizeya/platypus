from typeclasses.objects import Object
from evennia.utils import evmenu
from evennia.utils.utils import list_to_string
from evennia import default_cmds
from evennia import create_object

class Furniture(Object):
    """
    This typeclass describes a wearable object.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        self.locks.add("puppet:superuser()")

        #Item specific traits
        self.db.furniture = True
        self.db.seating = True
        self.db.desc = "This is a piece of furniture."
        self.db.occupant_pose = "sitting on the"
        self.db.position = "against the wall."
        self.db.occupants = []
        self.db.container = False

class Container(Furniture):
    def at_object_creation(self):
        super().at_object_creation();
        self.db.seating = False
        self.db.desc = "This is a furniture container."
        self.db.container = True
        self.db.prep = "in"
        self.db.open = True
        self.db.locked = False

    def return_appearance(self, looker):
        text = f"|c{self.get_display_name(looker)}|n"

        if self.db.desc:
            text += "\n"+self.db.desc

        if self.db.open:
            if not self.contents:
                text += f"\nThe {self} is empty."
            else:
                text += f"\nInside the {self} you see: "
                items = []
                for content in self.contents:
                    items.append(content.get_display_name(looker))

                text += list_to_string(items)
        else:
            text += f"\nThe {self} is closed."

        return text

class LockingContainer(Container):
    """
    This is a test
    """
    def at_object_creation(self):
        super().at_object_creation()
        self.db.code = 1234
        self.db.programming = False

    def on_push(self, caller, args):
        mode = "unlock"
        #function: push lock on container
        if args == "lock":
            #Check error conditions
            if self.db.open:
                self.location.msg_contents(f"The {self} beeps angrily and the \"container open\" light flashes three times.")
                return
            elif self.db.locked:
                self.location.msg_contents(f"The {self} doesn't do anything. It must already be locked.")
                return

            #All checks pass, unlock the locker
            self.db.locked = True
            self.location.msg_contents(f"The {self} beeps happily and a lock clicks into place.")
            return

        #function: push program <code> on locker
        if "program " in args:
            args = args.replace("program ", "")
            mode = "program"

        #function: push cancel on locker
        if args == "cancel":
            if self.db.programming:
                self.db.programming = False
                self.location.msg_contents(f"The {self} beeps happily and the \"programming\" light stops blinking.")
            else:
                self.location.msg_contents(f"Nothing happens.")
            return
        
        #function: push <code> on container
        try:
            code = int(args)
        except:
            self.location.msg_contents(f"The {self} beeps angrily.")
            return

        if self.db.programming:
            self.db.code = code
            self.location.msg_contents(f"The {self} beeps twice.")
            return

        if code == self.db.code:
            if mode == "unlock":
                if self.db.locked:
                    self.location.msg_contents(f"The {self} beeps happily and unlocks.")
                    self.db.locked = False
                else:
                    self.location.msg_contents(f"Nothing happens.")
                return

            elif mode == "program":
                self.location.msg_contents(f"The {self} beeps happily and the \"programming\" light begins to blink.")
                self.db.programming = True
                return

        else:
            self.location.msg_contents(f"The {self} beeps angrily.")
            return


class Beeper(Furniture):
    def at_object_creation(self):
        super().at_object_creation();

    def on_push(self, caller, args):
        try:
            count = int(args)
        except:
            caller.msg(f"The {self} doesn't do anything.")
            return

        for i in range(0, count):
            self.location.msg_contents(f"The {self} beeps.")
