import numpy as np
from collections import defaultdict

class Stop:
    def __init__(self, stop_id, loc, demand_rate, board_rate, demand_start_time):
        """
        init method for Link 

        Args:
        loc: bus stop loc
        demand_rate: pax arrival rate, pax/sec
        board_rate: pax boarding rate, pax/sec
        next_link: next link object
        demand_start_time: the start time of the first pax's arrival, sec
        """

        # unchangable ...
        self.stop_id = stop_id
        self._loc = loc
        self._demand_rate = demand_rate
        self._board_rate = board_rate
        self._demand_start_time = demand_start_time
        self._next_link = None

        self._pax_queue = 0 # the pax queue at the stop
        self._bus_list = [] # the bus(es) at the stop
        self.last_bus_arr = 0.0 # record the last bus' arrival time, for calculating the headway 

        # stats
        self.arr_times = []
        self.dpt_times = []

    def __call__(self, next_link):
        '''
        For linking the stop and link
        '''
        self._next_link = next_link

    def enter_bus(self, bus, curr_time):
        '''
        Enter one bus into the stop from the link
        '''
        bus.loc = self._loc
        if self.last_bus_arr != 0.0: # at least one bus has ever reached this stop
            bus.prev_arr_times[self.stop_id] = self.last_bus_arr
        else:
            bus.prev_arr_times[self.stop_id] = 0.0
        
        self.last_bus_arr = curr_time
        self._bus_list.append(bus)
        if len(self._bus_list) >= 2: # bunched
            return True
        self.arr_times.append(curr_time)


    def operation(self, delta_t, curr_time):
        '''
        Stop operations
        '''
        self._pax_arrive(curr_time) 
        self._boarding(delta_t) 
        self._leaving(curr_time) 

    def _pax_arrive(self, curr_time):
        '''
        randomly generate pax's arrival
        '''
        if self._demand_start_time <= curr_time:
            self._pax_queue += np.random.poisson(self._demand_rate)

    def _boarding(self, delta_t):
        '''
        move the pax from queue to the bus
        '''
        for bus in self._bus_list:
            self._pax_queue -= self._board_rate*delta_t

    def _leaving(self, curr_time):
        '''
        check if the bus can leave (when no pax is leftover)       
        '''
        for bus in self._bus_list:
            if self._pax_queue <= 0:
                if self._next_link:
                    self._next_link.enter_bus(bus, 0)
                else: # finished
                    bus.is_running = False
                self._bus_list = []
            else: # still serving, record the "constant" trajectory
                bus.trajectories[curr_time] = bus.loc

    def reset(self):
        self._bus_list = []
        self._pax_queue = 0
        # stats
        self.arr_times = []
        self.dpt_times = []
        self.last_bus_arr = 0.0