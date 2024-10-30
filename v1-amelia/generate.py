import csv
import random
import functools
import math
import pprint
import itertools

difficulty = 0
iterations = 1000
spaces_per_card = 6
card_count = 12
improvements_space_count = 12
spaces_total = spaces_per_card * card_count
spots_total = spaces_total + improvements_space_count
score_spread = 17
scores = [2,3,4,2,3,4,2,3,4,2,3,4]
count_scores = []
fences = [3,3,3,3,3]
scoring = 0.5
nonscoring = 1-scoring
scoring /= 2
nonscoring /= 2
max_repeats = 3


low_all = [2,4,5,6,7,8,9,10,11,0.5,1,3,4.5,12,13,14,15]
high_all = [17,20,21,23,26,27,28,16,19,22,24,25]
score_all = [0.5,1,3,4.5,12,13,14,15,16,18,19,22,24,25]

low_spaces = [2,4,5,6,7,8,9,10,11]
low_scoring_spaces = [0.5,1,3,4.5,12,13,14,15]
high_spaces = [17,20,21,23,26,27,28]
high_scoring_spaces = [16,18,19,22,24,25]

all_scoring_spaces = low_scoring_spaces + high_scoring_spaces

low_always_priority = [6,12,3,9,8,10,2,14]
low_early_priority = [1,13,10,15,0.5]
low_late_priority = [15,4.5,7,5,4,11]

high_always_priority = [16,19,22,24,25]
high_early_priority = [21,20,18,17]
high_late_priority = [28,27,26,23]

always_priority = low_always_priority + high_always_priority
early_priority = low_early_priority + high_early_priority
late_priority = low_late_priority + high_late_priority

all_priorities = low_always_priority + low_early_priority + low_late_priority + high_always_priority + high_early_priority + high_late_priority

spaces = {
    0:{'gain':None,'hits':0,'scores':True},
    0.5:{'name':'Copse','gain':'wood','hits':0,'scores':True},
    1:{'name':'Grove','gain':'wood','hits':0,'scores':True},
    2:{'name':'Resource Market','gain':None,'hits':0,'scores':False},
    3:{'name':'Hollow','gain':'clay','hits':0,'scores':True},
    4:{'name':'Lessons','gain':None,'hits':0,'scores':False},
    4.5:{'name':'Traveling Players','gain':'food','hits':0,'scores':True},
    5:{'name':'Farm Expansion','gain':None,'hits':0,'scores':False},
    6:{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False},
    7:{'name':'Grain Seeds','gain':None,'hits':0,'scores':False},
    8:{'name':'Farmland','gain':None,'hits':0,'scores':False},
    9:{'name':'Lessons2','gain':None,'hits':0,'scores':False},
    10:{'name':'Day Laborer','gain':None,'hits':0,'scores':False},
    11:{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True},
    12:{'name':'Forest','gain':'wood','hits':0,'scores':True},
    13:{'name':'Clay Pit','gain':'clay','hits':0,'scores':True},
    14:{'name':'Reed Bank','gain':'reed','hits':0,'scores':True},
    15:{'name':'Fishing','gain':'food','hits':0,'scores':True},
    16:{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False},
    17:{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False},
    18:{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False},
    19:{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True},
    20:{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False},
    21:{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False},
    22:{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True},
    23:{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False},
    24:{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True},
    25:{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True},
    26:{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False},
    27:{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False},
    28:{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}
}

for space in spaces:
    if space != 0:
        if not space in all_priorities:
            raise Exception(f"Space [{space}] has no priority!")
        if not all_priorities.count(space):
            raise Exception(f"Found duplicate priority for [{space}]")


frequency = {}
improvements = [16,19,22,24,26,17,20,23,25,27]
improvements2 = [1,2,3,4,5,6,7,8,9,10]
improvements3 = [0,1,1,1,1,4,2,3,2,2,2]
improvementLookup = {
    1:16,
    2:19,
    3:22,
    4:24,
    5:26,
    6:17,
    7:20,
    8:23,
    9:25,
    10:27
}
scoring_count = 0
unscored_count = 0
high_count = 0
low_count = 0
cards = [[],[],[],[],[],[],[],[],[],[],[],[]]
card_hits ={
    0:[],
    1:[],
    2:[],
    3:[],
    4:[],
    5:[],
    6:[],
    7:[],
    8:[],
    9:[],
    10:[],
    11:[]
}

sets = [
    low_spaces, low_scoring_spaces, high_spaces, high_scoring_spaces
]

set_counts = [
    0,0,0,0
]

set_target_counts = [
    math.floor(nonscoring * spaces_total),
    math.floor(scoring * spaces_total),
    math.floor(nonscoring * spaces_total),
    math.floor(scoring * spaces_total),
]

