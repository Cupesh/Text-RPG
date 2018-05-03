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
width = os.get_terminal_size().columns
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
        self.knows_magic = False
        self.spells = []
        self.area = 'City'
        self.position = 'a1'
        self.gold = 100
        self.weapons_inventory = [[dagger, 1], [short_sword, 0], [long_sword, 0], [two_handed_sword, 0], [axe, 0], [battleaxe, 0],
        [spear, 0]]
        self.potions_inventory = [[healing_potion, 0], [mana_potion, 0], [rejuvenation_potion, 0], [speed_potion, 0], [ironskin_potion, 0],
        [strength_potion, 0]]
        self.armors_inventory = [[clothes, 0], [leather_armor, 0], [studded_leather_armor, 0], [chain_mail_armor, 0], [plate_armor, 0],
        [mage_robe, 0], [master_robe, 0]]
        self.equipped_weapon = None
        self.equipped_armor = None
        self.level = 1
        self.xp = 0
        self.next_level = 50


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
        if self.level % 3 == 0:                                                 # Every third level player can add +1 to a stat
            self.stat_increase(previous_screen)
        input('\n<Continue (Press Enter)>')
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
        previous_screen()                                                       # Return to the previous screen before player leveled up

# ----------------------------------------------------------- stats --------------------------------------------------------------------
    def display_stats(self):                                                    # Displays player's stats
        os.system('cls')
        print(self.name.center(width))
        print('{} Level: {}, XP: {}, Next Level: {}'.format(self.job, str(self.level), str(self.xp), str(self.next_level - self.xp)).center(width))
        print('')
        print('{}HP: {}/{}'.format((' ' * 45), self.max_hp, self.hp))
        print('{}MP: {}/{}'.format((' ' * 45), self.max_mp, self.mp))
        print('\n{}Attack: {}'.format((' ' * 45), self.attack))
        print('{}Defence: {}'.format((' ' * 45), self.defence))
        print('{}Speed: {}'.format((' ' * 45), self.speed))
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
        for i in self.weapons_inventory:
            if i[1] > 0:
                c = ' ' * (30 - len(i[0].name))
                print('{}{}x{}     DMG: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].damage), str(i[0].speed), str(i[0].value)))
        print('{:-^99}'.format(' Potions '))
        for i in self.potions_inventory:
            if i[1] > 0:
                c = ' ' * (30 - len(i[0].name))
                print('{}{}x{}                      Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].value)))
        print('{:-^99}'.format(' Armors '))
        for i in self.armors_inventory:
            if i[1] > 0:
                c = ' ' * (30 - len(i[0].name))
                print('{}{}x{}     DEF: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].defence_bonus), str(i[0].speed), str(i[0].value)))
        self.inventory_prompt()                                                     # ^ Displays inventory and prompts the player

    def inventory_prompt(self):
        options = ['1', '2', '3', '4', '5']
        print('\n[1] Use\n[2] Toss\n[3] Equip\n[4] De-equip\n[5] Leave\n')          # De-equip or unequip, fuck I don't know
        answer = input('> ')
        while answer not in options:
            self.display_inventory
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
        for i in self.potions_inventory:                                            # Subject to change? So far only potions can be used 
            if i[1] > 1:                                                            # from the game window print_location().
                print('{}x {}'.format(i[0].name, str(i[1])))
        print('')
        print('<Use what?> (type \'back\' to return)')
        options = [i[0].name.lower() for i in self.potions_inventory] + ['back']
        answer = input('> ').lower()                                                # This while-loop is used many times throughout the code
        while answer not in options:                                                # limiting player's accepted inputs by checking with
            self.inventory_use()                                                    # 'options' list that contains all acceptable inputs.
        if answer == 'back':
            self.display_inventory()
        for i in self.potions_inventory:                                            # My way of handling inventory functions. For loops
            if answer == i[0].name.lower():                                         # used in the same manner throughout the whole code.
                if i[1] > 0:                                                        # At first converts any player's input into all lower
                    Potion.use_potion(i[0], self)                                   # case string and then loops through the particular
                    i[1] -= 1                                                       # inventory type, converting each item's name into a
                    self.inventory_use()                                            # lowercase string and then looks for a match.
                else:
                    ('<You don\'t have that!>')
                    input('\n<Continue (Press Enter)>')
                    self.inventory_use()

    def inventory_toss(self):
        print('\n<Toss what?> (type \'back\' to return)')
        a = [i[0].name.lower() for i in self.weapons_inventory if i[1] > 0]         # My stupid way of making options list, probably don't 
        b = [i[0].name.lower() for i in self.potions_inventory if i[1] > 0]         # know how to handle lists or I just chose a stupid
        c = [i[0].name.lower() for i in self.armors_inventory if i[1] > 0]          # inventory handling.
        options = a + b + c + ['back']
        answer = input('> ').lower()
        while answer not in options:
            self.inventory_toss()
        if answer == 'back':
            self.display_inventory()
        for i in self.weapons_inventory:
            if answer == i[0].name.lower():
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                input('\n<Continue (Press Enter)>')
                self.display_inventory()
        for i in self.potions_inventory:
            if answer == i[0].name.lower():
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                input('\n<Continue (Press Enter)>')
                self.display_inventory()                 
        for i in self.armors_inventory:
            if answer == i[0].name.lower():
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                input('\n<Continue (Press Enter)>')
                self.display_inventory()                
        print('\nYou don\'t have that!')
        self.inventory_toss()        

    def inventory_equip(self):
        os.system('cls')
        print('\nEquipped Weapon: {}'.format(self.equipped_weapon))                 # Displays equipped weapon and armor. self.name attribute 
        print('Equipped Armor: {}'.format(self.equipped_armor))                     # not called because of __str__ method in Item class
        print('')
        print('{:-^99}'.format(' Weapons '))                                        # Prints 'Weapons' surrounded with 99 '-'. Nice format
        for i in self.weapons_inventory:                                            # function.
            if i[1] > 0:
                c = ' ' * (30 - len(i[0].name))                                     # var 'c' creates equal allignement
                print('{}{}x{}     DMG: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].damage), str(i[0].speed), str(i[0].value)))
        print('{:-^99}'.format(' Armors '))
        for i in self.armors_inventory:
            if i[1] > 0:
                c = ' ' * (30 - len(i[0].name))
                print('{}{}x{}     DEF: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].defence_bonus), str(i[0].speed), str(i[0].value)))
        print('\n<Equip what?> (type \'back\' to return)')
        back = ['back']
        a = [i[0].name.lower() for i in self.weapons_inventory if i[1] > 0]
        b = [i[0].name.lower() for i in self.armors_inventory if i[1] > 0]
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
                for i in self.weapons_inventory:
                    if i[0].name == self.equipped_weapon.name:                      # Adds the weapon to the inventory after removing
                        i[1] += 1                                                   # from hand.
                self.equipped_weapon = None
            for i in self.weapons_inventory:
                if answer == i[0].name.lower():                                     # Equips new weapon, adds its effects to the player
                    self.equipped_weapon = i[0]                                     # and removes from the inventory.
                    i[1] -= 1
                    self.attack += i[0].damage
                    self.speed += i[0].speed
                    print('\nYou equipped {}'.format(i[0].name))
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
                for i in self.armors_inventory:
                    if i[0].name == self.equipped_armor.name:
                        i[1] += 1
                self.equipped_armor = None
            for i in self.armors_inventory:
                if answer == i[0].name.lower():
                    self.equipped_armor = i[0]
                    i[1] -= 1
                    self.defence += i[0].defence_bonus
                    self.speed += i[0].speed
                    self.max_mp += i[0].mana_bonus
                    print('\nYou are now wearing {}'.format(self.equipped_armor.name))
                    input('\n<Continue (Press Enter)>')
                    self.display_inventory()

    def inventory_deequip(self):
        os.system('cls')
        print('\nEquipped Weapon: {}'.format(self.equipped_weapon))
        print('Equipped Armor: {}'.format(self.equipped_armor))
        print('')
        print('<De-equip what?> (type \'back\' to return)')
        if self.equipped_weapon == None:                                                # The way I handled the 'None has no .name attribute
            a = None                                                                    # bug'. Probably temporary, but it works.
        else:
            a = self.equipped_weapon.name.lower()
        if self.equipped_armor == None:
            b = None
        else:
            b = self.equipped_armor.name.lower()
        options = ['back', a, b]
        answer = input('> ').lower()
        while answer not in options:
            self.inventory_deequip()
        if answer == 'back':
            self.display_inventory()
        for i in self.weapons_inventory:
            if answer == i[0].name.lower():
                i[1] += 1
                print('\n<You de-equipped {}.>'.format(self.equipped_weapon.name))
                self.attack -= self.equipped_weapon.damage
                self.speed -= self.equipped_weapon.speed
                self.equipped_weapon = None
        for i in self.armors_inventory:
            if answer == i[0].name.lower():
                i[1] += 1
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
        for i in self.spells:
            a = ' ' * (15 - len(i.name))                                                # Variables to handle alignements.
            b = ' ' * (60 - len(i.description))
            print('{}{}{}{}Cost: {} MP'.format(i.name, a, i.description, b, i.mp_cost))
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
    
    def use_spell(self):                                                                # So far only healing spells can be used.
        options = ['minor healing', 'healing', 'major healing', 'back']                 # Not sure what about other spells...
        print('\n<Use what? (type \'back\' to return)>')                                # Has to be typed. Probably will import
        answer = input('> ').lower()                                                    # numbered prompt.
        while answer not in options:
            print('\n<Can\'t use that. Try a healing spell.>')
            self.use_spell()
        if answer == 'back':
            self.display_magic()
        for i in self.spells:
            if answer == i.name.lower():
                if self.mp < i.mp_cost:                                                 # Checking if player has enough mana.
                    print('\n<You don\'t have enough mana!>')
                else:
                    i.heal_spell_cast(myplayer)
        input('\n<Continue (Press Enter)>')
        self.display_magic()


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
    print('[1] Start Game'.center(width))
    print('[2] Load Game'.center(width))
    print('[3] Help     '.center(width))
    print('[4] Quit Game'.center(width))
    option = input('\n> ')
    if option.lower() in ['1', 'start']:
        character_creation()
    elif option.lower() in ['2', 'load']:
        load_game()
    elif option.lower() in ['3', 'help']:
        help_menu()
    elif option.lower() in ['4', 'quit']:
        sys.exit()
    else:
        title_screen()

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

def help_menu():
    pass


# ---------------------------------------------------- starting the game, character creation ------------------------------------------
def character_creation():
    os.system('cls')                                                                    # clears the screen
    print('\n' * 24)                                                                    # Don't know how to center vertically.
    print('What is your name?\n'.center(width))
    playername = input('> ')
    if len(playername) < 1:                                                             # Making sure player entered something.
        print('<You need to enter a name.>')
        input('\n<Continue (Press Enter)>')
        character_creation()
    myplayer.name = playername                                                          # passes name into player object
    
    os.system('cls')
    print('\n' * 24)
    options = ['1', '2']
    print('What is your job?'.center(width))
    print('[1] Warrior'.center(width))
    print('[2] Mage'.center(96))
    answer = input('\n> ')
    while answer not in options:
        character_creation()
    if answer == '1':                                                                   # Job values are a subject to change.
        myplayer.job = 'Warrior'
        myplayer.max_hp = 20
        myplayer.hp = 20
        myplayer.max_mp = 0
        myplayer.mp = 0
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

def game_introduction():                                                                 # Welcoming screen
    os.system('cls')
    print('\n' * 24)
    print('Wecome, {} the {}!'.format(myplayer.name, myplayer.job).center(width))
    print('This is a small game, a Python learning project. Hope you\'ll enjoy!'.center(width))
    print('')
    input('<Continue (Press Enter)>'.center(width))
    print_location()


# ------------------------------------------------------ main game window  ------------------------------------------------------------
def print_location():                                                                   # This is a main game window.
    os.system('cls')
    print(('-' * 40).center(99))
    print('HP: {}\{} MP: {}\{}'.format(myplayer.max_hp, myplayer.hp, myplayer.max_mp, myplayer.mp).center(width))
    print('Level: {} XP: {} Next Level: {}'.format(myplayer.level, myplayer.xp, myplayer.next_level).center(99))
    print(('-' * 40).center(width))
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))      # Checks player location, position and from worldmap.py
    print('')                                                                           # pulls out location name.
    if gamemap[myplayer.area][myplayer.position]['VISITED']:                             # Checks whether player already visited this location
        print(gamemap[myplayer.area][myplayer.position]['VISITED_DESCRIPTION'])          # before, for a different message to display.
        prompt()
    else:
        print(gamemap[myplayer.area][myplayer.position]['DESCRIPTION'])                 # Prints out first-time-visit message and then 
        if 'ENEMY' in gamemap[myplayer.area][myplayer.position]:                        # checks whether location has an enemy present.
            battle_start()
        else:
            prompt()

# ======================================================================================================================================
# ======================================================== GAME INTERACTIVITY ==========================================================

# -------------------------------------------------------- main prompt window ----------------------------------------------------------
def prompt():                                                                           # Main prompt window.
    print('\n<What would you like to do?>\n')
    menu = ['Go']
    end_menu = ['Player', 'Inventory', 'Save', 'Quit']
    options = ['g', 'q', 'i', 's', 'p']
    if myplayer.job == 'Mage':
        options.append('m')
        end_menu.insert(0, 'Magic')
    if 'NPC' in gamemap[myplayer.area][myplayer.position]:
        options.append('c')
        menu.append('Chat')
    if 'SHOP' in gamemap[myplayer.area][myplayer.position]:
        options.append('t')
        menu.append('Trader')
    for i in menu:
        print('[{}] {}'.format(i[0].lower(), i))
    for i in end_menu:
        print('[{}] {}'.format(i[0].lower(), i))
    answer = input('\n> ').lower()
    while answer not in options:
        prompt()
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
        chat()

# ----------------------------------------------------------- movement ------------------------------------------------------------------
def player_movement():
    print('\n<Go where?>\n')
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
    myplayer.position = destination
    print_location()

def travel_handler(area, destination):
    print('\n<You have traveled to the {}.>'.format(gamemap[area]['NAME']).center(width))
    input('\n<Continue (Press Enter)>'.center(width))
    gamemap[myplayer.area][myplayer.position]['VISITED'] = True                          # Marks the previous grid as visited and moves to
    myplayer.area = area                                                                # a new area and its starting grid.
    myplayer.position = destination
    print_location()

# ------------------------------------------------------------------- Battling -------------------------------------------------------------
def battle_start():
    pass

def cast_spell():
    pass

# -------------------------------------------------------------------- shop ---------------------------------------------------------------
def shop():
    os.system('cls')
    myplayer.position = gamemap[myplayer.area][myplayer.position]['SHOP']               # allocates player's new position
    npc = gamemap[myplayer.area][myplayer.position]['NPC']                              # Searches for the npc
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))
    print('')
    print('{}: {}'.format(npc.name, npc.dialogue['WELCOME']))                           # Shows npc's welcoming message
    print('')
    shop_prompt(npc)

def shop_prompt(npc):
    print('<What would you like to do?>')
    print('[1] Shop\n[2] Talk\n[3] Leave')
    options = ['1', '2', '3']
    answer = input('> ')
    while answer not in options:
        shop_prompt(npc)        
    if answer == '1':
        shop_window(npc)
    elif answer == '2':
        dialogue(npc, shop_prompt)
    elif answer == '3':
        print('\n{}: {}'.format(npc.name, npc.dialogue['LEAVE']))                       # Prints npc's goodbye message
        myplayer.position = gamemap[myplayer.area][myplayer.position]['LEAVE']          # Finds the leaving grid from the shop
        input('\n<Continue (Press Enter)>')
        print_location()

def shop_window(npc):
    os.system('cls')
    print(npc.name.upper().center(width))                                               # Npc's name in the center
    print('-' * 100)
    print('{:_^99}'.format(' Weapons '))
    print('')
    for i in npc.weapons_inventory:
        if i[1] > 0:
            c = ' ' * (30 - len(i[0].name))
            print('{}{}x{}     DMG: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].damage), str(i[0].speed), str(i[0].value)))

    print('')
    print('\n{:_^99}'.format(' Potions '))
    print('')
    for i in npc.potions_inventory:
        if i[1] > 0:
            c = ' ' * (30 - len(i[0].name))
            print('{}{}x{}                      Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].value)))

    print('')
    print('\n{:_^99}'.format(' Armors '))
    print('')
    for i in npc.armors_inventory:
        if i[1] > 0:
            c = ' ' * (30 - len(i[0].name))
            print('{}{}x{}     DEF: {} SPEED: {} Price: {}'.format(i[0].name, c, str(i[1]), str(i[0].defence_bonus), str(i[0].speed), str(i[0].value))) 
    print('')
    print('-' * 100)
    print('\nYour gold: {}'.format(myplayer.gold))
    answers = ['1', '2', '3']
    print('\nCame to buy or sell?')
    print('\n[1] Buy\n[2] Sell\n[3] Back')
    answer = input('\n> ')
    while answer not in answers:
        shop_window(npc)
    if answer == '1':
        shop_buy(npc)
    elif answer == '2':
        shop_sell(npc)
    elif answer == '3':
        shop_prompt(npc)

def shop_buy(npc):
    print('\n<Buy what?> (type \'back\' to return)')
    back = ['back']
    a = [i[0].name.lower() for i in npc.weapons_inventory if i[1] > 0]
    b = [i[0].name.lower() for i in npc.potions_inventory if i[1] > 0]
    c = [i[0].name.lower() for i in npc.armors_inventory if i[1] > 0]
    options = a + b + c + back
    answer = input('> ').lower()
    while answer not in options:
        print('\nI don\'t have that.')
        shop_buy(npc)
    if answer == 'back':
        shop_window(npc)
    for i in npc.weapons_inventory:
        if answer == i[0].name.lower():
            if myplayer.gold >= i[0].value:                                         # Checks if player has enough gold for the transaction
                print('\nYou bought {}!'.format(i[0].name))
                myplayer.gold -= i[0].value                                         # Takes away the gold from the player
                i[1] -= 1                                                           # takes away the item from the npc
                for i in myplayer.weapons_inventory:                                # Adds the item to the player's inventory
                    if i[0].name.lower() == answer:
                        i[1] += 1
            else:
                print("\nYou don\'t have enough gold!")
                shop_buy(npc)
    for i in npc.potions_inventory:
        if answer == i[0].name.lower():
            if myplayer.gold >= i[0].value:
                print('\nYou bought {}!'.format(i[0].name))
                myplayer.gold -= i[0].value
                i[1] -= 1
                for i in myplayer.potions_inventory:
                    if i[0].name.lower() == answer:
                        i[1] += 1
            else:
                print("\nYou don\'t have enough gold!")
                shop_buy(npc)
    for i in npc.armors_inventory:
        if answer == i[0].name.lower():
            if myplayer.gold >= i[0].value:
                print('\nYou bought {}!'.format(i[0].name))
                myplayer.gold -= i[0].value
                i[1] -= 1
                for i in myplayer.armors_inventory:
                    if i[0].name.lower() == answer:
                        i[1] += 1
            else:
                print("\nYou don\'t have enough gold!")
                shop_buy(npc)
    input('\n<Continue (Press Enter)>')        
    shop_window(npc)

def shop_sell(npc):
    os.system('cls')
    options = ['back']
    for i in myplayer.weapons_inventory:
        if i[1] > 0:
            options.append(i[0].name.lower())
            selling_price = str(i[0].value // 3)                                        # Selling value is a third of original value
            print('{}: x{}    Price: {}'.format(i[0].name, str(i[1]), selling_price))
    for i in myplayer.potions_inventory:
        if i[1] > 0:
            options.append(i[0].name.lower())
            print('{}: x{}    Price: {}'.format(i[0].name, str(i[1]), selling_price))
    for i in myplayer.armors_inventory:
        if i[1] > 0:
            options.append(i[0].name.lower())
            print('{}: x{}    Price: {}'.format(i[0].name, str(i[1]), selling_price))
    
    print('\nWhat do you want to sell? <(type \'back\' to go back')
    answer = input('\n> ').lower()
    while answer not in options:
        print('\nYou don\'t have that.')
        input('\n<Continue (Press Enter)>')         
        shop_sell(npc)
    if answer == 'back':
        shop_window(npc)
    for i in myplayer.weapons_inventory:
        if answer == i[0].name.lower():
            selling_price = i[0].value // 3
            print('\nYou sold {}!'.format(i[0].name))
            myplayer.gold += selling_price
            i[1] -= 1
            for i in npc.weapons_inventory:
                if i[0].name.lower() == answer:
                    i[1] += 1

    for i in myplayer.potions_inventory:
        if answer == i[0].name.lower():
            selling_price = i[0].value // 3
            print('\nYou sold {}!'.format(i[0].name))
            myplayer.gold += selling_price
            i[1] -= 1
            for i in npc.potions_inventory:
                if i[0].name.lower() == answer:
                    i[1] += 1

    for i in myplayer.armors_inventory:
        if answer == i[0].name.lower():
            selling_price = i[0].value // 3
            print('\nYou sold {}!'.format(i[0].name))
            myplayer.gold += selling_price
            i[1] -= 1
            for i in npc.armors_inventory:
                if i[0].name.lower() == answer:
                    i[1] += 1
    input('\n<Continue (Press Enter)>')
    shop_window(npc)

# ----------------------------------------------------------------- NPC interaction -------------------------------------------------------
def chat():
    print('Talk to who?')
    count = 0
    options = []
    npcs = []
    for i in gamemap[myplayer.area][myplayer.position]['NPC']:
        count += 1
        print('[{}] {}'.format(count, i.name))
        options.append(str(count))
        npcs.append(i)
    count += 1
    print('[{}] (Back)'.format(count))
    options.append(str(count))
    answer = input('> ')
    while answer not in options:
        chat()
    if answer == options[-1]:
        print_location()
    a = npcs[int(answer) - 1]
    dialogue(a, print_location)        
        


def dialogue(npc, screen):
    previous_screen = screen                                            # Takes the previous screen attribute to know where to return after
    os.system('cls')
    print('{}: {}'.format(npc.name, npc.dialogue['GREET']))
    print('-' * len(npc.name))
    print(' ')
    count = 0
    options = []
    for i in npc.dialogue['DIALOGUE']:                                  # Count the amount of possible quesitions and prints them with
        count += 1                                                      # 'Count' var is the associated number with player's input
        print('[{}] {}'.format(count, i[0]))                            
        options.append(str(count))                                      # append the number to options
    count += 1
    print('[{}] Leave'.format(count))
    options.append(str(count))
    answer = input('> ')
    while answer not in options:
        dialogue(npc, previous_screen)
    if answer == options[-1]:                                   # The last option is alway 'back'
        if previous_screen == shop_prompt:
            npc.met = True
            previous_screen(npc)
        npc.met = True
        previous_screen()

    print('\n{}: {}'.format(myplayer.name, npc.dialogue['DIALOGUE'][int(answer)-1][0]))     # Looks up for the associated answer in npc's
    print('-' * (len(myplayer.name) + 1))
    print('\n{}: {}'.format(npc.name, npc.dialogue['DIALOGUE'][int(answer)-1][1]))          # dialogues.
    print('-' * (len(npc.name) + 1))
    input('\n<Back (Press Enter)>')
    dialogue(npc, previous_screen)





title_screen()
