import sys
import csv
import random
import functools
import math
import pprint
import itertools
import copy

import map_spaces as ms

def debug(message):
    if True:
        print(message)

difficulty = 0
iterations = 1000

automa_cards = []
card_count = 24

map_spaces = ms.ortho_wrap_around_map_spaces
majors = [0,0,0,0,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10]
points = [4,2,3,2,4,2,3,2,4,2,3,2,4,2,3,2,4,2,3,2,4,2,3,2,3,2,3,2,3,2,3,2]
deltas = [
    [0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],
    [1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,-1],[2,0],[0,2],
    [2,2],[-2,-2],[2,1],[1,2],[2,-1],[-1,2],[1,-1],[-1,1]
]

class CompassDir:
    def __init__(self, name, next, previous,opposite):
        self.name = name
        self.next = next
        self.previous = previous
        self.opposite = opposite

compass_dirs = [
    CompassDir('N','NE','NW','S'),
    CompassDir('NE','E','N','SW'),
    CompassDir('E','SE','NE','W'),
    CompassDir('SE','S','E','NW'),
    CompassDir('S','SW','SE','N'),
    CompassDir('SW','W','S','NE'),
    CompassDir('W','NW','SW','E'),
    CompassDir('NW','N','W','SE')
]

ortho_compass_dirs = [
    CompassDir('N','E','W','S'),
    CompassDir('E','S','N','W'),
    CompassDir('S','W','E','N'),
    CompassDir('W','N','S','E'),
]

compass_dirs = ortho_compass_dirs

compass_lookup = {}

for compass_dir in compass_dirs:
    compass_lookup[compass_dir.name] = compass_dir

class AutomaCard:
    def __init__(self, ii, compass_dir, points, delta_col, delta_row,major_diff):
        self.card_id = ii
        self.compass_dir = compass_dir
        self.points = points
        self.delta_col = delta_col
        self.delta_row = delta_row
        self.major_diff = major_diff
        self.x_moves = []
        self.y_moves = []
        self.delta_y_amount = 0
        self.delta_x_amount = 0
        self.delta_x_dir = None
        self.delta_y_dir = None
        if self.delta_col < 0:
            self.delta_x_dir = 'W'
            self.delta_x_amount = -1 * self.delta_col
            for ii in range(0,self.delta_x_amount):
                self.x_moves.append('W')
        if self.delta_col > 0:
            self.delta_x_dir = 'E'
            self.delta_x_amount = self.delta_col
            for ii in range(0,self.delta_x_amount):
                self.x_moves.append('E')
        if self.delta_row < 0:
            self.delta_y_dir = 'N'
            self.delta_y_amount = -1 * self.delta_row
            for ii in range(0,self.delta_y_amount):
                self.y_moves.append('N')
        if self.delta_row > 0:
            self.delta_y_dir = 'S'
            self.delta_y_amount = self.delta_row
            for ii in range(0,self.delta_y_amount):
                self.y_moves.append('S')

    def next_move_x(self):
        if self.has_move_x():
            return self.x_moves.pop()
        return None

    def has_move_x(self):
        return len(self.x_moves) > 0

    def next_move_y(self):
        if self.has_move_y():
            return self.y_moves.pop()
        return None

    def has_move_y(self):
        return len(self.y_moves) > 0

    def __str__(self):
        return f'Card {self.card_id}, {self.compass_dir.name}, {self.points} points, {self.delta_x_amount} {self.delta_x_dir}, {self.delta_y_amount} {self.delta_y_dir}'

class AutomaDeck:
    def __init__(self,cards):
        self.perm_deck = cards
        self.temp_deck = copy.deepcopy(cards)
        random.shuffle(self.temp_deck)

    def draw(self):
        if len(self.temp_deck) <= 0:
            self.temp_deck = copy.deepcopy(self.perm_deck)
            random.shuffle(self.temp_deck)
        return self.temp_deck.pop()

for ii in range(0,card_count):
    compass_dir = compass_dirs[ii % len(compass_dirs)]
    point = points[ii % len(points)]
    delta_row = deltas[ii % len(deltas)][0]
    delta_col = deltas[ii % len(deltas)][1]
    major_diff = majors[ii % len(majors)]
    automa_cards.append(AutomaCard(ii,compass_dir,point,delta_row,delta_col,major_diff))

