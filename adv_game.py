# Define XP required for each level
XP_THRESHOLDS = [0, 100, 300, 600, 1000]  # Example thresholds for levels 1-5

# Define stat increases per level
STAT_INCREASES = {
    "max_health": [10, 15, 20, 25, 30],  # Increase in health per level
    "max_attack": [2, 3, 4, 5, 6],        # Increase in attack per level
    "max_defense": [1, 2, 3, 4, 5]        # Increase in defense per level
}

# Define allowed movements
LOCATION_MAP = {
    "Village": ["Forest", "Tavern", "Blacksmith"],
    "Tavern": ["Village"],
    "Blacksmith": ["Village"],
    "Forest": ["Village", "Castle"],
    "Castle": ["Forest", "Cave"],
    "Cave": ["Castle"]
}

# Define key items required for locations
LOCATION_REQUIREMENTS = {
    "Castle": "Forest Key",
    "Cave": "Castle Seal"
}

# Define items available in the shop
SHOP_ITEMS = {
    "Sword": {"price": 50, "type": "melee", "attack": 5},
    "Shield": {"price": 40, "type": "shield", "defense": 3},
    "Armor": {"price": 60, "type": "armor", "defense": 5},
    "Ring of Health": {"price": 30, "type": "accessory", "health": 10}
}

# Game Initialization
def initialize_game():
    print("Welcome to the Pyieval RPG!")
    player = {
        "name": input("Enter your character's name: "),
        "level": 1,
        "experience": 0,
        "health": 100,
        "max_health": 100,
        "attack": 10,
        "max_attack": 10,
        "defense": 5,
        "max_defense": 5,
        "location": "Village",
        "inventory": [],
        "gold": 100,
        "equipped_items": {
            "melee": None,
            "armor": None,
            "shield": None,
            "accessory": None
        }
    }
    print(
    f"Welcome {player['name']}, "
    "Your village is in grave danger. The once peaceful land is now overshadowed "
    "\nby a menacing dragon that resides in a cave at the edge of the world. To make matters worse, "
    "\nthe nearby castle, which once stood as a bastion of hope and protection, has fallen into the hands "
    "\nof ruthless ghouls. The villagers are desperate, and as the last remaining brave soul, you are their only hope."
    )
    return player

# Main Game Loop
def main_game_loop(player):
    while True:
        if player["location"] == "Village":
            print(f"\nYou are in the {player['location']}. Would you like to 'move', view 'stats', 'equip' an item, or 'quit'?")
        elif player["location"] == "Tavern":
            print(f"\nYou are in the {player['location']}. Would you like to 'move', 'rest', view 'stats', 'equip' an item, or 'quit'?")
        elif player["location"] == "Blacksmith":
            print(f"\nYou are in the {player['location']}. Would you like to 'move', 'shop', view 'stats', 'equip' an item, or 'quit'?")    
        else:
            print(f"\nYou are in the {player['location']}. Would you like to 'move', 'fight', view 'stats', 'equip' an item, or 'quit'?")
        
        action = input("> ").strip().lower()
        
        if action == "move":
            move(player)
        elif player["location"] == "Tavern" and action == "rest":
            rest(player)
        elif player["location"] == "Blacksmith" and action == "shop":
            shop(player)
        elif action == "equip":
            equip_item(player)
        elif action == "fight":
            if player["location"] not in ["Village", "Tavern", "Blacksmith"]:
                combat(player)
            else:
                print("You can't fight here.")
        elif action == "stats":
            stats(player)
        elif action == "quit":
            print("Thank you for playing!")
            break
        else:
            print("Invalid action. Try again.")

# Shop Function
def shop(player):
    print("Welcome to the Blacksmith's shop! Here are the items available for purchase:")
    for item, details in SHOP_ITEMS.items():
        print(f"{item}: {details['price']} gold")

    item_keys = {item.lower(): item for item in SHOP_ITEMS}  # Create a mapping of lowercase keys to original item names

    while True:
        choice = input("What would you like to buy? (or type 'exit' to leave): ").strip().lower()

        if choice == "exit":
            break

        if choice in item_keys:
            item_name = item_keys[choice]
            if player["gold"] >= SHOP_ITEMS[item_name]["price"]:
                player["gold"] -= SHOP_ITEMS[item_name]["price"]
                player["inventory"].append(item_name)
                print(f"You have purchased a {item_name}!")
            else:
                print("You don't have enough gold to buy that item.")
        else:
            print("That item is not available in the shop.")


