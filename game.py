import os
import sys
import cmd
import random
import dill
import textwrap
from worldmap import gamemap
from items import *

# custom window size 
os.system('mode con: cols=100 lines=50')
width = 99
length = os.get_terminal_size().lines

# ==========================================================================================================================
# ================================================== CHARACTER CLASS =======================================================
class Player:
    def __init__(self):
        self.name = ''
        self.job = ''
        self.max_hp = 0
        self.hp = 0
        self.max_mp = 0
        self.mp = 0
        self.attack = 0
        self.defence = 0
        self.speed = 10
        self.max_energy = 100
        self.energy = 100
        self.knows_magic = False
        self.spells = []
        self.searching = 0
        self.opening_locks = 0
        self.disarming_traps = 0
        self.successfull_searches = 0
        self.successfull_traps = 0
        self.area = 'City'
        self.position = 'a1'
        self.previous_position = None
        self.gold = 100
        self.weapons_inventory = [[dagger, 1], [short_sword, 0], [long_sword, 0], [two_handed_sword, 0], [axe, 0], [battleaxe, 0],
        [spear, 0]]
        self.potions_inventory = [[healing_potion, 0], [mana_potion, 0], [rejuvenation_potion, 0], [speed_potion, 0], [ironskin_potion, 0],
        [strength_potion, 0]]
        self.armors_inventory = [[clothes, 0], [leather_armor, 0], [studded_leather_armor, 0], [chain_mail_armor, 0], [plate_armor, 0],
        [mage_robe, 0], [master_robe, 0]]
        self.consumables_inventory = [[bread, 1], [water, 1], [raw_meat, 0], [cooked_meat, 0], [potato, 0], [cooked_potato, 0], [carrot, 0],
        [rotten_meat, 0], [wine, 0], [beer, 0], [apple, 0], [full_meal, 0]]
        self.equipped_weapon = None
        self.equipped_armor = None
        self.level = 1
        self.xp = 0
        self.next_level = 50
        self.quests = []
        self.kill_count = [['Giant Rat', 0],['Goblin', 0],['Skeleton', 0], ['Zombie', 0], ['Bandit greenhorn', 0]]
        self.day = 1


