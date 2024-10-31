class MapSpace:
    def __init__(self, space_index, abbr, compass, props,has_major=False,has_minor=False,has_growth=False):
        self.name = props['name']
        self.props = props
        self.space_index = space_index
        self.abbr = abbr
        self.compass_lookup = compass
        self.has_long_west_edge = 'long_west_edge' in props
        self.has_major = has_major
        self.has_minor = has_minor
        self.has_growth = has_growth

    def __str__(self):
        return f"MapSpace: {self.abbr}, {self.space_index}, major {self.has_major}, minor {self.has_minor}, growth {self.has_growth}"

eight_point_map_spaces_no_wrap = [
    MapSpace(1,'C',{'N':'0','NE':'0','E':'FE','SE':'MP','S':'G','SW':'0','W':'0','NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',{'N':'C','NE':'FE','E':'MP','SE':'GS','S':'RM','SW':'0','W':'0','NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM',{'N':'G','NE':'MP','E':'GS','SE':'F1','S':'H','SW':'0','W':'0','NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',{'N':'RM','NE':'GS','E':'F1','SE':'L2','S':'L1','SW':'0','W':'0','NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1',{'N':'H','NE':'F1','E':'L2','SE':'DL','S':'TP','SW':'0','W':'0','NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP',{'N':'L1','NE':'L2','E':'DL','SE':'0','S':'0','SW':'0','W':'0','NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE',{'N':'0','NE':'0','E':'1','SE':'1','S':'MP','SW':'G','W':'C','NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP',{'N':'FE','NE':'1','E':'1','SE':'F2','S':'GS','SW':'RM','W':'G','NW':'C'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False},has_major=True),
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
    MapSpace(20,'4',{'N':'3','NE':'6','E':'7','SE':'0','S':'0','SW':'0','W':'F3','NW':'CP'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True},has_major=True,has_minor=True),
    MapSpace(21,'5',{'N':'0','NE':'0','E':'8','SE':'9','S':'6','SW':'3','W':'2','NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6',{'N':'5','NE':'8','E':'9','SE':'0','S':'7','SW':'4','W':'3','NW':'2'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False},has_major=True,has_minor=True),
    MapSpace(23,'7',{'N':'6','NE':'9','E':'0','SE':'0','S':'0','SW':'0','W':'4','NW':'3'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False},has_minor=True,has_growth=True),
    MapSpace(24,'8',{'N':'0','NE':'0','E':'10','SE':'11','S':'9','SW':'6','W':'5','NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9',{'N':'8','NE':'10','E':'11','SE':'0','S':'0','SW':'7','W':'6','NW':'5'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'0','NE':'0','E':'12','SE':'13','S':'11','SW':'9','W':'8','NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'12','E':'13','SE':'0','S':'0','SW':'0','W':'9','NW':'8'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'0','NE':'0','E':'14','SE':'0','S':'13','SW':'11','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False},has_growth=True),
    MapSpace(29,'13',{'N':'12','NE':'14','E':'0','SE':'0','S':'0','SW':'0','W':'11','NW':'10'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'0','NE':'0','E':'0','SE':'0','S':'0','SW':'13','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]

ortho_wrap_around_map_spaces = [
    MapSpace(1,'C',  {'N':'TP','NE':'0','E':'FE','SE':'0','S':'G', 'SW':'0','W':'14', 'NW':'0'},{'name':'Copse','gain':'wood','hits':0,'scores':True}),
    MapSpace(2,'G',  {'N':'C', 'NE':'0','E':'MP','SE':'0','S':'RM','SW':'0','W':'14', 'NW':'0'},{'name':'Grove','gain':'wood','hits':0,'scores':True}),
    MapSpace(3,'RM', {'N':'G', 'NE':'0','E':'GS','SE':'0','S':'H', 'SW':'0','W':'13', 'NW':'0'},{'name':'Resource Market','gain':None,'hits':0,'scores':False}),
    MapSpace(4,'H',  {'N':'RM','NE':'0','E':'F1','SE':'0','S':'L1','SW':'0','W':'13', 'NW':'0'},{'name':'Hollow','gain':'clay','hits':0,'scores':True}),
    MapSpace(5,'L1', {'N':'H', 'NE':'0','E':'L2','SE':'0','S':'TP','SW':'0','W':'7', 'NW':'0'},{'name':'Lessons1','gain':None,'hits':0,'scores':False}),
    MapSpace(6,'TP', {'N':'L1','NE':'0','E':'DL','SE':'0','S':'C', 'SW':'0','W':'7', 'NW':'0'},{'name':'Traveling Players','gain':'food','hits':0,'scores':True}),
    MapSpace(7,'FE', {'N':'DL','NE':'0','E':'1', 'SE':'0','S':'MP','SW':'0','W':'C', 'NW':'0'},{'name':'Farm Expansion','gain':None,'hits':0,'scores':False}),
    MapSpace(8,'MP', {'N':'FE','NE':'0','E':'1', 'SE':'0','S':'GS','SW':'0','W':'G', 'NW':'0'},{'name':'Meeting Place','gain':'improvement','hits':0,'scores':False},has_minor=True),
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
    MapSpace(20,'4', {'N':'3', 'NE':'0','E':'7', 'SE':'0','S':'2', 'SW':'0','W':'F3','NW':'0'},{'name':'Stage 1 - Major Improvement','gain':'improvement','hits':0,'scores':False,'long_west_edge':True},has_major=True,has_minor=True),
    MapSpace(21,'5', {'N':'7', 'NE':'0','E':'8', 'SE':'0','S':'6', 'SW':'0','W':'2', 'NW':'0'},{'name':'Stage 2 - Western Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(22,'6', {'N':'5', 'NE':'0','E':'9', 'SE':'0','S':'7', 'SW':'0','W':'3', 'NW':'0'},{'name':'Stage 2 - House Redevelopment','gain':'improvement','hits':0,'scores':False},has_major=True,has_minor=True),
    MapSpace(23,'7', {'N':'6', 'NE':'0','E':'TP','SE':'0','S':'5', 'SW':'0','W':'4', 'NW':'0'},{'name':'Stage 2 - Basic Wish for Children','gain':None,'hits':0,'scores':False},has_growth=True,has_minor=True),
    MapSpace(24,'8', {'N':'9', 'NE':'0','E':'10','SE':'0','S':'9', 'SW':'0','W':'5', 'NW':'0'},{'name':'Stage 3 - Pig Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(25,'9', {'N':'8', 'NE':'0','E':'11','SE':'0','S':'8', 'SW':'0','W':'6', 'NW':'0'},{'name':'Stage 3 - Vegetable Seeds','gain':None,'hits':0,'scores':False}),
    MapSpace(26,'10',{'N':'11','NE':'0','E':'12','SE':'0','S':'11','SW':'0','W':'8', 'NW':'0'},{'name':'Stage 4 - Eastern Quarry','gain':'ore','hits':0,'scores':True}),
    MapSpace(27,'11',{'N':'10','NE':'0','E':'13','SE':'0','S':'10','SW':'0','W':'9', 'NW':'0'},{'name':'Stage 4 - Cattle Market','gain':'animal','hits':0,'scores':True}),
    MapSpace(28,'12',{'N':'13','NE':'0','E':'14','SE':'0','S':'13','SW':'0','W':'10','NW':'0'},{'name':'Stage 5 - Urgent Wish for Children','gain':None,'hits':0,'scores':False},has_growth=True),
    MapSpace(29,'13',{'N':'12','NE':'0','E':'H', 'SE':'0','S':'12','SW':'0','W':'11','NW':'0'},{'name':'Stage 5 - Cultivation','gain':None,'hits':0,'scores':False}),
    MapSpace(30,'14',{'N':'14','NE':'0','E':'G', 'SE':'0','S':'14','SW':'0','W':'12','NW':'0'},{'name':'Stage 6 - Farm Redevelopment','gain':None,'hits':0,'scores':False}),
]