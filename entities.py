import random
from items import *

# ===================== DIALOGUES =========================
shopkeep_dialogue = {
        'WELCOME' : 'Welcome to my shop. Look at my wares and please buy some.', 
        'LEAVE' : 'Bye adventurer! Please come again!', 
        'DIALOGUE' : [
                ['How are you?', 'I\'m fine'], 
                ['What do you sell?', 'Just a sword and a potion.'],
                ['Did you hear any gossips lately?', 'Ur mom.']
]
}

# ======================= NPC ==============================

class NPC:
    def  __init__(self, name, dialogue = None):
        self.name = name
        self.weapons_inventory = [[dagger, 0], [short_sword, 0], [long_sword, 0], [two_handed_sword, 0], [axe, 0], [battleaxe, 0],
        [spear, 0]]
        self.potions_inventory = [[healing_potion, 0], [mana_potion, 0], [rejuvenation_potion, 0], [speed_potion, 0], [ironskin_potion, 0],
        [strength_potion, 0]]
        self.armors_inventory = [[clothes, 0], [leather_armor, 0], [studded_leather_armor, 0], [chain_mail_armor, 0], [plate_armor, 0],
        [mage_robe, 0], [master_robe, 0]]
        self.dialogue = dialogue

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

shopkeep = NPC('Shopkeep', dialogue = shopkeep_dialogue)

shopkeep.npc_add_item(dagger, 1)
shopkeep.npc_add_item(short_sword, 1)
shopkeep.npc_add_item(leather_armor, 1)
shopkeep.npc_add_item(studded_leather_armor, 1)
shopkeep.npc_add_item(healing_potion, 3)
shopkeep.npc_add_item(mana_potion, 3)
shopkeep.npc_add_item(strength_potion, 3)
# ===================== ENEMIES ==============================

class Goblin:
    def __init__(self):
        self.name = 'Goblin'
        self.max_hp = random.randint(5, 7)
        self.hp = self.max_hp
        self.attack = random.randint(3, 5)
        self.defence = random.randint(2, 4)
        self.speed = random.randint(4, 5)
        self.gold = random.randint(0, 5)
