import random

class Item:
    def __init__(self, name, shortcut, value):
        self.name = name
        self.shortcut = shortcut
        self.value = value

class Weapon(Item):
    def __init__(self, name, shortcut, value, damage, speed):
        super().__init__(name, shortcut, value)
        self.damage = damage
        self.speed = speed

    def __str__(self):
        return('{}    -> Damage: {} Speed: {} Price:{}'.format(self.name, self.damage, self.speed, self.value))

class Potion(Item):
    def __init__(self, name, shortcut, value, hp_up = False, mp_up = False, speed_up = False, defence_up = False, attack_up = False):
        super().__init__(name, shortcut, value)
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
    def __init__(self, name, shortcut, value, defence_bonus, speed, mana_bonus = 0):
        super().__init__(name, shortcut, value)
        self.defence_bonus = defence_bonus
        self.speed = speed
        self.mana_bonus = mana_bonus

    def __str__(self):
        return('{}    -> Defence: {} Speed: {} Price: {}'.format(self.name, self.defence_bonus, self.speed, self.value))

class Consumable(Item):
    def __init__(self, name, shortcut, value, energy_up, hp_up = None, mp_up = None):
        super().__init__(name, shortcut, value)
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
        print('\n<Used {}. Restored {} energy!>\n'.format(self.name, self.energy_up))

# weapons
dagger = Weapon('Dagger', 'da', value = 4, damage = 3, speed = -1)
short_sword = Weapon('Short sword', 'shs', value = 10, damage =  4, speed = -2)
long_sword = Weapon('Long Sword', 'ls', value = 35, damage = 6, speed = -3)
two_handed_sword = Weapon('Two-Handed Sword', 'ths', value = 80, damage = 8, speed =-5)
axe = Weapon('Axe', 'ax', value = 27, damage = 5, speed = -3)
battleaxe = Weapon('Battle Axe', 'bax', value = 92, damage = 9, speed = -6)
spear = Weapon('Spear', 'sp', value = 58, damage = 7, speed = -4)


# armor
clothes = Armor('Clothes', 'cl', value = 1, defence_bonus = 1, speed = 0)
leather_armor = Armor('Leather Armor', 'la', value = 20, defence_bonus = 3, speed = -2)
studded_leather_armor = Armor('Studded Leather Armor', 'sla', value = 45, defence_bonus = 4, speed = -3)
chain_mail_armor = Armor('Chain Mail Armor', 'cma', value = 120, defence_bonus = 6, speed = -4)
plate_armor = Armor('Plate Armor', 'pa', value = 250, defence_bonus = 8, speed = -5)
mage_robe = Armor('Mage Robe', 'mr', value = 30, defence_bonus = 2, speed = -1, mana_bonus = 10)
master_robe = Armor('Master Mage Robe', 'mmr', value = 200, defence_bonus = 4, speed = -2, mana_bonus = 20)

# potions
mana_potion = Potion('Mana Potion', 'mp', value = 20, mp_up = True)
healing_potion = Potion('Healing Potion', 'hp', value = 20, hp_up = True)
rejuvenation_potion = Potion('Rejuvenation Potion', 'rp', value = 50, hp_up = True, mp_up = True)
speed_potion = Potion('Speed Potion', 'spp', value = 15, speed_up = True)
ironskin_potion = Potion('Ironskin Potion', 'ip', value = 35, defence_up = True)
strength_potion = Potion('Strenght Potion', 'stp', value = 35, attack_up = True)

# consumables
bread = Consumable('Bread', 'br', value = 2, energy_up = 5)
water = Consumable('Water', 'wa', value = 1, energy_up = 3)
raw_meat = Consumable('Raw meat', 'rm', value = 5, energy_up = 5, hp_up=-3)
cooked_meat = Consumable('Cooked meat', 'cm', value = 7, energy_up = 10, hp_up=2)
potato = Consumable('Potato', 'po', value = 1, energy_up = 3)
cooked_potato = Consumable('Cooked potato', 'cpo', value = 2, energy_up = 5, hp_up=1)
carrot = Consumable('Carrot', 'ca', value = 1, energy_up = 3)
rotten_meat = Consumable('Rotten meat', 'rom', value = 1, energy_up = 2, hp_up=-5)
wine = Consumable('Wine', 'wi', value = 6, energy_up = 2, mp_up=5)
beer = Consumable('Beer', 'be', value = 2, energy_up = 1, mp_up=2)
apple = Consumable('Apple', 'ap', value = 1, energy_up = 5)
full_meal = Consumable('Full meal', 'fum', value = 10, energy_up = 15, hp_up = 3)