def get_spot(card_index):
    global spaces_total
    global improvements_space_count
    global set_percent_targets
    global set_counts
    global sets
    global spaces
    target_slot = len(cards[card_index])
    target_spaces = always_priority + early_priority + late_priority
    if target_slot <= 3:
        target_spaces = early_priority + always_priority + late_priority
    if target_slot >=6:
        target_spaces = late_priority + always_priority + early_priority

    lows = 0
    highs = 0
    itscores = 0
    itunscores = 0
    for ii in range(1,len(cards[card_index])):
        if cards[card_index][ii] > 15:
            highs += 1
        else:
            lows += 1
        if cards[card_index][ii] in all_scoring_spaces:
            itscores += 1
        else:
            itunscores += 1

    valid_spaces = []
    for target in target_spaces:
        if lows >= 3 and target <= 15 or highs >= 3 and target > 15:
            continue
        if itscores > itunscores and target in all_scoring_spaces:
            continue
        if target in frequency and frequency[target] > 3:
            continue
        if not target in cards[card_index] and not spaces[target]['gain'] in card_hits[card_index]:
            valid_spaces.append(target)
    if len(valid_spaces) < 1:
        pprint.pprint(cards)
        raise Exception("No valid spaces left to choose!")

    lowest = 10
    next = None
    for valid in valid_spaces:
        if spaces[valid]['hits'] < lowest:
            next = valid
            lowest = spaces[valid]['hits']

    if next == None:
        pprint.pprint(cards)
        raise Exception("No valid spaces left to choose!")

    spaces[next]['hits'] += 1
    if spaces[next]['gain'] != None:
        card_hits[card_index].append(spaces[next]['gain'])
    if not next in frequency:
        frequency[next] = 1
    else:
        frequency[next] = frequency[next] + 1

    found_index = 0
    for ii in range(0,len(sets)):
        if next in sets[ii]:
            found_index = ii

    set_counts[found_index] += 1

    return next

spot_count = 0
for ii in range(0,spaces_per_card + 1):
    for jj in range(0,card_count):
        if ii == 0:
            if len(improvements) > 0:
                cards[jj].append(improvements.pop(0))
            else:
                cards[jj].append(0)
                card_hits[jj].append('improvement')
        else:
            cards[jj].append(get_spot(jj))
        spot_count += 1

unscored_count = set_counts[0] + set_counts[2]
scoring_count = set_counts[1] + set_counts[3]
low_count = set_counts[0] + set_counts[1]
high_count = set_counts[2] + set_counts[3]

print(f"Spots placed [{spot_count}]")

scored_cards = 12
for card in cards:
    card.pop(0)
    if len(improvements2) > 0:
        card.append(improvements2.pop(0))
    else:
        card.append(0)
    next_score = scores.pop(0)
    card.append(next_score)
    count_scores.append(next_score)

print("Overriding card list")
cards = [
    [1, 9, 24, 6, 22, 28, 1, 3],           # 0
    [13, 8, 25, 9, 24, 27, 2, 3],          # 1
    [10, 2, 4.5, 16, 25, 26, 3, 3],        # 2
    [15, 0.5, 27, 12, 20, 23, 4, 3],         # 3
    [7, 5, 23, 3, 18, 24, 5, 3],         # 4
    [21, 14, 26, 8, 4.5, 16, 6, 4],        # 5
    [18, 4, 1, 2, 28, 19, 7, 4],           # 6
    [20, 16, 13, 17, 4, 15, 8, 4],         # 7
    [17, 19, 10, 14, 11, 20, 9, 2],        # 8
    [4, 22, 0.5, 7, 26, 21, 10, 2],         # 9
    [12, 11, 21, 19, 27, 4.5, 0, 4],       # 10
    [6, 28, 15, 5, 23, 22, 0, 2]          # 11
]

count_scores = [x[-1] for x in cards]

print_cards = []
letters = ["A","B","C","D","E","F","G","H","I","J","K","L",]
card_index = 0
for card in cards:
    print_card = [letters[card_index]] + card.copy()
    print_cards.append(print_card)
    card_index += 1

headers = []
for ii in range(0,spaces_per_card):
    headers.append(f"P{ii+1}")
headers = ["Letter"] + headers + ['Major','Score']

with open('./agricola.csv','w',newline='') as fp:
    writer = csv.writer(fp, delimiter=",")
    writer.writerow(headers)
    writer.writerows(print_cards)