# ---------------------------------------------- leveling up --------------------------------------------------------------
    def exp(self, xp_amount, previous_screen):
        self.xp += xp_amount
        print("\n<You gained {} xp!>".format(str(xp_amount)))
        if self.xp >= self.next_level:
            self.next_level += 50 + (self.next_level // 10)
            self.level += 1
            print("\n<You leveled up to level {}!>".format(str(self.level)))
            self.level_up(previous_screen)                                      # If xp reached next level threshold, move to level_up() 
        input('\n<Continue (Press Enter)>')                                     # otherwise return to the previous screen argument passed 
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()                                                       # to this function.
    
    def level_up(self, previous_screen):
        a = random.randint(3,5)                                                 # Subject to change? Random value of HP and MP increase.
        if self.job == 'Warrior':                                               # Checking for character's job, warrior has HP increase,
            self.max_hp += a                                                    # mage has MP increase. Mage alo checks through spells 
            print('\n<Your HP went up by {}!>'.format(str(a)))                  # whether level requirements was reached and if so, appends
        elif self.job == 'Mage':                                                # to the player's spells list.
            self.max_mp += a
            print('\n<Your MP went up by {}!>'.format(str(a)))
            for i in all_spells_list:
                if i.level_required == self.level:
                    self.spells.append(i)
                    print('\n<You have learned new spell: {}!>'.format(i.name))  
        self.hp = self.max_hp                                                   # Making sure that HP isn't higher than MAX HP (MP too)
        self.mp = self.max_mp
        b = random.randint(1, 5)
        self.max_energy += b
        print('\nYour energy went up')

        if self.job == 'Thief':
            if self.level % 2 == 0:
                self.searching += 1
                self.opening_locks += 1
                self.disarming_traps += 1
                print('\n<Your skills improved!>')
        elif self.job == 'Warrior' or 'Mage':
            if self.level % 3 == 0:
                self.searching += 1
                self.opening_locks += 1
                self.disarming_traps += 1
                print('\n<Your skills improved!>')
        if self.level % 5 == 0:
            self.stat_increase(previous_screen)
            
        input('\n<Continue (Press Enter)>')
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()                                                       # Returns to the previous screen before player leveled up

    def stat_increase(self, previous_screen):                                   # Subject to change? Every 3rd level choose an attribute
        options = ['1', '2', '3']                                               # to increase.
        print('\n<You can choose an attribute to increase.>')
        print('\n[1] Attack\n[2] Defence\n[3] Speed')
        answer = input('> ')
        while answer not in options:
            self.stat_increase(previous_screen)
        if answer == '1':
            self.attack += 1
            print('\n<Your attack went up by 1!>')
        elif answer == '2':
            self.defence += 1
            print('\n<Your defence went up by 1!>')
        elif answer == '3':
            self.speed += 1
            print('\n<Your speed went up by 1!>')
        input('\n<Continue (Press Enter)>')
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()                                                       # Return to the previous screen before player leveled up

# ----------------------------------------------------------- stats --------------------------------------------------------------------
    def display_stats(self):                                                    # Displays player's stats
        os.system('cls')
        print(self.name.center(width))
        print('Day: {}'.format(str(self.day)).center(width))
        print('')
        print('{} Level: {}, XP: {}, Next Level: {}'.format(self.job, str(self.level), str(self.xp), str(self.next_level - self.xp)).center(width))
        print('')
        print('{}HP: {}/{}'.format((' ' * 45), self.hp, self.max_hp))
        print('{}MP: {}/{}'.format((' ' * 45), self.mp, self.max_mp))
        print('\n{}Energy: {}/{}'.format((' ' * 45), self.energy, self.max_energy))
        print('\n{}Attack: {}'.format((' ' * 45), self.attack))
        print('{}Defence: {}'.format((' ' * 45), self.defence))
        print('{}Speed: {}'.format((' ' * 45), self.speed))
        print('')
        print('Skills'.center(width))
        print('--------'.center(width))
        print('Searching: {} %'.format(str(self.searching)).center(width))
        print('Opening Locks: {} %'.format(str(self.opening_locks)).center(width))
        print('Disarming Traps: {} %'.format(str(self.disarming_traps)).center(width))
        input('\n<Continue (Press Enter)>')
        print_location()

# ------------------------------------------------------ inventory ---------------------------------------------------------------
    def display_inventory(self):
        os.system('cls')
        print('Equipped Weapon: {}'.format(self.equipped_weapon))
        print('Equipped Armor: {}'.format(self.equipped_armor))
        print('')
        print('Gold: {}'.format(self.gold))
        print('')

        print('{:-^99}'.format(' Weapons '))
        for item in self.weapons_inventory:
            if item[1] > 0:
                c = ' ' * (30 - len(item[0].name))
                print('[{}] {}{}x{}     DMG: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].damage), str(item[0].speed), str(item[0].value)))
        
        print('\n' + '{:-^99}'.format(' Potions '))
        for item in self.potions_inventory:
            if item[1] > 0:
                c = ' ' * (30 - len(item[0].name))
                print('[{}] {}{}x{}                      Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].value)))
        
        print('\n' + '{:-^99}'.format(' Armors '))
        for item in self.armors_inventory:
            if item[1] > 0:
                c = ' ' * (30 - len(item[0].name))
                print('[{}] {}{}x{}     DEF: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].defence_bonus), str(item[0].speed), str(item[0].value)))
        
        print('\n' + '{:-^99}'.format(' Consumables ')) 
        for item in self.consumables_inventory:
            if item[1] > 0:
                c = ' ' * (30 - len(item[0].name))
                print('[{}] {}{}x{}     Energy: {} HP: {} MP:{} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].energy_up), str(item[0].hp_up) or '-', str(item[0].mp_up) or '-', str(item[0].value)))

        self.inventory_prompt()                                                     # ^ Displays inventory and prompts the player


    def inventory_prompt(self):
        options = ['1', '2', '3', '4', '5']
        print('\n[1] Use\n[2] Toss\n[3] Equip\n[4] De-equip\n[5] Leave\n')          # De-equip or unequip, fuck I don't know
        
        answer = input('> ')
        while answer not in options:
            self.display_inventory()
        if answer == '1':                                                           # Accessing various inventory functions
            self.inventory_use()
        elif answer == '2':
            self.inventory_toss()
        elif answer == '3':
            self.inventory_equip()
        elif answer == '4':
            if self.equipped_armor == None and self.equipped_weapon == None:        # Checks whether player has anything equipped at all
                print('\n<Nothing is equipped!>')                                   # before even sending to the Equip screen.
                input('\n<Continue (Press Enter)>')
                self.display_inventory()
            else:
                self.inventory_deequip()                                            # If something's equipped, deequip prompt appears
        elif answer == '5':                                                         # Leaves back to the game
            print_location()

    def inventory_use(self):
        print('\n<Use what?> (type \'back\' to return)\n')
        options = [item[0].shortcut for item in self.potions_inventory if item[1] > 0] + ['back'] + [item[0].shortcut for item in self.consumables_inventory if item[1] > 0]
        
        answer = input('> ').lower()
        while answer not in options:
            self.inventory_use()
        if answer == 'back':
            self.display_inventory()
        for item in self.potions_inventory:
            if answer == item[0].shortcut:
                Potion.use_potion(item[0], self)
                item[1] -= 1
        for item in self.consumables_inventory:
            if answer == item[0].shortcut:
                Consumable.use_consumable(item[0], self)
                item[1] -= 1

        input('\n<Continue (Press Enter)>')
        self.inventory_use()

    def inventory_toss(self):
        print('\n<Toss what?> (type \'back\' to return)')
        a = [item[0].shortcut for item in self.weapons_inventory if item[1] > 0]         # My stupid way of making options list, probably don't 
        b = [item[0].shortcut for item in self.potions_inventory if item[1] > 0]         # know how to handle lists or I just chose a stupid
        c = [item[0].shortcut for item in self.armors_inventory if item[1] > 0]          # inventory handling.
        d = [item[0].shortcut for item in self.consumables_inventory if item[1] > 0]
        options = a + b + c + d + ['back']
        
        answer = input('> ').lower()
        while answer not in options:
            self.inventory_toss()
        if answer == 'back':
            self.display_inventory()

        for item in self.weapons_inventory:
            if answer == item[0].shortcut:
                item[1] -= 1
                print('\nYou tossed {} away!'.format(item[0].name))

        for item in self.potions_inventory:
            if answer == item[0].shortcut:
                item[1] -= 1
                print('\nYou tossed {} away!'.format(item[0].name))
              
        for item in self.armors_inventory:
            if answer == item[0].shortcut:
                item[1] -= 1
                print('\nYou tossed {} away!'.format(item[0].name))

        for item in self.consumables_inventory:
            if answer == item[0].shortcut:
                item[1] -= 1
                print('\nYou tossed {} away!'.format(item[0].name))

        input('\n<Continue (Press Enter)>')
        self.display_inventory()
   

    def inventory_equip(self):
        print('\n<Equip what?> (type \'back\' to return)')
        back = ['back']
        a = [item[0].shortcut for item in self.weapons_inventory if item[1] > 0]
        b = [item[0].shortcut for item in self.armors_inventory if item[1] > 0]
        options = a + b + back
        
        answer = input('> ').lower()
        while answer not in options:
            self.inventory_equip()
        if answer == 'back':
            self.display_inventory()
        
        if answer in a:
            if self.equipped_weapon != None:                                        # If player already hold an equipped weapon, it will
                print('\nYou de-equipped {}'.format(self.equipped_weapon.name))     # first unequip it before equiping the new one.
                self.attack -= self.equipped_weapon.damage
                self.speed -= self.equipped_weapon.speed                            # Equipped weapon's effects removed from the player
                for item in self.weapons_inventory:
                    if item[0].name == self.equipped_weapon.name:                      # Adds the weapon to the inventory after removing
                        item[1] += 1                                                   # from hand.
                self.equipped_weapon = None
            for item in self.weapons_inventory:
                if answer == item[0].shortcut:                                     # Equips new weapon, adds its effects to the player
                    self.equipped_weapon = item[0]                                     # and removes from the inventory.
                    item[1] -= 1
                    self.attack += item[0].damage
                    self.speed += item[0].speed
                    print('\nYou equipped {}'.format(item[0].name))
                    input('\n<Continue (Press Enter)>')
                    self.display_inventory()
        
        elif answer in b:
            if self.equipped_armor != None:
                print('\nYou de-equipped {}'.format(self.equipped_armor.name))
                self.defence -= self.equipped_armor.defence_bonus
                self.speed -= self.equipped_armor.speed
                self.max_mp -= self.equipped_armor.mana_bonus
                if self.mp > self.max_mp:
                    self.mp = self.max_mp
                for item in self.armors_inventory:
                    if item[0].name == self.equipped_armor.name:
                        item[1] += 1
                self.equipped_armor = None
            for item in self.armors_inventory:
                if answer == item[0].shortcut:
                    self.equipped_armor = item[0]
                    item[1] -= 1
                    self.defence += item[0].defence_bonus
                    self.speed += item[0].speed
                    self.max_mp += item[0].mana_bonus
                    print('\nYou are now wearing {}'.format(self.equipped_armor.name))
                    input('\n<Continue (Press Enter)>')
                    self.display_inventory()

    def inventory_deequip(self):
        print('<De-equip what?> (type \'back\' to return)')
        if self.equipped_weapon == None:                                                # The way I handled the 'None has no .name attribute
            weapon = None                                                                    # bug'. Probably temporary, but it works.
        else:
            weapon = self.equipped_weapon.shortcut
        if self.equipped_armor == None:
            armor = None
        else:
            armor = self.equipped_armor.shortcut
        options = ['back', weapon, armor]
        answer = input('> ').lower()
        
        while answer not in options:
            self.inventory_deequip()
        if answer == 'back':
            self.display_inventory()
        
        for item in self.weapons_inventory:
            if answer == item[0].shortcut:
                item[1] += 1
                print('\n<You de-equipped {}.>'.format(self.equipped_weapon.name))
                self.attack -= self.equipped_weapon.damage
                self.speed -= self.equipped_weapon.speed
                self.equipped_weapon = None
        
        for item in self.armors_inventory:
            if answer == item[0].shortcut:
                item[1] += 1
                print('\n<You\'re no longer wearing {}.>'.format(self.equipped_armor.name))
                self.defence -= self.equipped_armor.defence_bonus
                self.speed -= self.equipped_armor.speed
                self.max_mp -= self.equipped_armor.mana_bonus
                if self.mp > self.max_mp:
                    self.mp = self.max_mp
                self.equipped_armor = None
        
        input('\n<Continue (Press Enter)>')
        self.display_inventory()

 # ----------------------------------------------------- magic ----------------------------------------------------------------   
    def display_magic(self):
        os.system('cls')
        print('HP: {}\{}     MP: {}\{}'.format(self.max_hp, self.hp, self.max_mp, self.mp).center(width))
        print('{:-^99}'.format(' Spells '))
        for spell in self.spells:
            txt_frmt_1 = ' ' * (15 - len(spell.name))                                                # Variables to handle alignements.
            txt_frmt_2 = ' ' * (60 - len(spell.description))
            print('{}{}{}{}Cost: {} MP'.format(spell.name, txt_frmt_1, spell.description, txt_frmt_2, spell.mp_cost))
        
        print('\n' * 2)
        print('\n[1] Use Spell\n[2] Back')
        options = ['1', '2']
        answer = input('> ')
        while answer not in options:
            self.display_magic()
        if answer == '2':
            print_location()
        elif answer == '1':
            self.use_spell()
    
    def use_spell(self):
        options = [spell.shortcut for spell in self.spells if isinstance(spell, HealingSpell)] + ['back']
        print('\n<Use what? (type \'back\' to return)>\n')
        for spell in self.spells:
            if isinstance(spell, HealingSpell):
                print('[{}] {}'.format(spell.shortcut, spell.name))

        answer = input('\n> ').lower()
        while answer not in options:
            self.use_spell()
        if answer == 'back':
            self.display_magic()
        for spell in self.spells:
            if answer == spell.shortcut:
                if self.mp < spell.mp_cost:
                    print('\n<You don\'t have enough mana!>')
                    self.use_spell()
                spell.use_spell(myplayer)

        input('\n<Continue (Press Enter)>')
        self.display_magic()


# -------------------------------------------------------------- journal --------------------------------------------------------
    def journal(self):
        os.system('cls')
        if self.quests:
            for quest in self.quests:
                if quest.steps['FIRST'] == True:
                    print(quest.name)
                    print('From: {}'.format(quest.owner) + '\n')
                    print(quest.message['FIRST'])
                    print('\n' + '-' * 99)
                elif quest.steps['SECOND'] == True:
                    print(quest.name)
                    print('From: {}'.format(quest.owner) + '\n')
                    print(quest.message['FIRST'] + '\n')
                    print(quest.message['SECOND'])
                    print('\n' + '-' * 99)               
        else:
            print('You have no active quest at this moment!'.center(width))
        input('\n' + '<Continue (Press Enter)>'.center(width))
        print_location()



# --------------------------------------------------------- Death Screen --------------------------------------------------------------
def death_screen():
    os.system('cls')
    print('Youd DIED!'.center(width) + '\n')
    input('OK'.center(width))
    title_screen()


myplayer = Player()  # character created with no stats or name, those values will be passed in the object during the character creation

# =====================================================================================================================================
# ======================================================== GAME FUNCTIONALITY =========================================================

# ---------------------------------------------------- main menu, save, load, help ----------------------------------------------------
def title_screen():
    os.system('cls')
    print('\n' * 10)
    print('=========================================='.center(width))                   # Main menu, possibly some cool ASCII image
    print('==  Welcome to a Python Text Based RPG  =='.center(width))                   # when actual game title is made.
    print('==                                      =='.center(width))
    print('==      This is a learning project.     =='.center(width))
    print('==                                      =='.center(width))
    print('==       2018 Martin "Coop" Cupak       =='.center(width))
    print('=========================================='.center(width))
    print('')
    print('[1] Start Game'.center(width) + '\n')
    print('[2] Load Game'.center(width) + '\n')
    print('[3] Instructions'.center(width) + '\n')
    print('[4] Quit Game'.center(width) + '\n')
    
    options = ['1', '2', '3', '4']
    answer = input('\n> ')
    while answer not in options:
        title_screen()
    if answer == '1':
        character_creation()
    elif answer == '2':
        load_game()
    elif answer == '3':
        instructions()
    elif answer == '4':
        sys.exit()

def save_game():
    dill.dump_session('savefile.pkl')                                                   # Using dill library for state saving. Creates 
    print('\nGame has been saved!')                                                     # .pkl file with save state.
    input('<Continue (Press Enter)>')
    print_location()

def load_game():
    if os.path.exists('savefile.pkl') == True:                                          # Checks whether .pkl file exists.
        dill.load_session('savefile.pkl')
        print('Game succesfully loaded!')
        input('<Continue (Press Enter)>')
        print_location()
    else:
        os.system('cls')
        print("There\'s no saved game to load!")
        input('<Return (Press Enter)>')
        title_screen()

def instructions():
    print(textwrap.fill('Welcome to my small text-based RPG made with Python, passion and patience. It is a learning project, that I started working on in April 2018. I was a beginner programmer, when I started working on this game and the code clearly reflects that. I would appreaciate any advice you can have to improve my coding skills. Please visit github.com/Cupesh/Text-RPG to review my code. How to play the game? Most of the time the player can choose what to do, by typing the corresponding letter to the action prompted on the screen, shown in brackets, like this: \"[p] Play\". Where typing \"p\" and pressing Enter will select the Play option. Only in a few scenarios, like buying or selling items, is player prompted to type out the whole name. In that case, type the whole name of the item. Everything player enters in the console is case insensitive, so capitalizing doesn\'t matter. Game uses only very basic RPG elements. Leveling up, experience points and a few stats. Attack, Defence, Speed. Attack and Defence is self-explanatory. Can be increased by buying weapons and armor. Speed is an attribute, that determines, who will attack first in the battle. Starting at value 10 and decreasing with equipping weapons and armor. Player also have a fatigue value, that decrease as player travels or fight or uses magic. It can be replenished eating food and sleeping in the inn or wilderness. Enjoy the game!', width = 99))
    input('Back (Press Enter)')
    title_screen()


# ---------------------------------------------------- starting the game, character creation ------------------------------------------
def character_creation():
    os.system('cls')                                                                    # clears the screen
    print('\n' * 24)                                                                    # Don't know how to center vertically.
    print('What is your name?'.center(width) + '\n')
    playername = input('> ')
    if len(playername) < 1:                                                             # Making sure player entered something.
        print('<You need to enter a name.>')
        input('\n<Continue (Press Enter)>')
        character_creation()
    myplayer.name = playername                                                          # passes name into player object
    
    os.system('cls')
    print('\n' * 24)
    options = ['1', '2', '3']
    print('What is your job?'.center(width) + '\n')
    print('[1] Warrior'.center(width))
    print('[2] Mage'.center(96))
    print('[3] Thief'.center(98))
    answer = input('> ')
    while answer not in options:
        character_creation()
    if answer == '1':                                                                   # Job values are a subject to change.
        myplayer.job = 'Warrior'
        myplayer.max_hp = 20
        myplayer.hp = 20
        myplayer.max_mp = 0
        myplayer.mp = 0
        myplayer.attack += 1
        myplayer.defence += 1
        game_introduction()

    elif answer == '2':
        myplayer.job = 'Mage'
        myplayer.max_hp = 15
        myplayer.hp = 15
        myplayer.max_mp = 10
        myplayer.mp = 10
        myplayer.knows_magic = True
        myplayer.speed = 7
        myplayer.spells.append(minor_healing)
        myplayer.spells.append(fireball)
        game_introduction()

    elif answer == '3':
        myplayer.job = 'Thief'
        myplayer.max_hp = 17
        myplayer.hp = 17
        myplayer.max_mp = 0
        myplayer.mp = 0
        myplayer.knows_magic = False
        myplayer.speed = 11
        myplayer.searching = 7
        myplayer.opening_locks = 5
        myplayer.disarming_traps = 3
        game_introduction()

def game_introduction():                                                                 # Welcoming screen
    os.system('cls')
    print('\n' * 24)
    print('Wecome, {} the {}!'.format(myplayer.name, myplayer.job).center(width))
    print('This is a small game, a Python learning project. Hope you\'ll enjoy!'.center(width))
    print('')
    input('<Continue (Press Enter)>'.center(width))
    print_location()


# ------------------------------------------------------ main game window  ------------------------------------------------------------
def print_location():
    if myplayer.energy < 1:
        death_screen()
    if myplayer.hp < 1:
        death_screen()
    os.system('cls')
    print(('-' * 40).center(width))
    print('HP: {}/{} MP: {}/{}'.format(myplayer.hp, myplayer.max_hp, myplayer.mp, myplayer.max_mp).center(width))
    print('Level: {} XP: {} Next Level: {}'.format(myplayer.level, myplayer.xp, (myplayer.next_level - myplayer.xp)).center(width))
    print(' ' * 35 + 'Energy: {}/{}'.format(myplayer.energy, myplayer.max_energy) + (' ' * 6) + 'Day: {}'.format(str(myplayer.day)))
    print(('-' * 40).center(width))
    print(' ')
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))      # Checks player location, position and from worldmap.py
    print('')
    if gamemap[myplayer.area][myplayer.position]['VISITED']:                             # Checks whether player already visited this location
        print(gamemap[myplayer.area][myplayer.position]['VISITED_DESCRIPTION'])          # before, for a different message to display.
        print('')
        print('=' * 99)
        prompt()
    else:
        print(gamemap[myplayer.area][myplayer.position]['DESCRIPTION'])                 # Prints out first-time-visit message and then 
        print('')
        print('=' * 99)
        if 'ENEMY' in gamemap[myplayer.area][myplayer.position]:                        # checks whether location has an enemy present.
            input('\n<Continue>')
            battle_start()
        else:
            prompt()

# ======================================================================================================================================
# ======================================================== GAME INTERACTIVITY ==========================================================

# -------------------------------------------------------- main prompt window ----------------------------------------------------------
def prompt():
    print('')                                                                           # Main prompt window.
    menu = ['gGo']
    end_menu = ['jJournal', 'pPlayer', 'iInventory', 'sSave', 'qQuit']
    options = ['g', 'q', 'i', 's', 'p', 'j']
    if myplayer.job == 'Mage':
        options.append('m')
        end_menu.insert(0, 'mMagic')
    if 'NPC' in gamemap[myplayer.area][myplayer.position]:
        options.append('c')
        menu.append('cTalk')
    if 'SHOP' in gamemap[myplayer.area][myplayer.position]:
        options.append('t')
        menu.append('tShop')
    if 'TAVERN' in gamemap[myplayer.area][myplayer.position]:
        options.append('b')
        menu.append('bTavern')
    if 'SEARCH' in gamemap[myplayer.area][myplayer.position]:
        options.append('x')
        menu.append('xSearch')
    for i in menu:
        print('[{}] {}'.format(i[0].lower(), i[1:]))
    for i in end_menu:
        print('[{}] {}'.format(i[0].lower(), i[1:]))
    
    answer = input('\n> ').lower()
    while answer not in options:
        print_location()
    if answer == 'g':
        player_movement()
    elif answer == 'q':
        sys.exit()
    elif answer == 't':
        shop()
    elif answer == 'i':
        myplayer.display_inventory()
    elif answer == 's':
        save_game()
    elif answer == 'p':
        myplayer.display_stats()
    elif answer == 'm':
        myplayer.display_magic()
    elif answer == 'c':
        chat(print_location)
    elif answer == 'j':
        myplayer.journal()
    elif answer == 'b':
        tavern()
    elif answer == 'x':
        search(gamemap[myplayer.area][myplayer.position]['SEARCH'])

# ----------------------------------------------------------- movement ------------------------------------------------------------------
def player_movement():
    print('')
    options = []
    directions = {}                                                                             # will change to n,s,e,w probably
    if gamemap[myplayer.area][myplayer.position]['UP'] == True:
        options.append('n')
        a = gamemap[myplayer.area][myplayer.position]['AREA']
        directions['North'] = '(Travel to {})'.format(a)
    elif gamemap[myplayer.area][myplayer.position]['UP']:
        options.append('n')
        a = gamemap[myplayer.area][myplayer.position]['UP']
        if gamemap[myplayer.area][a]['VISITED'] == True:
            directions['North'] = '({})'.format(gamemap[myplayer.area][a]['GRIDNAME'])
        else:
            directions['North'] = ''

    if gamemap[myplayer.area][myplayer.position]['LEFT'] == True:
        options.append('w')
        a = gamemap[myplayer.area][myplayer.position]['AREA']
        directions['West'] = '(Travel to {})'.format(a)
    elif gamemap[myplayer.area][myplayer.position]['LEFT']:
        options.append('w')
        a = gamemap[myplayer.area][myplayer.position]['LEFT']
        if gamemap[myplayer.area][a]['VISITED'] == True:
            directions['West'] = '({})'.format(gamemap[myplayer.area][a]['GRIDNAME'])
        else:
            directions['West'] = ''
    if gamemap[myplayer.area][myplayer.position]['DOWN'] == True:
        options.append('s')
        a = gamemap[myplayer.area][myplayer.position]['AREA']
        directions['South'] = '(Travel to {})'.format(a)
    elif gamemap[myplayer.area][myplayer.position]['DOWN']:
        options.append('s')
        a = gamemap[myplayer.area][myplayer.position]['DOWN']
        if gamemap[myplayer.area][a]['VISITED'] == True:
            directions['South'] = '({})'.format(gamemap[myplayer.area][a]['GRIDNAME'])
        else:
            directions['South'] = ''
    if gamemap[myplayer.area][myplayer.position]['RIGHT'] == True:
        options.append('e')
        a = gamemap[myplayer.area][myplayer.position]['AREA']
        directions['East'] = '(Travel to {})'.format(a)
    elif gamemap[myplayer.area][myplayer.position]['RIGHT']:
        options.append('e')
        a = gamemap[myplayer.area][myplayer.position]['RIGHT']
        if gamemap[myplayer.area][a]['VISITED'] == True:
            directions['East'] = '({})'.format(gamemap[myplayer.area][a]['GRIDNAME'])
        else:
            directions['East'] = ''

    for key, value in directions.items():
        print(('[{}] {} {}').format(key[0].lower(), key, value))

    answer = input('\n> ').lower()

    while answer not in options:
        player_movement()

    if answer == 'n':                                                        # Checks for direction, whether player can
        if gamemap[myplayer.area][myplayer.position]['UP'] == True:                         # travel from current grid to a chosen direction.
            area = gamemap[myplayer.area][myplayer.position]['AREA']                        # None will tell player that there's nothing
            destination = gamemap[myplayer.area][myplayer.position]['GRID']                 # there. 'True' means that chosen direction
            travel_handler(area, destination)                                               # is a travel direction.
        elif gamemap[myplayer.area][myplayer.position]['UP']:                               # String means it's just moving into a different
            destination = gamemap[myplayer.area][myplayer.position]['UP']                   # grid but in the same area.
            movement_handler(destination)

    elif answer == 's':
        if gamemap[myplayer.area][myplayer.position]['DOWN'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['DOWN']:
            destination = gamemap[myplayer.area][myplayer.position]['DOWN']
            movement_handler(destination)

    elif answer == 'w':
        if gamemap[myplayer.area][myplayer.position]['LEFT'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['LEFT']:
            destination = gamemap[myplayer.area][myplayer.position]['LEFT']
            movement_handler(destination)

    elif answer == 'e':
        if gamemap[myplayer.area][myplayer.position]['RIGHT'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['RIGHT']:
            destination = gamemap[myplayer.area][myplayer.position]['RIGHT']
            movement_handler(destination)

def movement_handler(destination):                                                      # Marks the previsous grid as visisted and moves
    gamemap[myplayer.area][myplayer.position]['VISITED'] = True                          # to a new grid.
    myplayer.previous_position = myplayer.position
    myplayer.position = destination
    myplayer.energy -= 1
    print_location()

def travel_handler(area, destination):
    print('\n<You have traveled to the {}.>'.format(gamemap[area]['NAME']).center(width))
    input('\n<Continue (Press Enter)>'.center(width))
    gamemap[myplayer.area][myplayer.position]['VISITED'] = True                          # Marks the previous grid as visited and moves to
    myplayer.area = area                                                                # a new area and its starting grid.
    myplayer.position = destination
    myplayer.energy -= 10
    print_location()


# ------------------------------------------------------------------- Battling -------------------------------------------------------------
def battle_start():
    enemy = gamemap[myplayer.area][myplayer.position]['ENEMY']
    if myplayer.speed > enemy.speed:
        battle_player_turn(enemy)
    else:
        battle_enemy_turn(enemy)

def battle_player_turn(enemy):
    os.system('cls')
    print(('#' * 14).center(width))
    print('#####    #####'.center(width))
    print('##  BATTLE  ##'.center(width))
    print('#####    #####'.center(width))
    print(('#' * 14).center(width))
    print('#' * 99 + '\n')
    print('{:=^99}'.format('Player\'s turn'))
    print('')
    print(myplayer.name.center(width))
    print('HP: {}/{}'.format(myplayer.hp, myplayer.max_hp).center(width))
    print('MP: {}/{}'.format(myplayer.mp, myplayer.max_mp).center(width))
    print('-' * 99)
    print(enemy.name.center(width).center(width))
    print('HP: {}/{}'.format(enemy.hp, enemy.max_hp).center(width))
    print('-' * 99)
    print('\n')

    attack = myplayer.attack + random.randint(1, 4)
    defence = enemy.defence + random.randint(1, 4)

    options = ['1', '2', '3', '4']
    print('[1] Attack\n[2] Magic\n[3] Items\n[4] Run\n')
    answer = input('> ')
    while answer not in options:
        battle_player_turn(enemy)
    if answer == '4':
        myplayer.position = myplayer.previous_position
        damage = random.randint(1, 4)
        myplayer.hp -= damage
        print('\n<{} striked you as you were running away and dealt {} damage!>'.format(enemy.name, str(damage)))
        input('\n(Continue)')
        print_location()
    elif answer == '3':
        battle_item_use(enemy)
    elif answer == '2':
        battle_cast_spell_prompt(enemy)
    elif answer == '1':
        damage = attack - defence
        if damage < 0:
            damage = 0
        enemy.hp -= damage
        print('\n<You attacked {} and dealt {} damage!>'.format(enemy.name, str(damage)))
        if enemy.hp < 1:
            print('<{} died!>'.format(enemy.name))
            input('\n(Continue)')
            battle_win(enemy)
        input('\n(Continue)')
        battle_enemy_turn(enemy)

def battle_enemy_turn(enemy):
    os.system('cls')
    print('{:=^99}'.format('Enemy\'s turn'))
    print('')
    print(myplayer.name.center(width))
    print('HP: {}/{}'.format(myplayer.hp, myplayer.max_hp).center(width))
    print('MP: {}/{}'.format(myplayer.mp, myplayer.max_mp).center(width))
    print('-' * 99)
    print(enemy.name.center(width).center(width))
    print('HP: {}/{}'.format(enemy.hp, enemy.max_hp).center(width))
    print('-' * 99)
    print('\n')

    attack = enemy.attack + random.randint(1, 4)
    defence = myplayer.defence + random.randint(1, 4)

    input('\n(Continue)')

    damage = attack - defence
    if damage < 0:
        damage = 0

    print('\n<{} attacked and dealt {} damage to you!>'.format(enemy.name, str(damage)).center(width))
    myplayer.hp -= damage
    if myplayer.hp <= 0:
        death_screen()
    else:
        input('\n(Continue)')
        battle_player_turn(enemy)

def battle_item_use(enemy):
    for item in myplayer.potions_inventory:
        if item[1] > 0:
            print('[{}] {} x {}'.format(item[0].shortcut, item[0].name, str(item[1])))
    for item in myplayer.consumables_inventory:
        if item[1] > 0:
            print('[{}] {} x {}'.format(item[0].shortcut, item[0].name, str(item[1])))
    print('')
    print('\n<Use what?> (type \'back\' to return)\n')
    
    options = [item[0].shortcut for item in myplayer.potions_inventory if item[1] > 0] + ['back'] + [item[0].shortcut for item in myplayer.consumables_inventory if item[1] > 0]
    answer = input('> ').lower()
    while answer not in options:
        battle_item_use(enemy)
    if answer == 'back':
        battle_player_turn(enemy)
    for item in myplayer.potions_inventory:
        if answer == item[0].shortcut:
            Potion.use_potion(item[0], myplayer)
            item[1] -= 1
            input('\n(Continue)')
            battle_enemy_turn(enemy)
    for item in myplayer.consumables_inventory:
        if answer == item[0].shortcut:
            Consumable.use_consumable(item[0], myplayer)
            item[1] -= 1
            input('\n(Continue)')
            battle_enemy_turn(enemy)



def battle_cast_spell_prompt(enemy):
    print('\n' * 2)
    print('{:-^99}'.format(' Spells '))
    for spell in myplayer.spells:
        a = ' ' * (15 - (len(spell.name) + len(spell.shortcut)))
        b = ' ' * (30 - len(spell.description))
        print('[{}] {} {} {} {} Cost: {}'.format(spell.shortcut, spell.name, a, spell.description, b, spell.mp_cost))
    print('\n' * 2)

    options = [spell.shortcut for spell in myplayer.spells] + ['back']
    answer = input('> ').lower()
    while answer not in options:
        battle_cast_spell_prompt(enemy)
    if answer == 'back':
        battle_player_turn(enemy)
    for spell in myplayer.spells:
        if answer == spell.shortcut:
            if myplayer.mp < spell.mp_cost:
                print('\n<You don\'t have enough mana!>')
                battle_cast_spell_prompt(enemy)
            elif isinstance(spell, HealingSpell):
                spell.use_spell(myplayer)
            elif isinstance(spell, DamageSpell):
                spell.use_spell(myplayer, enemy)
    
    if enemy.hp < 1:
        print('<{} died!>'.format(enemy.name))
        input('\n(Continue)')
        battle_win(enemy)
    
    input('\n<Continue>')
    battle_enemy_turn(enemy)



def battle_win(enemy):
    print('\n<You defeated {}!'.format(enemy.name))
    print('\n<You gained {} gold!>'.format(str(enemy.gold)))
    myplayer.gold += enemy.gold
    
    gamemap[myplayer.area][myplayer.position]['VISITED'] = True
    gamemap[myplayer.area][myplayer.position]['ENEMY'] = None
    
    myplayer.energy -= 7
    
    for mob in myplayer.kill_count:
        if mob[0] == enemy.name:
            mob[1] += 1
    
    input('\n(Continue)')
    myplayer.exp(enemy.xp, print_location)

# -------------------------------------------------------------------- shop ---------------------------------------------------------------
def shop():
    os.system('cls')
    myplayer.position = gamemap[myplayer.area][myplayer.position]['SHOP']               # allocates player's new position
    npc = gamemap[myplayer.area][myplayer.position]['OWNER']                              # Searches for the npc
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']) + '\n')
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    print(npc_name)
    print(npc.dialogue['WELCOME'].center(width))
    npc.met = True
    shop_prompt(npc)

def shop_prompt(npc):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    print('\n[1] Shop\n[2] Talk\n[3] Leave')
    options = ['1', '2', '3']
    answer = input('> ')
    while answer not in options:
        shop_prompt(npc)        
    if answer == '1':
        shop_window(npc, shop_prompt)
    elif answer == '2':
        dialogue(npc, shop_prompt)
    elif answer == '3':
        print(npc_name)
        print(npc.dialogue['LEAVE'].center(width) + '\n')                       #
        myplayer.position = gamemap[myplayer.area][myplayer.position]['LEAVE']          # Finds the leaving grid from the shop
        input('<Continue (Press Enter)>'.center(width))
        print_location()

def shop_window(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    os.system('cls')
    print(npc.name.upper().center(width))                                               # Npc's name in the center
    print('-' * 100)
    
    print('{:_^99}'.format(' Weapons '))
    print('')
    for item in npc.weapons_inventory:
        if item[1] > 0:
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     DMG: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].damage), str(item[0].speed), str(item[0].value)))

    print('')
    print('\n{:_^99}'.format(' Potions '))
    print('')
    for item in npc.potions_inventory:
        if item[1] > 0:
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}                      Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].value)))

    print('')
    print('\n{:_^99}'.format(' Armors '))
    print('')
    for item in npc.armors_inventory:
        if item[1] > 0:
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     DEF: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].defence_bonus), str(item[0].speed), str(item[0].value))) 
    print('')
    print('\n{:_^99}'.format(' Consumables '))
    print('')
    for item in npc.consumables_inventory:
        if item[1] > 0:
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     Energy: {} HP: {} MP:{} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].energy_up), str(item[0].hp_up) or '-', str(item[0].mp_up) or '-', str(item[0].value)))
    print('')
    print('-' * 100)
    
    print('\nYour gold: {}'.format(myplayer.gold))
    
    options = ['1', '2', '3']
    print('\n' + npc_name)
    print('Came to buy or sell?'.center(width))
    print('\n[1] Buy\n[2] Sell\n[3] Back')
    
    answer = input('\n> ')
    while answer not in options:
        shop_window(npc, previous_screen)
    if answer == '1':
        shop_buy(npc, previous_screen)
    elif answer == '2':
        shop_sell(npc, previous_screen)
    elif answer == '3':
        shop()

