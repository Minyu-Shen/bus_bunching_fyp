from simulator import Simulator
import matplotlib.pyplot as plt
from collections import defaultdict
import parameters as paras

'''
    The entry of the program
'''

instance_no = 1 # you can repeat the simulaiton multiple times and take the mean for your desired metric(s)
# the simulation logic is implemented in the Simulator class
simulator = Simulator(paras.sim_duration, paras.dspt_times, \
    paras.stop_locs, paras.demand_rates, paras.board_rates, paras.stop_num, paras.demand_start_times, \
        paras.link_mean_speeds, paras.link_cv_speeds, paras.link_lengths, paras.link_start_locs, \
            paras.cycle_lengths, paras.green_ratios,\
                paras.signal_offsets, paras.signal_locs)

# I take the "headways at stops" for example
stop_headways = defaultdict(lambda: list) # stop_no -> headways
for stop in range(paras.stop_num):
    stop_headways[stop] = []

# the main logic
for sim_r in range(instance_no):
    # the time-based logic is implemented in this for-loop
    for t in range(paras.sim_duration):
        is_bunched = simulator.move_one_step(paras.delta_t)
        # when two buses bunches, the simulation of this round will terminate
        if is_bunched: break

    for stop in range(paras.stop_num):
        arr_hdws_list = simulator.get_stop_headways(stop)
        stop_headways[stop] += arr_hdws_list
    
    # the time-space diagram is plotted here, for checking the rightness of the simulation logic
    if sim_r == instance_no-1:
        simulator.plot_time_space()
    # reset the simulator, for next round's simulaiton if any
    simulator.reset(paras.dspt_times)

