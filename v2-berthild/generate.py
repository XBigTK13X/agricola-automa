import sys
import csv
import random
import copy

import map_spaces

def debug(message):
    if True:
        print(message)

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

class CompassDir:
    def __init__(self, name, next, previous,opposite):
        self.name = name
        self.next = next
        self.previous = previous
        self.opposite = opposite

compass_dirs = [
    CompassDir('N','E','W','S'),
    CompassDir('E','S','N','W'),
    CompassDir('S','W','E','N'),
    CompassDir('W','N','S','E'),
]

compass_lookup = {}

for compass_dir in compass_dirs:
    compass_lookup[compass_dir.name] = compass_dir

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
    compass_dir = compass_dirs[ii % len(compass_dirs)]
    point = card_infos[ii][0]
    delta_row = card_infos[ii][2][0]
    delta_col = card_infos[ii][2][1]
    major_diff = card_infos[ii][1]
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
            space.action.refill()

    def human_random_space(self, max_space_index):
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

    def human_claim(self,abbr):
        self.claimed_spaces[abbr] = 'human'
        self.space_hits[abbr] += 1
        return abbr

    def automa_claim(self,abbr):
        self.claimed_spaces[abbr] = 'automa'
        self.space_hits[abbr] += 1
        return abbr

    def human_pick_space(self, human, max_space_index):
        keys = list(self.claimed_spaces.keys())
        random.shuffle(keys)
        open_space_abbrs = []
        while len(keys) > 0:
            target_abbr = keys.pop()
            if self.space_by_abbr[target_abbr].space_index <= max_space_index:
                if self.claimed_spaces[target_abbr] == 'empty':
                    open_space_abbrs.append(target_abbr)

        desires = ['wood','reed','food','grain','clay','vegetable','sheep','stone','pig','cow']
        for abbr in open_space_abbrs:
            space = self.get_space_by_abbr(abbr)
            # Always go first
            if space.action.has_action('start_player') and not human.is_first:
                return self.human_claim(abbr)
            # Try to get workers
            if space.action.has_growth and human.wants_workers():
                return self.human_claim(abbr)
            # Try to build rooms
            if space.action.has_action('room') and human.wants_rooms():
                return self.human_claim(abbr)
            # Try to get resources
            for desire in desires:
                if human.wants_resource(desire,space.action.has_resource(desire)):
                    return self.human_claim(abbr)
        # Otherwise, pick a random one
        return self.human_random_space(max_space_index)

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
        debug(f"Automa trying to goto {next_space.action.name}")
        automa_spaces = []
        if self.claimed_spaces[next_space.abbr] == 'empty':
            debug(f"The first space was empty. Going there.")
            self.automa_claim(next_space.abbr)
            automa_spaces.append(next_space)
        space_index = next_space.space_index
        while len(automa_spaces) < 3:
            space_index += 1
            if space_index > 30:
                space_index = 1
            try_space = self.space_by_index[space_index]
            if self.claimed_spaces[try_space.abbr] == 'empty':
                self.automa_claim(try_space.abbr)
                automa_spaces.append(try_space)
        return [xx.abbr for xx in automa_spaces]

    def display(self):
        display_spaces = copy.deepcopy(self.claimed_spaces)
        x = display_spaces
        for k,v in self.claimed_spaces.items():
            display_spaces[k] = (" "+v[0]+" ").upper()
            if v == 'empty':
                display_spaces[k] = '   '
                space = self.space_by_abbr[k]
                if space.action.boon_count() > 0 and space.action.accumulate:
                    if space.action.boon_count() < 10:
                        display_spaces[k] = f' {space.action.boon_count()}{space.action.gain[0][0][0]}'
                    else:
                        display_spaces[k] = f'{space.action.boon_count()}{space.action.gain[0][0][0]}'
        ss = '   '
        map =  f"|{x['C']}|{x['FE']}|{x['1']}|{x['2']}|{x['5']}|{x['8']}|{x['10']}|{x['12']}|{x['14']}|\n"
        map += f"|{x['G']}|{x['MP']}|{ss}|{ss}|{ss}|{ss}|{ss}|{ss}|{ss}|\n"
        map += f"|{x['RM']}|{x['GS']}|{x['F2']}|{x['3']}|{x['6']}|{x['9']}|{x['11']}|{x['13']}|\n"
        map += f"|{x['H']}|{x['F1']}|{x['CP']}|{ss}|{ss}|{ss}|{ss}|{ss}|\n"
        map += f"|{x['L1']}|{x['L2']}|{x['RB']}|{x['4']}|{x['7']}|\n"
        map += f"|{x['TP']}|{x['DL']}|{x['F3']}|{ss}|{ss}|"
        debug(map)

    def print_hit_counts(self):
        import plotext as plt

        x_axis = [xx.abbr for xx in self.map_spaces]
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

                if reverse_end.action.name != space.action.name:
                    if end_space == '0' or reverse_end == '0':
                        continue
                    if reverse_end.has_long_west_edge or space.has_long_west_edge or end_space.has_long_west_edge:
                        continue

                    debug(f"Mismatch! {space.action.name} <-> {reverse_end}")
                    debug(f"{space.action.name} points {dir_compass} to {end_space}")
                    debug(f'{end_space} points {reverse_dir} to {reverse_end}')
                    errors += 1
        if errors == 0:
            debug("No map errors found")
        else:
            debug("MAP ERRORS FOUND! See logs above.")

    def get_space_by_abbr(self,abbr):
        return self.space_by_abbr[abbr]

