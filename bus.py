from collections import defaultdict

class Bus(object):
    """Recording the bus's status"""
    
    def __init__(self, bus_id, stop_num):
        self.bus_id = bus_id   # an integer indicating the bus id
        self.loc = 0.0 # record the bus's current location
        self.trajectories = defaultdict(float) # for ploting the trajectory and check the rightness
        self.is_running = True
        # None means not at the stop
        self.current_stop = None
        self.holding_time = None

        # arrival times at each stop
        self.arr_times = defaultdict(float)
        # previous arrival times at each stops
        self.prev_arr_times = defaultdict(float)

        self.travel_speed_this_link = None # when bus enters a link, generate the link travel speed and assign it to this property

if __name__ == "__main__":
    pass