import random
from items import *

# ===================== DIALOGUES =========================
shopkeep_dialogue = {
        'WELCOME' : 'Welcome to my shop. Look at my wares and please buy some.', 
        'LEAVE' : 'Bye adventurer! Please come again!', 
        'GREET' : 'What was it, adventurer?',
        'DIALOGUE' : [
                ['How are you?', 'I\'m fine'], 
                ['What do you sell?', 'Just a sword and a potion.'],
                ['Did you hear any gossips lately?', 'Ur mom.']
]}

tavernkeep_dialogue = {
        'WELCOME' : 'Welcome to this small tavern. You can order food or you can sleep here. For a small fee of course.',
        'LEAVE' : 'Farewell!',
        'GREET' : 'What would you like to know?',
        'BED': 'You can sleep here for 5 gold pieces.',
        'DIALOGUE' : [
                ['How many people are here?', 'Two, lol.'],
                ['What do you sell?', 'Healing potions.'],
                ['Is this just a testing dialogue?', 'I don\'t know. Is it?']
]}

npc_01_dia = {
        'Q_GREET' : 'Hello stranger. Can you do something for me?',
        'Q_ONGOING' : 'Have you bring me my item?',
        'Q_PROMPT' : ['What is it?', 'Help yourself.'],
        'Q_REFUSED' : 'go fuck yourself then',
        'Q_ACCEPTED' : 'That\'s great. Thank you!',
        'Q_COMPLETED' : 'Oh thank you so much, here\'s your reward.',
        'GREET' : 'Yes?',
        'DIALOGUE' : [
            ['Good day.', 'Good day to you, young man.'],
            ['I want a quest', 'Okay, here it is.']
]}

npc_02_dia = {
        'Q_GREET' : 'Hello buddy, got a minute?',
        'Q_ONGOING' : 'Did you kill them all?',
        'Q_PROMPT' : ['What do you need young man?', 'Don\'t have time for this.'],
        'Q_REFUSED' : 'Fuck off then.',
        'Q_ACCEPTED' : 'Awesome!',
        'Q_COMPLETED' : 'You\'re a baddas. Here\'s your reward.',
        'GREET' : 'Hello.',
        'DIALOGUE' : [
            ['How is it going?', 'good good'],
            ['Any gossips', 'Nope']
        ]
}
# ======================= NPC ==============================

class NPC:
    def  __init__(self, xname, name, dialogue = None, quest = None, met = False):
        self.xname = xname
        self.name = name
        self.dialogue = dialogue
        self.quest = quest
        self.met = met

    @property
    def name(self):
        if self.met == True:
            return(self.xname)
        return(self._name)

    @name.setter
    def name(self, val):
        self._name = val
    


class Merchant(NPC):
    def __init__(self, xname, name, dialogue = None, quest = None, met = False, bed_price = 0):
        super().__init__(xname, name, dialogue, quest, met)
        self.weapons_inventory = [[dagger, 0], [short_sword, 0], [long_sword, 0], [two_handed_sword, 0], [axe, 0], [battleaxe, 0],
        [spear, 0]]
        self.potions_inventory = [[healing_potion, 0], [mana_potion, 0], [rejuvenation_potion, 0], [speed_potion, 0], [ironskin_potion, 0],
        [strength_potion, 0]]
        self.armors_inventory = [[clothes, 0], [leather_armor, 0], [studded_leather_armor, 0], [chain_mail_armor, 0], [plate_armor, 0],
        [mage_robe, 0], [master_robe, 0]]
        self.bed_price = bed_price

    def npc_add_item(self, item, amount):
        for i in self.weapons_inventory:
            if i[0] == item:
                i[1] += amount
        for i in self.potions_inventory:
            if i[0] == item:
                i[1] += amount
        for i in self.armors_inventory:
            if i[0] == item:
                i[1] += amount

    def npc_remove_item(self, item):
        for i in self.weapons_inventory:
            if i[0] == item:
                i[1] -= 1
        for i in self.potions_inventory:
            if i[0] == item:
                i[1] -= 1
        for i in self.armors_inventory:
            if i[0] == item:
                i[1] -= 1


shopkeep = Merchant('Steve', 'Shopkeep', dialogue = shopkeep_dialogue)
shopkeep.npc_add_item(dagger, 1)
shopkeep.npc_add_item(short_sword, 1)
shopkeep.npc_add_item(leather_armor, 1)
shopkeep.npc_add_item(studded_leather_armor, 1)
shopkeep.npc_add_item(healing_potion, 3)
shopkeep.npc_add_item(mana_potion, 3)
shopkeep.npc_add_item(strength_potion, 3)

tavernkeep = Merchant('Karl', 'Tavernkeeper', dialogue = tavernkeep_dialogue, bed_price = 5)
tavernkeep.npc_add_item(healing_potion, 3)
npc_01 = NPC('Mary', 'Old lady', dialogue = npc_01_dia, quest = first_quest)
npc_02 = NPC('Jim', 'small boy', dialogue = npc_02_dia, quest = second_quest)
# ===================== ENEMIES ==============================

class GiantRat:
    def __init__(self):
        self.name = 'Giant Rat'
        self.max_hp = random.randint(3, 5)
        self.hp = self.max_hp
        self.attack = random.randint(1, 2)
        self.defence = random.randint(1, 2)
        self.speed = random.randint(5, 7)
        self.gold = random.randint(0, 2)
        self.xp = 3

class Goblin:
    def __init__(self):
        self.name = 'Goblin'
        self.max_hp = random.randint(5, 7)
        self.hp = self.max_hp
        self.attack = random.randint(3, 4)
        self.defence = random.randint(2, 3)
        self.speed = random.randint(4, 5)
        self.gold = random.randint(0, 5)
        self.xp = 5

class Skeleton:
    def __init__(self):
        self.name = 'Skeleton'
        self.max_hp = random.randint(6, 8)
        self.hp = self.max_hp
        self.attack = random.randint(3, 5)
        self.defence = random.randint(2, 4)
        self.speed = random.randint(3, 5)
        self.gold = random.randint(0, 6)
        self.xp = 7

class Zombie:
    def __init__(self):
        self.name = 'Zombie'
        self.max_hp = random.randint(10, 15)
        self.hp = self.max_hp
        self.attack = random.randint(2, 5)
        self.defence = random.randint(2, 4)
        self.speed = random.randint(0, 1)
        self.gold = random.randint(2, 8)
        self.xp = 9
       
class BanditGreenhorn:
    def __init__(self):
        self.name = 'Bandit greenhorn'
        self.max_hp = random.randint(7, 10)
        self.hp = self.max_hp
        self.attack = random.randint(3, 5)
        self.defence = random.randint(2, 4)
        self.speed = random.randint(4, 6)
        self.gold = random.randint(2, 7)
        self.xp = 8
