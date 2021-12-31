from typeclasses.objects import Object
from evennia import default_cmds

class Wearable(Object):
    """
    This typeclass describes a wearable object.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        #self.cmdset.add_default(default_cmds.CharacterCmdSet)
        #self.cmdset.add(WearCmdSet, permanent=True)
        self.locks.add("puppet:superuser();call:false()")

        #Item specific traits
        self.db.wearable = True
        self.db.desc = "This is a wearable object."
        self.db.worn = "They're wearing a basic t-shirt."

        #Shirt
        self.db.coverage = "upper_body"
        self.db.wearing = False

class Top(Wearable):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.coverage = "upper_body"
        self.db.worn = "They're wearing a basic black t-shirt."

class Bottom(Wearable):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.coverage = "lower_body"
        self.db.worn = "They're wearing a simple pair of jeans."

class Shoes(Wearable):
    def at_object_creation(self):
        super().at_object_creation()
        self.db.coverage = "feet"
        self.db.worn = "They're wearing a pair of well worn boots."
