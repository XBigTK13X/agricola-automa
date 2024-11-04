import copy
import sys
import random
from debug import debug
import map_spaces as ms

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

class GameMap:
    def __init__(self):
        self.space_hits = {}
        self.map_spaces = ms.randomize_round_actions()
        self.space_by_index = {}
        self.space_by_abbr = {}
        for space in self.map_spaces:
            self.space_hits[space.abbr] = 0
            self.space_by_index[space.space_index] = space
            self.space_by_abbr[space.abbr] = space

    def new_round(self,max_index):
        self.claimed_spaces = {}
        for space in self.map_spaces:
            self.claimed_spaces[space.abbr] = 'empty'
            if max_index >= space.space_index:
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
        open_space_abbrs = [xx for xx in keys if self.space_by_abbr[xx].space_index <= max_space_index and self.claimed_spaces[xx] == 'empty']
        open_space_abbrs.sort(key=lambda xx: self.space_by_abbr[xx].action.boon_count(),reverse=True)
        desires = ['food','wood','reed','grain','clay','vegetable','sheep','stone','pig','cow']
        for abbr in open_space_abbrs:
            space = self.get_space_by_abbr(abbr)
            # Try to always be the first player
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
            for abbr in open_space_abbrs:
                space = self.get_space_by_abbr(abbr)
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
            debug(f"{next_space.action.name} was empty. Going there.")
            self.automa_claim(next_space.abbr)
            automa_spaces.append(next_space)
        space_index = next_space.space_index
        dir = 1 if automa_card.horiz_choice == 'bottom' else -1
        while len(automa_spaces) < 3:
            space_index += dir
            if space_index > max_space_index:
                space_index = 1
            if space_index < 1:
                space_index = max_space_index
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