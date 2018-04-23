import os
import sys
import cmd
import time
import random
import dill
import textwrap
from worldmap import gamemap
from items import *

os.system('mode con: cols=100 lines=50')
width = os.get_terminal_size().columns
length = os.get_terminal_size().lines
# ======== CHARACTER CLASS ==========
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
        self.area = 'City'
        self.position = 'a1'
        self.gold = 50
        self.weapons_inventory = [[dagger, 1], [short_sword, 0], [long_sword, 0], [two_handed_sword, 0], [axe, 0], [battleaxe, 0],
        [spear, 0]]
        self.potions_inventory = [[healing_potion, 0], [mana_potion, 0], [rejuvenation_potion, 0], [speed_potion, 0], [ironskin_potion, 0],
        [strength_potion, 0]]
        self.armors_inventory = [[clothes, 0], [leather_armor, 0], [studded_leather_armor, 0], [chain_mail_armor, 0], [plate_armor, 0],
        [mage_robe, 0], [master_robe, 0]]
        self.equipped_weapon = None
        self.equipped_armor = None

    def display_inventory(self):
        os.system('cls')
        print('Equipped Weapon: {}'.format(self.equipped_weapon))
        print('Equipped Armor: {}'.format(myplayer.equipped_armor))
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
        myplayer.inventory_prompt()

    def inventory_prompt(self):
        options = ['1', '2', '3', '4', '5']
        print('\n[1] Use\n[2] Toss\n[3] Equip\n[4] De-equip\n[5] Leave\n')
        answer = input('> ')
        while answer not in options:
            myplayer.display_inventory
        if answer == '1':
            myplayer.inventory_use()
        elif answer == '2':
            myplayer.inventory_toss()
        elif answer == '3':
            pass
        elif answer == '4':
            pass
        elif answer == '5':
            print_location()

    def inventory_use(self):
        for i in self.potions_inventory:
            if i[1] > 1:
                print('{}x {}'.format(i[0].name, str(i[1])))
        print('')
        print('<Use what?> (type \'back\' to return)')
        options = [i[0].name.lower() for i in self.potions_inventory] + ['back']
        answer = input('> ')
        while answer.lower() not in options:
            myplayer.inventory_use()
        if answer.lower() == 'back':
            myplayer.display_inventory()
        for i in self.potions_inventory:
            if answer.lower() == i[0].name.lower():
                if i[1] > 0:
                    Potion.use_potion(i[0], myplayer)
                    i[1] -= 1
                    myplayer.inventory_use()
                else:
                    ('<You don\'t have that!>')
                    myplayer.inventory_use()

    def inventory_toss(self):
        print('\n<Toss what?> (type \'back\' to return)')
        back = ['back']
        a = [i[0].name.lower() for i in self.weapons_inventory]
        b = [i[0].name.lower() for i in self.potions_inventory]
        c = [i[0].name.lower() for i in self.armors_inventory]
        options = a + b + c + back
        answer = input('> ')
        while answer.lower() not in options:
            myplayer.inventory_toss()
        if answer.lower() == 'back':
            myplayer.display_inventory()
        for i in self.weapons_inventory:
            if i[1] > 0:
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                myplayer.inventory_toss()
            else:
                print('\nYou don\'t have that!')
                myplayer.inventory_toss()
        for i in self.potions_inventory:
            if i[1] > 0:
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                myplayer.inventory_toss()                 
            else:
                print('\nYou don\'t have that!')
                myplayer.inventory_toss()
        for i in self.armors_inventory:
            if i[1] > 0:
                i[1] -= 1
                print('\nYou tossed {} away!'.format(i[0].name))
                myplayer.inventory_toss()                 
            else:
                print('\nYou don\'t have that!')
                myplayer.inventory_toss()        



global myplayer
myplayer = Player()  # character created with no stats or name, those values will be passed in the object during the character creation

# ========== GAME FUNCTIONALITY ====================


def title_screen():
    os.system('cls')
    print('\n' * 10)
    print('=========================================='.center(width))
    print('==  Welcome to a Python Text Based RPG  =='.center(width))
    print('==                                      =='.center(width))
    print('==      This is a learning project.     =='.center(width))
    print('==                                      =='.center(width))
    print('==       2018 Martin "Coop" Cupak       =='.center(width))
    print('=========================================='.center(width))
    print('')
    print('[1] Start Game'.center(width))
    print('[2] Load Game'.center(width))
    print('[3] Help     '.center(100))
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
    dill.dump_session('savefile.pkl')
    print('\nGame has been saved!')
    input('<Continue (Press Enter)>')
    print_location()

