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


tree = [[randint(0, 9) for a in range(i+1)] for i in range(800)]

      
print('iterative')
results = {}
start_time = time()
listfinder(tree)
print("--- %s seconds ---" % (time() - start_time))

print('recursive')
results = {}
start_time = time()
print(pathfinder(tree))
print("--- %s seconds ---" % (time() - start_time))

