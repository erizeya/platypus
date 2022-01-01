from evennia.commands.command import Command as BaseCommand
from evennia.utils import utils, evtable
from evennia.utils.search import search_object
from custom import cardinal_to_index, is_valid_cardinal, print_cardinal_list
from custom import genderize
from typeclasses.npc import Npc
from typeclasses.furniture import Bar

class Command(BaseCommand):
    pass

# Wear a wearable object.
#
# Usage:
#  wear [object]
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
            #Detect if we're looking for multiples
            target_obj = target_obj.split(" ")
            if is_valid_cardinal(target_obj[0]):
                count = cardinal_to_index(target_obj[0])
                del target_obj[0]
                target_obj = " ".join(target_obj)
            else:
                target_obj = " ".join(target_obj)

            obj = caller.search(
                target_obj,
                location=caller,
                quiet=True,
            )

            if len(obj) == 0:
                caller.msg(f"You aren't carrying {self.args.strip()}")
                return
            elif len(obj) > 1 and count is None:
                print_cardinal_list(f"Which {target_obj}?", obj, caller)
                return
            elif len(obj) > 1 and not count is None:
                obj = obj[count]
            else:
                obj = obj[0]

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
            #Detect if we're looking for multiples
            target_obj = target_obj.split(" ")
            if is_valid_cardinal(target_obj[0]):
                count = cardinal_to_index(target_obj[0])
                del target_obj[0]
                target_obj = " ".join(target_obj)
            else:
                target_obj = " ".join(target_obj)

            obj = caller.search(
                target_obj,
                location=caller,
                quiet=True,
            )

            if len(obj) == 0:
                caller.msg(f"You aren't carrying {self.args.strip()}")
                return
            elif len(obj) > 1 and count is None:
                print_cardinal_list(f"Which {target_obj}?", obj, caller)
                return
            elif len(obj) > 1 and not count is None:
                obj = obj[count]
            else:
                obj = obj[0]

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
                target_obj = caller.search(target)
                if target_obj and target_obj.db.furniture and target_obj.db.seating:
                    caller.msg(f"You sit on the {target_obj}.")
                    caller.location.msg_contents(f"{caller.name} sits on the {target_obj}.",exclude=caller)
                    target_obj.db.occupants.append(caller)
                    caller.db.occupying = target_obj
                    caller.db.sitting = True
                else: 
                    caller.msg(f"You can't sit on {target_obj}")
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

# Set your look place
# 
# Usage:
#   @lp <look place message>
# 
class CmdLp(BaseCommand):
    key = "@lp"
    aliases = []
    lock = "cmd:all()"
    help_category = "General"

    def func(self):
        if not self.args:
            self.caller.msg("@look_place message cleared.")
            self.caller.db.look_place = " is here."
        else:
            self.caller.db.look_place = self.args
        self.caller.msg(f"Other players now see: {self.caller}{self.caller.db.look_place}")

# Set or display your nakeds
# 
# Usage:
#   @naked[s]
#       Display all nakeds as a lit
#   @naked[s] <location> = <description>
#       Set a specific naked 
#
class CmdNaked(BaseCommand):
    """
    """
    key = "@naked"
    aliases = ["@nakeds"]
    lock = "cmd:all()"
    help_category = "General"


    def func(self):
        nakeds = ["head", "face", "upper_body", "hands", "lower_body", "feet"]
        if not self.args:
            for naked in nakeds:
                self.caller.msg(f"@naked {naked} = "+self.caller.db.naked[naked])
        else:
            arg_list = self.args.split("=")
            l_arg = arg_list[0].strip()
            r_arg = arg_list[1].strip()

            #Set object properties
            if l_arg in nakeds:
                self.caller.db.naked[l_arg] = r_arg
                self.caller.msg(f"@naked {l_arg} is now \"{r_arg}\"")
            else:
                self.caller.msg("Invalid naked location")

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
    
        #Detect if we're looking for multiple
        target_obj = target_obj.split(" ")
        if is_valid_cardinal(target_obj[0]):
            count = cardinal_to_index(target_obj[0])
            del target_obj[0]
            target_obj = " ".join(target_obj)
        else:
            target_obj = " ".join(target_obj)
        
        obj = caller.search(
            target_obj,
            location=caller,
            nofound_string=f"You aren't carrying {self.args.strip()}",
            quiet=True,
        )

        if len(obj) == 0: 
            caller.msg(f"You aren't carrying {self.args.strip()}")
            return
        elif len(obj) > 1 and count is None:
            print_cardinal_list(f"Which {target_obj}?", obj, caller)
            return
        elif len(obj) > 1 and not count is None:
            obj = obj[count]
        else:
            obj = obj[0]

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

