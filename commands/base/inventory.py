from evennia import Command

# View the contents of your inventory.
# Usage:
#   inventory
#   inv
#
# Modifies default Evennia behavior
#
class CmdInventory(Command):

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        items = self.caller.contents
        if not items:
            string = "You are not carrying anything."
        else:
            from evennia.utils.ansi import raw as raw_ansi

            table = self.styled_table(border="header")
            for item in items:
                if item.db.wearing:
                    table.add_row(
                        f"|C{item.name} (|cworn|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                elif item == self.caller.db.l_hand:
                    table.add_row(
                        f"|C{item.name} (|cleft hand|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                elif item == self.caller.db.r_hand:
                    table.add_row(
                        f"|C{item.name} (|cright hand|C)|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )
                else:
                    table.add_row(
                        f"|C{item.name}|n",
                        "{}|n".format(utils.crop(raw_ansi(item.db.desc), width=50) or ""),
                    )

            string = f"|wYou are carrying...\n{table}"
        self.caller.msg(string)
