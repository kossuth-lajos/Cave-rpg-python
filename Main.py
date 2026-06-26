# Main.py
import random
import time
from Character import Player, slow_print
from Map import show_map
from SaveSystem import save_game, load_game

# AZ ÚJ IMPORTJAINK:
from Combat import fight_rat, fight_dragon
from Location import enter_witch_brewery, enter_goblin_gambler


dragon_dead = False
current_room = "Entrance"

potion_shop = {
    "1": {"name": "Health Potion", "cost": 25, "stat": "hp", "bonus": 30},
    "2": {"name": "Strength Elixir", "cost": 40, "stat": "atk_bonus", "bonus": 10},
    "3": {"name": "Defense Tonic", "cost": 40, "stat": "def_bonus", "bonus": 10}
}

slow_print("--- WELCOME TO THE CAVE ---", 0.05)

load_choice = input("Do you want to load your previous game? (yes/no): ").lower().strip()
if load_choice == "yes":
    hero = Player("Temporary", 100, 0)
    saved_room, saved_dragon_status = load_game(hero)
    if saved_room and saved_dragon_status is not None:
        current_room = saved_room
        dragon_dead = saved_dragon_status
    else:
        player_name = input("Enter your name, brave adventurer: ")
        hero = Player(player_name, 100, 0)
else:
    player_name = input("Enter your name, brave adventurer: ")
    hero = Player(player_name, 100, 0)

