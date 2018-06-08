import random
import items as it

# ===================== DIALOGUES =========================
shopkeep_dialogue = {
        'WELCOME': 'Welcome to my shop. Look at my wares and please buy some.',
        'LEAVE': 'Bye adventurer! Please come again!',
        'GREET': 'What was it, adventurer?',
        'DIALOGUE': [
                ['How are you?', 'I\'m fine'],
                ['What do you sell?', 'Just a sword and a potion.'],
                ['Did you hear any gossips lately?', 'Ur mom.']
                     ]
                     }

tavernkeep_dialogue = {
        'WELCOME': 'Welcome to this small tavern. '
                   'You can order food or you can sleep here. '
                   'For a small fee of course.',
        'LEAVE': 'Farewell!',
        'GREET': 'What would you like to know?',
        'BED': 'You can sleep here for 5 gold pieces.',
        'DIALOGUE': [
                ['How many people are here?', 'Two, lol.'],
                ['What do you sell?', 'Healing potions.'],
                ['Is this just a testing dialogue?', 'I don\'t know. Is it?']
                     ]
                       }

npc_01_dia = {
        'Q_GREET': 'Hello stranger. Can you do something for me?',
        'Q_ONGOING': 'Have you bring me my item?',
        'Q_PROMPT': ['What is it?', 'Help yourself.'],
        'Q_REFUSED': 'go fuck yourself then',
        'Q_ACCEPTED': 'That\'s great. Thank you!',
        'Q_COMPLETED': 'Oh thank you so much, here\'s your reward.',
        'GREET': 'Yes?',
        'DIALOGUE': [
            ['Good day.', 'Good day to you, young man.'],
            ['I want a quest', 'Okay, here it is.']
                    ]
               }

npc_02_dia = {
        'Q_GREET': 'Hello buddy, got a minute?',
        'Q_ONGOING': 'Did you kill them all?',
        'Q_PROMPT': ['What do you need young man?',
                     'Don\'t have time for this.'],
        'Q_REFUSED': 'Fuck off then.',
        'Q_ACCEPTED': 'Awesome!',
        'Q_COMPLETED': 'You\'re a baddas. Here\'s your reward.',
        'GREET': 'Hello.',
        'DIALOGUE': [
            ['How is it going?', 'good good'],
            ['Any gossips', 'Nope']
                     ]
              }
# ======================= NPC ==============================


class NPC:
    def __init__(self, xname, name, dialogue=None, quest=None, met=False):
        self.xname = xname
        self.name = name
        self.dialogue = dialogue
        self.quest = quest
        self.met = met

    @property
    def name(self):
        if self.met is True:
            return(self.xname)
        return(self._name)

    @name.setter
    def name(self, val):
        self._name = val


class Merchant(NPC):
    def __init__(
            self, xname, name, dialogue=None,
            quest=None, met=False, bed_price=0):
        super().__init__(xname, name, dialogue, quest, met)
        self.inventory = [
            [it.dagger, 1], [it.short_sword, 0], [it.long_sword, 0],
            [it.two_handed_sword, 0], [it.axe, 0], [it.battleaxe, 0],
            [it.spear, 0], [it.healing_potion, 0], [it.mana_potion, 0],
            [it.rejuvenation_potion, 0], [it.speed_potion, 0],
            [it.ironskin_potion, 0], [it.strength_potion, 0],
            [it.clothes, 0], [it.leather_armor, 1],
            [it.studded_leather_armor, 0],
            [it.chain_mail_armor, 0], [it.plate_armor, 0],
            [it.mage_robe, 0], [it.master_robe, 0], [it.bread, 1],
            [it.water, 1], [it.raw_meat, 0],
            [it.cooked_meat, 0], [it.potato, 0], [it.cooked_potato, 0],
            [it.carrot, 0], [it.rotten_meat, 0], [it.wine, 0], [it.beer, 0],
            [it.apple, 0], [it.full_meal, 0], [it.picklock, 0]
                            ]

    def npc_add_item(self, item, amount):
        for i in self.inventory:
            if i[0] == item:
                i[1] += amount

    def npc_remove_item(self, item):
        for i in self.inventory:
            if i[0] == item:
                i[1] -= 1


shopkeep = Merchant('Steve', 'Shopkeep', dialogue=shopkeep_dialogue)
shopkeep.npc_add_item(it.dagger, 1)
shopkeep.npc_add_item(it.short_sword, 1)
shopkeep.npc_add_item(it.leather_armor, 1)
shopkeep.npc_add_item(it.studded_leather_armor, 1)
shopkeep.npc_add_item(it.healing_potion, 3)
shopkeep.npc_add_item(it.mana_potion, 3)
shopkeep.npc_add_item(it.strength_potion, 3)
shopkeep.npc_add_item(it.full_meal, 3)

tavernkeep = Merchant('Karl', 'Tavernkeeper',
                      dialogue=tavernkeep_dialogue, bed_price=5)
tavernkeep.npc_add_item(it.healing_potion, 3)
tavernkeep.npc_add_item(it.bread, 2)
npc_01 = NPC('Mary', 'Old lady', dialogue=npc_01_dia, quest=it.first_quest)
npc_02 = NPC('Jim', 'small boy', dialogue=npc_02_dia, quest=it.second_quest)
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
