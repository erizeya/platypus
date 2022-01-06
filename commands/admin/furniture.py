from evennia import Command
from custom import is_valid_cardinal

class CmdFurniture(Command):
    """
    Admin commands for modifying furniture
    
    Usage:
      !furniture <furniture> position <position string>
          Sets the position of furniture in a room desc. Ex: "against the far wall."
      !furniture <furniture> occupant_pose <string>
          Sets the description of occupants of furniture in a room desc. Ex: "sitting on the"
      !furniture <furniture> seating <on/off>
          Enables/disables the ability for characters to sit on furniture.
    """
    key = "!furniture"
    locks = "cmd:perm_above(Helper)"
    help_category = "Building"

    def func(self):
        caller = self.caller
        location = caller.location
        args = self.args.strip()

        #Parse arguments
        arg_list = args.split(" ")

        #Check for multiples
        if is_valid_cardinal(arg_list[0]):
            # [0] is count
            # [1] is item
            # [2] is subcommand
            target_obj = arg_list[0]+" "+arg_list[1]
            del arg_list[0]
        else:
            # [0] is item
            # [1] is subcommand
            target_obj = arg_list[0]
        del arg_list[0]

        #Search for the object
        obj = caller.multiple_search(target_obj, location=caller.location)
        if not obj:
            return
        
        # [0] is now be the subcommand after prior deletions
        subcommand = arg_list[0]
        del arg_list[0]

        #What remains in the argument being provided to the subcommand
        arg = " ".join(arg_list)
        
        #Set object properties
        if subcommand == "position":
            obj.db.position = arg
            caller.msg("Furniture position desc now set.")
        elif subcommand == "occupant_pose":
            obj.db.occupant_pose = arg
            caller.msg("Furniture occupant_pose desc now set.")
        elif subcommand == "seating":
            if arg == "on":
                obj.db.seating = True
                caller.msg(f"{obj} now allows sitting.")
            elif arg == "off":
                obj.db.seating = False
                caller.msg(f"{obj} no longer allows sitting.")
        else:
            caller.msg("valid subcommand values are: position, occupant_pose, and seating.")

