import copy
import random

class MapSpace:
    def __init__(self, space_index, abbr, compass, action=None,long_west_edge=False):
        self.space_index = space_index
        self.abbr = abbr
        self.compass_lookup = compass
        self.action = action
        self.has_long_west_edge = long_west_edge

    def __str__(self):
        return f"MapSpace: {self.abbr}, {self.space_index}, {self.action.name}"

class ActionCard:
    def __init__(self,stage,name,gain=None,accumulate=False,action=None,long_west_edge=False):
        self.has_long_west_edge = long_west_edge
        self.has_major = False if not action else 'major' in action
        self.has_minor = False if not action else 'minor' in action
        self.has_growth = False if not action else 'growth' in action
        self.accumulate = accumulate
        self.gain = gain
        self.action = action
        self.name = name
        self.stage = stage
        self.resources = {}
        if self.gain:
            for xx in self.gain:
                self.resources[xx[0]] = 0 if self.accumulate else xx[1]
        else:
            self.resources = {}

    def boon_count(self):
        return sum(self.resources[xx] for xx in list(self.resources.keys()))

    def take_resources(self):
        resources = copy.deepcopy(self.resources)
        if self.accumulate:
            for xx in self.gain:
                self.resources[xx[0]] = 0
        return resources

    def has_resource(self,name):
        return 0 if not name in self.resources else self.resources[name]

    def has_action(self,name):
        if self.action:
            return name in self.action
        return False

    def refill(self):
        if self.gain and self.accumulate:
            for rate in self.gain:
                self.resources[rate[0]] += rate[1]

map_spaces = [
    MapSpace(space_index=1, abbr='C', compass={'N':'TP','E':'FE','S':'G', 'W':'14'}, action=ActionCard(stage=0,name='Copse',gain=[['wood',1]],accumulate=True)),
    MapSpace(space_index=2, abbr='G', compass={'N':'C', 'E':'MP','S':'RM','W':'14'}, action=ActionCard(stage=0,name='Grove',gain=[['wood',2]],accumulate=True)),
    MapSpace(space_index=3, abbr='RM',compass={'N':'G', 'E':'GS','S':'H', 'W':'13'}, action=ActionCard(stage=0,name='Resource Market',gain=[['reed',1],['stone',1],['food',1]])),
    MapSpace(space_index=4, abbr='H', compass={'N':'RM','E':'F1','S':'L1','W':'13'}, action=ActionCard(stage=0,name='Hollow',gain=[['clay',2]],accumulate=True)),
    MapSpace(space_index=5, abbr='L1',compass={'N':'H', 'E':'L2','S':'TP','W':'7'},  action=ActionCard(stage=0,name='Lessons1',action=['occupation'])),
    MapSpace(space_index=6, abbr='TP',compass={'N':'L1','E':'DL','S':'C', 'W':'7'},  action=ActionCard(stage=0,name='Traveling Players',gain=[['food',1]],accumulate=True)),
    MapSpace(space_index=7, abbr='FE',compass={'N':'DL','E':'1', 'S':'MP','W':'C'},  action=ActionCard(stage=0,name='Farm Expansion',action=['room','stable'])),
    MapSpace(space_index=8, abbr='MP',compass={'N':'FE','E':'1', 'S':'GS','W':'G'},  action=ActionCard(stage=0,name='Meeting Place',action=['start_player','minor'])),
    MapSpace(space_index=9, abbr='GS',compass={'N':'MP','E':'F2','S':'F1','W':'RM'}, action=ActionCard(stage=0,name='Grain Seeds',gain=[['grain',1]])),
    MapSpace(space_index=10,abbr='F1',compass={'N':'GS','E':'CP','S':'L2','W':'H'},  action=ActionCard(stage=0,name='Farmland',action=['plow'])),
    MapSpace(space_index=11,abbr='L2',compass={'N':'F1','E':'RB','S':'DL','W':'L1'}, action=ActionCard(stage=0,name='Lessons2',action=['occupation'])),
    MapSpace(space_index=12,abbr='DL',compass={'N':'L2','E':'F3','S':'FE','W':'TP'}, action=ActionCard(stage=0,name='Day Laborer',gain=[['food',2]])),
    MapSpace(space_index=13,abbr='1', compass={'N':'F3','E':'2', 'S':'F2','W':'MP'}, long_west_edge=True),
    MapSpace(space_index=14,abbr='F2',compass={'N':'1', 'E':'3', 'S':'CP','W':'GS'}, action=ActionCard(stage=0,name='Forest',gain=[['wood',3]],accumulate=True)),
    MapSpace(space_index=15,abbr='CP',compass={'N':'F2','E':'3', 'S':'RB','W':'F1'}, action=ActionCard(stage=0,name='Clay Pit',gain=[['clay',1]],accumulate=True)),
    MapSpace(space_index=16,abbr='RB',compass={'N':'CP','E':'4', 'S':'F3','W':'L2'}, action=ActionCard(stage=0,name='Reed Bank',gain=[['reed',1]],accumulate=True)),
    MapSpace(space_index=17,abbr='F3',compass={'N':'RB','E':'4', 'S':'1', 'W':'DL'}, action=ActionCard(stage=0,name='Fishing',gain=[['food',1]],accumulate=True)),
    MapSpace(space_index=18,abbr='2', compass={'N':'4', 'E':'5', 'S':'3', 'W':'1'}),
    MapSpace(space_index=19,abbr='3', compass={'N':'2', 'E':'6', 'S':'4', 'W':'CP'}, long_west_edge=True),
    MapSpace(space_index=20,abbr='4', compass={'N':'3', 'E':'7', 'S':'2', 'W':'F3'}, long_west_edge=True),
    MapSpace(space_index=21,abbr='5', compass={'N':'7', 'E':'8', 'S':'6', 'W':'2'}),
    MapSpace(space_index=22,abbr='6', compass={'N':'5', 'E':'9', 'S':'7', 'W':'3'}),
    MapSpace(space_index=23,abbr='7', compass={'N':'6', 'E':'TP','S':'5', 'W':'4'}),
    MapSpace(space_index=24,abbr='8', compass={'N':'9', 'E':'10','S':'9', 'W':'5'}),
    MapSpace(space_index=25,abbr='9', compass={'N':'8', 'E':'11','S':'8', 'W':'6'}),
    MapSpace(space_index=26,abbr='10',compass={'N':'11','E':'12','S':'11','W':'8'}),
    MapSpace(space_index=27,abbr='11',compass={'N':'10','E':'13','S':'10','W':'9'}),
    MapSpace(space_index=28,abbr='12',compass={'N':'13','E':'14','S':'13','W':'10'}),
    MapSpace(space_index=29,abbr='13',compass={'N':'12','E':'H', 'S':'12','W':'11'}),
    MapSpace(space_index=30,abbr='14',compass={'N':'14','E':'G', 'S':'14','W':'12'})
]