def equip_item(player):
    if not player["inventory"]:
        print("Your inventory is empty. Nothing to equip.")
        return
    
    item_keys = {item.lower(): item for item in player["inventory"]}

    print("Your inventory: ")
    for item in player["inventory"]:
        print(item)

    choice = input("Which item would you like to equip? ").strip().lower()
    
    if choice in item_keys:
        item_name = item_keys[choice]
        item_type = SHOP_ITEMS[item_name]["type"]
        
        # Check if there's already an item in the slot
        if player["equipped_items"][item_type]:
            print(f"You already have a {item_type} equipped. Unequipping {player['equipped_items'][item_type]}.")
            player["inventory"].append(player["equipped_items"][item_type])
            # Apply item stats without the previously equipped item
            remove_item_stats(player, player["equipped_items"][item_type])

        player["equipped_items"][item_type] = item_name
        player["inventory"].remove(item_name)
        apply_item_stats(player)
        print(f"You have equipped the {item_name}.")
    else:
        print("That item is not in your inventory.")

# Apply Stats
def apply_item_stats(player):
    # Initialize base stats
    player["attack"] = player["max_attack"]
    player["defense"] = player["max_defense"]
    player["health"] = player["max_health"]

    # Apply effects of equipped items
    for slot, item in player["equipped_items"].items():
        if item:
            if "attack" in SHOP_ITEMS[item]:
                player["max_attack"] += SHOP_ITEMS[item]["attack"]
            if "defense" in SHOP_ITEMS[item]:
                player["max_defense"] += SHOP_ITEMS[item]["defense"]
            if "health" in SHOP_ITEMS[item]:
                player["max_health"] += SHOP_ITEMS[item]["health"]

    # Ensure the current stats do not exceed max stats
    player["attack"] = player["max_attack"]
    player["defense"] = player["max_defense"]
    player["health"] = player["max_health"]

# Remove Stats
def remove_item_stats(player, item_name):
    item_type = SHOP_ITEMS[item_name]["type"]
    
    if item_type == "accessory" and "health" in SHOP_ITEMS[item_name]:
        # Remove the health effect
        player["max_health"] -= SHOP_ITEMS[item_name]["health"]
        player["health"] = min(player["health"], player["max_health"])
    
    if item_type == "melee" and "attack" in SHOP_ITEMS[item_name]:
        # Adjust attack if it was a weapon
        player["attack"] -= SHOP_ITEMS[item_name]["attack"]

    if item_type == "shield" and "defense" in SHOP_ITEMS[item_name]:
        # Adjust defense if it was a shield
        player["defense"] -= SHOP_ITEMS[item_name]["defense"]
    
    # Reapply stats with remaining equipped items
    apply_item_stats(player)

# Rest Feature
def rest(player):
    player["health"] = player["max_health"]
    print("You rest in the Tavern and restore your health to full.")

# Player Stats
def stats(player):
    equipped_items = ', '.join([f"{slot.capitalize()}: {item}" if item else f"{slot.capitalize()}: None" for slot, item in player['equipped_items'].items()])
    inventory_items = ', '.join(player['inventory']) if player['inventory'] else 'Empty'
    
    print(f"Player Stats:\n"
          f"Name: {player['name']}\n"
          f"Level: {player['level']}\n"
          f"Experience: {player['experience']}\n"
          f"Health: {player['health']}/{player['max_health']}\n"
          f"Attack: {player['attack']}\n"
          f"Defense: {player['defense']}\n"
          f"Location: {player['location']}\n"
          f"Gold: {player['gold']}\n"
          f"Inventory: {inventory_items}\n"
          f"Equipped Items: {equipped_items}")
    
# Add item to inventory
def add_item(player, item):
    player["inventory"].append(item)
    print(f"You have acquired a {item}.")

# Zone Navigation
def move(player):
    current_location = player["location"]
    possible_locations = LOCATION_MAP[current_location]

    print(f"Where would you like to go? Available locations: {', '.join(possible_locations)}")
    new_location = input("> ").strip().title()

    # Check if the new location has a requirement
    if new_location in LOCATION_REQUIREMENTS:
        required_item = LOCATION_REQUIREMENTS[new_location]
        if required_item not in player["inventory"]:
            print(f"You need the {required_item} to enter the {new_location}.")
            return

    if new_location in possible_locations:
        player["location"] = new_location
        print(f"You move to the {new_location}.")
    else:
        print("You can't go there from here. Try again.")

# Level Up System
def gain_experience(player, xp):
    player["experience"] += xp
    while player["level"] < len(XP_THRESHOLDS) and player["experience"] >= XP_THRESHOLDS[player["level"]]:
        level_up(player)