def shop_buy(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    print('\n<Buy what?> (type \'back\' to return)')
    
    a = [item[0].shortcut for item in npc.weapons_inventory if item[1] > 0]
    b = [item[0].shortcut for item in npc.potions_inventory if item[1] > 0]
    c = [item[0].shortcut for item in npc.armors_inventory if item[1] > 0]
    d = [item[0].shortcut for item in npc.consumables_inventory if item[1] > 0]
    options = a + b + c + d + ['back']
    
    answer = input('> ').lower()
    while answer not in options:
        print('\n' + npc_name)
        print('I don\'t have that.'.center(width))
        shop_buy(npc, previous_screen)
    if answer == 'back':
        shop_window(npc, previous_screen)
    
    for item in npc.weapons_inventory:
        if answer == item[0].shortcut:
            if myplayer.gold >= item[0].value:                                         # Checks if player has enough gold for the transaction
                print('\n<You bought {}!>'.format(item[0].name))
                myplayer.gold -= item[0].value                                         # Takes away the gold from the player
                item[1] -= 1                                                           # takes away the item from the npc
                for item in myplayer.weapons_inventory:                                # Adds the item to the player's inventory
                    if item[0].shortcut == answer:
                        item[1] += 1
            else:
                print('\n' + npc_name)
                print("You don\'t have enough gold!".center(width))
                shop_buy(npc, previous_screen)
    
    for item in npc.potions_inventory:
        if answer == item[0].shortcut:
            if myplayer.gold >= item[0].value:
                print('\n<You bought {}!>'.format(item[0].name))
                myplayer.gold -= item[0].value
                item[1] -= 1
                for item in myplayer.potions_inventory:
                    if item[0].shortcut == answer:
                        item[1] += 1
            else:
                print('\n' + npc_name)
                print("You don\'t have enough gold!".center(width))
                shop_buy(npc, previous_screen)
    
    for item in npc.armors_inventory:
        if answer == item[0].shortcut:
            if myplayer.gold >= item[0].value:
                print('\n<You bought {}!>'.format(item[0].name))
                myplayer.gold -= item[0].value
                item[1] -= 1
                for item in myplayer.armors_inventory:
                    if item[0].shortcut == answer:
                        item[1] += 1
            else:
                print('\n' + npc_name)
                print("You don\'t have enough gold!".center(width))
                shop_buy(npc, previous_screen)
    
    for item in npc.consumables_inventory:
        if answer == item[0].shortcut:
            if myplayer.gold >= item[0].value:
                print('\n<You bought {}!>'.format(item[0].name))
                myplayer.gold -= item[0].value
                item[1] -= 1
                for item in myplayer.consumables_inventory:
                    if item[0].shortcut == answer:
                        item[1] += 1
            else:
                print('\n' + npc_name)
                print("You don\'t have enough gold!".center(width))
                shop_buy(npc, previous_screen)
    
    input('\n<Continue (Press Enter)>'.center(width))        
    previous_screen(npc)

def shop_sell(npc, previous_screen):
    os.system('cls')
    options = ['back']

    print('{:-^99}'.format(' Weapons '))
    for item in myplayer.weapons_inventory:
        if item[1] > 0:
            selling_price = item[0].value // 3
            options.append(item[0].shortcut)
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     DMG: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].damage), str(item[0].speed), str(selling_price)))
        
    print('\n' + '{:-^99}'.format(' Potions '))
    for item in myplayer.potions_inventory:
        if item[1] > 0:
            selling_price = item[0].value // 3
            options.append(item[0].shortcut)
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}                      Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(selling_price)))
        
    print('\n' + '{:-^99}'.format(' Armors '))
    for item in myplayer.armors_inventory:
        if item[1] > 0:
            selling_price = item[0].value // 3
            options.append(item[0].shortcut)
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     DEF: {} SPEED: {} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].defence_bonus), str(item[0].speed), str(selling_price)))
        
    print('\n' + '{:-^99}'.format(' Consumables ')) 
    for item in myplayer.consumables_inventory:
        if item[1] > 0:
            selling_price = item[0].value // 3
            options.append(item[0].shortcut)
            c = ' ' * (30 - len(item[0].name))
            print('[{}] {}{}x{}     Energy: {} HP: {} MP:{} Price: {}'.format(item[0].shortcut, item[0].name, c, str(item[1]), str(item[0].energy_up), str(item[0].hp_up) or '-', str(item[0].mp_up) or '-', str(selling_price)))
    
    
    print('\n<What do you want to sell?> (type \'back\' to go back)')
    answer = input('\n> ').lower()
    while answer not in options:       
        shop_sell(npc, previous_screen)
    if answer == 'back':
        shop_window(npc, previous_screen)
    
    for item in myplayer.weapons_inventory:
        if answer == item[0].shortcut:
            selling_price = item[0].value // 3
            print('\n<You sold {}!>'.format(item[0].name))
            myplayer.gold += selling_price
            item[1] -= 1
            for item in npc.weapons_inventory:
                if item[0].shortcut == answer:
                    item[1] += 1

    for item in myplayer.potions_inventory:
        if answer == item[0].shortcut:
            selling_price = item[0].value // 3
            print('\n<You sold {}!>'.format(item[0].name))
            myplayer.gold += selling_price
            item[1] -= 1
            for item in npc.potions_inventory:
                if item[0].shortcut == answer:
                    item[1] += 1

    for item in myplayer.armors_inventory:
        if answer == item[0].shortcut:
            selling_price = item[0].value // 3
            print('\n<You sold {}!>'.format(item[0].name))
            myplayer.gold += selling_price
            item[1] -= 1
            for item in npc.armors_inventory:
                if item[0].shortcut == answer:
                    item[1] += 1

    for item in myplayer.consumables_inventory:
        if answer == item[0].shortcut:
            selling_price = item[0].value // 3
            print('\n<You sold {}!>'.format(item[0].name))
            myplayer.gold += selling_price
            item[1] -= 1
            for item in npc.consumables_inventory:
                if item[0].shortcut == answer:
                    item[1] += 1
    
    input('\n<Continue (Press Enter)>'.center(width))
    shop_window(npc, previous_screen)


