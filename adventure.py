"""Emily Byrnes - week 5 coding assignment"""
import random

def display_player_status(player_stats):
    """displays the health of the player"""
    print(f"Your current health: {player_stats['health']}")

def handle_path_choice(player_stats):
    """This function determines the path direction"""
    path = random.choice(["left", "right"])
    if path == "left":
        print("You encounter a friendly gnome who heals you for 10 health points.")
        player_stats['health'] += 10
        if player_stats['health'] > 100:
            player_stats['health'] = 100
    if path == "right":
        print("You fall into a pit and lose 15 health points.")
        player_stats['health'] -= 15
        if player_stats['health'] < 0:
            player_stats['health'] = 0
            print("You are barely alive!")
    return player_stats

def player_attack(monster_health):
    """this function attacks the monster"""
    print("You strike the monster for 15 damage!")
    monster_health -= 15
    return monster_health

def monster_attack(player_stats):
    """this function attacks the player"""
    critical_hit = random.choice([True, False])
    if critical_hit is True:
        player_stats['health'] -= 20
        print("The monster lands a critical hit for 20 damage!")
    if critical_hit is False:
        player_stats['health'] -= 10
        print("The monster hits you for 10 damage!")
    return player_stats

def combat_encounter(player_stats, monster_health, has_treasure):
    """this function is the combat sequence"""
    while player_stats['health'] > 0 and monster_health > 0:
        monster_health = player_attack(monster_health)
        print(f'line 49: player_stats type: {type(player_stats)}, player_stats: {player_stats}')
        if monster_health <= 0:
            print("You defeated the monster!")
            break
        display_player_status(player_stats)
        player_stats['health'] = monster_attack(player_stats)
        if player_stats['health']<= 0:
            print("Game Over!")
            break
    return has_treasure, player_stats

def check_for_treasure(has_treasure):
    """This function determines if the player finds the treasure"""
    if has_treasure is True:
        print("You found the hidden treasure! You win!")
    if has_treasure is False:
        print("The monster did not have the treasure. You continue your journey.")

def acquire_item(inventory, item):
    """This function allows the items collected to go into the inventory list"""
    """I used an append opperation to add the item to the end of the list"""
    inventory.append(item)
    print(f"You acquired a {item}!")
    return inventory

def display_inventory(inventory):
    """This function displays the player's inventory list"""
    if not inventory:
        print("Your inventory is empty.")
    else:
        """I will use the enumerate function to list out the numbers of
        the inventory items, follow by their names"""
        print("Your inventory:")
        for index, item in enumerate(inventory):
            print(f"{index + 1}. {item}")

def enter_dungeon(player_stats, inventory, dungeon_rooms, artifacts):
    """In this section, I use the "in" opperator to run
    through all the possible dungeon rooms in the
    list of tuples."""
    for room in dungeon_rooms:
        print(f"You enter {room[0]}")
        print(f"You found a {room[1]} in the room.")
        """I attempt to modify a tuple,
        which gives an error message since that is impossible."""
        try:
            room[1] = "candle"
        except:
            print("Error: cannot modify a tuple. Tuples are immutable.")
            acquire_item(inventory, room[1])
        if room[2] == "none":
            print("There doesn't seem to be a challenge in this room. You move on.")

        if room[2] == "puzzle":
            print("You encounter a puzzle!")
            solve_or_skip = input("Will you solve or skip the puzzle?")
            if solve_or_skip == "solve":
                solve_rate = random.choice([True, False])
                if solve_rate is True:
                    print(room[3][0])
                else:
                    print(room[3][1])
                    print(f"You lost {room[3][2]} HP.")
            if solve_or_skip == "skip":
                if artifacts.get("staff_of_wisdom") == None:
                    print(room[3][1])
                player_stats['health'] += room[3][2]
                if artifacts.get("satff_of_wisdom") != None:
                    print("you used your knowledge to bypass the challenge")

        if room[2] == "trap":
            print("You see a potential trap!")
            disarm_or_bypass = input("Will you disarm or bypass the trap?")
            if disarm_or_bypass == "disarm":
                disarm_rate = random.choice([True, False])
                if disarm_rate is True:
                    print(room[3][0])
                else:
                    print(room[3][1])
                    print(f"You lost {room[3][2]} HP.")
            if disarm_or_bypass == "bypass":
                print(room[3][1])
            player_stats['health'] += room[3][2]
        if room[2] == "library":
            clues = ["The treasure is hidden where the dragon sleeps.",
            "The key lies with the gnome.",
            "Beware the shadows.",
            "The amulet unlocks the final door."]
            print(random.sample(clues, 2))
            find_clue(clues)


        display_inventory(inventory)
        display_player_status(player_stats)
    return player_stats, inventory

def discover_artifact(player_stats, artifacts, artifact_name):
    for artifact in artifacts:
        artifact_name = artifacts.get("artifact does not exist", "You found nothing of interest.")
        print(artifacts[artifact_name])
        if artifacts['effect'] == 'increase health':
            player_stats['health'] + artifacts['power']
            print(f"your health increased by {artifacts['power']}")
        if artifacts['effect'] == 'enhances attack':
            player_stats['attack'] + artifacts['power']
            print(f"your attack increased by {artifacts['power']}")
        del artifacts[artifact_name]
    return player_stats, artifacts

def find_clue(clues, new_clue):
    if clues.intersection(new_clue):
        print("You already know this clue.")
    else:
        clues.add(new_clue)
        print(f"You discovered a new clue: {[new_clue]}")

def main():
    """Main game loop."""

    player_stats = {'health': 100, 'attack': 5}
    monster_health = 70
    inventory = []
    clues = set()
    
    """Here is the list of possible dungeon rooms the player encounters"""
    dungeon_rooms = [("A mysterious library", "book", "puzzle",
    ("You solved the puzzle!", "The puzzle remains unsolved.", -5)),
    ("a long hallway", "sword", "none", None),
    ("a throne room", "crown", "trap", ("You escaped the trap!", "you were caught in the trap", -20)),
    ("A vast library filled with ancient, cryptic texts.", "none", "library", None)
    ]
   
    """Here is the list of artifacts"""
    artifacts = {
        "amulet_of_vitality": {
            "description": "Glowing amulet, life force.",
            "power": 15,
            "effect": "increases health"
        },
        "ring_of_strength": {
            "description": "Powerful ring, attack boost.",
            "power": 10,
            "effect": "enhances attack"
        },
        "staff_of_wisdom": {
            "description": "Staff of wisdom, ancient.",
            "power": 5,
            "effect": "solves puzzles"
        }
    }

    has_treasure = random.choice([True, False])

    display_player_status(player_stats)

    player_stats = handle_path_choice(player_stats)

    if player_stats['health'] > 0:
        treasure_obtained_in_combat = combat_encounter(player_stats, monster_health, has_treasure)

        if treasure_obtained_in_combat is not None:

            check_for_treasure(treasure_obtained_in_combat)


        if random.random() < 0.3:

            artifact_keys = list(artifacts.keys())

            if artifact_keys:

                artifact_name = random.choice(artifact_keys)

                player_stats, artifacts = discover_artifact(player_stats, artifacts, artifact_name)

                display_player_status(player_stats)


        if player_stats['health'] > 0:

            player_stats, inventory, clues = enter_dungeon(

                player_stats, inventory, dungeon_rooms, clues)

            print("\n--- Game End ---")

            display_player_status(player_stats)

            print("Final Inventory:")

            display_inventory(inventory)

            print("Clues:")

            if clues:

                for clue in clues:

                    print(f"- {clue}")

            else:

                print("No clues.")

if __name__ == "__main__":
    main()