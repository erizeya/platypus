from typeclasses.objects import Object

class Readable(Object):
    """
    This typeclass describes a wearable object.
    """
    def at_object_creation(self):
        "This is called only when object is first created"
        self.locks.add("puppet:superuser()")

        #Item specific traits
        self.db.desc = "A readable item."
        self.db.text = "This is what is displayed when the read command is used on this item."
