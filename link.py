import numpy as np
from collections import defaultdict

class Link:
    def __init__(self, link_id, mean_speed, cv_speed, length, start_loc):
        """Init method.

        init method for Link 

        Args:
        length: the total length of this link.
        start_loc: starting loc.

        """

        self._link_id = link_id
        self._mean_speed = mean_speed
        self._cv_speed = cv_speed
        self._start_loc = start_loc
        self._length = length
        self._end_loc = start_loc + length
        self._next_stop = None

        # for signals, no need to look at it
        self._signals = []
        self._sublink_dict = defaultdict(lambda: list) # 'no' -> bus list
        self._sublink_dict[0] = []

    def __call__(self, next_stop):
        '''
        For linking the stop and link
        '''
        self._next_stop = next_stop

    # for signals, no need to look at it
    def add_signal(self, signal):
        self._signals.append(signal)
        current_no = len(self._sublink_dict)
        self._sublink_dict[current_no] = []

    def enter_bus(self, bus, sub_link_no):
        '''
        When the bus in the stop finishes the service, enter it into the link
        '''
        bus.loc = self._start_loc
        bus.travel_speed_this_link = np.random.normal(self._mean_speed, self._cv_speed*self._mean_speed)
        self._sublink_dict[sub_link_no].append(bus)

    def forward(self, delta_t, curr_time):
        '''
        Advance the bus on the link, according to its randomly-generated travel speed
        Note that the implementation in this function contains the operations on the signalized intersection. If you have any question, feel free to contact me
        '''
        for sub_link_no in range(len(self._sublink_dict)):
            buses_on_sub_link = self._sublink_dict[sub_link_no] 
            
            if sub_link_no == (len(self._sublink_dict)-1): # check the next stop
                sent_buses_list = []
                for bus in buses_on_sub_link:
                    bus.loc += bus.travel_speed_this_link * delta_t
                    bus.trajectories[curr_time] = bus.loc
                    if bus.loc >= self._end_loc: # reach the next stop
                        bus.loc = self._end_loc
                        bus.trajectories[curr_time] = bus.loc
                        is_bunched = self._next_stop.enter_bus(bus, curr_time)
                        sent_buses_list.append(bus)
                        buses_on_sub_link.remove(bus)
                        if is_bunched:
                            return sent_buses_list, True
                return sent_buses_list, False
    
            else: # check the next signal
                # 1. sublink operations
                next_signal = self._signals[sub_link_no]
                for bus in buses_on_sub_link:
                    bus.loc += bus.travel_speed_this_link * delta_t
                    bus.trajectories[curr_time] = bus.loc
                    if bus.loc >= next_signal.start_loc: # reach the signal
                        bus.loc = next_signal.start_loc
                        bus.trajectories[curr_time] = bus.loc
                        next_signal.enter_bus(bus, curr_time)
                        buses_on_sub_link.remove(bus)

                # 2. signal operations
                buses_on_next_sub_link = self._sublink_dict[sub_link_no+1]
                discharged_buses = next_signal.discharge(curr_time)
                for bus in discharged_buses:
                    buses_on_next_sub_link.append(bus)

        
    def reset(self):
        self._sublink_dict = defaultdict(lambda: list) # 'no' -> bus list
        self._sublink_dict[0] = []
        

