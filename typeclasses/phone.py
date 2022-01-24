from typeclasses.objects import Object
from typeclasses.characters import Character
from typeclasses.rooms import Room
from evennia import GLOBAL_SCRIPTS
from evennia.utils.search import search_object
from evennia.utils import delay
from custom import genderize
import re

#TODO: Voicemail
#TODO: Text messaging
#TODO: Whisper to phone
#TODO: Handling "-" in phone numbers

class Phone(Object):
    """
    This typeclass describes a phone.
    """
    def at_object_creation(self):
        #Assigns the phone number
        phone_manager = GLOBAL_SCRIPTS.phone_number_manager

        #The phone's phone number
        self.db.number = phone_manager.generate_number()

        #The phone number being called
        self.db.to_num = None

        #Whether a call is fully established
        self.db.connected = False

        #The object for the phone being called/connected to
        self.db.connected_to = None

        #Ringer set to silent or not
        self.db.silent = False

        #How many times the phone will ring
        self.db.ring_count = 5

        #Recently placed calls
        self.db.recent_in = []

        #Recent recieved calls
        self.db.recent_out = []

    def on_push(self, caller, args):
        #Hangupg phone
        if "disconnect" in args or "hangup" in args or "end" in args:
            if self.db.connected:
                if type(self.db.connected_to.location) is Character:
                    self.db.connected_to.location.msg(f"> *The other end hangs up*")
                    self.db.connected_to.location.msg("Your phone lets out a single beep and the screen reads, \"Call Ended.\"")
                if not self.db.silent: caller.msg("Your phone lets out a single beep and the screen reads, \"Call Ended.\"")
                caller.location.msg_contents(genderize(f"{caller} ends %p phone call.", caller.db.gender),exclude=caller)
                self.db.connected_to.db.connected = False
                self.db.connected_to.db.connected_to = None
                self.db.connected = False
                self.db.connected_to = None
                self.db.to_num = None

            else:
                caller.msg("You phone doesn't do anything.")
        
        #Cancel dialing a number
        if "cancel" in args:
            if self.db.to_num:
                self.db.to_num = None
                caller.msg("The number dialed into your phone disappears.")
                return
            #Cancel a call in progress TODO: Test this
            elif self.db.connected_to and not self.db.connected:
                target_phone = self.db.connected_to
                caller.msg("You cancel your phone call.")
                caller.location.msg_contents(genderize(f"{caller} ends %p phone call.", caller.db.gender),exclude=caller)
                target_phone.db.connected_to = None
                self.db.connected = False
                self.db.connected_to = None
                self.ndb.out_call = False
                if type(target_phone.location) is Character:
                    target_phone.location.location.msg_contents(f"{target_phone.location}'s phone stops ringing.", exclude=target_phone.location)
                    target_phone.location.msg("Your phone stops ringing.")
                elif type(target_phone.location) is Room:
                    target_phone.location.msg_contents(f"The phone stops ringing.")
            else:
                caller.msg("You phone doesn't do anything.")
        
        #Answer a ringing phone
        if "answer" in args:
            if self.db.connected:
                caller.msg("You're already on a call.")
            elif not self.ndb.ringing:
                caller.msg("Your phone isn't ringing.")
            elif self.ndb.ringing:
                self.db.connected = True
                self.db.connected_to.db.connected = True
                caller.msg("You answer your phone.")
                caller.location.msg_contents(genderize(f"{caller} answers %p {self}.", caller.db.gender),exclude=caller)
                if type(self.db.connected_to.location) is Character:
                    self.db.connected_to.location.msg(f"> *The other end picks up*")
                elif type(self.db.connected_to.location) is Room:
                    self.db.connected_to.location.msg_contents(f"> *The other end picks up*")
        #Redial                    
        if "redial" in args:
            if len(self.db.recent_out) == 0:
                caller.msg("How do you plan to redail a phone without a call log?")
                return
            self.db.to_num = self.db.recent_out[0]
            args = "call"

        #Place a dailed call
        if "call" in args:
            if self.db.connected:
                caller.msg("You're already on a call.")
                return
            elif not self.db.to_num:
                caller.msg("You need to punch a number into your phone.")
            else:
                # Log outgoing call
                if len(self.db.recent_out) >= 5:
                    del self.db.recent_out[4]
                self.db.recent_out.insert(0, self.db.to_num)

                #look for foreign phone
                obj = search_object("cellphone", typeclass=type(self))
                target_phone = None
                for phone in obj:
                    if int(phone.db.number) == int(self.db.to_num):
                        target_phone = phone
                
                #Can't find the phone we're looking for
                if not target_phone:
                    caller.msg(f"{self}> That number is out of service.")
                    self.db.to_num = None
                    caller.location.msg_contents(genderize(f"{caller} places a phone call on %p {self} but it quickly ends.", caller.db.gender),exclude=caller)
                    return 

                if target_phone.db.connected_to:
                    caller.msg(f"{self}> You hear a busy signal.")
                    self.db.to_num = None
                    caller.location.msg_contents(genderize(f"{caller} places a phone call on %p {self} but it quickly ends.", caller.db.gender),exclude=caller)
                    return 

                #Reset phone number when calling
                self.db.to_num = None

                #Found the phone, lets connect and begin ringing

                target_phone.ndb.rings_left = target_phone.db.ring_count
                self.db.connected_to = target_phone
                target_phone.db.connected_to = self 
                target_phone.ndb.ringing = True
                # Log inbound call
                if len(target_phone.db.recent_in) >= 5:
                    del target_phone.db.recent_in[4]
                target_phone.db.recent_in.insert(0, self.db.number)
                caller.location.msg_contents(genderize(f"{caller} places a phone call on their {self}.", caller.db.gender),exclude=caller)
                self.ndb.out_call = True
                delay(0, self.rering, caller)

        #Look at call log
        if "log" in args:
            i = 1
            res = "Recent outbound calls:\n"
            for call in self.db.recent_out:
                res += f"  {str(i)}: {str(call)}\n"
                i += 1
            i = 1
            res += "Recent inbound calls:\n"
            for call in self.db.recent_in:
                res += f"  {str(i)}: {str(call)}\n"
                i += 1
            self.location.msg(res)
        
        #Accept number input
        if re.search(r"\d{1,}", args):
            if self.db.to_num is None:
                self.db.to_num = args
            else:
                self.db.to_num = int(str(self.db.to_num)+str(args))
            caller.msg("You punch some numbers into your phone.")
            caller.location.msg_contents(genderize(f"{caller} punches some numbers into %p phone.", caller.db.gender),exclude=caller)

    def rering(self, caller):
        if not self.ndb.out_call:
            return
        target_phone = self.db.connected_to
        if target_phone:
            if not self.db.connected:
                if type(target_phone.location) is Character and target_phone.ndb.rings_left > 0:
                    caller.msg(f"{self}> *ringing*")
                    target_phone.location.location.msg_contents(f"You hear a ringing coming from {target_phone.location}.", exclude=target_phone.location)
                    target_phone.location.msg(f"Your {target_phone} is ringing.")
                elif type(target_phone.location) is Room and target_phone.ndb.rings_left > 0:
                    caller.msg(f"{self}> *ringing*")
                    target_phone.location.msg_contents(f"You hear a ringing coming from some phone sitting nearby.")
            if (not self.db.connected) and target_phone.ndb.rings_left > 0:
                target_phone.ndb.rings_left -= 1
                delay(3, self.rering, caller)
            elif target_phone.ndb.rings_left == 0 and (not self.db.connected):
                caller.msg(f"{self}> The wireless user you are calling is not available. Please try again later.")
                if type(target_phone.location) is Character:
                    target_phone.location.location.msg_contents(f"{target_phone.location}'s phone stops ringing.", exclude=target_phone.location)
                    target_phone.location.msg("Your phone stops ringing.")
                elif type(target_phone.location) is Room:
                    target_phone.location.msg_contents(f"The phone stops ringing.")
                self.db.connected_to = None
                target_phone.db.connected_to = None

    def return_appearance(self, *args, **kwargs):
        res = f"On the {self}'s screen you see...\n\n"
        res += "Status: Active\n"
        res += f"Your number: {self.db.number}\n"
        if self.db.connected:
            res += f"Connected to: {self.db.connected_to.db.number}\n"
        elif not self.db.connected and self.db.connected_to and not self.ndb.ringing:
            res += f"Calling: {self.db.connected_to.db.number}\n"
        elif not self.db.connected and self.db.connected_to and self.ndb.ringing:
            res += f"Incoming call from: {self.db.connected_to.db.number}\n"
        elif self.db.to_num:
            res += f"Ready to call: {self.db.to_num}\n"
        else:
            res += f"Ready to make call."
        return res
    
    def msg(self, msg="", **kwargs):
        text = kwargs["text"]
        msg_type = None
        from_obj = kwargs["from_obj"]
        try:
            msg_type = kwargs["text"][1]["type"]
        except:
            pass

        if msg_type and msg_type == "to":
            text = text[0].split(": ")[1:][0]
            self.location.msg()
            if self.db.connected:
                if type(self.db.connected_to.location) is Character:
                    self.db.connected_to.location.msg(f"{self}> {text}")
                elif type(self.db.connected_to.location) is Room:
                     self.db.connected_to.location.msg_contents(f"You hear indistinguishable speech coming from the {self.db.connected_to}.")