class Human:
    def __init__(self):
        self.resources = {
            'wood': 0,
            'food': 2,
            'reed': 0,
            'sheep': 0,
            'cow': 0,
            'pig': 0,
            'grain': 0,
            'vegetable': 0,
            'stone': 0,
            'clay': 0
        }
        self.workers = 2
        self.babies = 0
        self.begging = 0
        self.rooms = 2
        self.room_kind = 'wood'
        self.is_first = True

    def feed_workers(self):
        for ii in range(0,self.workers):
            if self.resources['food'] > 2:
                self.resources['food'] -= 2
            elif self.resources['food'] == 1:
                self.resources['food'] = 0
                self.begging += 1
            elif self.resources['food'] <= 0:
                self.begging += 2
        for ii in range(0,self.babies):
            if self.resources['food'] >= 1:
                self.resources['food'] -= 1
            elif self.resources['food'] <= 0:
                self.begging += 1
        self.workers += self.babies
        self.babies = 0

    def wants_rooms(self):
        return self.rooms < 5 and not self.wants_resource('wood',5) and not self.wants_resource('reed',2)

    def wants_workers(self):
        return self.workers < 5 and self.rooms > self.workers and self.resources['food'] > self.workers * 2

    def gain_resources(self, resources):
        for k,v in resources.items():
            self.resources[k] += v

    def wants_resource(self,name,amount):
        if name == 'wood' and self.resources['wood'] < 5 and amount >= 5:
            return True
        if name == 'clay' and self.resources['wood'] < 3 and amount >= 3:
            return True
        if name == 'stone' and self.resources['wood'] < 3 and amount >= 3:
            return True
        if name == 'food' and self.resources['food'] < self.workers * 2 and amount >= 3:
            return True
        if name == 'sheep' and self.resources['sheep'] < 1 and amount >= 1:
            return True
        if name == 'cow' and self.resources['cow'] < 1 and amount >= 1:
            return True
        if name == 'pig' and self.resources['pig'] < 1 and amount >= 1:
            return True
        if name == 'vegetable' and self.resources['vegetable'] < 1 and amount >= 1:
            return True
        if name == 'grain' and self.resources['grain'] < 1 and amount >= 1:
            return True
        if name == 'reed' and self.resources['reed'] < 2 and amount >= 2:
            return True
        return False

    def __str__(self):
        return f'''=-=-=-Human Info-=-=-=
    workers {self.workers}
    babies {self.babies}
    rooms {self.rooms}
    food {self.resources['food']}
    wood {self.resources['wood']}
    clay {self.resources['clay']}
    stone {self.resources['stone']}
    reed {self.resources['reed']}
    grain {self.resources['grain']}
    vegetable {self.resources['vegetable']}
    sheep {self.resources['sheep']}
    pig {self.resources['pig']}
    cow {self.resources['cow']}
    is_first? {self.is_first}
    beg_tokens {self.begging}
'''

def simulate():
    round_count = 0
    max_round_count = 14
    highest_space_index = 30
    automa_deck = AutomaDeck(automa_cards)
    automa_score = 0
    automa_major_points = 0
    automa_majors = 0

    space_map = GameMap(map_spaces.randomize_round_actions())

    human_first_count = 0
    automa_first_count = 0
    human = Human()
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
                human_space = space_map.human_pick_space(human, highest_revealed_index)
                debug(f'Human placed one meeple on {human_space}')
                if human_space == 'MP':
                    first_player = 'human'
                    human.is_first = True
                space = space_map.get_space_by_abbr(human_space)
                if space.action.has_growth and human.workers < 5:
                    human.workers += 1
                if space.action.boon_count() > 0:
                    human.gain_resources(space.action.take_resources())
                if space.action.has_major and len(list(claimed_majors.keys())) < 10:
                    for ii in range(0,10):
                        if not ii in claimed_majors:
                            claimed_majors[ii] = True
                            break
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