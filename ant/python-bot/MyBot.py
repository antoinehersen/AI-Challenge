#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        self.orders = {}
        self.targets = {}
        self.random_targets = {}
        pass

    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        self.ants = ants
        # initialize data structures after learning the game settings
        pass

    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use

    def do_move_direction_blocked( self, loc, l_direction):
        random.shuffle( l_direction)
        for direct in l_direction:
            if self.do_move_direction( loc, direct, False):
                return True
        return False

    def do_move_direction(self, loc, direction, default = True):
        new_loc = self.ants.destination(loc, direction)
        if (self.ants.unoccupied(new_loc) and new_loc not in self.orders):
            self.ants.issue_order((loc, direction))
            self.orders[new_loc] = loc
            return True
        else:
            if default:
                dirs = ['n', 'n', 'n', 'n', 'n', 'e', 'e', 'e', 's', 's','w']
                return self.do_move_direction_blocked( loc, dirs)
            else:
                return False



    def do_move_location(self, loc, dest):
        if loc == dest:
            return False
#        print >> sys.stderr, (loc, dest)
        directions = self.ants.path_finding(loc, dest, [])

        if directions != False:
            direction = directions.pop(0)
            if self.do_move_direction(loc, direction):
                self.targets[dest] = loc
                return True
        return False

    def do_turn(self, ants):
        self.orders = {}
        self.targets = {}
        self.ants = ants

        for ant_loc in ants.my_ants():
            ant_id = ants.ant_id[ ant_loc ]
            if ant_id in self.random_targets:
                if self.random_targets[ ant_id] == ant_loc :
                    self.random_targets[ ant_id ] = ants.random_loc()


        ant_dist = []
        for food_loc in ants.food():
            for ant_loc in ants.my_ants():
                dist = ants.distance(ant_loc, food_loc)
                ant_dist.append((dist, ant_loc, food_loc))
        ant_dist.sort()
        busy_ants = []
        for dist, ant_loc, food_loc in ant_dist:
            if food_loc not in self.targets and ant_loc not in self.targets.values():
                self.do_move_location(ant_loc, food_loc)
                busy_ants.append( ant_loc)

            # check if we still have time left to calculate more orders
            if ants.time_remaining() < 10:
                break
#        print >> sys.stderr, self.random_targets
#

        for ant_loc in ants.my_ants():
            if ant_loc not in busy_ants:
                ant_id = ants.ant_id[ ant_loc ]
                if ant_id in self.random_targets:
                    obj = self.random_targets[ ant_id]
                    if ants.passable( obj):
                        self.do_move_location(ant_loc, obj)
                        continue
                r_loc = ants.random_loc()
                self.random_targets[ ant_id ] = r_loc
                self.do_move_location(ant_loc, r_loc)



if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