#================================================================================================================================
#================================================================================================================================

class Spell:
    def __init__(self, name, shortcut, description, level_required, mp_cost):
        self.name = name
        self.shortcut = shortcut
        self.description = description
        self.level_required = level_required
        self.mp_cost = mp_cost

    def __str__(self):
        return(self.name)

class DamageSpell(Spell):
    def __init__(self, name, shortcut, description, level_required, mp_cost, damage):
        super().__init__(name, shortcut, description, level_required, mp_cost)
        self.damage = damage

    def use_spell(self, player, enemy):
        enemy.hp -= self.damage
        player.mp -= self.mp_cost
        print('\n<{} dealt {} damage to {}!>'.format(self.name, self.damage, enemy.name))

class HealingSpell(Spell):
    def __init__(self, name, shortcut, description, level_required, mp_cost, heal_value):
        super().__init__(name, shortcut, description, level_required, mp_cost)
        self.heal_value = heal_value

    def use_spell(self, player):
        player.hp += self.heal_value
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        player.mp -= self.mp_cost
        print('\n<You have used {}!>'.format(self.name))

class SkillSpell(Spell):
    def __init__(self, name, shortcut, description, level_required, mp_cost):
        super().__init__(name, shortcut, description, level_required,mp_cost)


# healing spells
minor_healing = HealingSpell('Minor Healing', 'mih', 'Heals 10 HP', 1, 6, 10)
healing = HealingSpell('Healing', 'he', 'Heals 20 HP', 5, 13, 20)
major_healing = HealingSpell('Full Heal', 'mah', 'Fully restores HP', 10, 30, 999)

# damage spells
fireball = DamageSpell('Fireball', 'fb', '5 HP DMG', 1, 5, 5)
frostbite = DamageSpell('Frostbite', 'fr', '7 HP DMG', 3, 7, 7)
thunder = DamageSpell('Thunder', 'th', '10 HP DMG', 5, 10, 10)
flames = DamageSpell('Flames', 'fl', '15 HP DMG', 7, 15, 15)
blizzard = DamageSpell('Blizzard', 'bl', '20 HP DMG', 10, 20, 20)
storm = DamageSpell('Storm', 'st', '30 HP DMG', 15, 30, 30)

# skill spells
vision = SkillSpell('Vision', 'vis', 'Greatly increases the chance of succesfull search.', 2, 2)
spell_disarm_trap = SkillSpell('Disarm Trap', 'dat', 'Safely disarms traps', 3, 3)
spell_open_lock = SkillSpell('Open', 'op', 'Unlocks any lock.', 4, 4)

all_spells_list = [minor_healing, healing, major_healing, fireball, frostbite, thunder, flames, blizzard, storm, vision, spell_disarm_trap, spell_open_lock]


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



class Trap:
    def __init__(self, message, chance, damage, xp, disarmed = False):
        self.message = message
        self.chance = chance
        self.damage = damage
        self.xp = xp
        self.disarmed = disarmed

trap_1 = Trap('You stepped on ', 20, 4, 3)

class Treasure:
    def __init__(self, chance, xp, gold, item, force):
        self.chance = chance
        self.xp = xp
        self.gold = gold
        self.item = item
        self.force = force

treasure_1 = Treasure(50, 3, 10, [dagger], 3)

class Search:
    def __init__(self, item=None, gold=None, xp=None, trap=None, chance=None, treasure=None):
        self.item = item
        self.gold = gold
        self.xp = xp
        self.trap = trap
        self.chance = chance
        self.treasure = treasure

srch_cave_a2 = Search(item = [healing_potion, mana_potion], gold = 3, xp = 3, trap = trap_1, chance = 50, treasure = treasure_1)
