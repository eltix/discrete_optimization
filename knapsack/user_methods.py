import os, sys
import scipy as sp



def solution(items, numItems, capacity, method):
    #print 'items:', items
    ratio = 1
    weights = sp.array([int(ratio*item.weight) for item in items])
    capacity = int(ratio*capacity)
    values = sp.array([item.value for item in items])
    if method == 1:
        cut = numItems #min(5,numItems)
        idx = greedy(weights, values, numItems, capacity)[:cut]
        #x = dynamic_programming_sparse_smart(weights[idx], values[idx], min(numItems,cut), capacity)
        x = dynamic_programming_sparse_smart(weights[idx], values[idx], min(numItems,cut), capacity)
        return idx[x]
    if method == 0: return greedy(weights, values, numItems, capacity)

def dynamic_programming(weights, values, numItems, capacity):
    T = sp.zeros((capacity+1, numItems+1)).astype('int')
    for i in range(numItems):
        col = i+1
        w = weights[i]
        v = values[i]
        #cumulated_weight += weights[i]
        for k in range(w, capacity):
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
    B = sp.zeros((capacity+1, numItems+1), dtype=bool)
    for i in range(numItems):
        print 'item ',i
        col = i+1
        w = weights[i]
        v = values[i]
        #cumulated_weight += weights[i]
        for k in range(w, capacity):
            row = k+1 # partial capacity
            if (w <= row):
                if (v + Tl[row-w] > Tl[row]):
                    Tr[row] = v + Tl[row-w]
                    B[row, col] = True
                else:
                    Tr[row] = Tl[row]
            else:
                Tr[row] = Tl[row]
        Tl = Tr.copy()
    x = []#sp.zeros((numItems,)).astype('int')
    row = capacity
    for col in range(1,numItems+1)[::-1]:
        if (B[row,col]):
            row -= weights[col-1]
            x.append(col-1)
    return x

def dynamic_programming_sparse_smart(weights, values, numItems, capacity):
    print 'sparse dynamic programming'
    Tl = sp.zeros((capacity+1,), dtype=int)
    #Tr = sp.zeros((capacity+1,))
    B = sp.zeros((capacity+1, numItems+1), dtype=bool)
    for i in range(numItems):
        print 'item ',i
        col = i+1
        w = weights[i]
        v = values[i]
        B[w:,col] = Tl[w:] < v+Tl[:-w]
        Tl[w:] = sp.maximum(Tl[w:], v+Tl[:-w])
        #cumulated_weight += weights[i]
        # for k in range(w, capacity):
        #     row = k+1 # partial capacity
        #     if (w <= row):
        #         if (v + Tl[row-w] > Tl[row]):
        #             Tr[row] = v + Tl[row-w]
        #             B[row, col] = True
        #         else:
        #             Tr[row] = Tl[row]
        #     else:
        #         Tr[row] = Tl[row]
        #Tl = Tr.copy()
    x = []#sp.zeros((numItems,)).astype('int')
    row = capacity
    for col in range(1,numItems+1)[::-1]:
        if (B[row,col]):
            row -= weights[col-1]
            x.append(col-1)
    print 'optimal value = ', Tl[-1]
    return x

def greedy(weights, values, numItems, capacity):
    density = values/weights
    #print density
    idx = sp.argsort(density)[::-1]
    #print idx
    return idx

