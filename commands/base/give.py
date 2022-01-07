from evennia.commands.command import Command as BaseCommand

# give something to someone
# Usage:
#   give <inventory obj> <to||=> <target>
# Gives an items from your inventory to another character,
# placing it in their inventory.
class CmdGive(BaseCommand):
    key = "give"
    locks = "cmd:all()"
    arg_regex = r"\s|$"
    help_category = "General"

    def func(self):
        """Implement give"""

        caller = self.caller
        args = self.args.strip()
        held = None
        dest_hand = None
        err_msg = "Usage: give <object> to <target>"

        if not self.args:
            caller.msg(err_msg)
            return

        try:
            arg_list = args.split(" to ") 
        except:
            caller.msg(err_msg)
            return

        #Prep item
        target_item = arg_list[0]
        item = caller.multiple_search(target_item)
        if not item:
            return

        #Verify item is being held
        if caller.db.l_hand == item:
            held = "left"
        elif caller.db.r_hand == item:
            held = "right"

        if not held:
            caller.msg(f"You have to be holding the {item} to give it to somebody.")
            return

        #Prep recipient
        target_recipient = arg_list[1]
        recipient = caller.multiple_search(target_recipient, location=caller.location)
        if not recipient:
            return

        #Make sure recipient has a free hand
        if recipient.db.r_hand == None:
            dest_hand = "right"
        elif recipient.db.l_hand == None:
            dest_hand = "left"

        if not dest_hand:
            caller.msg(f"{recipient}'s hands are full.")
            return

        # calling at_before_give hook method
        if not item.at_before_give(caller, recipient):
            return


        #Clear giver's hands
        if held == "right":
            caller.db.r_hand = None
        elif held == "left":
            caller.db.l_hand = None

        # give object
        success = item.move_to(recipient, quiet=True)

        #Assign to recipient's hand
        if dest_hand == "right":
            recipient.db.r_hand = item
        elif dest_hand == "left":
            recipient.db.l_hand = item

        if not success:
            caller.msg("This could not be given.")
        else:
            caller.msg(f"You give {item} to {recipient}.")
            recipient.msg(f"{caller} gives you {item}.")
            # Call the object script's at_give() method.
            item.at_give(caller, recipient)


