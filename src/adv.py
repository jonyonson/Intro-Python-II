import textwrap
from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside': Room("Outside Cave Entrance", """North of you, the cave mount
beckons"""),

    'foyer': Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':  Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.
player = Player(room['outside'])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

# Add items to the rooms
bread = Item('bread', 'Much needed energy for the journey')
room['foyer'].items.append(bread)

beer = Item('beer', 'Much needed courage for the journey')
room['overlook'].items.append(beer)


def move_direction(direction):
    if hasattr(player.current_room, direction + '_to'):
        room = getattr(player.current_room, direction + '_to')
        player.current_room = room
    else:
        print("There is no room in that direction")


def show_inventory():
    """ Prints out a players current inventory """
    if player.inventory:
        inventory = ""
        for item in player.inventory:
            inventory += item.name + " "
        print(f"Inventory: {inventory}")
    else:
        print("You don't have anything in your inventory.")


while True:
    # Print the current room name
    print(f"\nRoom: {player.current_room.name}")
    # Print the current room description
    description = textwrap.fill(text=player.current_room.description, width=80)
    print(description)

    # Print out all the items that are visible in current room
    if player.current_room.items:
        items = ""
        for item in player.current_room.items:
            items += item.name + " "
        print(f"Items available in room: {items}")
    else:
        print("No items available in room.")

    # Get user input
    cmd = input('> ').lower().split(" ")

    if len(cmd) == 1:
        if cmd[0] in "nsew":
            move_direction(cmd[0])
        elif cmd[0] == "i" or cmd[0] == "inventory":
            show_inventory()
        elif cmd[0] == "q":
            print("\nThanks for playing!\n")
            break
        else:
            print("Command not recognized")

    if len(cmd) == 2:
        action = cmd[0]

        if action == "get" or action == "take":
            if player.current_room.items:
                for item in player.current_room.items:
                    if cmd[1] == item.name:
                        # remove item from room
                        player.current_room.items.remove(item)
                        # add item to player inventory
                        player.inventory.append(item)
                        item.on_take()
            else:
                print(f"\nYou can't {action} what is not here.")

        elif action == "drop":
            if player.inventory:
                for item in player.inventory:
                    if cmd[1] == item.name:
                        # remove item from inventory
                        player.inventory.remove(item)
                        # add item to room
                        player.current_room.items.append(item)
                        item.on_drop()
            else:
                print(f"\nYou can't {action} what you don't have.")

        else:
            print("Command not recognized")
