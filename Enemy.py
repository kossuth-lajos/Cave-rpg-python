import random
import time
import sys

# Használjuk itt is a slow_print-et a szép játékélményért!
def slow_print(text, speed=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

class Enemy:
    def __init__(self, name, health, attack_power, gold_reward, exp_reward):
        self.name = name
        self.hp = health
        self.atk = attack_power
        self.gold = gold_reward
        self.exp = exp_reward

    def attack(self, player):
        # Ezt az alapértelmezett metódust hagyjuk meg, ha egy sima szörny nem kap egyedi logikát
        slow_print(f"The {self.name} attacks you!")
        player.take_damage(self.atk)

class Dragon(Enemy):
    def __init__(self):
        super().__init__(name="Dragon", health=125, attack_power=12, gold_reward=150, exp_reward=100)

    def attack(self, player):
        rnd = random.randint(1, 3)
        damage = self.atk  # Alap sebzés

        if rnd == 1:
            slow_print("🐉 The dragon stomps hard with his foot!")
            
        elif rnd == 2:
            slow_print("🔥 The dragon breathes fire!")
            damage += 10
            if random.randint(1, 2) == 1:
                slow_print("⚠️ You catch on fire and will take 5 damage for 3 turns.")
                player.is_burning = True
                player.burned_turns = 3
                player.burn_damage = 5

        else:
            slow_print("🐊 The dragon bites you with his sharp teeth!")
            damage += 5

        # A végén EGYETLEN helyen adjuk be a sebzést az ősosztály logikáját kihasználva
        player.take_damage(damage)

class Rat(Enemy):
    def __init__(self):
        super().__init__(name="Rat", health=30, attack_power=5, gold_reward=10, exp_reward=random.randint(10, 15))

    def attack(self, player):
        rnd = random.randint(1, 3)
        
        if rnd == 1:
            slow_print("🐀 The rat bites you!")
            if random.randint(1, 10) <= 3:
                slow_print("🤢 The rat was infected with weakness, it spreads to you!")
                player.is_weakened = True
                player.weakened_turns = 1
                slow_print("Lucky you, it only lasts for 1 turn.")
            player.take_damage(self.atk)
                
        elif rnd == 2:
            slow_print("🐾 The rat scratches you with his claws!")
            player.take_damage(self.atk + 2)
            
        else:
            slow_print("💨 The rat missed you! You dodge gracefully.")
            # Itt nem hívjuk meg a take_damage-et, így 0 lesz a sebzés!