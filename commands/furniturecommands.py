
from evennia import Command
from evennia import CmdSet
from evennia import default_cmds
from evennia import create_object
from typeclasses.consumable import Tea

# Admin commands for modifying furniture
# 
# Usage:
#   !furniture position = <position string>
#       Sets the position of furniture in a room desc. Ex: "against the far wall."
#   !furniture occupant_pose = <string>
#       Sets the description of occupants of furniture in a room desc. Ex: "sitting on the"
#   !furniture seating = <on/off>
#       Enables/disables the ability for characters to sit on furniture.
class CmdFurnitureProperties(Command):
    key = "!furniture"
    locks = "cmd:perm_above(Helper)"

    def func(self):
        caller = self.caller
        location = caller.location
        obj = self.obj

        #Parse arguments
        arg_list = self.args.split("=")
        try:
            l_arg = arg_list[0].strip()
            r_arg = arg_list[1].strip()
        except:
            caller.msg("Missing arguments")
            return 
        
        #Set object properties
        if l_arg == "position":
            obj.db.position = r_arg
        elif l_arg == "occupant_pose":
            obj.db.occupant_pose = r_arg
        elif l_arg == "seating":
            if r_arg == "on":
                obj.db.seating = True
                caller.msg(f"{obj} now allows sitting.")
            elif r_arg == "off":
                obj.db.seating = False
                caller.msg(f"{obj} no longer allows sitting.")
        else:
            caller.msg("valid l-hand values are: position, occupant_pose")

class FurnitureCmdSet(CmdSet):
    key = "furniturecmdset"
    
    def at_cmdset_creation(self):
        self.add(CmdFurnitureProperties())
