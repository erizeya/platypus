from evennia.commands.command import Command as BaseCommand
from evennia.utils import utils, evtable
from custom import genderize

class Command(BaseCommand):
    pass

# Wear a wearable object.
#
# Usage:
#  wear [object]
#
# Supports multiples
#
class CmdWear(BaseCommand):
    key = "wear"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        count = None

        if not self.args:
            caller.msg("What do you want to wear?")
        else:
            obj = caller.multiple_search(target_obj)
            if not obj:
                return
            #Check if the object is wearable
            if not obj.db.wearable:
                caller.msg(f"How are you expecting to wear your {obj.name}?")

            #Check if the object is already being worn
            elif obj.db.wearing:
                caller.msg(f"You are already wearing your {obj.name}")

            #If checks pass, equip item
            else:
                caller.msg("You put on your %s" % obj.name)
                caller.location.msg_contents(genderize(f"{caller.name} puts on %p {obj.name}",caller.db.gender),exclude=caller)
                obj.db.wearing = True
                caller.db.worn[obj.db.coverage].append(obj)

# Remove a wearable object
# 
# Usage:
#   remove [item]
#
# Supports multiples
#
class CmdRemove(BaseCommand):

    key = "remove"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        count = None

        if not self.args:
            caller.msg("What do you want to remove?")
        else:

            obj = caller.multiple_search(target_obj)
            if not obj:
                return

            #Check if the object is worn
            if not obj.db.wearing:
                caller.msg("You are not wearing your %s." % obj.name)

            #If checks pass, equip item
            else:
                #Make sure nothing is over the item
                if caller.db.worn[obj.db.coverage][-1].id != obj.id:
                    caller.msg(f"You are wearing something over your {obj.name}.")
                else:
                    caller.msg(f"You take off on your {obj.name}.")
                    caller.location.msg_contents(f"{caller.name} takes off their {obj.name}.",exclude=caller)
                    obj.db.wearing = False
                    caller.db.worn[obj.db.coverage].pop()

