# Locations.py
from Character import slow_print
import random

def enter_witch_brewery(hero, potion_shop):
    print("The air is thick with the scent of herbs and bubbling potions. A cackling witch stirs a cauldron in the corner.")
    print("She offers you a chance to buy potions that could aid you in your quest. But beware, her prices are steep!")
    
    for key, potion in potion_shop.items():
        print(f"{key}. {potion['name']} - {potion['cost']} gold (Restores {potion['bonus']} {potion['stat'].upper()})")
    print("4. Rest at the cauldron (Fully restores HP for 50 gold)")
    
    while True:
        potion_choice = input("Enter the number of the potion you want to buy (or 'leave' to exit): ").strip()
        if potion_choice in potion_shop:
            selected_potion = potion_shop[potion_choice]
            if hero.gold >= selected_potion["cost"]:
                hero.gold -= selected_potion["cost"]
                hero.inventory.append(selected_potion["name"])
                print(f"Bought {selected_potion['name']}!")
            else:
                print("You don't have enough gold for that potion!")
        elif potion_choice.lower() == "leave":
            slow_print("You decide to leave the witch's brewery and head back to the entrance.")
            break
        elif potion_choice == "4":
            if hero.gold >= 50:
                for t in range(5):
                    slow_print("Resting at the cauldron... " + "." * (t + 1), 0.5)
                hero.gold -= 50
                hero.hp = hero.max_hp  # Dinamikus max_hp-ra töltünk vissza!
                print("You rest at the cauldron and feel completely rejuvenated! HP fully restored!")
                break
            else:
                print("You don't have enough gold to rest at the cauldron!")
        else:                    
            print("Invalid choice, please select a valid potion number or 'leave'.")

def enter_goblin_gambler(hero):
    slow_print("The goblin grins and shuffles his cards. 'Fancy a game of chance? Win some gold, or lose some!'")
    gamble_choice = input("Do you want to gamble with the goblin? (yes/no): ").lower().strip()
    
    if gamble_choice == "no":
        slow_print("You politely decline and head back to the entrance.")
        return

    slow_print("The goblin grins and hands you a six sided dice.")
    slow_print("The rule is simple: if your roll is higher than the goblin's, you win double your bet. If lower, you lose it. Tie = money back.")
    
    while True:
        print(f"You have {hero.gold} gold.")
        if hero.gold <= 0:
            slow_print("You don't have any gold left! The goblin laughs and pushes you out of the room.")
            break
            
        bet = input("Enter your bet amount (or 'leave' to exit): ").strip()
        if bet.lower() == "leave":
            break
        if not bet.isdigit():
            slow_print("That's not a valid number!")
            continue
            
        bet = int(bet)
        if bet > hero.gold:
            slow_print("You don't have that much gold!")
            continue
            
        input("Press ENTER to roll the dice...")
        player_roll = random.randint(1, 6)
        hero.gold -= bet  
        goblin_roll = random.randint(1, 6)
        
        slow_print(f"You rolled a {player_roll}!")
        slow_print(f"The goblin rolled a {goblin_roll}!")
        
        if player_roll > goblin_roll:
            winnings = bet * 2
            hero.gold += winnings
            hero.gain_exp(50)
            slow_print(f"Congratulations! You win {winnings} gold!")
        elif player_roll < goblin_roll:
            slow_print(f"Unlucky! You lose {bet} gold!")
        else:
            slow_print("It's a tie! No gold is won or lost.")
            hero.gold += bet  
            
        print("\n---------------------------------")
        play_again = input("Do you want to play again with the goblin? (yes/no): ").lower().strip()
        if play_again not in ["yes", "y"]:
            slow_print("You step away from the gambling table.")
            break