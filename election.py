#!/usr/bin/python
import random
import math
import copy
import matplotlib.pyplot as plt

#initial_districts = \
#[
#    [1,1,1,0,0],
#    [1,1,0,0,0],
#    [2,2,3,3,4],
#    [2,2,3,4,4],
#    [2,3,3,4,4],
#]
#political_affiliations = \
#[
#    [1,1,0,0,0],
#    [0,1,1,0,1],
#    [1,0,0,0,0],
#    [0,0,1,1,0],
#    [0,0,0,0,1],
#]

initial_districts = [[int(math.floor(i/2)) for i in xrange(0, 14)] for _ in xrange(0, 10)]
political_affiliations = \
[
    [0,0,0,0,1,0,1,1,0,0,0,0,0,0],
    [0,0,0,1,1,0,1,1,0,0,0,0,0,0],
    [0,0,0,0,1,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,1,1,0,0,0,0],
    [1,1,1,0,1,1,1,0,1,1,0,0,0,0],    
    [0,0,1,0,0,0,1,1,1,1,1,1,0,0],
    [0,1,1,0,0,1,1,1,1,1,1,1,0,0]
]
x_dimension = 14
y_dimension = 10
num_districts = 7
population_per_district = 20
max_winning_districts = 0


def swap(districts):

    x = random.randint(0,x_dimension-1)
    y = random.randint(0,y_dimension-1)

    del_x = random.randint(-1,1)
    del_y = random.randint(-1,1)


    #Error checking
    if x+del_x > x_dimension-1 or x+del_x < 0:
        del_x = -1*del_x
    if y+del_y > y_dimension-1 or y+del_y < 0:
        del_y = -1*del_y
    #print("x: " + str(x) + " y: " + str(y) + " x2: " + str(x+del_x) + " y2: " + str(y+del_y))
    #flip
    #print("x : " + str(x) + " y : " + str(y))
    temp_storage = districts[y+del_y][x+del_x]
    districts[y+del_y][x+del_x] = districts[y][x]
    districts[y][x] = temp_storage
    #format_districts(districts)
    
    
    #Check cont, false means don't continue, duh
    if check_cont(districts):
        if check_winner(districts):
            #print("ayy")
            return check_winner(districts)
        else:
            return 1
    else:
        temp_storage = districts[y+del_y][x+del_x]
        districts[y+del_y][x+del_x] = districts[y][x]
        districts[y][x] = temp_storage
        return True

    
def check_cont(districts):
    cont = 1
    for dist_in_question in range(0,num_districts):
        havent_found_district = True
        temp_districts = copy.deepcopy(districts)
        while havent_found_district:
            x = random.randint(0,x_dimension-1)
            y = random.randint(0,y_dimension-1)
            #print("x : " + str(x) + " y : " + str(y))
            if temp_districts[y][x] == dist_in_question:
                havent_found_district = False
        current_size = 0
        places_to_explore = \
        [
            [y,x]
        ]
        paths = 1
        if find_size(temp_districts,places_to_explore,current_size,paths,dist_in_question) < population_per_district:
            cont = 0
    return cont


def find_size(temp_districts,places_to_explore,size,paths,dist_in_question):
    #Find # of paths you can take from your location
#    while size < population_per_district and paths:
    while size < 300 and paths:

        paths = paths - 1
        for del_x, del_y in [(-1,0), (1,0), (0,-1), (0,1)]:
            if check_bounds(places_to_explore[0][1],del_x,places_to_explore[0][0],del_y) and dist_in_question == temp_districts[places_to_explore[0][0]+del_y][places_to_explore[0][1]+del_x]:
                paths = paths + 1
                places_to_explore.append([places_to_explore[0][0]+del_y,places_to_explore[0][1]+del_x])
                temp_districts[places_to_explore[0][0]+del_y][places_to_explore[0][1]+del_x] = 77
        temp_districts[places_to_explore[0][0]][places_to_explore[0][1]] = 77
        #format_districts(temp_districts)
        size = size + 1
        places_to_explore.remove([places_to_explore[0][0],places_to_explore[0][1]])
    return size


def check_bounds(x,del_x,y,del_y):
    if x+del_x > x_dimension-1 or x+del_x < 0 or y+del_y > y_dimension-1 or y+del_y < 0:
        return False
    return True
    
def check_winner(districts):
    sum_of_blue = [20,20,20,20,20,20,20] #use to change to sum_of_red
    #sum_of_blue = [0,0,0,0,0,0,0]

    district_threshold = int(population_per_district/2)
    #state_threshold = int(math.ceil(num_districts/2))
    winning_districts = 0

    for x in range(0,x_dimension):
        for y in range(0,y_dimension):
            sum_of_blue[districts[y][x]] = sum_of_blue[districts[y][x]] - political_affiliations[y][x]
            
    for column in sum_of_blue:
        if column >= district_threshold:
            winning_districts = winning_districts + 1
    return winning_districts
#  _____                          _
# |  ___|__  _ __ _ __ ___   __ _| |_ ___ _ __ ___
# | |_ / _ \| '__| '_ ` _ \ / _` | __/ _ \ '__/ __|
# |  _| (_) | |  | | | | | | (_| | ||  __/ |  \__ \
# |_|  \___/|_|  |_| |_| |_|\__,_|\__\___|_|  |___/
#

def format_districts(districts):
    print 'districts:'
    for district_row in districts:
        print '\t' + str(district_row)
    print


format_districts(initial_districts)
paths = 0
#loop it up
districts = initial_districts
ww = 0
while max_winning_districts < 7:
    winning_districts = swap(districts)
    if winning_districts > max_winning_districts:
        max_winning_districts = winning_districts
        print("Max_winning_districts = " + str(max_winning_districts))
        format_districts(districts)
        print(" ")
    ww = ww + 1
    photocopy = copy.deepcopy(districts)
    for i in range(0,x_dimension):
        for j in range(0,y_dimension):
            if photocopy[j][i] != 1:
                photocopy[j][i] = 0
    plt.imshow(photocopy)
    #plt.show()
    plt.savefig(str(ww)+'.png')
    #print(ww)
    #format_districts(districts)
    continue
