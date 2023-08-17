class Room:
    def __init__(self, name, description, exits, items=None, locked_doors=None):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items if items else []
        self.locked_doors = locked_doors if locked_doors else []

    def get_info(self):
        info = f"Current Room: {self.name}\n{self.description}\nExits: "
        for direction, room_name in self.exits.items():
            command = f"type '{direction.lower()}' to go {direction.lower()}"
            info += f"{command}, "
        info = info[:-2] + "\n"
        for door in self.locked_doors:
            info += f"You see a locked door to the {door}.\n"
        return info


class Player:
    def __init__(self, health, inventory, location):
        self.health = health
        self.inventory = inventory
        self.location = location

    def get_stats(self):
        return f"Player Stats:\nHealth: {self.health}\nInventory: {', '.join(self.inventory)}\nLocation: {self.location.name}\n"


# Rooms
entrance_hall = Room("Entrance Hall", "Entrance of the dungeon.", {"north": "Kitchen", "east": "Library", "west": "Wizard's Lair"}, locked_doors=["west"])
library = Room("Library", "A room filled with books.", {"west": "Entrance Hall"}, items=["Key"])
kitchen = Room("Kitchen", "A place to cook.", {"south": "Entrance Hall", "east": "Armory"})
armory = Room("Armory", "Weapons and armors.", {"west": "Kitchen"}, items=["Sword"])
wizard_lair = Room("Wizard's Lair", "A dark room where an evil wizard resides.", {}, items=["Treasure Chest"])

rooms = {"Entrance Hall": entrance_hall, "Library": library, "Kitchen": kitchen, "Armory": armory, "Wizard's Lair": wizard_lair}
player = Player(100, ["Torch"], entrance_hall)

def main():
    print("Welcome to the dungeon!")
    while True:
        print(player.location.get_info())
        print(player.get_stats())
        command = input("> ").strip().lower()

        # Move player
        if command in player.location.exits:
            new_room_name = player.location.exits[command]
            if command in player.location.locked_doors and "Key" not in player.inventory:
                print("The door is locked! You need a Key to unlock it.")
            else:
                if command in player.location.locked_doors and "Key" in player.inventory:
                    print("You use the Key to unlock the door!")
                    player.location.locked_doors.remove(command)  # Remove locked status from the door
                player.location = rooms[new_room_name]
                print(f"You enter the {new_room_name}.")

                if new_room_name == "Wizard's Lair":
                    if "Sword" in player.inventory:
                        print("Congratulations, adventurer! You have defeated the evil wizard and saved the kingdom!")
                        break
                    else:
                        print("The evil wizard defeated you! You lose 50 health and are sent back to the starting room.")
                        player.health -= 50
                        player.location = entrance_hall
                        if player.health <= 0:
                            print("Game over! You have lost all your health. The kingdom is doomed...")
                            break

        # Unlock door using the key
        elif command == "unlock" and "Key" in player.inventory:
            direction = input("Which direction would you like to unlock? ").strip().lower()
            if direction in player.location.locked_doors:
                print(f"You unlocked the door to the {direction}!")
                player.location.locked_doors.remove(direction)  # Remove locked status from the door
            else:
                print(f"There's no locked door to the {direction}.")


        # Inspect current room
        elif command == "inspect":
            items = player.location.items
            if items:
                print(f"You find: {', '.join(items)}!")
                player.inventory.extend(items)
                player.location.items = []  # Remove items from the room
            else:
                print("Nothing to inspect.")

        else:
            print("Invalid command. Type 'north', 'south', 'east', or 'west' to move, 'inspect' to inspect the room, or 'unlock' to use a Key.")

if __name__ == "__main__":
    main()