#------------------------------------------------------------------- Tavern -----------------------------------------------------------------
def tavern():
    os.system('cls')
    myplayer.position = gamemap[myplayer.area][myplayer.position]['TAVERN']
    npc = gamemap[myplayer.area][myplayer.position]['OWNER']
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))
    print('\n' + npc.name.center(width))
    print(('-' * (len(npc.name) + 2)).center(width))
    print(npc.dialogue['WELCOME'].center(width))
    npc.met = True
    tavern_prompt(npc)

def tavern_prompt(npc):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    print('[1] Bed\n[2] Order food\n[3] Talk to ' + npc.name + '\n[4] Talk to people\n[5] Leave')
    options = ['1', '2', '3', '4', '5']
    answer = input('> ')
    while answer not in options:
        tavern_prompt(npc)        
    if answer == '1':
        tavern_bed(npc)
    elif answer == '2':
        shop_window(npc, tavern_prompt)
    elif answer == '3':
        dialogue(npc, tavern_prompt)
    elif answer == '4':
        chat(tavern_prompt)
    elif answer == '5':
        print(npc_name)
        print(npc.dialogue['LEAVE'].center(width) + '\n')                       #
        myplayer.position = gamemap[myplayer.area][myplayer.position]['LEAVE']          # Finds the leaving grid from the shop
        input('<Continue (Press Enter)>'.center(width))
        print_location()

