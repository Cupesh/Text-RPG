from entities import *

gamemap = {
    'City' : {'NAME' : 'City',
        'a1' : {
        'GRIDNAME' : 'City Square West',
        'DESCRIPTION' : 'This is the west part of the city square. One of the buildings is a shop. The city square continues to the east. The city gates is south.',
        'SOLVED_DESCRIPTION': "This is the west part of the city square. One of the buildings is a shop. The city square continues to the east. The city gates is south.",
        'SOLVED' : False,
        'SHOP' : 's1',
        'UP' : None,
        'DOWN' : 'b1',
        'LEFT' : None,
        'RIGHT' : 'a2',
},
        'a2' : {
        'GRIDNAME' : 'City Square East',
        'DESCRIPTION' : 'This is the east part of the city square. One of the buildings is blacksmith\'s workshop.',
        'SOLVED_DESCRIPTION': "This is the east part of the city square. One of the buildings is blacksmith\'s workshop.",
        'SOLVED' : False,
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'a1',
        'RIGHT' : None,
},
        'b1' : {
        'GRIDNAME' : 'City Gate',
        'DESCRIPTION' : 'This is a gate to the city, guarded by two armed soldiers. Southwise is a cave.',
        'SOLVED_DESCRIPTION': "This is a gate to the city, guarded by two armed soldiers. Southwise is a cave.",
        'SOLVED' : False,
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
        'SOLVED_DESCRIPTION': "This is a cave entrance. You see light coming from outside.",
        'SOLVED' : False,
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
        'SOLVED_DESCRIPTION' : "This room doesn't lead anywhere. Pile of bones on the ground has nothing interesting in it.",
        'SOLVED' : False,
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'a1',
        'RIGHT' : None,
},
        'b1': {
        'GRIDNAME' : 'Cave Room 2',
        'DESCRIPTION' : 'You entered a room, there\'s a goblin looking at you.',
        'SOLVED_DESCRIPTION' : "A dead goblin is lying on the ground.",
        'SOLVED' : False,
        'ENEMY' : Goblin(),
        'UP' : 'a1',
        'DOWN' : None,
        'LEFT' : None,
        'RIGHT' : 'b2',
},
        'b2': {
        'GRIDNAME' : 'Cave Trasure Room',
        'DESCRIPTION' : 'This is a dead end. You see a chest with gold.',
        'SOLVED_DESCRIPTION' : "This room is a dead end and there's an empty chest lying on the ground.",
        'SOLVED' : False,
        'UP' : None,
        'DOWN' : None,
        'LEFT' : 'b1',
        'RIGHT' : None,
},
}
}       