class GameMap:
    def __init__(self, map_spaces):
        self.space_hits = {}
        self.map_spaces = map_spaces
        self.space_by_index = {}
        self.space_by_abbr = {}
        for space in map_spaces:
            self.space_hits[space.abbr] = 0
            self.space_by_index[space.space_index] = space
            self.space_by_abbr[space.abbr] = space
        self.new_round()

    def new_round(self):
        self.claimed_spaces = {}
        for space in self.map_spaces:
            self.claimed_spaces[space.abbr] = 'empty'

    def human_claim_random(self, max_space_index):
        keys = list(self.claimed_spaces.keys())
        random.shuffle(keys)
        while len(keys) > 0:
            target_abbr = keys.pop()
            if self.space_by_abbr[target_abbr].space_index <= max_space_index:
                if self.claimed_spaces[target_abbr] == 'empty':
                    self.claimed_spaces[target_abbr] = 'human'
                    self.space_hits[target_abbr] += 1
                    return target_abbr
        return None

    def walk_spaces(self,max_index,compass_dir,current_space,depth,first_space):
        # Looped around during the delta and hit itself
        if current_space.abbr == first_space.abbr:
            return current_space
        # No single direction loop has more than 8 links
        if depth > 10:
            return None
        debug(f'Going {compass_dir} from {current_space} max_index {max_index} current_index {current_space.space_index} depth {depth}')
        if current_space.space_index <= max_index and depth > 0:
            return current_space
        return self.walk_spaces(max_index,compass_dir,self.space_by_abbr[current_space.compass_lookup[compass_dir]],depth+1,first_space)

    def automa_claim_space(self, start_index, automa_card, max_space_index):
        next_space = self.space_by_index[start_index]
        while automa_card.has_move_x():
            next_move = automa_card.next_move_x()
            next_space = self.walk_spaces(max_space_index,next_move,next_space,0,next_space)
            if next_space == None:
                self.display()
                print("Ran out of spaces to find during the delta X!")
                sys.exit(1)
        while automa_card.has_move_y():
            next_move = automa_card.next_move_y()
            next_space = self.walk_spaces(max_space_index,next_move,next_space,0,next_space)
            if next_space == None:
                self.display()
                print("Ran out of spaces to find during the delta Y!")
                sys.exit(1)
        debug(f"Automa trying to goto {next_space.name}")
        automa_spaces = []
        if self.claimed_spaces[next_space.abbr] == 'empty':
            debug(f"The first space was empty. Going there.")
            self.claimed_spaces[next_space.abbr] = 'automa'
            automa_spaces.append(next_space)
        # def v1_rotate_compass_strategy():
        #     compass_search_count = 0
        #     current_compass = automa_card.compass_dir.name
        #     start_space = next_space
        #     while compass_search_count < len(compass_dirs) and len(automa_spaces) < 3:
        #         next_space = self.walk_spaces(max_space_index,current_compass,start_space,0)
        #         if next_space == None:
        #             self.display()
        #             print("Ran out of spaces to find when placing fences!")
        #             sys.exit(1)
        #         if self.claimed_spaces[next_space.abbr] == 'empty':
        #             debug(f"A compass space {current_compass} was empty. Going there.")
        #             self.claimed_spaces[next_space.abbr] = 'automa'
        #             print(next_space.name)
        #             automa_spaces.append(next_space)
        #         current_compass = compass_lookup[current_compass].next
        #         compass_search_count += 1
        space_index = next_space.space_index
        while len(automa_spaces) < 3:
            space_index += 1
            if space_index > 30:
                space_index = 1
            try_space = self.space_by_index[space_index]
            if self.claimed_spaces[try_space.abbr] == 'empty':
                automa_spaces.append(try_space)
        for space in automa_spaces:
            if hasattr(space,'abbr'):
                self.space_hits[space.abbr] += 1
            else:
                self.space_hits[space] += 1
        return [xx.abbr for xx in automa_spaces]

    def display(self):
        x = self.claimed_spaces
        for k,v in self.claimed_spaces.items():
            self.claimed_spaces[k] = v[0]
            if v == 'empty':
                self.claimed_spaces[k] = ' '
        map =  f"|{x['C']}|{x['FE']}|{x['1']}|{x['2']}|{x['5']}|{x['8']}|{x['10']}|{x['12']}|{x['14']}|\n"
        map += f"|{x['G']}|{x['MP']}| | | | | | | |\n"
        map += f"|{x['RM']}|{x['GS']}|{x['F2']}|{x['3']}|{x['6']}|{x['9']}|{x['11']}|{x['13']}|\n"
        map += f"|{x['H']}|{x['F1']}|{x['CP']}| | | | | |\n"
        map += f"|{x['L1']}|{x['L2']}|{x['RB']}|{x['4']}|{x['7']}|\n"
        map += f"|{x['TP']}|{x['DL']}|{x['F3']}| | |"
        debug(map)

    def print_hit_counts(self):
        import plotext as plt

        x_axis = [xx.abbr for xx in map_spaces]
        y_axis = [self.space_hits[xx] for xx in x_axis]

        plt.bar(x_axis, y_axis,width=.1)
        plt.title("Times Spaces Used")
        plt.plot_size(120,10)
        plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
        plt.show()

    def validate_connections(self):
        debug("Ensuring the space map is valid")
        errors = 0
        for space in self.map_spaces:
            for dir_compass,end_space in space.compass_lookup.items():
                if end_space == '0':
                    continue
                reverse_dir = compass_lookup[dir_compass].opposite
                reverse_end = self.space_by_abbr[end_space].compass_lookup[reverse_dir]

                if reverse_end.name != space.name:
                    if end_space == '0' or reverse_end == '0':
                        continue
                    if reverse_end.has_long_west_edge or space.has_long_west_edge or end_space.has_long_west_edge:
                        continue

                    debug(f"Mismatch! {space.name} <-> {reverse_end}")
                    debug(f"{space.name} points {dir_compass} to {end_space}")
                    debug(f'{end_space} points {reverse_dir} to {reverse_end}')
                    errors += 1
        if errors == 0:
            debug("No map errors found")
        else:
            debug("MAP ERRORS FOUND! See logs above.")

    def get_space_by_abbr(self,abbr):
        return self.space_by_abbr[abbr]