# Lower a held item from being in-hand to inventory.
#
# Usage:
#   lower <item>
#       Lower the specific in-hand item and return it to the inventory.
#
# Supports multiples.
class CmdLower(BaseCommand):
    """
    TODO: This description
    """

    key = "lower"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        target_obj = self.args.strip()
        count = None
        if not self.args:
            caller.msg("Hold what?")
            return

        #Detect if we're looking for multiple
        target_obj = target_obj.split(" ")
        if is_valid_cardinal(target_obj[0]):
            count = cardinal_to_index(target_obj[0])
            del target_obj[0]
            target_obj = " ".join(target_obj)
        else:
            target_obj = " ".join(target_obj)

        obj = caller.search(
            target_obj,
            location=caller,
            nofound_string=f"You aren't carrying {self.args.strip()}.",
            quiet=True
        )

        if len(obj) == 1:
            obj = obj[0]
        elif len(obj) > 1 and count is None:
            #See if we can figure this out by which item is being held in the hand.
            if caller.db.l_hand is None or caller.db.r_hand is None:
                for i in obj:
                    if i == caller.db.r_hand:
                        caller.db.r_hand = None
                        caller.msg(f"You put your {i} away.")
                        caller.location.msg_contents(genderize(f"{caller.name} puts %p {i} away.",caller.db.gender), exclude=caller)
                        return
                    elif i == caller.db.l_hand:
                        caller.db.l_hand = None
                        caller.msg(f"You put your {i} away.")
                        caller.location.msg_contents(genderize(f"{caller.name} puts %p {i} away.",caller.db.gender), exclude=caller)
                        return
            print_cardinal_list(f"Which {target_obj}?", obj, caller)
            return
        elif len(obj) > 1 and count >= 0:
            obj = obj[count]

        if caller.db.r_hand == obj:
            caller.db.r_hand = None
        elif caller.db.l_hand == obj:
            caller.db.l_hand = None
        else:
            caller.msg(f"You are not holding {self.args.strip()}.")

        caller.msg(f"You put your {obj} away.")
        caller.location.msg_contents(genderize(f"{caller.name} puts %p {obj} away.",caller.db.gender), exclude=caller)

