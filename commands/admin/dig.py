from evennia.commands.default.building import ObjManipCommand
from django.conf import settings
from evennia.utils import create

class _CmdDig(ObjManipCommand):
    """
    Deprecated. Please use !dig instead.
    """

    key = "@dig"
    aliases = "dig"

    def func(self):
        self.caller.msg("Deprecated. Please use !dig instead.")

class CmdDig(ObjManipCommand):
    """
    build new rooms and connect them to the current location

    Usage:
      dig[/switches] <roomname>[;alias;alias...][:typeclass]
            [= <exit_to_there>[;alias][:typeclass]]
               [, <exit_to_here>[;alias][:typeclass]]

    Switches:
       tel or teleport - move yourself to the new room
       door - set up the exit as an open/closable door

    Examples:
       dig kitchen = north;n, south;s
       dig house:myrooms.MyHouseTypeclass
       dig sheer cliff;cliff;sheer = climb up, climb down

    This command is a convenient way to build rooms quickly; it creates the
    new room and you can optionally set up exits back and forth between your
    current room and the new one. You can add as many aliases as you
    like to the name of the room and the exits in question; an example
    would be 'north;no;n'.
    """

    key = "!dig"
    switch_options = ("teleport","door")
    locks = "cmd:perm(dig) or perm(Builder)"
    help_category = "Building"

    # lockstring of newly created rooms, for easy overloading.
    # Will be formatted with the {id} of the creating object.
    new_room_lockstring = (
        "control:id({id}) or perm(Admin); "
        "delete:id({id}) or perm(Admin); "
        "edit:id({id}) or perm(Admin)"
    )

    def func(self):
        """Do the digging. Inherits variables from ObjManipCommand.parse()"""

        caller = self.caller

        if not self.lhs:
            string = "Usage: dig[/teleport] <roomname>[;alias;alias...]" "[:parent] [= <exit_there>"
            string += "[;alias;alias..][:parent]] "
            string += "[, <exit_back_here>[;alias;alias..][:parent]]"
            caller.msg(string)
            return

        room = self.lhs_objs[0]

        if not room["name"]:
            caller.msg("You must supply a new room name.")
            return
        location = caller.location

        # Create the new room
        typeclass = room["option"]
        if not typeclass:
            typeclass = settings.BASE_ROOM_TYPECLASS

        # create room
        new_room = create.create_object(
            typeclass, room["name"], aliases=room["aliases"], report_to=caller
        )
        lockstring = self.new_room_lockstring.format(id=caller.id)
        new_room.locks.add(lockstring)
        alias_string = ""
        if new_room.aliases.all():
            alias_string = " (%s)" % ", ".join(new_room.aliases.all())
        room_string = "Created room %s(%s)%s of type %s." % (
            new_room,
            new_room.dbref,
            alias_string,
            typeclass,
        )

        # create exit to room
        exit_to_string = ""
        exit_back_string = ""
        new_to_exit =  None
        new_back_exit = None    

        if self.rhs_objs:
            to_exit = self.rhs_objs[0]
            if not to_exit["name"]:
                exit_to_string = "\nNo exit created to new room."
            elif not location:
                exit_to_string = "\nYou cannot create an exit from a None-location."
            else:
                # Build the exit to the new room from the current one
                typeclass = to_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS

                new_to_exit = create.create_object(
                    typeclass,
                    to_exit["name"],
                    location,
                    aliases=to_exit["aliases"],
                    locks=lockstring,
                    destination=new_room,
                    report_to=caller,
                )



                alias_string = ""
                if new_to_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_to_exit.aliases.all())
                exit_to_string = "\nCreated Exit from %s to %s: %s(%s)%s."
                exit_to_string = exit_to_string % (
                    location.name,
                    new_room.name,
                    new_to_exit,
                    new_to_exit.dbref,
                    alias_string,
                )

        # Create exit back from new room

        if len(self.rhs_objs) > 1:
            # Building the exit back to the current room
            back_exit = self.rhs_objs[1]
            if not back_exit["name"]:
                exit_back_string = "\nNo back exit created."
            elif not location:
                exit_back_string = "\nYou cannot create an exit back to a None-location."
            else:
                typeclass = back_exit["option"]
                if not typeclass:
                    typeclass = settings.BASE_EXIT_TYPECLASS
                new_back_exit = create.create_object(
                    typeclass,
                    back_exit["name"],
                    new_room,
                    aliases=back_exit["aliases"],
                    locks=lockstring,
                    destination=location,
                    report_to=caller,
                )
                alias_string = ""
                if new_back_exit.aliases.all():
                    alias_string = " (%s)" % ", ".join(new_back_exit.aliases.all())
                exit_back_string = "\nCreated Exit back from %s to %s: %s(%s)%s."
                exit_back_string = exit_back_string % (
                    new_room.name,
                    location.name,
                    new_back_exit,
                    new_back_exit.dbref,
                    alias_string,
                )
        caller.msg("%s%s%s" % (room_string, exit_to_string, exit_back_string))
        if "door" in self.switches:
            caller.msg("Linking doors")
            new_to_exit.db.door = True 
            new_back_exit.db.door = True
            new_to_exit.db.pair = new_back_exit
            new_back_exit.db.pair = new_to_exit
        if new_room and "teleport" in self.switches:
            caller.move_to(new_room)