# --- MAIN GAME LOOP ---
while hero.hp > 0:
    print(f"\n[ LOCATION: {current_room} | HP: {hero.hp}/{hero.max_hp} | GOLD: {hero.gold} | ATK: +{hero.atk_bonus} | DEF: +{hero.def_bonus} ]")
    print("What do you want to do?")
    print("1. Move\n2. See inv or equip gear\n3. Use potion\n4. See map\n5. Quit\n6. Save Game")
    
    choice = input("Pick a number from 1-6: ").strip()
    
    if choice == "4":
        show_map(current_room)
        continue
    if choice == "5":
        slow_print("You retreat from the cave... for now.")
        break
    if choice == "6":
        save_game(hero, current_room, dragon_dead)
        continue

    if choice == "3":
        potion_name = input("Type the name of the potion you want to use (or 'cancel' to go back): ").strip()
        if potion_name.lower() == "cancel":
            continue
            
        hero_has_it = any(item.lower() == potion_name.lower() for item in hero.inventory)
        if hero_has_it:
            # Megkeressük a rendes nevet (kis/nagybetű függetlenül)
            actual_name = [i for i in hero.inventory if i.lower() == potion_name.lower()][0]
            found_potion_data = next((data for data in potion_shop.values() if data["name"].lower() == potion_name.lower()), None)
            
            if found_potion_data:
                hero.use_potion(found_potion_data)
            else:
                print("Something went wrong with the potion data.")
        else: 
            print("❌ You don't have that in your inventory!")
        continue

    if choice == "2":
        hero.equip_gear()
        continue
        
    if choice == "1":
        print("You can go: north, south, east, west ")
        dir_choice = input("Which direction do you want to go? ").lower().strip()

        # --- ENTRANCE ---
        if current_room == "Entrance":
            if dir_choice == "north":
                current_room = "Dark Hallway"
                slow_print("You step into a cold hallway where the light doesn't reach.")
            elif dir_choice == "east":
                if dragon_dead:
                    slow_print("You walk through the already opened golden doors.")
                    current_room = "THE KINGS ROOM"
                elif "key" in hero.inventory:
                    slow_print("The SHINY KEY fits perfectly. The massive doors groan open...")
                    current_room = "THE KINGS ROOM"
                else:
                    slow_print("A massive golden door blocks your path. It requires a key.")
            elif dir_choice == "south":
                current_room = "Goblin Gambler"
                enter_goblin_gambler(hero)  # MODUL MEGHÍVÁSA
                current_room = "Entrance"   # Játékmenet szerint visszatér az előtérbe
            elif dir_choice == "west":
                current_room = "Witch Brewery"
                enter_witch_brewery(hero, potion_shop) # MODUL MEGHÍVÁSA
                current_room = "Entrance"   # Vásárlás után visszatér
            else:
                slow_print("That's not a real direction!")

        # --- DARK HALLWAY ---
        elif current_room == "Dark Hallway":
            if random.randint(1, 10) <= 4:
                fight_rat(hero)  # MODUL MEGHÍVÁSA
                if hero.hp <= 0:
                    continue
                current_room = "The Search Room"
                continue

            if dir_choice == "south":
                current_room = "Entrance"
                slow_print("You head back toward the faint light of the entrance.")
            elif dir_choice == "north":
                current_room = "The Search Room"
                slow_print("You move further up the hallway into a dusty chamber.")
            else:
                slow_print("You can't go that way from here.")

        # --- THE SEARCH ROOM ---
        elif current_room == "The Search Room":
            print("\nThe floor is littered with debris.")
            search = input("Do you want to search for items? (search/continue): ").lower().strip()
            
            if search == "search":
                roll = random.randint(1, 10)
                if roll <= 4 and "key" not in hero.inventory:
                    slow_print("✨ Your fingers brush against cold metal... You found the SHINY KEY!")
                    hero.inventory.append("key")
                elif roll > 6:
                    gold_found = random.randint(10, 35)
                    hero.gold += gold_found
                    slow_print(f"💰 You found a small pouch containing {gold_found} gold!")
                else:
                    slow_print("Dust and echoes. You found nothing.")
                
                # Keresés után megkérdezzük, merre akar menni, így nem a régi irány dönt!
                print("\nWhere do you want to go now?")
                next_move = input("Type 'north' for Armory or 'south' to go back: ").lower().strip()
                if next_move == "north":
                    current_room = "Armory"
                elif next_move == "south":
                    current_room = "Dark Hallway"
                else:
                    slow_print("Invalid direction, you stay here.")
                continue # Frissítjük a kört az új szobával!

            else:
                # Ha nem keresett, hanem rögtön továbbment
                print("You continue wandering the cave...")
                current_room = "Armory"
                continue

        # --- THE KING'S ROOM ---
        elif current_room == "THE KINGS ROOM":
            if dragon_dead:
                slow_print("The Son of the Dragon King is already defeated. The treasure is yours to take.")
                current_room = "Entrance"
            else:
                slow_print("You stand before the Son of the Dragon King. He sits atop a mountain of gold.")
                action = input("What will you do? (fight/sneak): ").lower().strip()
                
                if action == "sneak":
                    if random.randint(1, 10) <= 4:
                        slow_print("❌ Your armor clangs! The Dragon's eyes snap open!")
                        action = "fight"
                    else:
                        gold_stolen = random.randint(50, 150)
                        hero.gold += gold_stolen
                        hero.exp += 50
                        slow_print(f"🤫 You fill your pockets with {gold_stolen} gold and slip away!")
                        current_room = "Entrance"

                if action == "fight":
                    dragon_dead = fight_dragon(hero)  # MODUL MEGHÍVÁSA
                    current_room = "Entrance"

        # --- ARMORY ---
        elif current_room == "Armory":
            dir_choice = "" # 1. FIX: Kitöröljük a beragadt "north" irányt!

            # Ha a menü után mégis mozgást választana a játékos:
            print("\nYou can go: south (back to Search Room)")
            armory_move = input("Do you want to move or stay here? (move/stay): ").lower().strip()

            if armory_move == "move":
                dir_choice = input("Which direction? ").lower().strip()
                if dir_choice == "south":
                    current_room = "The Search Room"
                    slow_print("You walk back into the debris-covered Search Room.")
                    continue
                elif dir_choice in ["north", "east", "west"]:
                    slow_print("There are no paths leading that way.")
                    continue # 2. FIX: Visszaugrik a főmenübe, nem engedi lefutni az Armory alját!

            # Ha marad a szobában, akkor jön a fegyverkereső menü!
            slow_print("Racks of rusted swords and shattered shields line the walls...")
            armory_choice = input("Do you want to search for (common/rare): ").lower().strip()
            
            if armory_choice == "common":
                armory_roll = random.randint(1, 10)
                if armory_roll <= 4:
                    armory_common_loot = {"item": "Rusty Sword", "type": "atk", "bonus": 5}
                elif armory_roll <= 7:
                    armory_common_loot = {"item": "Old Shield", "type": "def", "bonus": 5}
                else:
                    armory_common_loot = {"item": "Leather Armor", "type": "def", "bonus": 3}
                    
                armory_common_pick = input(f"You found an {armory_common_loot['item']}! Do you want to take it? (yes/no): ").lower().strip()
                if armory_common_pick == "yes":
                    hero.inventory.append(armory_common_loot["item"])
                current_room = "The Search Room"
                continue

            elif armory_choice == "rare":
                slow_print("⚠️ You venture deeper into the darkness...")
                secret_target = random.randint(4, 9)
                input("\n[ Press ENTER to start your blind 2-second trial... ]")
                
                start_time = time.time()
                click_count = 0
                while time.time() - start_time < 2:
                    input(f"💥 CRANK! (You have tapped: {click_count + 1})")
                    click_count += 1

                if secret_target - 1 <= click_count <= secret_target + 1:
                    slow_print("🌟 UNBELIEVABLE GUESS! The lock shatters open!")
                    rare_roll = random.randint(1, 2)
                    rare_loot = "Dragon-Slayer Bow" if rare_roll == 1 else "Crystal Plate Armor"
                    hero.inventory.append(rare_loot)
                    slow_print(f"🎒 Found: {rare_loot}! Remember to equip it from your inventory.")
                else:
                    slow_print("❌ MISSED IT! The magical feedback explodes in your face!")
                    trap_dmg = random.randint(20, 30)
                    hero.hp -= trap_dmg
                    slow_print(f"❤️ You take {trap_dmg} damage! Remaining HP: {hero.hp}")

                    if hero.hp <= 0:
                        continue
                
                current_room = "The Search Room"
                continue

# --- GAME OVER STATE ---
if hero.hp <= 0:
    slow_print("\n💀 Darkness takes you. Your journey ends here.")