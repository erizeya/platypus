# Platypus
Platypus is a MOO database being designed to follow in the footsteps of the GhostCore database for LambdaMOO which is the database upon which two notable Cyberpunk MOOs: Cybersphere and Sindome are based upon. 

## Currently Implemented Features

* Chat
  * `to` command for directed conversation.
* Clothing
  * Per-body part description (nakeds).
  * Layerable clothing that hides nakeds.
* Pronoun substitution (%s, %o, %p, %q, and %r) in character descriptions, clothing descriptions, and automatic messages.
* Furniture
  * Static furniture such as signs, statues, etc.
  * Interactable furniture (sit, lay, stand) which integrates into room descriptions
  * Vending furniture which can dispense items to players.
  * Containers which can hold items.
* Consumables
    * Food and drink which are "finished" and deleted after a certain number of uses. Food and drink have message for first bite, taste, subsequent bites, and final bite.
* NPCs
  * NPCs can listen to conversations in the surrounding room. 
  * NPCs can respond when directly addressed via `to`
* Items
  * Character/NPC hands. NPCs and characters can hold items in their left and rigth hands.
* Exits
 * When `look`ing at an exit the description of the connected room will be shown.
 * Exits configured as doors can be opened and closed.

## Command Documentation
### IC Commands
`hold[-left/-right] [first/second/etc] <item>`
#### General
`wear <item>`  
Wear a specific item of clothing. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`remove <item>`  
Removes a worn piece of clothing. Clothing which has other clothing over it cannot be removed. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`i[nv[entory]]`  
Displays the character's inventory with designators for worn objects and held objects.

`sit[ [on/at] furniture]`  
Causes a character to sit on a piece of furniture or down on the ground.

`stand`  
Rise from a piece of furniture

`to <character> <message>`  
Directs a message to a specific character or NPC.

`hold [count] <item>`  
Hold an item in your inventory in an open hand. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`hold-left/hold-right [count] <item>`  
Hold an item in your inventory in a specific hand. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`lower [count] <item>`  
Lower a held item back into your inventory. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`get/take/grab [count] item[ from <container>]`  
Take an item from the current room, or from a container in that room. If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`put item[ from <container>]`  
Put a held item into a container. Does not support multiples.

`drop [count] item`  
Drop a held item onto the ground.  If more than one item matches the <item> argument a "count" such as "first" or "2nd" can be used to specify which item should be held.

`open <exit>`  
Open an exit which is marked as a door.

`close <exit>`
Close an exit which is marked as a door.

#### Consumables
`eat`  
Consume a currently held food item. Does not support multiples.

`drink`  
Consume a currenty held drink item Does not support multiples.

#### Locking Containers (Passcode)

Locking containers can be used to securely(?) store items and support the following commands

`push lock on <container>`
Locks the container. Containers must be closed to be locked.

`push <passcode> on <container>`
Unlocks the container given the passcode is correct. 

`push program <passcode> on <container>`
Puts the container into programming mode. From this point forward, using the syntax `push <passcode> on <container>` will set the container's passcode to the provided code. Container remains in programming mode until the cancel button is pushed.

`push cancel on <container>`
Causes the container to exit programming mode.



#### Locking Containers (Key) - TBA


### OOC Commands
`@lp`  
Changes your character's "look_place" message, the message which is displayed in a room description.  
**Example**: `@lp is leaning against one wall.` would lead to the room desc containing "Character is leaning against one wall." when other players enter or `look` at room that your character is in.

`@naked[s]`  
Displays all descriptions set for nude body areas. 

`@naked[s] <location> = <desc>`  
Sets the description for a body location to match the provided text.

`@pronouns`  
Set the pronouns used by your character. Currently the following pronoun sets are supported: feminine (she/her), masucline (he/him), and spivak (e, em)

### Admin/Builder Commands
`!furniture position <position string>`  
Configures the position string of a piece of furniture when displayed in a room description.  
**Example**: `!furniture position sofa attached to the ceiling` would lead to the room desc containing "A sofa is attached to the ceiling".

`!furniture occupant_post <pose string>`  
Configures the pose string of a piece of furniture with occupants displayed in a room description.  
**Example**: `!furniture occupant_pose sofa sitting on the` would lead to the room desc containing "A, B, and C are sitting on the sofa attached to the ceiling".

`!pair <first exit> <second exit>`  
Pairs one to another. Should only be used on exits that connect to one another. The purpose of linking doors is to ensure that when one door opens or closes, the other half of it (in the connecting room) does as well.

`!link <NPC> <Bar>`  
Links a bartender NPC to the bar. When linked to a bar an NPC may serve the food and drink items available through the linked bar.


## Known Bugs
* Puppeted NPCs disappear from the room they occupy when the puppeting finishes.

## Todo List
- [ ] Normalize commands:
    - [ ] `bare` commands for in-character actions
    - [ ] `@at-sign` commands for OOC actions
    - [ ] `!exclamation` commands for admin commands
- [ ] New commands
   - [ ] `lower[-left/-right]`
- [ ] Currency
    - [ ] Bar tender must take money.
- [ ] Add permissions to bars so that only approved characters/npcs can use it.
- [ ] Refactor
   - [ ] Split commands into individual files
