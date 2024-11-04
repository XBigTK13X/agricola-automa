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

    def build_rooms(self):
        while self.resources['wood'] >= 5 and self.resources['reed'] >= 2 and self.rooms < 5:
            self.rooms += 1
            self.resources['wood'] -= 5
            self.resources['reed'] -= 2

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