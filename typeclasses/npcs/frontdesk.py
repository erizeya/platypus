from typeclasses.npc import Npc
from evennia.utils import delay
from evennia.utils.utils import list_to_string
from evennia import create_object
import re
import time
import random
from evennia import create_object

class FrontDesk(Npc):


    def at_post_unpuppet(self, account, session=None, **kwargs):
        pass

    def at_object_creation(self):
        super().at_object_creation()
        self.db.rooms = [] #Front Desk NPCs are linked to rentable rooms.
        self.db.convo_target = None #Track who I am talking to.
        self.db.convo_stage = 0 #Track what stage of a conversation I'm in.
        self.db.convo_expires = 0

        #Settable attributes
        self.db.price_per_duration = 10
        self.db.duration = 60 #seconds to multiply requested duration by.
        self.db.duration_text = "minutes"

    def at_heard_say(self, message, from_obj):
        
        self.update_rooms()

        res = ""

        #Check if the convo partner is already renting
        current = False
        current_room = None
        for room in self.db.rooms:
            if room.db.renter == from_obj:
                current = True
                current_room = room
        #Check if we're already mid-convo with someone else
        if self.db.convo_target != None and from_obj != self.db.convo_target:
            res += "I'm sorry, I'm helping another customer. Please give me a moment."
        #No active conversation
        elif self.db.convo_stage == 0:
            #Respond to hi
            if re.search(r"hi\b", message.lower()) or re.search(r"hey\b",message.lower()) or re.search(r"sup\b", message.lower()):
                res += "Hello. "

            if current and re.search(r"extend\b", message.lower()):
                res += f"Of course. I'd be happy to extend your stay. How many {self.db.duration_text} would you like to extend your stay by?"
                self.db.convo_stage = 1
                self.db.convo_target = from_obj
                self.db.convo_expires = int(time.time()) + 25
            elif current:
                res += "Welcome back. Are you enjoying your stay? Let me know if you would like to |uextend|n your stay."
            #Rent Response
            elif re.search(r"rent\b", message.lower()):
                vacant = False
                already_renting = False
                for room in self.db.rooms:
                    if room.db.renter is None:
                        vacant = True
                    if room.db.renter is from_obj:
                        already_renting = True
                        break
                if already_renting:
                    res += f"Sorry, you already have a room here. We do not allow multiple registrations."
                elif vacant:
                    res += f"Sure, I can help you with that. How many {self.db.duration_text} would you like to rent a room for?"
                    self.db.convo_stage = 1
                    self.db.convo_target = from_obj
                    self.db.convo_expires = int(time.time()) + 25
                    delay(30, self.check_convo)
                else:
                    res += "Sorry, we don't have any vacancies right now. Please check back in a day or two."
            #Other Responses
            elif re.search(r"room\b", message.lower()):
                res += "Are you looking to |urent|n a room for the night? I can help you with that."
            elif re.search(r"vacant\b", message.lower()) or re.search(r"vacancies", message.lower()):
                vacant = False
                already_renting = False
                for room in self.db.rooms:
                    if room.db.renter is None:
                        vacant = True
                if vacant:
                    res += "Yes, we have some vacancies. Would you like to rent a room?"
                else:
                    res += "Sorry, I do not have any available rooms right now. Check back in a few hours, maybe?"
            else:
                res += "Let me know if I can help you with anything or if you'd like to |urent|n a room."
        #Player has been asked how long they want to rent for
        elif self.db.convo_stage == 1:
            #Parse how many days, up to seven.
            days = 0
            days_spelled = ""
            if re.search(r"1\s|one", message.lower()):
                days = 1
                days_spelled = "one"
            elif re.search(r"2\s|two", message.lower()):
                days = 2
                days_spelled = "two"
            elif re.search(r"3\s|three", message.lower()):
                days = 3
                days_spelled = "three"
            elif re.search(r"4\s|four", message.lower()):
                days = 4
                days_spelled = "four"
            elif re.search(r"5\s|five", message.lower()):
                days = 5
                days_spelled = "five"
            elif re.search(r"6\s|six", message.lower()):
                days = 6
                days_spelled = "six"
            elif re.search(r"7\s|seven", message.lower()):
                days = 7
                days_spelled = "seven"
            
            #Respond based on parsed response.
            if not current:
                if days == 0:
                    res += f"Sorry, I didn't catch that. How many {self.db.duration_text} would you like to stay for? You can stay for up to seven {self.db.duration_text}."
                else:
                    if days == 1:
                        res += f"Just one {self.db.duration_text[:-1]}? Alright. That'll run be {str(days*self.db.price_per_duration)} money. Would you like me to book the room?"
                    else:
                        res += f"Great, {str(days_spelled)} {self.db.duration_text}? We can do that. That will cost {str(days*self.db.price_per_duration)} money. Would you like me to book the room?"

                    self.db.convo_expires = int(time.time()) + 25
                    self.ndb.days = days
                    self.db.convo_stage = 2
            else:
                if days == 0:
                    res += f"Sorry, I didn't catch that. How many {self.db.duration_text} would you like to stay for? You can add up to seven {self.db.duration_text}."
                else:
                    if days == 1:
                        res += f"One more {self.db.duration_text[:-1]}? Sure thing. That'll be {str(days*self.db.price_per_duration)} money. Is that alright?"
                    else:
                        res += f"Alright, {str(days_spelled)} more {self.db.duration_text}? No problem. That will cost {str(days*self.db.price_per_duration)} money. Should I extend your stay?"

                    self.db.convo_expires = int(time.time()) + 25
                    self.ndb.days = days
                    self.db.convo_stage = 2
            
        #Player has indicated how long they want to rent for we're waiting to see if they confirm
        elif self.db.convo_stage == 2:
            intent = None 
            if re.search(r"yes\b|yeah\b|sure\b|ok\b", message.lower()):
                if not current:
                    res += "Great! I'll get the booking set up right now..."
                    vacant_rooms = []
                    for room in self.db.rooms:
                        if room.db.renter is None:
                            vacant_rooms.append(room)
                    delay(2, self.rent_room, renter=from_obj, door=random.choice(vacant_rooms))
                else:
                    res += "Wonderful! I'll extend your booking right now..."
                    delay(2, self.extend_room, renter=from_obj, door=current_room)
                self.db.convo_target = None
                self.db.convo_stage = 0
                self.db.convo_expires = 0
            elif re.search(r"no\b|nope\b|nah\b", message.lower()):
                res += "Alright. Please don't hesitate to come back if you change your mind."
                self.db.convo_target = None
                self.db.convo_stage = 0
                self.db.convo_expires = 0
            else:
                res += "Sorry, what was that? Would you like me to book the room for you?"

        return  res

    def respond(self, **kwargs):
        say = kwargs["say"]
        self.execute_cmd(f"say {say}")

    def check_convo(self, **kwargs):
        if self.db.convo_expires < int(time.time()):
            if self.db.convo_target:
                self.execute_cmd(f"to {self.db.convo_target} I'll give you time to think, let me know if you need anything.")
                self.db.convo_target = None
                self.db.convo_stage = 0
                self.db.convo_expires = 0
            else:
                #Convo ended, we don't need to do anything
                pass
        else:
            delay(10, self.check_convo)
    
    def rent_room(self, renter=None, door=None, **kwags):
        amount = self.ndb.days * self.db.price_per_duration
        #Check renter has enough funds
        if renter.db.currency-amount < 0:
            self.execute_cmd(f"say Sorry, it doesn't look like you have enough money to stay that long.")
            return

        #Deduct money from renter
        renter.db.currency -= amount
        renter.msg(f"You pass {str(amount)} money to {self}")
        renter.location.msg_contents(f"{renter} passes some money to {self}.",exclude=renter)

        self.execute_cmd("fh")
        self.execute_cmd("emote types a few things into a computer.")

        #Setup the rental
        door.db.code = random.randint(11111,99999)
        door.db.renter = renter
        door.db.expire = int(time.time())+(self.ndb.days*self.db.duration)

        #Create card with reservation details
        obj = create_object("typeclasses.readable.Readable",key="Hotel Zim Registration Card")
        obj.aliases.add("card", "registration card")
        obj.desc = "A card bearing the Hotel Zim logo."
        obj.db.text = f"{door.destination}|/Code: {door.db.code}"
        obj.move_to(self, silent=True)
        self.db.r_hand = obj
        self.execute_cmd(f"give Hotel Zim Registration Card to {renter}")
        self.execute_cmd(f"to {renter} That's everything. Enjoy your stay!")

    def extend_room(self, renter=None, door=None, **kwags):
        amount = self.ndb.days * self.db.price_per_duration
        #Check renter has enough funds
        if renter.db.currency-amount < 0:
            self.execute_cmd(f"say Sorry, it doesn't look like you have enough money to stay that long.")
            return

        #Deduct money from renter
        renter.db.currency -= amount
        renter.msg(f"You pass {str(amount)} money to {self}")
        renter.location.msg_contents(f"{renter} passes some money to {self}.",exclude=renter)

        #Extend rental
        self.execute_cmd("emote types a few things into a computer.")
        door.db.expire = door.db.expire + (self.ndb.days*self.db.duration)

    def msg(self, text=None, from_obj=None, **kwargs):
        "Custom msg() method reacting to say."

        if from_obj != self:
            # make sure to not repeat what we ourselves said or we'll create a loop
            try:
                say_text, is_say = text[0], text[1]['type'] == 'to'
            except Exception:
                is_say = False
            if is_say:
                #Check if directed
                if " [to You]: " in text[0]:
                    # First get the response (if any)
                    response = self.at_heard_say(say_text, from_obj)
                    # If there is a response
                    if response != None:
                        delay(1, self.respond, say=response)
                    else:
                        delay(1, self.respond, say="Sorry, I couldn't hear you! [OOC: This is an error.]")
    
        # this is needed if anyone ever puppets this NPC - without it you would never
        # get any feedback from the server (not even the results of look)
        # 
        super().msg(text=text, from_obj=from_obj, subclass=True, **kwargs)

    def update_rooms(self):
        for room in self.db.rooms:
            #Expire rooms
            if room.db.renter != None and room.db.expire < int(time.time()):
                room.db.code = random.randint(11111,99999)
                room.db.renter = None