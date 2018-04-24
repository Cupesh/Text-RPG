import random
class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Weapon(Item):
    def __init__(self, name, value, damage, speed):
        super().__init__(name, value)
        self.damage = damage
        self.speed = speed

class Potion(Item):
    def __init__(self, name, value, hp_up = False, mp_up = False, speed_up = False, defence_up = False, attack_up = False):
        super().__init__(name, value)
        self.hp_up = hp_up
        self.mp_up = mp_up
        self.speed_up = speed_up
        self.defence_up = defence_up
        self.attack_up = attack_up

    def use_potion(self, player):
        if self.hp_up == True and self.mp_up == True:
            player.hp = player.max_hp
            player.mp = player.max_mp
            print('\nHP and MP restored!')
        elif self.hp_up == True:
            player.hp = player.max_hp
            print('\nHP restored!')
        elif self.mp_up == True:
            player.mp = player.max_hp
            print('\nMP restored!')
        elif self.speed_up == True:
            player.speed += 1
            print('\nYour speed has increased!')
        elif self.defence_up == True:
            player.defence += 1
            print('\nYour defence increased!')
        elif self.attack_up == True:
            player.attack += 1
            print('\nYour strenght increased!')


class Armor(Item):
    def __init__(self, name, value, defence_bonus, speed, mana_bonus = 0):
        super().__init__(name, value)
        self.defence_bonus = defence_bonus
        self.speed = speed
        self.mana_bonus = mana_bonus


# weapons
dagger = Weapon('Dagger', value = 4, damage = 3, speed = -1)
short_sword = Weapon('Short sword', value = 10, damage =  4, speed = -2)
long_sword = Weapon('Long Sword', value = 35, damage = 6, speed = -3)
two_handed_sword = Weapon('Two-Handed Sword', value = 80, damage = 8, speed =-5)
axe = Weapon('Axe', value = 27, damage = 5, speed = -3)
battleaxe = Weapon('Battle Axe', value = 92, damage = 9, speed = -6)
spear = Weapon('Spear', value = 58, damage = 7, speed = -4)


# armor
clothes = Armor('Clothes', value = 1, defence_bonus = 1, speed = 0)
leather_armor = Armor('Leather Armor', value = 20, defence_bonus = 3, speed = -2)
studded_leather_armor = Armor('Studded Leather Armor', value = 45, defence_bonus = 4, speed = -3)
chain_mail_armor = Armor('Chain Mail Armor', value = 120, defence_bonus = 6, speed = -4)
plate_armor = Armor('Plate Armor', value = 250, defence_bonus = 8, speed = -5)
mage_robe = Armor('Mage Robe', value = 30, defence_bonus = 2, speed = -1, mana_bonus = 10)
master_robe = Armor('Master Mage Robe', value = 200, defence_bonus = 4, speed = -2, mana_bonus = 20)

# potions
mana_potion = Potion('Mana Potion', value = 20, mp_up = True)
healing_potion = Potion('Healing Potion', value = 20, hp_up = True)
rejuvenation_potion = Potion('Rejuvenation Potion', value = 50, hp_up = True, mp_up = True)
speed_potion = Potion('Speed Potion', value = 15, speed_up = True)
ironskin_potion = Potion('Ironskin Potion', value = 35, defence_up = True)
strength_potion = Potion('Strenght Potion', value = 35, attack_up = True)
