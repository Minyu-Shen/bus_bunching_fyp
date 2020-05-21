delta_t = 1.0 # simulation time step in time-based simulation logic
sim_duration = int(3600*2)  # the total simulation duration for one round (you may repeat it for many times to get the convergent result)
dspt_headway = 10 * 60  # dispatch headways, 10 min = 10*60 seconds
sim_bus_no = sim_duration//dspt_headway + 1 # No. of buses needed for one simulation round
dspt_times = [(x+1)*dspt_headway for x in range(sim_bus_no)] # the dispatch time for each bus (when leaving the terminal stop)

# parameters for stop settings
stop_num = 12 # total stop No.
stop_spacing = 1500 # inter-stop distance
stop_locs = [(x+1)*stop_spacing for x in range(stop_num)] # the stop location
demand_rate = 2.0/60.0 # pax arrival rate  2 pax/min = 0.0333 pax/sec
board_rate = 0.5 # pax boarding rate, the unit is pax/sec, each time, 0.5 pax will board the bus. Note that here I just treat the pax as continuous variable for simplicity
demand_rates = [demand_rate] * stop_num # array of pax arrival rate for all the stops
board_rates = [board_rate] * stop_num # array of pax board rate for all the stops

# parameters for signal settings
# in this repository's code, I also added the signal at the middle of each (interstop) link 
# in your case, you might not need this one; just set the green ratio (in line 24) to be 1.0
n = 1 # each link has n signals
signal_num = n*stop_num
fake_total_signals = [stop_spacing/(n+1) + x*stop_spacing/(n+1) for x in range((n+1)*stop_num)]
signal_locs = [x for x in fake_total_signals if x not in stop_locs]
cycle_lengths = [120] * signal_num # sec
green_ratios = [1.0] * signal_num
signal_offsets = [0] * signal_num # the green start compared to the previous signal

# parameters for links settings
link_num = stop_num # link no. = stop no.
link_lengths = [stop_spacing] * link_num
# I assume that the link travel speed is a Gaussian R.V. with mean and coefficient of variation set below
link_mean_speeds = [30/3.6] * link_num # mean_travel speed, m/s
link_cv_speeds = [0.1] * link_num # the coefficient of variation in travel speed
link_start_locs = [x*stop_spacing for x in range(link_num)] # the start location of the link

# to mitigate initial condition's impact, I set a time threshold for the first pax's arrival time at each stop. before this time, no pax will arrive
demand_start_times = []
arrival_stop_time = link_lengths[0] / link_mean_speeds[0]
for stop in range(stop_num):
    link = stop
    demand_rate = demand_rates[stop]
    board_time_per_pax = 1 / board_rates[stop]
    whole_para_part = board_time_per_pax * demand_rate / (1-demand_rate*board_time_per_pax)
    depart_stop_time = arrival_stop_time + dspt_headway/(1+whole_para_part) * whole_para_part
    link_travel_time = link_lengths[link] / link_mean_speeds[link]
    demand_start_times.append(depart_stop_time)
    arrival_stop_time = depart_stop_time + link_travel_time