priorities = {}
scored_spaces = []
card_index = 0
for card in cards:
    score = 0
    unscore = 0
    next_count = 1
    score_yes = 0
    score_no = 0
    for next in card:
        if next_count < spaces_per_card + 1:
            if not next in priorities:
                priorities[next] = [next_count]
            else:
                priorities[next].append(next_count)
            if next in low_spaces or next in high_spaces:
                unscore += 1
                score_no += 1
            else:
                score += 1
                score_yes += 1
        next_count += 1
    scored_spaces.append([score_yes, score_no, card[-1], card_index])
    card_index += 1
    #print(f"card - scoring spots [{score}] and unscored spots [{unscore}]")
#pprint.pprint(card_hits)
#pprint.pprint(priorities)
print("Frequency")
pprint.pprint(frequency)
print("Always Priority Frequency")
for spot in always_priority:
    print(f"space [{spot}] = repeats [{frequency[spot]}] - [{spaces[spot]['name']}] - priority list [{priorities[spot]}]")
print("Early Priority Frequency")
for spot in early_priority:
    print(f"space [{spot}] = repeats [{frequency[spot]}] - [{spaces[spot]['name']}] - priority list [{priorities[spot]}]")
print("Late Priority Frequency")
for spot in late_priority:
    print(f"space [{spot}] = repeats [{frequency[spot]}] - [{spaces[spot]['name']}] - priority list [{priorities[spot]}]")
print(f"scoring spots [{scoring_count}] and unscored spots [{unscored_count}]")
print(f"high spots [{high_count}] and low spots [{low_count}]")
print("Card list")
pprint.pprint(cards)
pprint.pprint(scored_spaces)


print("Acheived these stats")
pprint.pprint([
    scoring,
    nonscoring,
    f"Low Score Spaces [{set_counts[1]}]",
    f"Low Spaces [{set_counts[0]}]",
    f"High Score Spaces [{set_counts[3]}]",
    f"High Spaces [{set_counts[2]}]"
])

for k,v in spaces.items():
    if spaces[k]['hits'] == 0 and k != 0:
        raise Exception(f"Space [{k}] was not included in the deck!")
for ii in range(0, len(cards)):
    card = cards[ii]
    card_dupe = {}
    for jj in range(0,len(card)):
        if card[-2] != 0 and jj < len(card)-2 and card[jj] == improvementLookup[card[-2]]:
            raise Exception(f"Card [{ii}] collides improvement [{card[-2]}]->[{improvementLookup[card[-2]]}]")
        if jj < len(card) - 2:
            if not card[jj] in card_dupe:
                card_dupe[card[jj]] = jj
            else:
                raise Exception(f"Duplicate card space! Card [{ii}] at spaces [{jj}] and [{card_dupe[card[jj]]}]")


# https://stackoverflow.com/a/31581790/389499
sequence_hits = {}
card_index = 0
for card in cards:
    dupe = card.copy()
    dupe.pop()
    dupe.pop()
    dupe.sort()
    for ii,jj in itertools.combinations(range(len(dupe) + 1), 2):
        key = ','.join([str(x) for x in dupe[ii:jj]])
        if not key in sequence_hits:
            sequence_hits[key] = [card_index]
        else:
            sequence_hits[key].append(card_index)
    card_index += 1
for k,v in sequence_hits.items():
    sequence_length = len(k.split(','))
    if len(v) > 1 and sequence_length > 1:
        #raise Exception(f"More than two space sequence [{k}] is repeated [{sequence_length}]")
        print(f"More than two space sequence [{k}] is repeated [{sequence_length}] at [{v}]")

def reset_board(current_round):
    global spaces
    board = {}
    space_limit = 16 + current_round
    for key,val in spaces.items():
        board[key] = {
            'taken': False,
            'scores': val['scores'],
            'available': space_limit > 0
        }
        space_limit -=1
    return board

def human_play(board):
    spaces = list(board.keys())
    random.shuffle(spaces)
    took_first = False
    for space in spaces:
        if board[space]['available'] and not board[space]['taken']:
            board[space]['taken'] = True
            if space == 6:
                took_first = True
                debug_game("GAME - Human took the first player pawn")
            debug_game(f"GAME - Player took space [{space}]")
            break
    return board,took_first

def debug_game(message):
    pass#print(message)

def draw_card(cards,current_card):
    if current_card >= len(cards) - 2:
        debug_game("GAME - Shuffling the automa deck")
        current_card = 0
        random.shuffle(cards)
    else:
        current_card += 1
    card = cards[current_card].copy()
    debug_game(f"GAME - Using automa card [{card}]")
    return cards,card,current_card

