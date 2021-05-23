def nearest_perfect_square(val):
    return int(pow(val,0.5))**2

def solution(area):
    left = area
    store = []
    while(left>0):
        np_val = nearest_perfect_square(left)
        left = left - np_val
        store.append(np_val)
    print(','.join([str(i) for i in store]))
    return store