def tavern_bed(npc):
    print(npc.dialogue['BED'])
    options = ['1', '2']
    print('[1] Accept\n[2] Refuse')
    answer = input('> ')
    while answer not in options:
        tavern_bed(npc)
    if answer == '1':
        if myplayer.gold < npc.bed_price:
            print('You don\'t have enough gold!')
            input('OK')
            tavern_prompt(npc)
        myplayer.gold -= npc.bed_price
        print('I\'ll take you to your room.')
        input('OK')
        sleep(tavern)
    elif answer == '2':
        tavern_prompt(npc)

def sleep(previous_screen):
    os.system('cls')
    myplayer.energy = myplayer.max_energy
    myplayer.hp = myplayer.max_hp
    myplayer.mp = myplayer.max_mp
    myplayer.day += 1
    print('<You slept well.>')
    print('<HP and MP replenished!>\n')
    input('OK')
    previous_screen()
# ----------------------------------------------------------------- NPC interaction -------------------------------------------------------
def chat(previous_screen):                                                         # when selecting 'chat' in prompt() it shows npc available to chat
    print('\n<Talk to who?>\n')
    count = 0
    options = []
    npcs = []
    
    for npc in gamemap[myplayer.area][myplayer.position]['NPC']:
        count += 1
        print('[{}] {}'.format(count, npc.name))
        options.append(str(count))
        npcs.append(npc)
    
    count += 1
    print('[{}] (Back)'.format(count))
    options.append(str(count))
    
    answer = input('> ')
    while answer not in options:
        chat(previous_screen)
    
    if answer == options[-1]:
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()
    
    selected_npc = npcs[int(answer) - 1]
    dialogue(selected_npc, previous_screen)        


