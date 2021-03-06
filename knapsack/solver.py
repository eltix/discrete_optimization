#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])
import scipy as sp
from user_methods import *

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    print 'num items = ', item_count
    print 'capacity =', capacity
    
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    # ratio = sp.array([item.value/item.weight for item in items])
    # idx = sp.argsort(ratio)[::-1]
    #if (item_count < 300):
    #    idx = solution(items, item_count, capacity, 1)
    #else:
    idx = solution(items, item_count, capacity, 1)

    for i in idx:
        item = items[i]
        if (weight + item.weight) <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    weights = sp.array([int(item.weight) for item in items])
    values = sp.array([item.value for item in items])
    idj = greedy(weights, values, item_count, capacity)
    # Filling up
    for j in idj:
        if (not j in(list(idx))):
            item = items[j]
            if (weight + item.weight) <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight   
    
    print 'total weight =', weight
    print 'capacity=', capacity
    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

