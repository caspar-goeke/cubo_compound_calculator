
##########################################################################
# Usage:
# Very Simple, enter your current Cubo reward per day as a value for "cubo_per_day_start" and 
# your compounding goal in "cubo_per_day_goal", then run the script with "python cubo_calculator.py".
# It will print out the best compounding path and the total number of days needed to achieve the goal.

# Rational:
# The calculations here is based on the fact that for each amount of Cubo per day there is 
# "a best node" which you should mint next. What is overall optimized here is the time it will
# take (shortest time) to reach a certain amount of Cubo per day starting with a smaller amount
# of Cubo per day. The "inflection points" (as seen below) are the points (at X amount of Cubo
# per day) where it will be better to mint the next node tier. 

#Additional Notes:
# 1. This calculation does not directly take the USD value of DAI into account. So if you want to 
# use your Cubo also for the Dai part the calculation will depend on the current Cubo price, which 
# is really hard to model. However because a) the amounts are 1:1 proportional and b) Cubo (at this
# point) is about 15 times more worth than Dai, the effect should not much influence the decision 
# what is the next best node to mint. 

# 2. The calculation assumes you start with 0 Cubo but a certain amount of Cubo reward per day. If you
# additionally have some Cubo or USD that you want to invest / put in the calculation then:
# a) Run the calculation once without it.
# b) See if your existing Cubo or USD can already buy the next best node or even a higher one.
# c) Buy the highest node possible which is not lower then the next best node path (otherwise wait).
# d) Run the calculation again with your new amount of Cubo per day.

########################################################################

cubo_per_day_start= 4
cubo_per_day_goal = 100

################# calculate inflection points by hand ##################

#  planck-femto
#(25/0.1)+(25/0.2)+(25/0.3)= 458.333
#(50/0.1)= 500
#(25/0.2)+(25/0.3)+(25/0.4) =270
#(50/0.2)= 250
#Planck end threshold  = 0
#Planck end threshold  = 0.1
#femto start threshold  = 0.2

#  femto-pico
#(50/0.3)+(50/0.6) =250
#(75/0.3) =250
#femto end threshold  = 0.29
#pico start threshold  = 0.3

# pico-nano
#((75/0.5)+(75/1.1))*(1.5/1.7) == 192.51
#(100/0.5) = 200
#((75/0.6)+(75/1.2))*(1.6/1.8) == 166.66
#(100/0.6) = 166.66
#((75/0.7)+(75/1.3))*(1.7/1.9) == 147
#(100/0.7) = 142
#pico end threshold  = 0.59
#nano start threshold  = 0.6

# nano-mini
#(100/2)+(100/3)+(100/4) == 108
#(250/2) = 125
#(100/3)+(100/4)+(100/5) == 78
#(250/3) = 83
#(100/4)+(100/5)+(100/6) == 61.25
#(250/4) = 62.5
#(100/4.3)+(100/5.3)+(100/6.3) == 57.99
#(250/4.3) = 58.13
#(100/4.4)+(100/5.4)+(100/6.4) == 65.87
#(250/4.4) = 56.81
#nano end threshold  = 4.39
#mini start threshold  = 4.40

# mini-kilo
#(250/7)+(250/10)+(100/13) == 68.40
#(500/7) = 71.42
#(250/8)+(250/11)+(100/14) == 61.12
#(500/8) = 62.5
#(250/9)+(250/12)+(100/15) == 55.27
#(500/9) = 55.55
#(250/9.3)+(250/12.3)+(100/15.3) == 53.74
#(500/9.3) = 53.76
#(250/9.4)+(250/12.4)+(100/15.4) == 53.25
#(500/9.4) = 53.19
#mini end threshold  = 9.39
#kilo start threshold  = 9.40

# kilo-mega
#(500/17)+(500/24)+(100/31)+(100/32) == 56.59
#(1000/17) = 58.82
#(500/20)+(500/27)+(100/34)+(100/35) == 49.31
#(1000/20) = 50
#(500/22)+(500/29)+(100/36)+(100/37) == 45.44
#(1000/22) = 45.45
#(500/22.1)+(500/29.1)+(100/36.1)+(100/37.1) == 45.27
#(1000/22.1) =45.24
#kilo end threshold  = 22.0
#mega start threshold  = 22.1

# mega-giga
#(1000/137)+(1000/153)+(1000/169)+(1000/185)+(1000/201)+(1000/217)+(250/233)+(100/236) == 36.23
#(5000/137) = 36.49
#(1000/141)+(1000/157)+(1000/173)+(1000/189)+(1000/205)+(1000/221)+(250/237)+(100/240) == 35.40
#(5000/141) = 35.46
#(1000/142)+(1000/158)+(1000/174)+(1000/190)+(1000/206)+(1000/222)+(250/238)+(100/241) == 35.20
#(5000/142) = 35.21
#(1000/143)+(1000/159)+(1000/175)+(1000/191)+(1000/207)+(1000/223)+(250/239)+(100/242) == 35.00
#(5000/143) = 34.96
#mega end threshold  = 142
#mega start threshold  =143

########################################################################

nodes_cubo_prices = [25,50,75,100,250,500,1000,5000]
nodes_cubo_rewards = [0.1,0.3,0.6,1,3,7,16,100]
nodes_names = ['planck','femto','pico','nano','mini','kilo','mega','giga']
best_node_from = [0,0.2,0.3,0.6,4.4,9.4,22.1,143]

########################################################################

cubo_per_day_current = cubo_per_day_start
node_path = []
total_nr_days = 0

while (cubo_per_day_current<cubo_per_day_goal):

    # get best node
    next_node_found = False
    node_index = 0
    while(next_node_found==False):
        if(cubo_per_day_current>best_node_from[-1]):
            node_index= len(best_node_from)-1
            next_node_found = True
        else:
            node_a = best_node_from[node_index]
            node_b = best_node_from[node_index+1]
            if(cubo_per_day_current>=node_a) and (cubo_per_day_current<node_b):
                next_node_found = True
            else: node_index+=1
    
    # reduce node if too big
    added_amount = round(nodes_cubo_rewards[node_index],1)
    if(cubo_per_day_current+added_amount>cubo_per_day_goal):
        is_small_enough = False
        while(is_small_enough==False):
            node_index-=1
            added_amount = round(nodes_cubo_rewards[node_index],1)
            if(cubo_per_day_current+added_amount<=cubo_per_day_goal):
                is_small_enough = True

  
    # add to strategy path 
    node_path.append(nodes_names[node_index])
    added_nr_days = nodes_cubo_prices[node_index]/cubo_per_day_current
    total_nr_days +=added_nr_days
    added_amount = round(nodes_cubo_rewards[node_index],1)
    cubo_per_day_current+= added_amount
    cubo_per_day_current = round(cubo_per_day_current,1)

print("----------- Best Path -----------")
print(node_path)
print("----------- Total Number of Days -----------")
print(total_nr_days)
########################################################################