def load_game():
    if os.path.exists('savefile.pkl') == True:
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


def character_creation():
    os.system('cls') # clears the screen
    print('\n' * 24)
    print('What is your name?\n'.center(width))
    playername = input('> ')
    myplayer.name = playername     # passes name into player object
    
    os.system('cls')
    print('\n' * 24)
    print('What is your job?'.center(width))
    print('[1] Warrior'.center(width))
    print('[2] Mage'.center(96))
    playerjob = input('\n> ')
    if playerjob.lower() in ['1', 'warrior']:
        myplayer.job = 'Warrior'
        myplayer.max_hp = 20
        myplayer.hp = 20
        myplayer.max_mp = 0
        myplayer.mp = 0
        start_game()

    elif playerjob.lower() in ['2', 'mage']:
        myplayer.job = 'Mage'
        myplayer.max_hp = 15
        myplayer.hp = 15
        myplayer.max_mp = 10
        myplayer.mp = 10
        myplayer.knows_magic = True
        myplayer.speed = 7
        start_game()


def start_game():
    os.system('cls')
    print('\n' * 24)
    print('Wecome, {} the {}!'.format(myplayer.name, myplayer.job).center(width))
    print('This is a small game, a Python learning project. Hope you\'ll enjoy!'.center(width))
    print('')
    input('<Continue (Press Enter)>'.center(width))
    print_location()


def print_location():
    os.system('cls')
    print('')
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))
    print('')
    if gamemap[myplayer.area][myplayer.position]['SOLVED']:
        print(gamemap[myplayer.area][myplayer.position]['SOLVED_DESCRIPTION'])
        prompt()
    else:
        print(gamemap[myplayer.area][myplayer.position]['DESCRIPTION'])
        if 'ENEMY' in gamemap[myplayer.area][myplayer.position]:
            time.sleep(5)
            battle_start(gamemap[myplayer.area][myplayer.position]['ENEMY'])
        else:
            prompt()

def movement_handler(destination):
    gamemap[myplayer.area][myplayer.position]['SOLVED'] = True
    myplayer.position = destination
    print_location()


def travel_handler(area, destination):
    print('\n<You have traveled to the {}.>'.format(gamemap[area]['NAME']).center(width))
    input('\n<Continue (Press Enter)>'.center(width))
    gamemap[myplayer.area][myplayer.position]['SOLVED'] = True
    myplayer.area = area
    myplayer.position = destination
    print_location()




# =============== GAME INTERACTIVITY =======================

def prompt():
    print('\n<What would you like to do?> (go, shop, inventory, quit, save)\n')
    answers = ['go', 'quit', 'shop', 'inventory', 'save']
    action = input('> ')
    while action not in answers:
        prompt()
    if action.lower() == 'go':
        player_movement()
    elif action.lower() == 'quit':
        sys.exit()
    elif action.lower() == 'shop':
        if 'SHOP' in gamemap[myplayer.area][myplayer.position]:
            shop()
        else:
            print('\n<There is no shop here.>')
            print('--------------------------')
            prompt()
    elif action.lower() == 'inventory':
        myplayer.display_inventory()
    elif action.lower() == 'save':
        save_game()

def battle_start(enemy):
    os.system('cls')
    a = (myplayer.name + '     ' + enemy.name)
    print('<{} is attacking you!>\n'.format(enemy.name))
    while myplayer.hp > 0:
        print(a)
        print(str(myplayer.hp) + '/' + str(myplayer.max_hp) + (' ' * (len(a) -10)) + str(enemy.hp) + '/' + str(enemy.max_hp))
        print('\n\n\n')
        print('<What would you like to do?>')
        print('[1] Attack\n[2] Magic\n[3] Run')
        action = input('> ')

        if action == '1':
            damage = myplayer.attack - enemy.defence
            enemy.hp -= damage
            if enemy.hp > 0:
                enemy_damage = enemy.attack - myplayer.defence            
                if enemy_damage <= 0:
                    enemy_damage = 1
                myplayer.hp -= enemy_damage
            else:
                print('<You killed {}.>'.format(enemy.name))
                print('<You have collected {} gold.>'.format(str(enemy.gold)))
                myplayer.gold += enemy.gold
                gamemap[myplayer.area][myplayer.position]['SOLVED'] = True
                gamemap[myplayer.area][myplayer.position]['ENEMY'] = None
                time.sleep(5)
                print_location()
        elif action == '2':
            cast_spell()
        elif action == '3':
            myplayer.position = 'a1'
            print_location()

    print("<You died. Game over.>")
    time.sleep(3)
    title_screen()
                

