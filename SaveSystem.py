def save_game(hero, current_room, dragon_dead):
    """Saves the current game state to a file."""
    try:
        with open("savegame.txt", "w") as f:
            f.write(f"{hero.name}\n")
            f.write(f"{hero.hp}\n")
            f.write(f"{hero.gold}\n")
            f.write(f"{hero.atk_bonus}\n")
            f.write(f"{hero.def_bonus}\n")
            f.write(f"{current_room}\n")
            f.write(f"{dragon_dead}\n")
            f.write(",".join(hero.inventory) + "\n")
        print("💾 Game saved successfully!")
    except Exception as e:
        print(f"❌ Error saving game: {e}")

def load_game(hero):
    """Loads the game state from a file."""
    try:
        with open("savegame.txt", "r") as f:
            lines = f.read().splitlines()

        hero.name = lines[0]
        hero.hp = int(lines[1])
        hero.gold = int(lines[2])
        hero.atk_bonus = int(lines[3])
        hero.def_bonus = int(lines[4])
        current_room = lines[5]
        dragon_dead = lines[6] == "True"

        if lines[7].strip():
            hero.inventory = lines[7].split(",")
        else:
            hero.inventory = []

        print("💾 Game loaded successfully!")
        return current_room, dragon_dead
    except FileNotFoundError:
        print("❌ No save file found. Starting a new game.")
        return None, None