def get_last_abbr(max_index):
    return map_spaces[max_index-1].abbr

# This is getting too complicated in real life. Simplify the rules
def walk_from_space(max_index,round,start_abbr,compass,wrap_shift,top):
    if start_abbr == 'C':
        if compass == 'E':
            return 'FE'
        if compass == 'S':
            return 'G'
        if compass == 'N':
            if wrap_shift:
                return get_last_abbr(max_index)
            else:
                return 'TP'
        if compass == 'W':
            if wrap_shift:
                if round < 4:
                    return 'F3'
                if round < 7:
                    return '4'
                return '7'
            else:
                if round < 2:
                    return '1'
                if round < 5:
                    return '2'
                if round < 8:
                    return '5'
                if round < 10:
                    return '8'
                if round < 12:
                    return '10'
                if round < 14:
                    return '12'
                return '10'

action_cards = [
    ActionCard(stage=1,name='Sheep Market',gain=[['sheep',1]],accumulate=True),
    ActionCard(stage=1,name='Fencing',action=['fence']),
    ActionCard(stage=1,name='Grain Utilization',action=['sow','bake']),
    ActionCard(stage=1,name='Major Improvement',action=['major','minor']),
    ActionCard(stage=2,name='Western Quarry',gain=[['stone',1]],accumulate=True),
    ActionCard(stage=2,name='House Redevelopment',action=['renovate','major','minor']),
    ActionCard(stage=2,name='Basic Wish for Children',action=['growth','minor']),
    ActionCard(stage=3,name='Pig Market',gain=[['pig',1]],accumulate=True),
    ActionCard(stage=3,name='Vegetable Seeds',gain=[['vegetable',1]]),
    ActionCard(stage=4,name='Eastern Quarry',gain=[['stone',1]],accumulate=True),
    ActionCard(stage=4,name='Cattle Market',gain=[['cow',1]],accumulate=True),
    ActionCard(stage=5,name='Urgent Wish for Children',action=['growth']),
    ActionCard(stage=5,name='Cultivation',action=['plow','sow']),
    ActionCard(stage=6,name='Farm Redevelopment',action=['renovate','fence'])
]

def randomize_round_actions():
    actions = copy.deepcopy(action_cards)
    spaces = copy.deepcopy(map_spaces)
    stage1 = [0,1,2,3]
    stage2 = [4,5,6]
    stage3 = [7,8]
    stage4 = [9,10]
    stage5 = [11,12]
    stage6 = [13]
    random.shuffle(stage1)
    random.shuffle(stage2)
    random.shuffle(stage3)
    random.shuffle(stage4)
    random.shuffle(stage5)
    round_actions = stage1 + stage2 + stage3 + stage4 + stage5 + stage6
    for space in spaces:
        if not space.action:
            space.action = actions[round_actions.pop(0)]
    return spaces