def cast_spell():
    pass


def player_movement():
    print('\n<Go where?> (north, south, east, west, cancel)\n')
    answers = ['north', 'south', 'east', 'west', 'up', 'down', 'left', 'right', 'shop']
    direction = input('> ')

    if direction.lower() == 'cancel':
        print_location()

    while direction not in answers:
        player_movement()

    if direction.lower() in ['north', 'up']:
        if gamemap[myplayer.area][myplayer.position]['UP'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['UP']:
            destination = gamemap[myplayer.area][myplayer.position]['UP']
            movement_handler(destination)
        else:
            print("<You cannot go there!>")
            player_movement()

    elif direction.lower() in ['south', 'down']:
        if gamemap[myplayer.area][myplayer.position]['DOWN'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['DOWN']:
            destination = gamemap[myplayer.area][myplayer.position]['DOWN']
            movement_handler(destination)
        else:
            print("<You cannot go there!>")
            player_movement()

    elif direction.lower() in ['west', 'left']:
        if gamemap[myplayer.area][myplayer.position]['LEFT'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['LEFT']:
            destination = gamemap[myplayer.area][myplayer.position]['LEFT']
            movement_handler(destination)
        else:
            print("<You cannot go there!>")
            player_movement()

    elif direction.lower() in ['east', 'right']:
        if gamemap[myplayer.area][myplayer.position]['RIGHT'] == True:
            area = gamemap[myplayer.area][myplayer.position]['AREA']
            destination = gamemap[myplayer.area][myplayer.position]['GRID']
            travel_handler(area, destination)
        elif gamemap[myplayer.area][myplayer.position]['RIGHT']:
            destination = gamemap[myplayer.area][myplayer.position]['RIGHT']
            movement_handler(destination)
        else:
            print("<You cannot go there!>")
            player_movement()


def shop():
    os.system('cls')
    new_position = gamemap[myplayer.area][myplayer.position]['SHOP']
    myplayer.position = new_position
    npc = gamemap[myplayer.area][myplayer.position]['NPC']
    print('{:=^99}'.format(gamemap[myplayer.area][myplayer.position]['GRIDNAME']))
    print('')
    print('{}: {}'.format(npc.name, npc.dialogue['WELCOME']))
    print('')
    shop_prompt(npc)

def shop_prompt(npc):
    print('<What would you like to do?>')
    print('[1] Shop\n[2] Talk\n[3] Leave')
    answer = input('> ')
    if answer == '1':
        shop_window(npc)
    elif answer == '2':
        dialogue(npc, shop_prompt)
    elif answer == '3':
        print('\n{}: {}'.format(npc.name, npc.dialogue['LEAVE']))
        myplayer.position = gamemap[myplayer.area][myplayer.position]['LEAVE']
        input('\n<Continue (Press Enter)>')
        print_location()
    else:
        shop_prompt(npc)

def shop_window(npc):
    os.system('cls')
    print(npc.name.upper().center(width))
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
    a = [i[0].name.lower() for i in npc.weapons_inventory]
    b = [i[0].name.lower() for i in npc.potions_inventory]
    c = [i[0].name.lower() for i in npc.armors_inventory]
    answers = a + b + c + back
    answer = input('> ')
    while answer not in answers:
        print('\nI don\'t have that.')
        shop_buy(npc)
    if answer.lower() == 'back':
        shop_window(npc)
    for i in npc.weapons_inventory:
        if answer.lower() == i[0].name.lower():
            if i[1] > 0:
                if myplayer.gold >= i[0].value:
                    print('\nYou bought {}!'.format(i[0].name))
                    myplayer.gold -= i[0].value
                    i[1] -= 1
                    for i in myplayer.weapons_inventory:
                        if i[0].name.lower() == answer:
                            i[1] += 1
                    input('\n<Continue (Press Enter)>')
                    shop_window(npc)
                else:
                    print("\nYou don\'t have enough gold!")
                    shop_buy(npc)
            else:
                print('\nI\'m sorry, I\'m out of stock of this item.')
                shop_buy(npc)
        else:
            pass
    for i in npc.potions_inventory:
        if answer == i[0].name.lower():
            if i[1] > 0:
                if myplayer.gold >= i[0].value:
                    print('\nYou bought {}!'.format(i[0].name))
                    myplayer.gold -= i[0].value
                    i[1] -= 1
                    for i in myplayer.potions_inventory:
                        if i[0].name.lower() == answer:
                            i[1] += 1
                    input('\n<Continue (Press Enter)>')
                    shop_window(npc)
                else:
                    print("\nYou don\'t have enough gold!")
                    shop_buy(npc)
            else:
                print('\nI\'m sorry, I\'m out of stock of this item.')
                shop_buy(npc)

    for i in npc.armors_inventory:
        if answer == i[0].name.lower():
            if i[1] > 0:
                if myplayer.gold >= i[0].value:
                    print('\nYou bought {}!'.format(i[0].name))
                    myplayer.gold -= i[0].value
                    i[1] -= 1
                    for i in myplayer.armors_inventory:
                        if i[0].name.lower() == answer:
                            i[1] += 1
                    input('\n<Continue (Press Enter)>')        
                    shop_window(npc)
                else:
                    print("\nYou don\'t have enough gold!")
                    shop_buy(npc)
            else:
                print('\nI\'m sorry, I\'m out of stock of this item.')
                shop_buy(npc)

def shop_sell(npc):
    os.system('cls')
    options = ['back']
    for i in myplayer.weapons_inventory:
        if i[1] > 0:
            options.append(i[0].name.lower())
            selling_price = str(i[0].value // 3)
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
    answer = input('\n> ')
    while answer.lower() not in options:
        shop_sell(npc)
    if answer == 'back':
        shop_window(npc)
    for i in myplayer.weapons_inventory:
        if answer.lower() == i[0].name.lower():
            if i[1] > 0:
                selling_price = i[0].value // 3
                print('\nYou sold {}!'.format(i[0].name))
                myplayer.gold += selling_price
                i[1] -= 1
                for i in npc.weapons_inventory:
                    if i[0].name.lower() == answer:
                        i[1] += 1
                input('\n<Continue (Press Enter)>')
                shop_window(npc)
    for i in myplayer.potions_inventory:
        if answer.lower() == i[0].name.lower():
            if i[1] > 0:
                selling_price = i[0].value // 3
                print('\nYou sold {}!'.format(i[0].name))
                myplayer.gold += selling_price
                i[1] -= 1
                for i in npc.potions_inventory:
                    if i[0].name.lower() == answer:
                        i[1] += 1
                input('\n<Continue (Press Enter)>')
                shop_window(npc)
    for i in myplayer.armors_inventory:
        if answer.lower() == i[0].name.lower():
            if i[1] > 0:
                selling_price = i[0].value // 3
                print('\nYou sold {}!'.format(i[0].name))
                myplayer.gold += selling_price
                i[1] -= 1
                for i in npc.armors_inventory:
                    if i[0].name.lower() == answer:
                        i[1] += 1
                input('\n<Continue (Press Enter)>')
                shop_window(npc)




def dialogue(npc, screen):
    previous_screen = screen
    os.system('cls')
    print(npc.name)
    print('-----------------------------------\n')
    count = 1
    options = ['1']
    for i in npc.dialogue['DIALOGUE']:
        print('[{}] {}'.format(count, i[0]))
        count += 1
        options.append(str(count))
    print('[{}] Leave'.format(count))

    answer = input('> ')
    while answer not in options:
        dialogue(npc, previous_screen)
    if answer.lower() == options[-1]:
        previous_screen(npc)

    print('\n{}: {}'.format(myplayer.name, npc.dialogue['DIALOGUE'][int(answer)-1][0] ))
    print('\n{}: {}'.format(npc.name, npc.dialogue['DIALOGUE'][int(answer)-1][1]))
    input('\n<Back (Press Enter)>')
    dialogue(npc, previous_screen)





title_screen()
