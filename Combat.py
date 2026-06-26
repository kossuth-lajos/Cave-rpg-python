# Combat.py
from Character import slow_print
from Enemy import Rat, Dragon
import random
from Character import Player


def fight_rat(hero):
    slow_print("A giant RAT emerges from the shadows, its eyes glowing with hunger!")
    current_enemy = Rat()
    
    while current_enemy.hp > 0 and hero.hp > 0:
        print(f"\n{current_enemy.name} HP: {current_enemy.hp} | Your HP: {hero.hp}")
        
        current_weapon = hero.equipped_weapon if hero.equipped_weapon else "Bare Hands" 
        print(f"⚔️ [ WEAPON: {current_weapon} ]")
        print("1. Strike!")
        print("2. Change Weapon")
        weapon_choice = input("Choose (1 or 2): ").strip()
        
        if weapon_choice == "1":
            if current_weapon == "Rusty Sword":
                dmg = hero.sword_atk(current_enemy.name, 8, 8, 12)
                current_enemy.hp -= dmg
            elif current_weapon == "Dragon-Slayer Bow":
                dmg = hero.bow_atk(current_enemy.name, 7, 7, 20)
                current_enemy.hp -= dmg
            else:
                dmg = random.randint(2, 6)
                current_enemy.hp -= dmg
                slow_print(f"👊 You punch the {current_enemy.name} for {dmg} damage!")
                
            if hero.is_weakened:
                hero.weakened_turns -= 1
                if hero.weakened_turns == 0:
                    slow_print("The weakening effect wears off. You feel normal again.")
                    hero.is_weakened = False
                    
            # Ellenőrzések és a patkány köre (Csak ha az 1-est nyomta)
            if current_enemy.hp <= 0:
                slow_print("The rat collapses! You search its corpse and find 15 gold.")
                hero.gold += 15
                hero.exp += 30
                break
            else:
                current_enemy.attack(hero)
                
        elif weapon_choice == "2":
            hero.equip_gear()
            continue
        else:
            print("❌ That button does nothing")
            continue


def fight_dragon(hero):
    current_enemy = Dragon()
    round_count = 1
    
    while current_enemy.hp > 0 and hero.hp > 0:
        print(f"\n--- ROUND {round_count} ---")
        print(f"{current_enemy.name}: {current_enemy.hp} HP | You: {hero.hp} HP")
        
        current_weapon = hero.equipped_weapon if hero.equipped_weapon else "Bare Hands" 
        print(f"\n⚔️ [ WEAPON: {current_weapon} ]")
        print("1. Strike!")
        print("2. Change Weapon")
        weapon_choice = input("Choose (1 or 2): ").strip()
        
        if weapon_choice == "1":
            if current_weapon == "Rusty Sword":
                damage = hero.sword_atk(current_enemy.name, 8, 10, 20)
                current_enemy.hp -= damage
            elif current_weapon == "Dragon-Slayer Bow":
                damage = hero.bow_atk(current_enemy.name, 7, 15, 30)
                current_enemy.hp -= damage
            else:
                damage = random.randint(2, 6)
                current_enemy.hp -= damage
                slow_print(f"👊 You punch the {current_enemy.name} with your bare fists for {damage} damage!")
                
            if hero.is_weakened:
                hero.weakened_turns -= 1
                if hero.weakened_turns == 0:
                    slow_print("The weakening effect wears off. You feel normal again.")
                    hero.is_weakened = False

            # Kör végi események és visszatámadás beágyazva az 1-es gomb alá
            if current_enemy.hp > 0:
                current_enemy.attack(hero)
            else:
                slow_print("\n🏆 The Dragon collapses! The treasury is yours!")
                slow_print(f"FINAL SCORE: {hero.gold} GOLD.")
                slow_print("For the victory, you take his head off as a trophy. You might find this useful later on...")
                hero.inventory.append("dragon head No1")
                hero.exp += 50
                return True 
                
            round_count += 1  # Csak sikeres harci kör után nő a körök száma
            
        elif weapon_choice == "2":
            hero.equip_gear()
            continue
        else:
            print("❌ That button does nothing")
            continue
            
    return False