# View the contents of your inventory.
# Usage:
#   inventory
#   inv
#
# Modifies default Evennia behavior
#
class CmdInventory(BaseCommand):

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            from evennia.utils.ansi import raw as raw_ansi

            table = self.styled_table(border="header")
            for item in items:
                if item.db.wearing:
                    table.add_row(
                        f"|C{item.name} (|cworn|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                elif item == self.caller.db.l_hand:
                    table.add_row(
                        f"|C{item.name} (|cleft hand|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                elif item == self.caller.db.r_hand:
                    table.add_row(
                        f"|C{item.name} (|cright hand|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                else:
                    table.add_row(
                        f"|C{item.name}|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )

            string = f"|wYou are carrying...\n{table}"
        self.caller.msg(string)

# Sit on the ground or on an object. Sitting characters cannot move.
#
# Usage:
#   sit[ [on/at] <furniture>]
#
# TODO:
#   multiple support
#
class CmdSit(BaseCommand):
    key = "sit"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller

        if not self.args:
            caller.msg("You sit on the ground.")
            caller.location.msg_contents(f"{caller.name} sits on the ground.", exclude=caller)
            caller.db.sitting = True
        else:
            #Split out arguments to
            args = self.args.split(" ")
            target = None
            if args[1] == "on" and len(args) == 2:
                caller.msg("Sit on what?")
            elif args[1] == "at" and len(args) == 2:
                caller.msg("Sit at what?")
            elif (args[1] == "on" or args[1] == "at") and len(args) > 2:
                target = " ".join(args[2:])
            else:
                target = " ".join(args[1:])

            if target:
                #Find the object to sit on and confirm we can sit on it.
                
                obj = caller.multiple_search(target,location=caller.location)
                if obj and obj.db.furniture and obj.db.seating:
                    caller.msg(f"You sit on the {obj}.")
                    caller.location.msg_contents(f"{caller.name} sits on the {obj}.",exclude=caller)
                    obj.db.occupants.append(caller)
                    caller.db.occupying = obj
                    caller.db.sitting = True
                else: 
                    caller.msg(f"You can't sit on {obj}")
            else:
                caller.msg("Usage: sit[ [on/at] <furniture>]")

# Stand up from sitting
# 
# Usage:
#   stand
# 
class CmdStand(BaseCommand):
    key = "stand"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        if caller.db.sitting:
            if caller.db.occupying:
                caller.db.occupying.db.occupants.remove(caller)
                caller.msg(f"You stand up from the {caller.db.occupying.name}.")
                caller.location.msg_contents(f"{caller.name} stands up from the {caller.db.occupying.name}.",exclude=caller)
                caller.db.occupying = None
            else:
                caller.msg("You stand up.")
                caller.location.msg_contents(f"{caller.name} stands up.",exclude=caller)
            caller.db.sitting = False
        else:
            caller.msg("You are not sitting.")

# Direct a message to a specific player or group of players
#
# Usage:
#   to <character>
#
class CmdTo(BaseCommand):
    key = "to"
    locks = "cmd:all()"

    def func(self):
        """Run the whisper command"""

        caller = self.caller
        args = self.args

        args_l = args.strip().split(" ")
        lhs = args_l[0]
        rhs = " ".join(args_l[1:])

        if not lhs or not rhs:
            caller.msg("Usage: to <target> <message>")
            return

        target = caller.search(lhs)
        speech = rhs

        # If the speech is empty, abort the command
        if not speech or not lhs:
            return

        # Call a hook to change the speech before whispering
        speech = caller.at_pre_say(speech, to=True)

        # no need for self-message if we are whispering to ourselves (for some reason)
        #msg_self = None if caller is lhs else True

        caller.at_say(speech, msg_self=True, receivers=target, to=True)

# Takes an item that is currently in inventory and puts it into a free hand.
#
# Usage:
#   hold <item>
#       Puts item in the right hand, left if right is not free.
#   hold[-left/-right] <item>
#       Puts an item specifically into the left or right hand.
#
# Supports multiples
class CmdHold(BaseCommand):
    key = "hold"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        count = None
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Hold what?")
            return

        #Split out left/right arg.
        arg_list = self.args.split(" ")
        target_hand = None
        if arg_list[0].strip() == "-left":
            target_hand = "left"
            target_obj = " ".join(arg_list[1:])
        elif arg_list[0].strip() == "-right":
            target_hand = "right"
            target_obj = " ".join(arg_list[1:])
    
        #Search for object
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        #Case for wearing item
        if obj.db.wearing:
            caller.msg("You cannot hold something you're wearing.")

        #Case for both hands full
        elif caller.db.r_hand == obj or caller.db.l_hand == obj:
            caller.msg(f"You are already holding {obj}.")

        #Case for target_handed left hand but its full
        elif target_hand == "left" and not caller.db.l_hand == None:
            caller.msg("Your left hand is full")
        #Case for target_handed right hand but its full
        elif target_hand == "right" and not caller.db.r_hand == None:
            caller.msg("Your right hand is full.")

        #Case for empty right hand
        elif caller.db.r_hand == None and not target_hand == "left":
            caller.db.r_hand = obj
            caller.msg(f"You take your {obj} into your right hand")
            caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} in %p left hand",caller.db.gender), exclude=caller)

        #Case for empty left hand
        elif caller.db.l_hand == None and not target_hand == "right":
            caller.db.l_hand = obj
            caller.msg(f"You take your {obj} into your left hand")
            caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} in %p right hand",caller.db.gender), exclude=caller)

        else:
            caller.msg("Your hands are full.")

class CmdLower(BaseCommand):
    """
    Lower a held item from being in-hand to inventory.

    Usage:
      lower <item>
          Lower the specific in-hand item and return it to the inventory.
      lower-left/lower-right
          Lower the item held in the left or right hand.
    """

    key = "lower"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Lower what?")
            return

        #Case for lower-left and lower-right
        if "-left" in self.args:
            caller.msg(f"You put your {caller.db.l_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.l_hand} away.", caller.db.gender), exclude=caller)
            caller.db.l_hand = None
            return
        if "-right" in self.args:
            caller.msg(f"You put your {caller.db.r_hand} away.")
            caller.location.msg_contents(genderize(f"{caller} puts %p {caller.db.r_hand} away.", caller.db.gender), exclude=caller)
            caller.db.r_hand = None
            return

        #Search for the object
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        #Makre sure we're holding the object
        if caller.db.r_hand == obj:
            caller.db.r_hand = None
        elif caller.db.l_hand == obj:
            caller.db.l_hand = None
        else:
            caller.msg(f"You are not holding {self.args.strip()}.")
            return

        #Message player and room
        caller.msg(f"You put your {obj} away.")
        caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} away.",caller.db.gender), exclude=caller)

# Take an item from the ground
#
# Usage:
#   get/grab/take <item> [ from <container>]
#
class CmdGet(BaseCommand):
    key = "get"
    aliases = ["grab", "take"]
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        args = self.args.strip()
        caller = self.caller
        location = self.caller.location
        error_msg = "Usage: take <object> from <container>"
        if not args:
            caller.msg(error_msg)
            return

        #Check for full hands
        if not (caller.db.l_hand == None or caller.db.r_hand == None):
            caller.msg(f"Your hands are full.")
            return

        #Determine if we're taking from a container
        if " from " in args:
            arg_list = args.split(" from ")
            container = caller.multiple_search(arg_list[1], location=caller.location)
            if not container:
                return
            #Make sure the container is actually a container
            if not container.db.container:
                caller.msg(f"You can't put stuff into the {container}.")
                return

            #Ensure the container is open
            if not container.db.open:
                caller.msg(f"The {container} is closed.")
                return

            obj = caller.multiple_search(arg_list[0], location=container)
            if not obj:
                return
        else:
            obj = caller.multiple_search(args, location=caller.location)
            if not obj:
                return
            container = None

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        #Grab the item and call the post-grab hook
        if caller.db.r_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.r_hand = obj
        elif caller.db.l_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.l_hand = obj

        if not container:
            caller.msg(f"You take the {obj}.")
            caller.location.msg_contents(f"{caller} takes a {obj} from the {container}.", exclude=caller)
        else:
            caller.msg(f"You take the {obj} from the {container}.")
            caller.location.msg_contents(f"{caller} takes a {obj} from the {container}.", exclude=caller)

        return

            