def dialogue(npc, previous_screen):
    os.system('cls')
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)
    player_name = myplayer.name.center(width) + '\n' + ('-' * (len(myplayer.name) + 2)).center(width)
    
    if npc.quest:
        quest_prompt(npc, previous_screen)
    else:
        print(npc_name)
        print(npc.dialogue['GREET'].center(width) + '\n')
        npc.met = True
        count = 0
        options = []
        for i in npc.dialogue['DIALOGUE']:
            count += 1
            print('[{}] {}'.format(count, i[0]))                            
            options.append(str(count))
        count += 1
        print('[{}] Leave'.format(count))
        options.append(str(count))
        answer = input('> ')
        while answer not in options:
            dialogue(npc, previous_screen)
        if answer == options[-1]:
            if previous_screen == shop_prompt:
                previous_screen(npc)
            elif previous_screen == tavern_prompt:
                previous_screen(npc)
            previous_screen()

        print(player_name)
        print(npc.dialogue['DIALOGUE'][int(answer)-1][0].center(width) + ('\n' * 2))
        print(npc_name)
        print(npc.dialogue['DIALOGUE'][int(answer)-1][1].center(width) + ('\n' * 2))
        input('<Back (Press Enter)>'.center(width))
        dialogue(npc, previous_screen)

def quest_prompt(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)

    if myplayer.quests:                                              # check whether player has any ongoing fetchqests
        for quest in myplayer.quests:
            if quest == npc.quest:
                quest_ongoing(npc, previous_screen)
    print(npc_name)
    print(npc.dialogue['Q_GREET'].center(width) + '\n')
    npc.met = True
    options = ['1', '2', '3']
    print('[1] {}'.format(npc.dialogue['Q_PROMPT'][0]))
    print('[2] {}'.format(npc.dialogue['Q_PROMPT'][1]))
    print('[3] (Leave)')
    answer = input('\n> ').lower()
    while answer not in options:
        quest_prompt(npc, previous_screen)
    if answer == '3':
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()
    elif answer == '2':
        print(npc_name)
        print(npc.dialogue['Q_REFUSED'].center(width)+ '\n')
        input('Farewell (Leave)'.center(width))
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()
    elif answer == '1':
        quest_describing(npc, previous_screen)

