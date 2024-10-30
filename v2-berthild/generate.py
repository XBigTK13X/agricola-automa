import csv
import random
import functools
import math
import pprint
import itertools
import copy

difficulty = 0
iterations = 1000

spaces = {
    1:{'name':'Copse','gain':'wood','hits':0,'scores':True},
    2:{'name':'Grove','gain':'wood','hits':0,'scores':True},
    3:{'name':'Resource Market','gain':None,'hits':0,'scores':False},
    4:{'name':'Hollow','gain':'clay','hits':0,'scores':True},
    5:{'name':'Lessons1','gain':None,'hits':0,'scores':False},
    6:{'name':'Traveling Players','gain':'food','hits':0,'scores':True},
    7:{'name':'Farm Expansion','gain':None,'hits':0,'scores':False},
    8:{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False},
    9:{'name':'Grain Seeds','gain':None,'hits':0,'scores':False},
    10:{'name':'Farmland','gain':None,'hits':0,'scores':False},
    11:{'name':'Lessons2','gain':None,'hits':0,'scores':False},
    12:{'name':'Day Laborer','gain':None,'hits':0,'scores':False},
    13:{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True,'long_west_edge':True},
    14:{'name':'Forest','gain':'wood','hits':0,'scores':True},
    15:{'name':'Clay Pit','gain':'clay','hits':0,'scores':True},
    16:{'name':'Reed Bank','gain':'reed','hits':0,'scores':True},
    17:{'name':'Fishing','gain':'food','hits':0,'scores':True},
    18:{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False},
    19:{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False,'long_west_edge':True},
    20:{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True},
    21:{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True},
    22:{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False},
    23:{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False},
    24:{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True},
    25:{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False},
    26:{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True},
    27:{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True},
    28:{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False},
    29:{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False},
    30:{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}
}

spaces_abbr = {
    'C': 1,'G': 2,'RM':3,'H':4,'L1':5,'TP':6,
    'FE':7,'MP':8,'GS':9,'F1':10,'L2':11,'DL':12,
    '1':13,'F2':14,'CP':15,'RB':16,'F3':17,
    '2':18,'3':19,'4':20,'5':21,'6':22,'7':23,'8':24,
    '9':25,'10':26,'11':27,'12':28,'13':29,'14':30
}

spaces_compass = {
    'C':{'N':'0','NE':'0','E':'FE','SE':'MP','S':'G','SW':'0','W':'0','NW':'0'},
    'G':{'N':'C','NE':'FE','E':'MP','SE':'GS','S':'RM','SW':'0','W':'0','NW':'0'},
    'RM':{'N':'G','NE':'MP','E':'GS','SE':'F1','S':'H','SW':'0','W':'0','NW':'0'},
    'H':{'N':'RM','NE':'GS','E':'F1','SE':'L2','S':'L1','SW':'0','W':'0','NW':'0'},
    'L1':{'N':'H','NE':'F1','E':'L2','SE':'DL','S':'TP','SW':'0','W':'0','NW':'0'},
    'TP':{'N':'L1','NE':'L2','E':'DL','SE':'0','S':'0','SW':'0','W':'0','NW':'0'},

    'FE':{'N':'0','NE':'0','E':'1','SE':'1','S':'MP','SW':'G','W':'C','NW':'0'},
    'MP':{'N':'FE','NE':'1','E':'1','SE':'F2','S':'GS','SW':'RM','W':'G','NW':'C'},
    'GS':{'N':'MP','NE':'1','E':'F2','SE':'CP','S':'F1','SW':'H','W':'RM','NW':'G'},
    'F1':{'N':'GS','NE':'F2','E':'CP','SE':'RB','S':'L2','SW':'L1','W':'H','NW':'RM'},
    'L2':{'N':'F1','NE':'CP','E':'RB','SE':'F3','S':'DL','SW':'TP','W':'L1','NW':'H'},
    'DL':{'N':'L2','NE':'RB','E':'F3','SE':'0','S':'0','SW':'0','W':'TP','NW':'L1'},

    '1':{'N':'0','NE':'0','E':'2','SE':'3','S':'F2','SW':'GS','W':'MP','NW':'FE'},
    'F2':{'N':'1','NE':'2','E':'3','SE':'3','S':'CP','SW':'F1','W':'GS','NW':'MP'},
    'CP':{'N':'F2','NE':'3','E':'3','SE':'4','S':'RB','SW':'L2','W':'F1','NW':'GS'},
    'RB':{'N':'CP','NE':'3','E':'4','SE':'4','S':'F3','SW':'DL','W':'L2','NW':'F1'},
    'F3':{'N':'RB','NE':'4','E':'4','SE':'0','S':'0','SW':'0','W':'DL','NW':'L2'},

    '2':{'N':'0','NE':'0','E':'5','SE':'6','S':'3','SW':'F2','W':'1','NW':'0'},
    '3':{'N':'2','NE':'5','E':'6','SE':'7','S':'4','SW':'RB','W':'CP','NW':'1'},
    '4':{'N':'3','NE':'6','E':'7','SE':'0','S':'0','SW':'0','W':'F3','NW':'CP'},

    '5':{'N':'0','NE':'0','E':'8','SE':'9','S':'6','SW':'3','W':'2','NW':'0'},
    '6':{'N':'5','NE':'8','E':'9','SE':'0','S':'7','SW':'4','W':'3','NW':'2'},
    '7':{'N':'6','NE':'9','E':'0','SE':'0','S':'0','SW':'0','W':'4','NW':'3'},

    '8':{'N':'0','NE':'0','E':'10','SE':'11','S':'9','SW':'6','W':'5','NW':'0'},
    '9':{'N':'8','NE':'10','E':'11','SE':'0','S':'0','SW':'7','W':'6','NW':'5'},

    '10':{'N':'0','NE':'0','E':'12','SE':'13','S':'11','SW':'9','W':'8','NW':'0'},
    '11':{'N':'10','NE':'12','E':'13','SE':'0','S':'0','SW':'0','W':'9','NW':'8'},

    '12':{'N':'0','NE':'0','E':'14','SE':'0','S':'13','SW':'11','W':'10','NW':'0'},
    '13':{'N':'12','NE':'14','E':'0','SE':'0','S':'0','SW':'0','W':'11','NW':'10'},

    '14':{'N':'0','NE':'0','E':'0','SE':'0','S':'0','SW':'13','W':'12','NW':'0'},
}

