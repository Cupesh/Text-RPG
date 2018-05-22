# to do = TalkQuest
import random

class Item:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return(self.name)

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

class Consumable(Item):
    def __init__(self, name, value, energy_up, hp_up = None, mp_up = None):
        super().__init__(name, value)
        self.hp_up = hp_up
        self.mp_up = mp_up
        self.energy_up = energy_up

    def use_consumable(self, player):
        if self.hp_up:
            player.hp += self.hp_up
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            print('\n<Restored {} HP!>\n'.format(self.hp_up))
        if self.mp_up:
            player.mp += self.mp_up
            if player.mp > player.max_mp:
                player.mp = player.max_mp
            print('\n<Restored {} MP!>\n'.format(self.mp_up))
        player.energy += self.energy_up
        if player.energy > player.max_energy:
            player.energy = player.max_energy
        print('\n<Restored {} energy!>\n'.format(self.energy_up))

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

# consumables
bread = Consumable('Bread', value = 2, energy_up = 5)
water = Consumable('Water', value = 1, energy_up = 3)
raw_meat = Consumable('Raw meat', value = 5, energy_up = 5, hp_up=-3)
cooked_meat = Consumable('Cooked meat', value = 7, energy_up = 10, hp_up=2)
potato = Consumable('Potato', value = 1, energy_up = 3)
cooked_potato = Consumable('Cooked potato', value = 2, energy_up = 5, hp_up=1)
carrot = Consumable('Carrot', value = 1, energy_up = 3)
rotten_meat = Consumable('Rotten meat', value = 1, energy_up = 2, hp_up=-5)
wine = Consumable('Wine', value = 6, energy_up = 2, mp_up=5)
beer = Consumable('Beer', value = 2, energy_up = 1, mp_up=2)
apple = Consumable('Apple', value = 1, energy_up = 5)
full_meal = Consumable('Full meal', value = 10, energy_up = 15, hp_up = 3)

#================================================================================================================================
#================================================================================================================================

class Spell:
    def __init__(self, name, description, level_required, mp_cost):
        self.name = name
        self.description = description
        self.level_required = level_required
        self.mp_cost = mp_cost

    def __str__(self):
        return(self.name)

class DamageSpell(Spell):
    def __init__(self, name, description, level_required, mp_cost, damage):
        super().__init__(name, description, level_required, mp_cost)
        self.damage = damage

class HealingSpell(Spell):
    def __init__(self, name, description, level_required, mp_cost, heal_value):
        super().__init__(name, description, level_required, mp_cost)
        self.heal_value = heal_value

    def heal_spell_cast(self, player):
        player.hp += self.heal_value
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        player.mp -= self.mp_cost
        print('\n<You have used {}!>'.format(self.name))


# healing spells
minor_healing = HealingSpell('Minor Healing', 'Heals 10 HP', 1, 6, 10)
healing = HealingSpell('Healing', 'Heals 20 HP', 5, 13, 20)
major_healing = HealingSpell('Full Heal', 'Fully restores health', 10, 30, 999)

#damage spells
fireball = DamageSpell('Fireball', 'Launches a fireball that deals 5HP damage.', 1, 5, 5)
frostbite = DamageSpell('Frostbite', 'Casts several ice shards thats strike the enemy and deals 7 HP damage.', 3, 7, 7)
thunder = DamageSpell('Thunder', 'Strikes an oponent with a bolt of lightning that deals 10 HP damage.', 5, 10, 10)
flames = DamageSpell('Flames', 'Engulfs the enemy in flames. Deals 15 HP damage.', 7, 15, 15)
blizzard = DamageSpell('Blizzard', 'Casts a mighty blizzard on the enemy. Deals 20 HP damage.', 10, 20, 20)
storm = DamageSpell('Storm', 'Cast a mighty storm that hits the enemy with several lightning bolts. Deals 30 HP damage.', 15, 30, 30)

all_spells_list = [frostbite, thunder, flames, blizzard, storm, healing, major_healing]


class Quest:
    def __init__(self, name, description, owner, steps, message, xp_reward = 0, gold_reward = None, item_reward = None):
        self.name = name
        self.description = description
        self.owner = owner
        self.steps = steps
        self.message = message
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.item_reward = item_reward

class FetchQuest(Quest):
    def __init__ (self, name, description, owner, steps, message, xp_reward, gold_reward, item_reward, required_item = None, required_amount = None):
        super().__init__(name, description, owner, steps, message, xp_reward, gold_reward, item_reward)
        self.required_item = required_item
        self.required_amount = required_amount

class KillQuest(Quest):
    def __init__(self, name, description, owner, steps, message, xp_reward, gold_reward, item_reward, mob = None, kill_amount = None):
        super().__init__(name, description, owner, steps, message, xp_reward, gold_reward, item_reward)
        self.mob = mob
        self.kill_amount = kill_amount



first_quest = FetchQuest('Test Quest', 'Testing the quest system', 'Old Lady', {'FIRST' : True, 'SECOND' : False}, {'FIRST' : 'Bring 1x Short Sword', 'SECOND' : ''}, 20, 10, healing_potion, short_sword, 1)
second_quest = KillQuest('Test Kill Quest', 'Kill 3 Giant Rats!', 'Young man', {'FIRST' : True, 'SECOND' : False}, {'FIRST' : 'Kill 3x Giant Rat', 'SECOND' : ''},
                        25, 20, None, 'Giant Rat', 3)
