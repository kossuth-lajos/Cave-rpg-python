import random
import time
import sys


def slow_print(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

ITEM_STATS = {
    "Rusty Sword":         {"type": "atk", "bonus": 5},
    "Dragon-Slayer Bow":   {"type": "atk", "bonus": 20},
    "Old Shield":          {"type": "def", "bonus": 5},
    "Leather Armor":       {"type": "def", "bonus": 3},
    "Crystal Plate Armor": {"type": "def", "bonus": 10}
}


class Player:
    def __init__(self, name, hp, gold):
        self.name = name
        self._hp = hp
        self.max_hp = 100
        self.gold = gold
        self.inventory = []
        self.atk_bonus = 0
        self.def_bonus = 0
        self.equipped_weapon = None  # No weapon equipped by default
        self.is_weakened = False
        self.weakened_turns = 0
        self.level = 1
        self._exp = 0
        self.exp_needed = 100


    @property
    def hp(self):
        return self._hp
    
    @hp.setter
    def hp(self, value):
        if value > self.max_hp:
            self._hp = self.max_hp
        elif value < 0:
            self._hp = 0
        else:
            self._hp = value
    @property
    def exp(self):
        return self._exp
    
    @exp.setter
    def exp(self, value):
        self._exp = value
        while self._exp >= self.exp_needed:
            self.level += 1
            self._exp -= self.exp_needed
            self.exp_needed = int(self.exp_needed*1.5)
            slow_print(f"🚀 LEVEL UP! You are now level {self.level}!")
            self.max_hp += 20  # Minden szintlépésnél növeljük a max HP-t
            self.hp = self.max_hp  # HP visszatöltése a maxra szintlépéskor
            potions = ["Health Potion", "Strength Elixir", "Defense Tonic"]
            potion_for_level = random.choice(potions)
            self.inventory.append(potion_for_level)
            if self.level == 2:
                self.inventory.append("Warped Key")
            else:
                pass



    def equip_gear(self):
        if not self.inventory:
            slow_print("🎒 Your inventory is empty. No gear to equip.")
            return
        inventory_str = "\n".join(self.inventory)
        print(f"\n--- YOUR INVENTORY ---\n{inventory_str}\n----------------------")
        choice = input("Type the name of the item you want to equip (or 'cancel' to go back): ").strip()

        if choice in self.inventory:
            if choice in ITEM_STATS:
                item_data = ITEM_STATS[choice]
                if item_data["type"] == "atk":
                    self.equipped_weapon = choice
                    self.atk_bonus = item_data["bonus"]
                    slow_print(f"⚔️ Equipped {choice}! Your ATK bonus is now +{self.atk_bonus}.")
                elif item_data["type"] == "def":
                    self.def_bonus += item_data["bonus"]
                    slow_print(f"🛡️ Equipped {choice}! Your DEF bonus is now +{self.def_bonus}.")
            else:
                slow_print("📜 That item cannot be equipped (like a key or dragon head).")
        elif choice.lower() == "cancel":
            slow_print("Cancelled gear equip.")
            return
        else:
            slow_print("❌ You don't have that item!")
    def sword_atk(self, enemy, acc, min_dmg, max_dmg):
        # --- HIT CHECK ---
        if random.randint(1, 10) <= acc:
            dmg_roll = random.randint(min_dmg, max_dmg) + self.atk_bonus
            if self.is_weakened:
                dmg_roll //= 2
                slow_print(f"⚠️  Your sword feels like lead... WEAKENED! You deal {dmg_roll} damage.")
                return dmg_roll
            else:
                slow_print(f"⚔️  A clean slash! You dealt {dmg_roll} damage to the {enemy}.")
                return dmg_roll
        else:
            slow_print(f"🛡️  The {enemy} parries your strike with a golden claw! MISS!")
            return 0
            

    def bow_atk(self, enemy, acc, min_dmg, max_dmg):
        
        if random.randint(1, 10) <= acc:
            dmg_roll = random.randint(min_dmg, max_dmg) + self.atk_bonus
            
            if self.is_weakened:
                dmg_roll //= 2
                slow_print(f"⚠️  The venom in your veins makes your arms heavy... WEAKENED! you deal {dmg_roll} damage.")
                return dmg_roll

            elif random.randint(1, 10) <= 2:  # 20% chance for critical hit
                dmg_roll *= 2
                slow_print(f"🎯 BULLSEYE! A critical shot for {dmg_roll} damage!")
            else:
                slow_print(f"🏹 Your arrow finds its mark! {dmg_roll} damage dealt.")

            return dmg_roll
        else:
            slow_print(f"💨 The arrow whistles past the {enemy}'s head. MISS!")
            return 0
    def use_potion(self, potion_data):
        # Megnézzük, hogy a bájital neve benne van-e a táskánkban
        if potion_data["name"] in self.inventory:
            target_stat = potion_data.get("stat")
            potion_bonus = potion_data.get("bonus", 0)

            # Allowlist of safe attributes that potions can modify
            allowed_stats = ["atk_bonus", "def_bonus", "hp", "max_hp"]
            if target_stat not in allowed_stats:
                slow_print("❌ This potion cannot modify that stat.")
                return

            # Ensure attribute exists (initialize to 0 if missing)
            if not hasattr(self, target_stat):
                setattr(self, target_stat, 0)

            try:
                current_value = getattr(self, target_stat)
                updated_value = current_value + potion_bonus

                # Special handling for max_hp (increase cap and adjust current hp)
                if target_stat == "max_hp":
                    setattr(self, "max_hp", updated_value)
                    # Increase current hp by same bonus but don't exceed new max_hp
                    self.hp = min(self.hp + potion_bonus, updated_value)
                    slow_print(f"\n🧪 You drink the {potion_data['name']}!")
                    slow_print(f"✨ Your MAX_HP increased from {current_value} to {updated_value}!")
                    self.inventory.remove(potion_data["name"])
                    return

                # Special handling for hp (healing, capped at max_hp)
                if target_stat == "hp":
                    max_hp = getattr(self, "max_hp", self.hp)
                    updated_value = min(updated_value, max_hp)
                    setattr(self, "hp", updated_value)
                    slow_print(f"\n🧪 You drink the {potion_data['name']}!")
                    slow_print(f"✨ Your HP is now {updated_value}/{max_hp}!")
                    self.inventory.remove(potion_data["name"])
                    return

                # Default: modify atk_bonus or def_bonus
                setattr(self, target_stat, updated_value)
                slow_print(f"\n🧪 You drink the {potion_data['name']}!")
                slow_print(f"✨ Your {target_stat.upper()} upgraded from +{current_value} to +{updated_value}!")
                self.inventory.remove(potion_data["name"])
            except Exception:
                slow_print("❌ Could not apply the potion due to an unexpected error.")
                return
        else:
            slow_print("❌ You don't have that potion in your inventory!")
    def take_damage(self, amount):
        final_damage = amount - self.def_bonus
        if final_damage < 0:
            final_damage = 0
        self.hp = max(self.hp - final_damage, 0)
        slow_print(f"💥 You took {final_damage} damage after defense! Current HP: {self.hp}/{self.max_hp}")
    def __str__(self):
        weapon = self.equipped_weapon if self.equipped_weapon else "Bare Hands"
        return (f"\n✨ === {self.name} Status === ✨\n"
                f"🌟 Level: {self.level} | 🎖️ EXP: {self.exp}/{self.exp_needed}\n"
                f"❤️ HP: {self.hp}/{self.max_hp}\n"
                f"⚔️ ATK Bonus: +{self.atk_bonus} (Weapon: {weapon})\n"
                f"🛡️ DEF Bonus: +{self.def_bonus}\n"
                f"💰 Gold: {self.gold}\n"
                f"==========================")