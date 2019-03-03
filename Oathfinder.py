from random import randint
from time import time

def pathfinder(tree, row=0, col=0):
    if (row, col) in results: return results[row, col]
    value = tree[row][col]
    try:
        Ltot, Lpath = pathfinder(tree, row+1, col)
        Rtot, Rpath = pathfinder(tree, row+1, col+1)
        if Rtot > Ltot: rval = (value + Rtot, 'R' + Rpath)
        else: rval = (value + Ltot, 'L' + Lpath)
    except IndexError: return value, ''
    results[row, col] = rval
    return rval

def listfinder(tree):
    size = len(tree)
    results = [(value, '') for value in tree[-1]]
    for row in tree[-2::-1]:
        for col, value in enumerate(row):
            Ltot, Lpath = results[col]
            Rtot, Rpath = results[col+1]
            if Rtot > Ltot: results[col] = (value + Rtot, 'R' + Rpath)
            else: results[col] = (value + Ltot, 'L' + Lpath)
    print(results[0])

def get_value(data, point):
    return data[point[1]][point[0]]

def iterative_finder(data, starting_point):
    currentx = starting_point[0]
    currenty = starting_point[1]
    current_point = (currentx, currenty)
    todo = {starting_point: (get_value(data, starting_point), starting_point)}
    best_path = []
    current_path = [get_value(data, current_point), [current_point]]
    while todo:
        todo.pop(starting_point, 0)
        while current_point[0] < len(data[0])-1:
            next_point = (currentx+1, currenty)          
            options = [(currentx+1, min(currenty+1, len(data)-1)), (currentx+1, max(currenty-1, 0))]

            for option in options:
                if option not in todo:
                    todo[option] = [current_path[0]+get_value(data, option), current_path[1]+[(option)]]
                elif todo[option][0] > current_path[0]+get_value(data, option):
                    todo[option] = [current_path[0]+get_value(data, option), current_path[1]+[(option)]]

            current_path[0] += get_value(data, next_point)
            current_path[1].append(next_point) 

            if next_point[0] == len(data[0])-1:
                if not best_path or current_path[0] < best_path[0]:
                    best_path = current_path

            current_point = next_point
            currentx += 1
        next_do = todo.popitem()
        current_point = next_do[0]
        current_path = next_do[1]
        currentx, currenty = current_point[0], current_point[1]

    return best_path

tree = [[randint(0, 9) for a in range(i+1)] for i in range(800)]
data = []
with open('my_data.txt') as file:
    for line in file.readlines():
        data.append([int(num) for num in line.split()])
      
print(iterative_finder(data, (0, 4)))
# print('iterative')
# results = {}
# start_time = time()
# listfinder(tree)
# print("--- %s seconds ---" % (time() - start_time))

# print('recursive')
# results = {}
# start_time = time()
# print(pathfinder(tree))
# print("--- %s seconds ---" % (time() - start_time))

