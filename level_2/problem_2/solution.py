def pair_wise(arr):
    divisible_pairs = []
    num_divisiblepair_perval = [0]*len(arr)
    
    for pos_i, val_i in enumerate(arr):
        for j, val_j in enumerate(arr[pos_i+1:]):
            pos_j = pos_i + 1 + j # actual position
            if val_j%val_i==0: # if divisible
                num_divisiblepair_perval[pos_i] += 1 # add one to number of pairs
                divisible_pairs.append((pos_i, pos_j))

    return divisible_pairs, num_divisiblepair_perval

def solution(arr):
    """
    The problem statement is to find number of magic triplets (a_i, b_j, c_k) from interger array arr
    So that a_i divides b_j and b_j divides c_k where i < j < k.
    To do that we find all pairs of integers (x_i,y_j),
    where x_i divides y_j where j > i, and keep a count of all y_j that divide a particular x_i
    
    Now to find all magic triplets that start with (x_i, y_j) we simply add 
    the number of divisible pairs that begin y_j, hence summing up all the possible
    (x_i, y_j) we get the possible magic triplets
    """
    if len(arr) < 3:
        return 0
    # divisible pair num divisible
    divisible_pairs, num_divisible = pair_wise(arr)
    # sum up for all the pairs
    total_sum = 0
    for val1, val2 in divisible_pairs:
        total_sum += num_divisible[val2]
    return total_sum