automa_cards = []

card_count = 24

class CompassDir:
    def __init__(self, name, next, previous,opposite):
        self.name = name
        self.next = next
        self.previous = previous
        self.opposite = opposite

compass_dirs = [
    CompassDir('N','NE','NW','S'),
    CompassDir('NE','E','N','SW'),
    CompassDir('E','NE','SE','W'),
    CompassDir('SE','S','E','NW'),
    CompassDir('S','SW','SE','N'),
    CompassDir('SW','W','S','NE'),
    CompassDir('W','NW','SW','E'),
    CompassDir('NW','N','W','SE')
]

compass_lookup = {}

for compass_dir in compass_dirs:
    compass_lookup[compass_dir.name] = compass_dir

def validate_map():
    print("Ensuring the space map is valid")
    errors = 0
    for start_abbr,space_index in spaces_abbr.items():
        space_edges = spaces_compass[start_abbr]
        for dir_compass,end_space in space_edges.items():
            if end_space == '0':
                continue
            reverse_dir = compass_lookup[dir_compass].opposite
            reverse_end = spaces_compass[end_space][reverse_dir]

            if reverse_end != start_abbr:
                if end_space == '0' or reverse_end == '0':
                    continue
                if 'long_west_edge' in spaces[spaces_abbr[reverse_end]] \
                    or 'long_west_edge' in spaces[spaces_abbr[start_abbr]] \
                    or 'long_west_edge' in spaces[spaces_abbr[end_space]]:
                    continue

                print(f"Mismatch! {start_abbr} <-> {reverse_end}")
                print(f"{start_abbr} points {dir_compass} to {end_space}")
                print(f'{end_space} points {reverse_dir} to {reverse_end}')
                errors += 1
    if errors == 0:
        print("No map errors found")
    else:
        print("MAP ERRORS FOUND! See logs above.")

points = [2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
deltas = [
    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
    [1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[2,0],[0,2],
    [2,2],[-2,-2],[2,1],[1,2],[2,-1],[-1,2],[1,-1],[-1,1]
]

class AutomaCard:
    def __init__(self, ii, compass_dir, points, delta_col, delta_row):
        self.card_id = ii
        self.compass_dir = compass_dir
        self.points = points
        self.delta_col = delta_col
        self.delta_row = delta_row
        if self.delta_col < 0:
            self.delta_x_dir = 'W'
            self.delta_x_amount = -1 * self.delta_col
        else:
            self.delta_x_dir = 'E'
            self.delta_x_amount = self.delta_col
        if self.delta_row < 0:
            self.delta_y_dir = 'N'
            self.delta_y_amount = -1 * self.delta_row
        else:
            self.delta_y_dir = 'S'
            self.delta_y_amount = self.delta_row

    def debug(self):
        print(f'Card {self.card_id}, {self.compass_dir.name}, {self.points} points, {self.delta_x_amount} {self.delta_x_dir}, {self.delta_y_amount} {self.delta_y_dir}')


for ii in range(0,card_count):
    compass_dir = compass_dirs[ii % len(compass_dirs)]
    point = points[ii % len(points)]
    delta_row = deltas[ii % len(deltas)][0]
    delta_col = deltas[ii % len(deltas)][1]
    automa_cards.append(AutomaCard(ii,compass_dir,point,delta_row,delta_col))

validate_map()

def validate_scores():
    for point in points:
        pass

validate_scores()

def simulate():
    round_count = 0
    max_round_count = 14
    highest_space_index = 30
    temp_deck = copy.deepcopy(automa_cards)
    random.shuffle(temp_deck)
    automa_score = 0
    while round_count < max_round_count:
        if len(temp_deck) <= 0:
            temp_deck = copy.deepcopy(automa_cards)
            random.shuffle(temp_deck)
        automa_card = temp_deck.pop()
        highest_revealed_index = (highest_space_index - max_round_count) + round_count
        print(automa_card.debug())
        automa_score += automa_card.points
        round_count += 1
    print(f'Game over. Automa scored {automa_score}')

simulate()