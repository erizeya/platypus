from typeclasses.objects import Object

class Consumable(Object):
    """
    Base class for food and drink
    """
    def at_object_creation(self):
        self.db.desc = "This is a generic consumable."
        self.db.charges = 5
        self.db.untouched = True

    def reset_name(self):
        self.name = self.db.static_name

#
# Food
#
class Food(Consumable):
    def at_object_creation(self):
        super().at_object_creation()
        self.name = "generic food"
        self.db.static_name = self.name
        self.db.desc = "A generic piece of food."
        self.db.messages = {
            "taste": "You taste the most generic taste you've ever tasted.",
            "first_consume": f"You pull out a utensil and take a bite of your {self}",
            "consume": f"You take a bite of your {self}",
            "last_consume": f"You take the last bite of your {self} and throw it away."
        }

class Rice(Food):
    def at_object_creation(self):
        super().at_object_creation()
        self.name = "bowl of rice"
        self.db.static_name = self.name
        self.db.desc = "A bowl of rice."
        self.db.messages = {
            "taste": f"You taste the generic taste of rice. What were you expecting? Rice is, like, the water of foods.",
            "first_consume": f"You break apart a pair of chopsticks and shovel some {self} into your mouth.",
            "consume": f"You chopstick some of your {self} into your mouth.",
            "last_consume": f"You take the last bite of your {self} and set the bowl and chopsticks aside."
        }


#
# Drink
# 
class Drink(Consumable):
    def at_object_creation(self):
        super().at_object_creation()
        self.name = "generic drink"
        self.db.static_name = self.name
        self.db.desc = "A generic glass of drink."
        self.db.messages = {
            "taste": "You taste the most generic taste you've ever tasted.",
            "first_consume": f"You pop the lid of your {self} and take a drink.",
            "consume": f"You take a drink from your {self}",
            "last_consume": f"You drain your {self} to the last drop and throw it away."
        }

class Tea(Drink):
    def at_object_creation(self):
        super().at_object_creation()
        self.name = "cup of tea"
        self.db.static_name = self.name
        self.db.desc = "A warm cup of tea."
        self.db.messages = {
            "taste": f"You taste simple tea, slightly bitter, a little earthy. Yep, this is tea.",
            "first_consume": f"You take a slow sip of your tea, savoring the taste and heat.",
            "consume": f"You take another sip from your {self}",
            "last_consume": f"You take the last sip of your {self} and set the empty cup aside."
        }
