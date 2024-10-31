import csv
import random
import functools
import math
import pprint
import itertools
import copy

difficulty = 0
iterations = 1000

class MapSpace:
    def __init__(self, space_index, abbr, compass, props):
        self.name = props['name']
        self.props = props
        self.space_index = space_index
        self.abbr = abbr
        self.compass_lookup = compass
        self.has_long_west_edge = 'long_west_edge' in props

map_spaces = [
    MapSpace(1,'C',{'N':'0','NE':'0','E':'FE','SE':'MP','S':'G','SW':'0','W':'0','NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',{'N':'C','NE':'FE','E':'MP','SE':'GS','S':'RM','SW':'0','W':'0','NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM',{'N':'G','NE':'MP','E':'GS','SE':'F1','S':'H','SW':'0','W':'0','NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',{'N':'RM','NE':'GS','E':'F1','SE':'L2','S':'L1','SW':'0','W':'0','NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1',{'N':'H','NE':'F1','E':'L2','SE':'DL','S':'TP','SW':'0','W':'0','NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP',{'N':'L1','NE':'L2','E':'DL','SE':'0','S':'0','SW':'0','W':'0','NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE',{'N':'0','NE':'0','E':'1','SE':'1','S':'MP','SW':'G','W':'C','NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP',{'N':'FE','NE':'1','E':'1','SE':'F2','S':'GS','SW':'RM','W':'G','NW':'C'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False}),
    MapSpace(9,'GS',{'N':'MP','NE':'1','E':'F2','SE':'CP','S':'F1','SW':'H','W':'RM','NW':'G'},{'name':'Grain Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(10,'F1',{'N':'GS','NE':'F2','E':'CP','SE':'RB','S':'L2','SW':'L1','W':'H','NW':'RM'},{'name':'Farmland','gain':None,'hits':0,'scores':False}),
    MapSpace(11,'L2',{'N':'F1','NE':'CP','E':'RB','SE':'F3','S':'DL','SW':'TP','W':'L1','NW':'H'},{'name':'Lessons2','gain':None,'hits':0,'scores':False}),
    MapSpace(12,'DL',{'N':'L2','NE':'RB','E':'F3','SE':'0','S':'0','SW':'0','W':'TP','NW':'L1'},{'name':'Day Laborer','gain':None,'hits':0,'scores':False}),
    MapSpace(13,'1',{'N':'0','NE':'0','E':'2','SE':'3','S':'F2','SW':'GS','W':'MP','NW':'FE'},{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True,'long_west_edge':True}),
    MapSpace(14,'F2',{'N':'1','NE':'2','E':'3','SE':'3','S':'CP','SW':'F1','W':'GS','NW':'MP'},{'name':'Forest','gain':'wood','hits':0,'scores':True}),
    MapSpace(15,'CP',{'N':'F2','NE':'3','E':'3','SE':'4','S':'RB','SW':'L2','W':'F1','NW':'GS'},{'name':'Clay Pit','gain':'clay','hits':0,'scores':True}),
    MapSpace(16,'RB',{'N':'CP','NE':'3','E':'4','SE':'4','S':'F3','SW':'DL','W':'L2','NW':'F1'},{'name':'Reed Bank','gain':'reed','hits':0,'scores':True}),
    MapSpace(17,'F3',{'N':'RB','NE':'4','E':'4','SE':'0','S':'0','SW':'0','W':'DL','NW':'L2'},{'name':'Fishing','gain':'food','hits':0,'scores':True}),
    MapSpace(18,'2',{'N':'0','NE':'0','E':'5','SE':'6','S':'3','SW':'F2','W':'1','NW':'0'},{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False}),
    MapSpace(19,'3',{'N':'2','NE':'5','E':'6','SE':'7','S':'4','SW':'RB','W':'CP','NW':'1'},{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(20,'4',{'N':'3','NE':'6','E':'7','SE':'0','S':'0','SW':'0','W':'F3','NW':'CP'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(21,'5',{'N':'0','NE':'0','E':'8','SE':'9','S':'6','SW':'3','W':'2','NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6',{'N':'5','NE':'8','E':'9','SE':'0','S':'7','SW':'4','W':'3','NW':'2'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False}),
    MapSpace(23,'7',{'N':'6','NE':'9','E':'0','SE':'0','S':'0','SW':'0','W':'4','NW':'3'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(24,'8',{'N':'0','NE':'0','E':'10','SE':'11','S':'9','SW':'6','W':'5','NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9',{'N':'8','NE':'10','E':'11','SE':'0','S':'0','SW':'7','W':'6','NW':'5'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'0','NE':'0','E':'12','SE':'13','S':'11','SW':'9','W':'8','NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'12','E':'13','SE':'0','S':'0','SW':'0','W':'9','NW':'8'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'0','NE':'0','E':'14','SE':'0','S':'13','SW':'11','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(29,'13',{'N':'12','NE':'14','E':'0','SE':'0','S':'0','SW':'0','W':'11','NW':'10'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'0','NE':'0','E':'0','SE':'0','S':'0','SW':'13','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]

wrap_around_map_spaces = [
    MapSpace(1,'C',{'N':'0','NE':'0','E':'FE','SE':'MP','S':'G','SW':'0','W':'0','NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',{'N':'C','NE':'FE','E':'MP','SE':'GS','S':'RM','SW':'0','W':'0','NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM',{'N':'G','NE':'MP','E':'GS','SE':'F1','S':'H','SW':'0','W':'0','NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',{'N':'RM','NE':'GS','E':'F1','SE':'L2','S':'L1','SW':'0','W':'0','NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1',{'N':'H','NE':'F1','E':'L2','SE':'DL','S':'TP','SW':'0','W':'0','NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP',{'N':'L1','NE':'L2','E':'DL','SE':'0','S':'0','SW':'0','W':'0','NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE',{'N':'0','NE':'0','E':'1','SE':'1','S':'MP','SW':'G','W':'C','NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP',{'N':'FE','NE':'1','E':'1','SE':'F2','S':'GS','SW':'RM','W':'G','NW':'C'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False}),
    MapSpace(9,'GS',{'N':'MP','NE':'1','E':'F2','SE':'CP','S':'F1','SW':'H','W':'RM','NW':'G'},{'name':'Grain Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(10,'F1',{'N':'GS','NE':'F2','E':'CP','SE':'RB','S':'L2','SW':'L1','W':'H','NW':'RM'},{'name':'Farmland','gain':None,'hits':0,'scores':False}),
    MapSpace(11,'L2',{'N':'F1','NE':'CP','E':'RB','SE':'F3','S':'DL','SW':'TP','W':'L1','NW':'H'},{'name':'Lessons2','gain':None,'hits':0,'scores':False}),
    MapSpace(12,'DL',{'N':'L2','NE':'RB','E':'F3','SE':'0','S':'0','SW':'0','W':'TP','NW':'L1'},{'name':'Day Laborer','gain':None,'hits':0,'scores':False}),
    MapSpace(13,'1',{'N':'0','NE':'0','E':'2','SE':'3','S':'F2','SW':'GS','W':'MP','NW':'FE'},{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True,'long_west_edge':True}),
    MapSpace(14,'F2',{'N':'1','NE':'2','E':'3','SE':'3','S':'CP','SW':'F1','W':'GS','NW':'MP'},{'name':'Forest','gain':'wood','hits':0,'scores':True}),
    MapSpace(15,'CP',{'N':'F2','NE':'3','E':'3','SE':'4','S':'RB','SW':'L2','W':'F1','NW':'GS'},{'name':'Clay Pit','gain':'clay','hits':0,'scores':True}),
    MapSpace(16,'RB',{'N':'CP','NE':'3','E':'4','SE':'4','S':'F3','SW':'DL','W':'L2','NW':'F1'},{'name':'Reed Bank','gain':'reed','hits':0,'scores':True}),
    MapSpace(17,'F3',{'N':'RB','NE':'4','E':'4','SE':'0','S':'0','SW':'0','W':'DL','NW':'L2'},{'name':'Fishing','gain':'food','hits':0,'scores':True}),
    MapSpace(18,'2',{'N':'0','NE':'0','E':'5','SE':'6','S':'3','SW':'F2','W':'1','NW':'0'},{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False}),
    MapSpace(19,'3',{'N':'2','NE':'5','E':'6','SE':'7','S':'4','SW':'RB','W':'CP','NW':'1'},{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(20,'4',{'N':'3','NE':'6','E':'7','SE':'0','S':'0','SW':'0','W':'F3','NW':'CP'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(21,'5',{'N':'0','NE':'0','E':'8','SE':'9','S':'6','SW':'3','W':'2','NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6',{'N':'5','NE':'8','E':'9','SE':'0','S':'7','SW':'4','W':'3','NW':'2'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False}),
    MapSpace(23,'7',{'N':'6','NE':'9','E':'0','SE':'0','S':'0','SW':'0','W':'4','NW':'3'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(24,'8',{'N':'0','NE':'0','E':'10','SE':'11','S':'9','SW':'6','W':'5','NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9',{'N':'8','NE':'10','E':'11','SE':'0','S':'0','SW':'7','W':'6','NW':'5'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'0','NE':'0','E':'12','SE':'13','S':'11','SW':'9','W':'8','NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'12','E':'13','SE':'0','S':'0','SW':'0','W':'9','NW':'8'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'0','NE':'0','E':'14','SE':'0','S':'13','SW':'11','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(29,'13',{'N':'12','NE':'14','E':'0','SE':'0','S':'0','SW':'0','W':'11','NW':'10'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'0','NE':'0','E':'0','SE':'0','S':'0','SW':'13','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]

ortho_map_spaces = [
    MapSpace(1,'C',  {'N':'0', 'NE':'0','E':'FE','SE':'0','S':'G', 'SW':'0','W':'0', 'NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',  {'N':'C', 'NE':'0','E':'MP','SE':'0','S':'RM','SW':'0','W':'0', 'NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM', {'N':'G', 'NE':'0','E':'GS','SE':'0','S':'H', 'SW':'0','W':'0', 'NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',  {'N':'RM','NE':'0','E':'F1','SE':'0','S':'L1','SW':'0','W':'0', 'NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1', {'N':'H', 'NE':'0','E':'L2','SE':'0','S':'TP','SW':'0','W':'0', 'NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP', {'N':'L1','NE':'0','E':'DL','SE':'0','S':'0', 'SW':'0','W':'0', 'NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE', {'N':'0', 'NE':'0','E':'1', 'SE':'0','S':'MP','SW':'0','W':'C', 'NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP', {'N':'FE','NE':'0','E':'1', 'SE':'0','S':'GS','SW':'0','W':'G', 'NW':'0'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False}),
    MapSpace(9,'GS', {'N':'MP','NE':'0','E':'F2','SE':'0','S':'F1','SW':'0','W':'RM','NW':'0'},{'name':'Grain Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(10,'F1',{'N':'GS','NE':'0','E':'CP','SE':'0','S':'L2','SW':'0','W':'H', 'NW':'0'},{'name':'Farmland','gain':None,'hits':0,'scores':False}),
    MapSpace(11,'L2',{'N':'F1','NE':'0','E':'RB','SE':'0','S':'DL','SW':'0','W':'L1','NW':'0'},{'name':'Lessons2','gain':None,'hits':0,'scores':False}),
    MapSpace(12,'DL',{'N':'L2','NE':'0','E':'F3','SE':'0','S':'0', 'SW':'0','W':'TP','NW':'0'},{'name':'Day Laborer','gain':None,'hits':0,'scores':False}),
    MapSpace(13,'1', {'N':'0', 'NE':'0','E':'2', 'SE':'0','S':'F2','SW':'0','W':'MP','NW':'0'},{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True,'long_west_edge':True}),
    MapSpace(14,'F2',{'N':'1', 'NE':'0','E':'3', 'SE':'0','S':'CP','SW':'0','W':'GS','NW':'0'},{'name':'Forest','gain':'wood','hits':0,'scores':True}),
    MapSpace(15,'CP',{'N':'F2','NE':'0','E':'3', 'SE':'0','S':'RB','SW':'0','W':'F1','NW':'0'},{'name':'Clay Pit','gain':'clay','hits':0,'scores':True}),
    MapSpace(16,'RB',{'N':'CP','NE':'0','E':'4', 'SE':'0','S':'F3','SW':'0','W':'L2','NW':'0'},{'name':'Reed Bank','gain':'reed','hits':0,'scores':True}),
    MapSpace(17,'F3',{'N':'RB','NE':'0','E':'4', 'SE':'0','S':'0', 'SW':'0','W':'DL','NW':'0'},{'name':'Fishing','gain':'food','hits':0,'scores':True}),
    MapSpace(18,'2', {'N':'0', 'NE':'0','E':'5', 'SE':'0','S':'3', 'SW':'0','W':'1', 'NW':'0'},{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False}),
    MapSpace(19,'3', {'N':'2', 'NE':'0','E':'6', 'SE':'0','S':'4', 'SW':'0','W':'CP','NW':'0'},{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(20,'4', {'N':'3', 'NE':'0','E':'7', 'SE':'0','S':'0', 'SW':'0','W':'F3','NW':'0'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(21,'5', {'N':'0', 'NE':'0','E':'8', 'SE':'0','S':'6', 'SW':'0','W':'2', 'NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6', {'N':'5', 'NE':'0','E':'9', 'SE':'0','S':'7', 'SW':'0','W':'3', 'NW':'0'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False}),
    MapSpace(23,'7', {'N':'6', 'NE':'0','E':'0', 'SE':'0','S':'0', 'SW':'0','W':'4', 'NW':'0'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(24,'8', {'N':'0', 'NE':'0','E':'10','SE':'0','S':'9', 'SW':'0','W':'5', 'NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9', {'N':'8', 'NE':'0','E':'11','SE':'0','S':'0', 'SW':'0','W':'6', 'NW':'0'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'0', 'NE':'0','E':'12','SE':'0','S':'11','SW':'0','W':'8', 'NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'0','E':'13','SE':'0','S':'0', 'SW':'0','W':'9', 'NW':'0'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'0', 'NE':'0','E':'14','SE':'0','S':'13','SW':'0','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(29,'13',{'N':'12','NE':'0','E':'0', 'SE':'0','S':'0', 'SW':'0','W':'11','NW':'0'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'0', 'NE':'0','E':'0', 'SE':'0','S':'0', 'SW':'0','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]

ortho_wrap_around_map_spaces = [
    MapSpace(1,'C',  {'N':'TP','NE':'0','E':'FE','SE':'0','S':'G', 'SW':'0','W':'14', 'NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',  {'N':'C', 'NE':'0','E':'MP','SE':'0','S':'RM','SW':'0','W':'14', 'NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM', {'N':'G', 'NE':'0','E':'GS','SE':'0','S':'H', 'SW':'0','W':'13', 'NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',  {'N':'RM','NE':'0','E':'F1','SE':'0','S':'L1','SW':'0','W':'13', 'NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1', {'N':'H', 'NE':'0','E':'L2','SE':'0','S':'TP','SW':'0','W':'7', 'NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP', {'N':'L1','NE':'0','E':'DL','SE':'0','S':'C', 'SW':'0','W':'7', 'NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE', {'N':'DL','NE':'0','E':'1', 'SE':'0','S':'MP','SW':'0','W':'C', 'NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP', {'N':'FE','NE':'0','E':'1', 'SE':'0','S':'GS','SW':'0','W':'G', 'NW':'0'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False}),
    MapSpace(9,'GS', {'N':'MP','NE':'0','E':'F2','SE':'0','S':'F1','SW':'0','W':'RM','NW':'0'},{'name':'Grain Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(10,'F1',{'N':'GS','NE':'0','E':'CP','SE':'0','S':'L2','SW':'0','W':'H', 'NW':'0'},{'name':'Farmland','gain':None,'hits':0,'scores':False}),
    MapSpace(11,'L2',{'N':'F1','NE':'0','E':'RB','SE':'0','S':'DL','SW':'0','W':'L1','NW':'0'},{'name':'Lessons2','gain':None,'hits':0,'scores':False}),
    MapSpace(12,'DL',{'N':'L2','NE':'0','E':'F3','SE':'0','S':'FE','SW':'0','W':'TP','NW':'0'},{'name':'Day Laborer','gain':None,'hits':0,'scores':False}),
    MapSpace(13,'1', {'N':'F3','NE':'0','E':'2', 'SE':'0','S':'F2','SW':'0','W':'MP','NW':'0'},{'name':'Stage 1 - Sheep Market','gain':'animal','hits':0,'scores':True,'long_west_edge':True}),
    MapSpace(14,'F2',{'N':'1', 'NE':'0','E':'3', 'SE':'0','S':'CP','SW':'0','W':'GS','NW':'0'},{'name':'Forest','gain':'wood','hits':0,'scores':True}),
    MapSpace(15,'CP',{'N':'F2','NE':'0','E':'3', 'SE':'0','S':'RB','SW':'0','W':'F1','NW':'0'},{'name':'Clay Pit','gain':'clay','hits':0,'scores':True}),
    MapSpace(16,'RB',{'N':'CP','NE':'0','E':'4', 'SE':'0','S':'F3','SW':'0','W':'L2','NW':'0'},{'name':'Reed Bank','gain':'reed','hits':0,'scores':True}),
    MapSpace(17,'F3',{'N':'RB','NE':'0','E':'4', 'SE':'0','S':'1', 'SW':'0','W':'DL','NW':'0'},{'name':'Fishing','gain':'food','hits':0,'scores':True}),
    MapSpace(18,'2', {'N':'4', 'NE':'0','E':'5', 'SE':'0','S':'3', 'SW':'0','W':'1', 'NW':'0'},{'name':'Stage 1 - Fencing','gain':None,'hits':0,'scores':False}),
    MapSpace(19,'3', {'N':'2', 'NE':'0','E':'6', 'SE':'0','S':'4', 'SW':'0','W':'CP','NW':'0'},{'name':'Stage 1 - Grain Utilization','gain':None,'hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(20,'4', {'N':'3', 'NE':'0','E':'7', 'SE':'0','S':'2', 'SW':'0','W':'F3','NW':'0'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True}),
    MapSpace(21,'5', {'N':'7', 'NE':'0','E':'8', 'SE':'0','S':'6', 'SW':'0','W':'2', 'NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6', {'N':'5', 'NE':'0','E':'9', 'SE':'0','S':'7', 'SW':'0','W':'3', 'NW':'0'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False}),
    MapSpace(23,'7', {'N':'6', 'NE':'0','E':'TP','SE':'0','S':'5', 'SW':'0','W':'4', 'NW':'0'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(24,'8', {'N':'9', 'NE':'0','E':'10','SE':'0','S':'9', 'SW':'0','W':'5', 'NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9', {'N':'8', 'NE':'0','E':'11','SE':'0','S':'8', 'SW':'0','W':'6', 'NW':'0'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'11','NE':'0','E':'12','SE':'0','S':'11','SW':'0','W':'8', 'NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'0','E':'13','SE':'0','S':'10','SW':'0','W':'9', 'NW':'0'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'13','NE':'0','E':'14','SE':'0','S':'13','SW':'0','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False}),
    MapSpace(29,'13',{'N':'12','NE':'0','E':'H', 'SE':'0','S':'12','SW':'0','W':'11','NW':'0'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'14','NE':'0','E':'G', 'SE':'0','S':'14','SW':'0','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]

map_spaces = ortho_wrap_around_map_spaces

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

automa_cards = []

card_count = 24

points = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,]
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
    automa_cards.append(AutomaCard(ii,compass_dir,point,delta_row,delta_col))

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

    def walk_spaces(self,max_index,compass_dir,current_space,depth=0):
        if current_space.space_index <= max_index and depth > 0:
            return current_space
        return self.walk_spaces(max_index,compass_dir,self.space_by_abbr[current_space.compass_lookup[compass_dir]],depth+1)

    def automa_claim_space(self, start_index, automa_card, max_space_index):
        next_space = self.space_by_index[start_index]
        while automa_card.has_move_x():
            next_move = automa_card.next_move_x()
            next_space = self.walk_spaces(max_space_index,next_move,next_space,0)
        while automa_card.has_move_y():
            next_move = automa_card.next_move_y()
            next_space = self.walk_spaces(max_space_index,next_move,next_space,0)
        debug(f"Automa trying to goto {next_space.name}")
        automa_spaces = []
        if self.claimed_spaces[next_space.abbr] == 'empty':
            debug(f"The first space was empty. Going there.")
            self.claimed_spaces[next_space.abbr] = 'automa'
            automa_spaces.append(next_space)
        compass_search_count = 0
        current_compass = automa_card.compass_dir.name
        start_space = next_space
        while compass_search_count < len(compass_dirs) and len(automa_spaces) < 3:
            next_space = self.walk_spaces(max_space_index,current_compass,start_space,0)
            if self.claimed_spaces[next_space.abbr] == 'empty':
                debug(f"A compass space {current_compass} was empty. Going there.")
                self.claimed_spaces[next_space.abbr] = 'automa'
                print(next_space.name)
                automa_spaces.append(next_space)
            current_compass = compass_lookup[current_compass].next
            compass_search_count += 1
        for space in automa_spaces:
            if hasattr(space,'abbr'):
                self.space_hits[space.abbr] += 1
            else:
                self.space_hits[space] += 1
        return automa_spaces

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
        print(map)

    def print_hit_counts(self):
        import plotext as plt

        x_axis = [xx.abbr for xx in map_spaces]
        y_axis = [self.space_hits[xx] for xx in x_axis]

        plt.bar(x_axis, y_axis)
        plt.title("Times Spaces Used")
        plt.show()

    def validate_connections(self):
        print("Ensuring the space map is valid")
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

                    print(f"Mismatch! {space.name} <-> {reverse_end}")
                    print(f"{space.name} points {dir_compass} to {end_space}")
                    print(f'{end_space} points {reverse_dir} to {reverse_end}')
                    errors += 1
        if errors == 0:
            print("No map errors found")
        else:
            print("MAP ERRORS FOUND! See logs above.")

def validate_scores():
    for point in points:
        pass

validate_scores()

def debug(message):
    if True:
        print(message)

def simulate():
    round_count = 0
    max_round_count = 14
    highest_space_index = 30
    automa_deck = AutomaDeck(automa_cards)
    automa_score = 0

    space_map = GameMap(map_spaces)

    human_meeple = 2
    human_turns = human_meeple
    automa_turns = human_turns
    first_player = 'human'
    current_turn = 'human'
    while round_count < max_round_count:
        debug(f'Playing round {round_count+1}')
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
        #if round_count % 2 == 1:
        #    automa_space_index = 1
        for player in turns:
            if player == 'human':
                debug('Taking human turn')
                human_space = space_map.human_claim_random(highest_revealed_index)
                debug(f'Human placed one meeple on {human_space}')
            else:
                debug('Taking automa turn')
                automa_card = automa_deck.draw()
                space_map.automa_claim_space(automa_space_index,automa_card,highest_revealed_index)
                debug(f'Automa plays card: {automa_card}')
                automa_score += automa_card.points
        space_map.display()
        space_map.new_round()
        round_count += 1
    space_map.print_hit_counts()
    debug(f'Game over. Automa scored {automa_score}')

simulate()