def amelia_play(board,cards,card_index,person,humans):
    global improvements3
    global fences
    current_card = card_index
    took_first = False
    score = 0

    cards,card,current_card = draw_card(cards,current_card)
    card_score = card.pop()
    card_improvement = card.pop()

    fence_count = 0
    fence_max = fences[person]
    if humans == 2:
        fence_max -= 1
    scored = False
    improvements_taken = 0
    improvement_points = 0

    for ii in range(0,len(card)):
        space = card[ii]
        if fence_count >= fence_max:
            break
        if board[space]['available'] and not board[space]['taken']:
            if humans == 2 and not board[space]['scores'] and person == 0:
                continue
            board[space]['taken'] = True
            if board[space]['scores']:
                scored = True
                debug_game(f"GAME - Amelia took [{space}] and will score [{card_score if board[space]['scores'] else 0}] points")
            if space == 6:
                took_first = True
                debug_game("GAME - Amelia took the first player pawn")
            if space == 18 or space == 20:
                cards,improvement_card,current_card = draw_card(cards,current_card)
                if improvements3[improvement_card[-2]] != 0:
                    if difficulty == 1:
                        score += improvements3[improvement_card[-2]]
                        improvement_points += improvements3[improvement_card[-2]]
                        improvements3[improvement_card[-2]] = 0
                        improvements_taken += 1
                debug_game(f"GAME - Amelia took improvement [{improvement_card[-2]}]")
            fence_count += 1
    if scored and person == 0:
        score += card_score
    return board,took_first,score,current_card,cards,improvements_taken,improvement_points

aggressive_growth = [6,7,8]

def play_game(cards,growth,humans):
    round = 0
    people_max = 2
    first = False
    board = reset_board(1)
    amelia_score = 0
    improvements_taken = 0
    improvement_points = 0
    card_index = 0
    random.shuffle(cards)
    while round < 14:
        round += 1
        if round == 7:
            for card in cards:
                score = card.pop()
                improvement = card.pop()
                card.reverse()
                card.append(improvement)
                card.append(score)
        debug_game(f"GAME - Round [{round}]")
        if growth:
            if round in aggressive_growth:
                people_max += 1
        people = people_max
        if first:
            for ii in range(0,people):
                board,took_first,score,card_index,cards,i_taken,i_points = amelia_play(board,cards,card_index,ii,humans)
                amelia_score += score
                improvements_taken += i_taken
                improvement_points += i_points
                if took_first:
                    first = True
                board,took_first = human_play(board)
                if took_first:
                    first = False
                if humans == 2:
                    board,took_first = human_play(board)
                    if took_first:
                        first = False
        else:
            for ii in range(0,people):
                board,took_first = human_play(board)
                if took_first:
                    first = False
                if humans == 2:
                    board,took_first = human_play(board)
                if took_first:
                    first = False
                board,took_first,score,card_index,cards,i_taken,i_points = amelia_play(board,cards,card_index,ii,humans)
                if took_first:
                    first = True
                amelia_score += score
                improvements_taken += i_taken
        board = reset_board(round)
    return amelia_score,improvements_taken,improvement_points

def simulate(challenge, humans):
    global difficulty
    global iterations
    difficulty = challenge
    growth_scores = []
    growth_improvements = []
    small_scores = []
    small_improvements = []
    for ii in range(0,iterations):
        score,improvements,improvement_points = play_game(cards,True,humans)
        growth_scores.append(score)
        growth_improvements.append(improvement_points)

        score,improvements,improvement_points = play_game(cards,False,humans)
        small_scores.append(score)
        small_improvements.append(improvement_points)

    print(f"Difficulty Level [{challenge}]")
    print(f"Humans [{humans}]")
    print(f"Five Workers\n\tscores: min [{min(growth_scores)}] max [{max(growth_scores)}] mean [{sum(growth_scores)/len(growth_scores)}]\n\timprovements max [{max(growth_improvements)}] min [{min(growth_improvements)}] mean [{sum(growth_improvements)/len(growth_improvements)}]")
    print(f"Two Workers\n\tscores: min [{min(small_scores)}] max [{max(small_scores)}] mean [{sum(small_scores)/len(small_scores)}]\n\timprovements max [{max(small_improvements)}] min [{min(small_improvements)}] mean [{sum(small_improvements)/len(small_improvements)}]")

simulate(0, 1)
simulate(1, 1)
simulate(0, 2)
simulate(1, 2)

low_total = 0
count_scores.sort()
round_count = 0
while round_count < 14:
    for ii in range(0,len(count_scores)-2):
        round_count += 1
        low_total += count_scores[ii]
        if round_count >= 13:
            break;

high_total = 0
count_scores.reverse()
round_count = 0
while round_count < 14:
    for ii in range(0,len(count_scores)-2):
        round_count += 1
        high_total += count_scores[ii]
        if round_count >= 13:
            break;

print(f"Estimated low score [{low_total}] and high score [{high_total}]")