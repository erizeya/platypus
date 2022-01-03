"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from evennia.utils import make_iter
from custom import genderize, cardinal_to_index, is_valid_cardinal, print_cardinal_list 

class Character(DefaultCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_object_creation(self):
        #Gender and pronouns
        self.db.gender = 0

        #Hands
        self.db.l_hand = None
        self.db.r_hand = None

        #Nakeds
        self.db.naked = {
            "head": "%S has a forgettable head.",
            "face": "%S has an unremarkable face.",
            "upper_body": "%P upper body isn't anything special.",
            "hands": "%S has unnotable hands.",
            "lower_body": "%P lower body is commonly plain.",
            "feet": "%S has boring feet."
        }

        #Worn clothing
        self.db.worn = {
                "head": [],
                "face": [],
                "upper_body": [],
                "hands": [],
                "lower_body": [],
                "feet": []
        }

        "Position"
        self.db.occupying = None
        self.db.sitting = False

        "Look place"
        self.db.look_place = " is here."

    def return_appearance(self, looker):
        # Display character name
        text = "|c%s|n\n" % self.get_display_name(looker)

        #Display character desc
        text += self.db.desc

        #Display character nakeds
        text += "\n\n"
        naked_group = ["head", "face"]
        for naked in naked_group:
            if not self.db.worn["head"]:
                text += genderize(self.db.naked[naked], self.db.gender)
            else:
                text += self.db.worn[naked][-1].db.worn
            text += " "
        text += "\n\n"
        naked_group = ["upper_body", "hands"]
        for naked in naked_group:
            if not self.db.worn["head"]:
                text += genderize(self.db.naked[naked], self.db.gender)
            else:
                text += self.db.worn[naked][-1].db.worn
            text += " "
        text += "\n\n"
        naked_group = ["lower_body", "feet"]
        for naked in naked_group:
            if not self.db.worn["head"]:
                text += genderize(self.db.naked[naked], self.db.gender)
            else:
                text += self.db.worn[naked][-1].db.worn
            text += " "

        #Display character items
        text += "\n\n"
        if self.db.l_hand == None and self.db.r_hand == None:
            text += genderize(f"%P hands are empty",self.db.gender)
        elif not self.db.l_hand == None and self.db.r_hand == None:
            text += genderize(f"%S has a {self.db.l_hand} in their left hand.",self.db.gender)
        elif self.db.l_hand == None and not self.db.r_hand == None:
            text += genderize(f"%S has a {self.db.r_hand} in their right hand.",self.db.gender)
        elif not self.db.l_hand == None and not self.db.r_hand == None:
            text += genderize(f"%S has a {self.db.l_hand} in their left hand and a {self.db.r_hand} in their right hand.",self.db.gender)
        return text

    def at_pre_say(self, message, **kwargs):
        """
        Before the object says something.

        This hook is by default used by the 'say' and 'whisper'
        commands as used by this command it is called before the text
        is said/whispered and can be used to customize the outgoing
        text from the object. Returning `None` aborts the command.

        Args:
            message (str): The suggested say/whisper text spoken by self.
        Keyword Args:
            whisper (bool): If True, this is a whisper rather than
                a say. This is sent by the whisper command by default.
                Other verbal commands could use this hook in similar
                ways.
            receivers (Object or iterable): If set, this is the target or targets for the
                say/whisper.

        Returns:
            message (str): The (possibly modified) text to be spoken.

        """
        return message

    def at_say(
        self,
        message,
        msg_self=None,
        msg_location=None,
        receivers=None,
        msg_receivers=None,
        target=None,
        **kwargs,
    ):
        msg_type = "say"
        if kwargs.get("whisper", False):
            # whisper mode
            msg_type = "whisper"
            msg_self = (
                '{self} whisper to {all_receivers}, "|n{speech}|n"'
                if msg_self is True else msg_self
            )
            msg_receivers = msg_receivers or '{object} whispers: "|n{speech}|n"'
            msg_location = msg_location or '{object} whispers to {all_receivers}'
        if kwargs.get("to", False):
            msg_type = "to"
            msg_self = (
                'You [to {all_receivers}]: |n{speech}|n'
                if msg_self is True else msg_self
            )
            msg_receivers = msg_receivers or '{object} [to You]: |n{speech}|n'
            msg_location = msg_location or '{object} [to {all_receivers}]: |n{speech}|n'
        else:
            msg_self = '{self} sei, "|n{speech}|n"' if msg_self is True else msg_self
            msg_location = msg_location or '{object} says, "{speech}"'
            msg_receivers = msg_receivers or message

        custom_mapping = kwargs.get("mapping", {})
        receivers = make_iter(receivers) if receivers else None
        location = self.location

        if msg_self:
            self_mapping = {
                "self": "You",
                "object": self.get_display_name(self),
                "location": location.get_display_name(self) if location else None,
                "receiver": None,
                "all_receivers": ", ".join(recv.get_display_name(self) for recv in receivers)
                if receivers
                else None,
                "speech": message,
            }
            self_mapping.update(custom_mapping)
            self.msg(text=(msg_self.format(**self_mapping), {"type": msg_type}), from_obj=self)

        if receivers and msg_receivers:
            receiver_mapping = {
                "self": "You",
                "object": None,
                "location": None,
                "receiver": None,
                "all_receivers": None,
                "speech": message,
            }
            for receiver in make_iter(receivers):
                individual_mapping = {
                    "object": self.get_display_name(receiver),
                    "location": location.get_display_name(receiver),
                    "receiver": receiver.get_display_name(receiver),
                    "all_receivers": ", ".join(recv.get_display_name(recv) for recv in receivers)
                    if receivers
                    else None,
                }
                receiver_mapping.update(individual_mapping)
                receiver_mapping.update(custom_mapping)
                receiver.msg(
                    text=(msg_receivers.format(**receiver_mapping), {"type": msg_type}),
                    from_obj=self,
                )

        if self.location and msg_location:
            location_mapping = {
                "self": "You",
                "object": self,
                "location": location,
                "all_receivers": ", ".join(str(recv) for recv in receivers) if receivers else None,
                "receiver": None,
                "speech": message,
            }
            location_mapping.update(custom_mapping)
            exclude = []
            if msg_self:
                exclude.append(self)
            if receivers:
                exclude.extend(receivers)
            self.location.msg_contents(
                text=(msg_location, {"type": msg_type}),
                from_obj=self,
                exclude=exclude,
                mapping=location_mapping,
            )

    def multiple_search(self, target_obj, **kwargs):

        location = self
        mode = None
        count = None

        if "location" in kwargs:
            location = kwargs["location"]

        if "mode" in kwargs:
            mode = kwargs["mode"]

        target_obj = target_obj.split(" ")
        if is_valid_cardinal(target_obj[0]):
            count = cardinal_to_index(target_obj[0])
            del target_obj[0]
            target_obj = " ".join(target_obj)
        else:
            target_obj = " ".join(target_obj)

        if mode is "look":
            obj = self.search(
                target_obj,
                quiet=True,
            )
        else:
            obj = self.search(
                target_obj,
                location=location,
                quiet=True,
            )

        if len(obj) == 0 and mode is "look":
            self.msg(f"You don't see a {target_obj}")
            return None
        elif len(obj) == 0 and location == self:
            self.msg(f"You aren't carrying a {target_obj}")
            return None
        elif len(obj) == 0:
            self.msg(f"You don't see a {target_obj}")
            return None
        elif len(obj) > 1 and count is None:
            print_cardinal_list(f"Which {target_obj}?", obj, self)
            return None
        elif len(obj) > 1 and not count is None:
            return obj[count]
        else:
            return obj[0]
