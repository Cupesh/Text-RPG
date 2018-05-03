from entities import *
import textwrap

gamemap = {
    'City' : {'NAME' : 'City',
        'a1' : {
        'GRIDNAME' : 'City Square West',
        'DESCRIPTION' : textwrap.fill("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", width=100),
        'VISITED_DESCRIPTION': "This is the west part of the city square. One of the buildings is a shop. The city square continues to the east. The city gates is south.",
        'VISITED' : False,
        'SHOP' : 's1',
        'UP' : None,
        'DOWN' : 'b1',
        'LEFT' : None,
        'RIGHT' : 'a2',
},
        'a2' : {
        'GRIDNAME' : 'City Square East',
        'DESCRIPTION' : 'This is the east part of the city square. One of the buildings is blacksmith\'s workshop.',
        'VISITED_DESCRIPTION': "This is the east part of the city square. One of the buildings is blacksmith\'s workshop.",
        'VISITED' : False,
        'NPC' : [npc_01, npc_02],
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'a1',
        'RIGHT' : None,
},
        'b1' : {
        'GRIDNAME' : 'City Gate',
        'DESCRIPTION' : 'This is a gate to the city, guarded by two armed soldiers. Southwise is a cave.',
        'VISITED_DESCRIPTION': "This is a gate to the city, guarded by two armed soldiers. Southwise is a cave.",
        'VISITED' : False,
        'UP' : 'a1',
        'DOWN' : True,
        'LEFT' : None,
        'RIGHT' : None,
        'AREA' : 'Cave',
        'GRID' : 'a1'
},
        's1' : {
        'GRIDNAME' : 'Shop',
        'NPC' : shopkeep,
        'LEAVE' : 'a1'
}
},
    'Cave' : {'NAME' : 'Cave',
        'a1': {
        'GRIDNAME' : 'Cave Entrance',
        'DESCRIPTION' : 'You have entered a small cave. It is dark inside.',
        'VISITED_DESCRIPTION': "This is a cave entrance. You see light coming from outside.",
        'VISITED' : False,
        'UP' : True,
        'DOWN' : 'b1',
        'LEFT' : None,
        'RIGHT' : 'a2',
        'AREA' : 'City',
        'GRID' : 'b1'
},        
        'a2': {
        'GRIDNAME' : 'Cave Room 1',
        'DESCRIPTION' : 'This is a dead end. You see a pile of bones and a sword on the ground.',
        'VISITED_DESCRIPTION' : "This room doesn't lead anywhere. Pile of bones on the ground has nothing interesting in it.",
        'VISITED' : False,
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'a1',
        'RIGHT' : None,
},
        'b1': {
        'GRIDNAME' : 'Cave Room 2',
        'DESCRIPTION' : 'You entered a room, there\'s a goblin looking at you.',
        'VISITED_DESCRIPTION' : "A dead goblin is lying on the ground.",
        'VISITED' : False,
        'ENEMY' : Goblin(),
        'UP' : 'a1',
        'DOWN' : None,
        'LEFT' : None,
        'RIGHT' : 'b2',
},
        'b2': {
        'GRIDNAME' : 'Cave Trasure Room',
        'DESCRIPTION' : 'This is a dead end. You see a chest with gold.',
        'VISITED_DESCRIPTION' : "This room is a dead end and there's an empty chest lying on the ground.",
        'VISITED' : False,
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'b1',
        'RIGHT' : None,
},
}
}       