# Change your preferred pronouns
#
# Usage:
#   @pronouns <pronoun number>
#
class CmdGender(BaseCommand):
    key = "@pronouns"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        help_msg = "Usage: @pronouns [type]\nValid options:\n\tfeminine\n\tmasculine\n\tspivak"
        if not self.args:
            caller.msg(help_msg)
            return
        else:
            arg = self.args.split(" ")[1].strip()
            if arg == "feminine":
                caller.db.gender = 1
            elif arg == "masculine":
                caller.db.gender = 2
            elif arg == "spivak":
                caller.db.gender = 0
            else:
                caller.msg(help_msg)

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
        args = self.args
        caller = self.caller
        location = self.caller.location
        error_msg = "Usage: take <object> from <container>"
        count = None
        if not args:
            caller.msg(error_msg)
            return

        #Split args out
        args_list = args.strip().split(" ")
        #Check for cardinals
        if is_valid_cardinal(args_list[0].strip()):
            count = cardinal_to_index(args_list[0].strip())
            del args_list[0]
        try:
            split = args_list.index("from")
        #Case 1, regular take
        except:
            #Identify and find object
            target_obj = " ".join(args_list)
            obj = caller.search(target_obj,quiet=True,location=caller.location)

            #Check for multiple
            if len(obj) == 0: 
                caller.msg(f"You don't see a {target_obj} in here.")
                return
            elif len(obj) == 1:
                obj = obj[0]
            elif len(obj) > 1 and count is None:
                print_cardinal_list(f"Which {target_obj}?", obj, caller)
                return
            elif count is not None:
                obj = obj[count]

            #move object into character hands
            if not (caller.db.l_hand == None or caller.db.r_hand == None):
                caller.msg(f"Your hands are full.")
                return

            # calling at_before_get hook method
            if not obj.at_before_get(caller):
                return

            #Grab the item and call the post-grab hook
            if caller.db.r_hand == None:
                obj.move_to(caller, quiet=True)
                caller.db.r_hand = obj
                obj.at_get(caller)
                caller.msg(f"You take the {obj}") 
            elif caller.db.l_hand == None:
                obj.move_to(caller, quiet=True)
                caller.db.l_hand = obj
                obj.at_get(caller)
                caller.msg(f"You take the {obj}") 

            return

        #Case 2, take from container
        target_obj = " ".join(args_list[:split])
        target_container = " ".join(args_list[split+1:])
        if not target_obj or not target_container:
            caller.msg(error_msg)
            return 

        #verify container
        container = caller.search(target_container)
        if not container:
            caller.msg(error_msg)
            return 

        #find object in container
        obj = container.search(target_obj, location=container)
        if not obj:
            caller.msg(f"Cannot find {target_obj} in {container}")
            caller.msg(error_msg)
            return 

        #move object into character hands
        if not (caller.db.l_hand == None or caller.db.r_hand == None):
            caller.msg(f"Your hands are full.")
            return

        # calling at_before_get hook method
        if not obj.at_before_get(caller):
            return

        #Grab and call the post-grab hook.
        if caller.db.r_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.r_hand = obj
            obj.at_get(caller)
        elif caller.db.l_hand == None:
            obj.move_to(caller, quiet=True)
            caller.db.l_hand = obj
            obj.at_get(caller)

        caller.msg(f"You take a {obj} from the {container}.")
        container.location.msg_contents(f"{caller} takes a {obj} from the {container}.", exclude=caller)

            

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
        error_msg = "Usage: put <object> in <container>"
        if not args:
            caller.msg(error_msg)
            return

        #Split args out
        args_list = args.strip().split(" ")
        split = args_list.index("in")
        target_obj = " ".join(args_list[:split])
        target_container = " ".join(args_list[split+1:])
        if not target_obj or not target_container:
            caller.msg(error_msg)
            return 

        #verify container
        container = caller.search(target_container)
        if not container:
            caller.msg(error_msg)
            return 

        #find object in character's hand
        obj = caller.search(target_obj, location=caller)
        if not obj:
            caller.msg(error_msg)
            return
        if not (caller.db.l_hand == obj or caller.db.r_hand == obj):
            caller.msg(f"You have to be holding your {obj} to put it {container.db.prep} the {container}.")
            return

        #move object into character hands
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
        
        target = caller.search(self.args.strip())

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
        count = None
        if not self.args:
            caller.msg("Drop what?")
            return

        #Detect if we're looking for multiple
        target_obj = target_obj.split(" ")
        if is_valid_cardinal(target_obj[0]):
            count = cardinal_to_index(target_obj[0])
            del target_obj[0]
            target_obj = " ".join(target_obj)
        else:
            target_obj = " ".join(target_obj)

        obj = caller.search(
            target_obj,
            location=caller,
            nofound_string="You aren't carrying %s." % self.args,
            multimatch_string="You carry more than one %s:" % self.args,
            quiet=True
        )

        if len(obj) == 0:
            caller.msg(f"You don't have a {target_obj} to drop.")
        elif len(obj) > 1 and count == None:
            print_cardinal_list(f"Drop which {target_obj}?", obj, caller)
            return
        elif len(obj) >1 and not count == None:
            obj = obj[count]
        else:
            obj = obj[0]

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

        obj = caller.search(
            target_obj
        )

        if not object:
            return

        if not (obj.db.door or obj.db.container):
            caller.msg(f"It doesn't look like the {obj} is something you can open.")
            return

        if(obj.db.open):
            caller.msg(f"The {obj} is already open.")
            return

        #Open the door
        obj.db.open = True

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

        obj = caller.search(
            target_obj
        )
        if not object:
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

class CmdPair(BaseCommand):

    key = "!pair"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        arg_list = self.args.strip().split(" ") 
        target_obj = arg_list[0]
        target_link = arg_list[1]

        obj = caller.search(
            target_obj
        )

        link = search_object(
            target_link,
            exact = True
        )[0]

        if not (obj.db.door and link.db.door):
            caller.msg(f"Both objects need to be doors.")
            return

        caller.msg(f"Linking {obj} to {link}")

        obj.db.pair = link 
        link.db.pair = obj

class CmdLink(BaseCommand):

    key = "!link"
    locks = "cmd:all()"

    def func(self):
        caller = self.caller
        arg_list = self.args.strip().split(" ") 
        target_obj = arg_list[0]
        target_link = arg_list[1]
        help_str = "Usage !link <NPC> <Bar>"

        obj = caller.search(
            target_obj
        )

        link = search_object(
            target_link,
            exact = True
        )[0]

        if not type(obj) is Npc:
            caller.msg(f"First argument must be an NPC\n{help_str}")
            return

        if not type(link) is Bar:
            caller.msg(f"Second argument must be an NPC\n{help_str}")
            return

        obj.db.link = link

        caller.msg(f"Linked {obj} to {link}")