def quest_describing(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)

    print(npc_name)
    print(npc.quest.description.center(width) + '\n')
    options = ['1', '2']
    print('[1] Accept')
    print('[2] Refuse')
    answer = input('> ')
    while answer not in options:
        quest_describing(npc, previous_screen)
    if answer == '2':
        print(npc_name)
        print(npc.dialogue['Q_REFUSED'].center(width) + '\n')
        input('Farewell (Leave)'.center(width))
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()
    elif answer == '1':
        myplayer.quests.append(npc.quest)
        print(npc_name)
        print(npc.dialogue['Q_ACCEPTED'].center(width) + '\n')
        input('Farewell (Leave)'.center(width))
        if previous_screen == tavern_prompt:
            previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
        previous_screen()


def quest_ongoing(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)

    print(npc_name)
    print(npc.dialogue['Q_ONGOING'].center(width) + '\n')
    print('[1] Yes')
    print('[2] No')
    options = ['1', '2']
    answer = input('> ').lower()
    while answer not in options:
        quest_ongoing(npc, previous_screen)
    if answer == '1':
        quest_resolving(npc, previous_screen)
    elif answer == '2':
        print(npc_name)
        print('Then I\'ll be waiting.'.center(width) + '\n')
        input('Farewell (Leave)'.center(width))
    if previous_screen == tavern_prompt:
        previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
    previous_screen()

