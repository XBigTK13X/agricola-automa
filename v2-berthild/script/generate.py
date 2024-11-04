import sys
import csv
import random
import copy

import game_map as gm
import human as hh
from debug import debug

difficulty = 0
iterations = 1000

automa_cards = []
card_count = 24
unused_automa_cards = 0

card_infos = [
    [41,4,[2, 0]],
    [38,0,[0, 0]],
    [39,0,[2, -1]],
    [41,0,[0, 1]],
    [42,3,[-1, 0]],
    [38,2,[-1, -1]],
    [39,3,[-2, -2]],
    [39,4,[2, 1]],
    [40,3,[0, -1]],
    [41,1,[1, 0]],
    [38,4,[1, 0]],
    [39,3,[0, 1]],
    [40,4,[0, 2]],
    [42,2,[2, 2]],
    [36,1,[-1, 2]],
    [42,1,[0, 0]],
    [39,3,[0, -1]],
    [36,1,[-1, 1]],
    [37,0,[1, 1]],
    [42,2,[1, -1]],
    [40,3,[1, 2]],
    [41,2,[-1, 0]],
    [37,4,[1, 1]],
    [40,3,[-1, -1]]
]

major_points = [1,1,1,1,4,2,3,2,2,2]
claimed_majors = {}

class AutomaCard:
    def __init__(self, ii, compass_dir, points, delta_col, delta_row,major_diff):
        self.card_id = ii + 1
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
        self.dirs = ''
        if self.delta_col < 0:
            self.delta_x_dir = 'W'
            self.delta_x_amount = -1 * self.delta_col
            for ii in range(0,self.delta_x_amount):
                self.x_moves.append('W')
            self.dirs += 'x'
        if self.delta_col > 0:
            self.delta_x_dir = 'E'
            self.delta_x_amount = self.delta_col
            for ii in range(0,self.delta_x_amount):
                self.x_moves.append('E')
            self.dirs += 'x'
        if self.delta_row < 0:
            self.delta_y_dir = 'N'
            self.delta_y_amount = -1 * self.delta_row
            for ii in range(0,self.delta_y_amount):
                self.y_moves.append('N')
            self.dirs += 'y'
        if self.delta_row > 0:
            self.delta_y_dir = 'S'
            self.delta_y_amount = self.delta_row
            for ii in range(0,self.delta_y_amount):
                self.y_moves.append('S')
            self.dirs += 'y'

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

    def csv_list(self):
        #headers = ['card_id','points','dxa','dxd','dya','dyd','major_diff']
        return [self.card_id,self.points,self.delta_x_amount,self.delta_x_dir,self.delta_y_amount,self.delta_y_dir,self.major_diff,self.dirs]

class AutomaDeck:
    def __init__(self,cards):
        self.perm_deck = cards
        self.temp_deck = copy.deepcopy(cards)
        random.shuffle(self.temp_deck)

    def draw(self):
        if len(self.temp_deck) <= unused_automa_cards:
            self.temp_deck = copy.deepcopy(self.perm_deck)
            random.shuffle(self.temp_deck)
        return self.temp_deck.pop()

for ii in range(0,card_count):
    compass_dir = gm.compass_dirs[ii % len(gm.compass_dirs)]
    point = card_infos[ii][0]
    delta_row = card_infos[ii][2][0]
    delta_col = card_infos[ii][2][1]
    major_diff = card_infos[ii][1]
    automa_cards.append(AutomaCard(ii,compass_dir,point,delta_row,delta_col,major_diff))

def simulate():
    round_count = 0
    max_round_count = 14
    highest_space_index = 30
    automa_deck = AutomaDeck(automa_cards)
    automa_score = 0
    automa_major_points = 0
    automa_majors = 0

    space_map = gm.GameMap()

    human_first_count = 0
    automa_first_count = 0
    human = hh.Human()
    first_player = 'human'
    while round_count < max_round_count:
        debug(f'=== Playing round {round_count+1} with {first_player} going first using {human.workers} workers')
        highest_revealed_index = (highest_space_index - max_round_count) + round_count
        turns = []
        if first_player == 'human':
            human_first_count += 1
        else:
            automa_first_count += 1
        for ii in range(0,human.workers):
            if first_player == 'human':
                turns.append('human')
                turns.append('automa')
            else:
                turns.append('automa')
                turns.append('human')
        automa_space_index = highest_revealed_index
        automa_major_index = 0
        for player in turns:
            if player == 'human':
                debug('Taking human turn')
                space = space_map.human_pick_space(human, highest_revealed_index)
                space = space_map.get_space_by_abbr(space)
                debug(f'Human placed one meeple on {space}')
                if space.action.name == 'MP':
                    first_player = 'human'
                    human.is_first = True
                if space.action.has_growth and human.workers < 5:
                    human.workers += 1
                if space.action.boon_count() > 0:
                    human.gain_resources(space.action.take_resources())
                if space.action.has_major and len(list(claimed_majors.keys())) < 10:
                    for ii in range(0,10):
                        if not ii in claimed_majors:
                            claimed_majors[ii] = True
                            break
                if space.action.has_action('room') and human.rooms < 5:
                    human.build_rooms()

            else:
                debug(f'Taking automa turn, starting at space {automa_space_index}')
                automa_card = automa_deck.draw()
                automa_spaces = space_map.automa_claim_space(automa_space_index,automa_card,highest_revealed_index)
                if len(automa_spaces) <= 0:
                    space_map.display()
                automa_space_index = space_map.get_space_by_abbr(automa_spaces[-1]).space_index
                debug(f'Automa plays card: {automa_card}')
                print(automa_spaces)
                if 'MP' in automa_spaces:
                    first_player = 'automa'
                    human.is_first = False
                for abbr in automa_spaces:
                    space = space_map.get_space_by_abbr(abbr)
                    if space.action.boon_count() > 0:
                        space.action.take_resources()
                    if space.action.has_major and automa_card.major_diff != 0:
                        automa_major_index = (automa_major_index + automa_card.major_diff) % len(major_points)
                        if not automa_major_index in claimed_majors:
                            claimed_majors[automa_major_index] = True
                            automa_score += major_points[automa_major_index]
                            automa_major_points += major_points[automa_major_index]
                            automa_majors += 1
                            debug(f'Automa claimed major {automa_major_index} for {major_points[automa_major_index]}')


        space_map.display()
        print(human)
        space_map.new_round()
        human.feed_workers()
        round_count += 1

    space_map.print_hit_counts()
    last_card = automa_deck.draw()
    #debug(f'Game over. Automa base line score is {last_card.points} plus {automa_majors} majors worth {automa_major_points} for a total of {last_card.points + automa_major_points}')
    debug(f'Game over. Automa base line score is {last_card.points} and claimed {automa_majors} majors')
    debug(f'{human}')
    debug(f'Automa went first {automa_first_count} rounds, Human went first {human_first_count} rounds')


headers = ['card_id','points','dxa','dxd','dya','dyd','major_diff','dirs']
csv_cards = [xx.csv_list() for xx in automa_cards]

with open('./berthild.csv','w',newline='') as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(headers)
    writer.writerows(csv_cards)

simulate()