import os, sys
import scipy as sp



def solution(items, numItems, capacity, method):
    #print 'items:', items
    weights = sp.array([item.weight for item in items])
    values = sp.array([item.value for item in items])
    if method == 1:
        cut = min(5,numItems)
        idx = greedy(weights, values, numItems, capacity)[:cut]
        x = dynamic_programming(weights[idx], values[idx], min(numItems,cut), capacity)
        return idx[x]
    if method == 0: return greedy(weights, values, numItems, capacity)

def dynamic_programming(weights, values, numItems, capacity):
    T = sp.zeros((capacity+1, numItems+1))
    for i in range(numItems):
        col = i+1
        w = weights[i]
        v = values[i]
        #cumulated_weight += weights[i]
        for k in range(capacity):
            row = k+1 # partial capacity
            if (w <= row):
                T[row, col] = max(T[row,col-1], v + T[row-w, col-1])
            else:
                T[row, col] = T[row,col-1]
    x = []#sp.zeros((numItems,)).astype('int')
    row = capacity
    for col in range(1,numItems+1)[::-1]:
        if (T[row,col] > T[row,col-1]):
            row -= weights[col-1]
            x.append(col-1)
    return x

def dynamic_programming_sparse(weights, values, numItems, capacity):
    print 'sparse dynamic programming'
    Tl = sp.zeros((capacity+1,))
    Tr = sp.zeros((capacity+1,))
    jumpList = []
    for i in range(numItems):
        col = i+1
        w = weights[i]
        v = values[i]
        jump = []
        #cumulated_weight += weights[i]
        for k in range(capacity):
            row = k+1 # partial capacity
            if (w <= row):
                if (v + Tl[row-w] > Tl[row]):
                    Tr[row] = v + Tl[row-w]
                    jump.append(row)
                else:
                    Tr[row] = Tl[row]
            else:
                Tr[row] = Tl[row]
        jumpList.append(jump)
        Tl = Tr.copy()
    x = []#sp.zeros((numItems,)).astype('int')
    row = capacity
    for col in range(1,numItems+1)[::-1]:
        if (row in jumpList[col-1]):
            row -= weights[col-1]
            x.append(col-1)
    return x

def greedy(weights, values, numItems, capacity):
    density = values/weights
    #print density
    idx = sp.argsort(density)[::-1]
    #print idx
    return idx