def level_up(player):
    player["level"] += 1
    print(f"Congratulations! You've reached level {player['level']}!")

    # Add base increases for max stats
    player["max_health"] += STAT_INCREASES["max_health"][player["level"] - 1]
    player["max_attack"] += STAT_INCREASES["max_attack"][player["level"] - 1]
    player["max_defense"] += STAT_INCREASES["max_defense"][player["level"] - 1]
    
    # Update current stats to reflect new max values
    player["health"] = min(player["health"], player["max_health"])
    player["attack"] = min(player["attack"], player["max_attack"])
    player["defense"] = min(player["defense"], player["max_defense"])

    print(f"Your health is now {player['health']}.")
    print(f"Your attack is now {player['attack']}.")
    print(f"Your defense is now {player['defense']}.")

# Combat System
def combat(player):
    # Define enemies and their drops
    ENEMIES_FOREST = {
        "Goblin": {"health": 30, "attack": 5, "defense": 2, "drop": None, "weight": 1},
        "Wolf": {"health": 25, "attack": 7, "defense": 3, "drop": None, "weight": 1},
        "Ogre": {"health": 50, "attack": 10, "defense": 5, "drop": "Forest Key", "weight": 0.5}
    }
    ENEMIES_CASTLE = {
    "Ghoul": {"health": 50, "attack": 8, "defense": 6, "drop": None, "weight": 1},
    "Fallen Knight": {"health": 80, "attack": 12, "defense": 10, "drop": "Castle Seal", "weight": 0.5}
    }
    ENEMIES_CAVE = {
    "Giant Bat": {"health": 50, "attack": 10, "defense": 8, "drop": None, "weight": 1},
    "Dragon": {"health": 100, "attack": 15, "defense": 15, "drop": "Dragon Scale", "weight": 0.2}
    }

    ENEMIES_BY_LOCATION = {
        "Forest": ENEMIES_FOREST,
        "Castle": ENEMIES_CASTLE,
        "Cave": ENEMIES_CAVE
    }

    # Get the enemies for the current location
    enemies = ENEMIES_BY_LOCATION.get(player["location"], {})
    if not enemies:
        print("No enemies available in this location.")
        return

    # Create a list of enemies based on their weights
    weighted_enemies = []
    for enemy, details in enemies.items():
        weighted_enemies.extend([enemy] * int(details["weight"] * 10))  # Adjust weight multiplier as needed

    if not weighted_enemies:
        print("No enemies available in this location.")
        return

    enemy = random.choice(weighted_enemies)
    enemy_stats = enemies[enemy]
    print(f"A wild {enemy} appears!")

    while enemy_stats["health"] > 0 and player["health"] > 0:
        action = input("Do you want to 'attack' or 'run'? ").strip().lower()
        if action == "attack":
            # Player attack logic
            if random.random() < 0.1:  # 10% chance to miss
                player_damage = 0
                print("You missed!")
            else:
                if random.random() < 0.2:  # 20% chance for critical hit
                    player_damage = (random.randint(player["attack"] - 2, player["attack"] + 2) * 2)
                    player_damage = max(player_damage - enemy_stats["defense"], 0)
                    enemy_stats["health"] -= player_damage
                    print("Critical hit!")
                    print(f"You attack the {enemy} for {player_damage} damage.")
                else:
                    player_damage = random.randint(player["attack"] - 2, player["attack"] + 2)
                    player_damage = max(player_damage - enemy_stats["defense"], 0)
                    enemy_stats["health"] -= player_damage
                    print(f"You attack the {enemy} for {player_damage} damage.")

            if enemy_stats["health"] <= 0:
                print(f"You defeated the {enemy}!")
                gain_experience(player, 50)  # Example XP for defeating an enemy
                print("You gained 50 xp.")
                # Handle item drops
                if enemy_stats["drop"]:
                    add_item(player, enemy_stats["drop"])
                break

            # Enemy attack logic
            if random.random() < 0.1:  # 10% chance for enemy to miss
                enemy_damage = 0
                print(f"The {enemy} missed!")
            else:
                if random.random() < 0.2:  # 20% chance for enemy critical hit
                    enemy_damage = (random.randint(enemy_stats["attack"] - 2, enemy_stats["attack"] + 2) * 2)
                    enemy_damage = max(enemy_damage - player["defense"], 0)
                    player["health"] -= enemy_damage
                    print(f"The {enemy} lands a critical hit!")
                    print(f"The {enemy} attacks you for {enemy_damage} damage.")
                else:
                    enemy_damage = random.randint(enemy_stats["attack"] - 2, enemy_stats["attack"] + 2)
                    enemy_damage = max(enemy_damage - player["defense"], 0)
                    player["health"] -= enemy_damage
                    print(f"The {enemy} attacks you for {enemy_damage} damage.")

            if player["health"] <= 0:
                print("You have been defeated!")
                break

        elif action == "run":
            print("You run away!")
            break
        else:
            print("Invalid action. Try again.")

# Main Function
if __name__ == "__main__":
    import random
    player = initialize_game()
    main_game_loop(player)