def quest_resolving(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)

    if isinstance(npc.quest, FetchQuest):
        for i in myplayer.weapons_inventory:
            if i[0] == npc.quest.required_item:
                if i[1] >= npc.quest.required_amount:
                    quest_completing(npc, previous_screen)
        for i in myplayer.potions_inventory:
            if i[0] == npc.quest.required_item:
                if i[1] >= npc.quest.required_amount:
                    quest_completing(npc, previous_screen)
        for i in myplayer.armors_inventory:
            if i[0] == npc.quest.required_item:
                if i[1] >= npc.quest.required_amount:
                    quest_completing(npc, previous_screen)
        for item in myplayer.consumables_inventory:
            if item[0] == npc.quest.required_item:
                if item[1] >= npc.quest.required_amount:
                    quest_completing(npc, previous_screen)

        print(npc_name)
        print('You don\'t have what I need. Come back when you get {}x {}.'.format(str(npc.quest.required_amount), npc.quest.required_item).center(width))

    elif isinstance(npc.quest, KillQuest):
        for i in myplayer.kill_count:
            if i[0] == npc.quest.mob:
                if i[1] >= npc.quest.kill_amount:
                    quest_completing(npc, previous_screen)
        print(npc_name)
        print('You didn\'t complete the task. Come back when you kill {}x {}.'.format(str(npc.quest.kill_amount), npc.quest.mob).center(width))
    
    print('')
    input('Farewell (Leave)'.center(width))
    if previous_screen == tavern_prompt:
        previous_screen(gamemap[myplayer.area][myplayer.position]['OWNER'])
    previous_screen()

def quest_completing(npc, previous_screen):
    npc_name = npc.name.center(width) + '\n' + ('-' * (len(npc.name) + 2)).center(width)

    if isinstance(npc.quest, FetchQuest):
        print(npc_name)
        print(npc.dialogue['Q_COMPLETED'].center(width) + '\n')
        for i in myplayer.weapons_inventory:
            if i[0] == npc.quest.required_item:
                i[1] -= npc.quest.required_amount
        for i in myplayer.potions_inventory:
            if i[0] == npc.quest.required_item:
                i[1] -= npc.quest.required_amount
        for i in myplayer.armors_inventory:
            if i[0] == npc.quest.required_item:
                i[1] -= npc.quest.required_amount
        for item in myplayer.consumables_inventory:
            if item[0] == npc.quest.required_item:
                item[1] -= npc.quest.required_amount

        print('\n<{}x {} was removed from your inventory!>'.format(str(npc.quest.required_amount), npc.quest.required_item.name))

    elif isinstance(npc.quest, KillQuest):
        print(npc_name)
        print(npc.dialogue['Q_COMPLETED'].center(width))

    
    if npc.quest.gold_reward:
        print('\n<Received {} gold.>'.format(str(npc.quest.gold_reward)))
    if npc.quest.item_reward:
        for i in myplayer.weapons_inventory:
            if i[0] == npc.quest.item_reward:
                i[1] += 1
        for i in myplayer.potions_inventory:
            if i[0] == npc.quest.item_reward:
                i[1] += 1
        for i in myplayer.armors_inventory:
            if i[0] == npc.quest.item_reward:
                i[1] += 1
        for item in myplayer.consumables_inventory:
            if item[0] == npc.quest.item_reward:
                item[1] += 1
        print('\n<Received {}.>'.format(npc.quest.item_reward.name))
    
    myplayer.quests.remove(npc.quest)
    reward = npc.quest.xp_reward
    npc.quest = None
    input('\nFarewell (Leave)')
    myplayer.exp(reward, previous_screen)


def search(room):
    used_energy = 7 - (myplayer.speed // 2)
    if used_energy < 2:
        used_energy == 2

    success_chance = room.chance + myplayer.searching
    attempt = random.randint(1, 100)
    print(str(success_chance), str(attempt))
    if attempt <= success_chance:
        if room.trap:
            disarm_trap(room.trap)
            
            if room.trap.disarmed == False:
                myplayer.energy -= 5
                print('\n<You didn\'t find anything.>')
                room.chance += 15
                input('\n<Continue>')
                print_location()

        if room.gold:
            print('\n<You have found {} gold pieces!>'.format(str(room.gold)))
            myplayer.gold += room.gold
        if room.item:
            print('\n<You have found {}!>'.format(room.item.name))
            for i in myplayer.weapons_inventory:
                if i[0] == room.item:
                    i[1] += 1
            for i in myplayer.potions_inventory:
                if i[0] == room.item:
                    i[1] += 1
            for i in myplayer.armors_inventory:
                if i[0] == room.item:
                    i[1] += 1
            for i in myplayer.consumables_inventory:
                if i[0] == room.item:
                    i[1] += 1

        myplayer.successfull_searches += 1
        if myplayer.successfull_searches & 5 == 0:
            myplayer.searching += 1
            print('\n<Your skill increased!>')
        
        myplayer.energy -= 5
        del(gamemap[myplayer.area][myplayer.position]['SEARCH'])
        input('\n<Continue>')
        myplayer.exp(room.xp, print_location)

    else:
        myplayer.energy -= 5
        print('\n<You didn\'t find anything.>')
        room.chance += 15
        input('\n<Continue>')

    print_location()

def disarm_trap(trap):
    chance = trap.chance + myplayer.disarming_traps
    attempt = random.randint(1, 100)
        
    print('\n<While searching, you found a trap. Would you like to try and disarm it?' + ' (' + str(chance) + '%)')
    print('\n[1] Yes\n[2] No')
        
    options = ['1', '2']
    answer = input('\n> ')
    while answer not in options:
        trap.disarm_trap(myplayer)
    if answer == '1':
        if attempt <= chance:
            print('\n<You succesfully disarmed the trap!>')
            print('\n<You gained {} xp!>'.format(str(trap.xp)))
            myplayer.xp += trap.xp
            trap.disarmed = True
            myplayer.successfull_traps += 1
            if myplayer.successfull_traps % 3 == 0:
                print('\n<Your skill increased!>')
                myplayer.disarming_traps += 1
        else:
            print('\nYou failed at disarming the trap and triggered it!>')
            myplayer.hp -= trap.damage
            print('\n<You suffered {} HP damage!>'.format(str(trap.damage)))
    elif answer == '2':
        trap.chance += 100
    



title_screen()