def simulate():
    round_count = 0
    max_round_count = 14
    highest_space_index = 30
    automa_deck = AutomaDeck(automa_cards)
    automa_score = 0

    space_map = GameMap(map_spaces)

    human_meeple = 2
    first_player = 'human'
    while round_count < max_round_count:
        debug(f'=== Playing round {round_count+1} with {first_player} going first using {human_meeple} workers')
        highest_revealed_index = (highest_space_index - max_round_count) + round_count
        turns = []
        for ii in range(0,human_meeple):
            if first_player == 'human':
                turns.append('human')
                turns.append('automa')
            else:
                turns.append('automa')
                turns.append('human')
        automa_space_index = highest_revealed_index
        first_automa_turn = True
        for player in turns:
            if player == 'human':
                debug('Taking human turn')
                human_space = space_map.human_claim_random(highest_revealed_index)
                debug(f'Human placed one meeple on {human_space}')
                if human_space == 'MP':
                    first_player = 'human'
                space = space_map.get_space_by_abbr(human_space)
                if space.has_growth and human_meeple < 5:
                    human_meeple += 1
            else:
                debug(f'Taking automa turn, starting at space {automa_space_index}')
                automa_card = automa_deck.draw()
                automa_spaces = space_map.automa_claim_space(automa_space_index,automa_card,highest_revealed_index)
                if len(automa_spaces) <= 0:
                    space_map.display()
                automa_space_index = space_map.get_space_by_abbr(automa_spaces[-1]).space_index
                debug(f'Automa plays card: {automa_card}')
                if first_automa_turn:
                    automa_score += automa_card.points
                    first_automa_turn = False
                if 'MP' in automa_spaces:
                    first_player = 'automa'

        space_map.display()
        space_map.new_round()
        round_count += 1

    space_map.print_hit_counts()
    debug(f'Game over. Automa scored {automa_score}')

simulate()

def analyze_score_ranges():
    sorted_points = copy.deepcopy(points)
    sorted_points.sort()
    high_score = 0
    low_score = 0
    for ii in range(0,14):
        low_score += sorted_points[ii]
    for ii in range(10,24):
        high_score += sorted_points[ii]
    print(f'Base line low score: {low_score}')
    print(f'Base line high score: {high_score}')

analyze_score_ranges()