# Put a held item into a container
#
#   Usage:
#       put <item> in <container>
#
class CmdPut(BaseCommand):
    key = "put"
    locks = "cmd:all()"

    def func(self):
        args = self.args
        caller = self.caller
        location = self.caller.location
        count = None
        error_msg = "Usage: put <object> in <container>"
        if not args:
            caller.msg(error_msg)
            return


        #Split args out
        args_list = args.strip().split(" ")
        try:
            split = args_list.index("in")
        except:
            caller.msg(error_msg)
            return 
        target_obj = " ".join(args_list[:split])
        target_container = " ".join(args_list[split+1:])
        if not target_obj or not target_container:
            caller.msg(error_msg)
            return 

        #verify container
        container = caller.multiple_search(target_container, location=caller.location)
        if not container:
            caller.msg(error_msg)
            return 

        #Ensure the container is really a container
        if not container.db.container:
            caller.msg(f"You can't take anything from the {container}")
            return

        #Ensure the container is open
        if not container.db.open:
            caller.msg(f"The {container} is closed.")
            return

        #find object in character's hand
        obj = caller.multiple_search(target_obj)
        if not obj:
            caller.msg(error_msg)
            return
        if not (caller.db.l_hand == obj or caller.db.r_hand == obj):
            caller.msg(f"You have to be holding your {obj} to put it {container.db.prep} the {container}.")
            return

        #remove object from character hands
        if caller.db.r_hand == obj:
            obj.move_to(container, quiet=True)
            caller.db.r_hand = None
        elif caller.db.l_hand == obj:
            obj.move_to(container, quiet=True)
            caller.db.l_hand = None

        caller.msg(f"You put your {obj} {container.db.prep} the {container}.")
        container.location.msg_contents(genderize(f"{caller} puts %p {obj} {container.db.prep} the {container}.", caller.db.gender), exclude=caller)

# Use an interactive object
#
#   Usage:
#       use <object>
#
class CmdUse(BaseCommand):
    key = "use"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        args = self.args

        if not args:
            caller.msg("What do you want to use?")
            return
        
        target = caller.multiple_search(args.strip(), location=caller.location)
        if not target:
            return

        if not (caller.db.l_hand == None or caller.db.r_hand == None):
            caller.msg(f"How do you expect to use the {target} with both your hands full?")
            return

        if not target:
            return

        target.on_use(caller)
#
#    Lets you drop an object from your inventory into the
#    location you are currently in.
#
#    Usage:
#      drop <obj>
class CmdDrop(BaseCommand):

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        if not self.args:
            caller.msg("Drop what?")
            return

        #Detect if we're looking for multiple
        obj = caller.multiple_search(target_obj)
        if not obj:
            return

        # Call the object script's at_before_drop() method.
        if not obj.at_before_drop(caller):
            return

        #Remove the item from hands if held
        if caller.db.l_hand == obj:
            caller.db.l_hand = None
        elif caller.db.r_hand == obj:
            caller.db.r_hand = None

        success = obj.move_to(caller.location, quiet=True)

        if not success:
            caller.msg("This couldn't be dropped.")
        else:
            caller.msg("You drop %s." % (obj.name,))
            caller.location.msg_contents("%s drops %s." % (caller.name, obj.name), exclude=caller)
            # Call the object script's at_drop() method.
            obj.at_drop(caller)

#
# Open objects such as doors and bags
#

class CmdOpen(BaseCommand):

    key = "open"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()

        obj = caller.multiple_search(target_obj, location=caller.location)
        if not obj:
            return

        if not (obj.db.door or obj.db.container):
            caller.msg(f"It doesn't look like the {obj} is something you can open.")
            return

        if(obj.db.open):
            caller.msg(f"The {obj} is already open.")
            return

        #Open the door
        if not obj.db.locked:
            obj.db.open = True
        else:
            caller.msg(f"The {obj} is locked.")
            return

        #Open the other side too if acting on a door
        if obj.db.door:
            obj.db.pair.db.open = True

        caller.msg(f"You open the {obj}")
        return

#
# Close objects such as doors and bags
#

class CmdClose(BaseCommand):

    key = "close"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()

        obj = caller.multiple_search(target_obj, location=caller.location)
        if not obj:
            return

        if not (obj.db.door or obj.db.container):
            caller.msg(f"It doesn't look like the {obj} is something you can close.")
            return
        if(not obj.db.open):
            caller.msg(f"The {obj} is already closed.")
            return

        #Close the door or container
        obj.db.open = False

        #Close the other side too if this is a door
        if obj.db.door:
            obj.db.pair.db.open = False

        caller.msg(f"You close the {obj}")
        return
