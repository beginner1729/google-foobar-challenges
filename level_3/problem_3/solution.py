def integer_to_list(int1):
    """
    This function makes and list form integers
    example 25 -> [2,5]
    """
    list_int1 = list(str(int1))

    list_int1 = [int(i) for i in list_int1]
    return list_int1

def handle_carryover(list_ints):
    """
    Handles the carry over by carring over the tenths place
    """
    carry_over = 0
    carried_val = []
    for ints in reversed(list_ints):
        total = ints + carry_over
        carry_over = total//10
        carried_val.insert(0, (total%10))

    if carry_over > 0:
        carried_val = [carry_over] + carried_val

    return carried_val

def add_two_list(list1, list2):
    """
    Returns addition of two list like values as it if were int and returns and list as if it were int
    """
    if len(list1) < len(list2):
        list1 = [0]*(len(list2) - len(list1)) + list1
    else:
        list2 = [0]*(len(list1) - len(list2)) + list2

    total_sum = []
    for val1, val2 in zip(list1, list2):
        total_sum.append((val1+val2))

    return handle_carryover(total_sum)

def product(int1, int2):
    """
    Products large intergers
    returns list as if it were int
    """
    list_int1 = integer_to_list(int1)
    list_int2 = integer_to_list(int2)

    list_of_list = []
    
    for l2 in list_int2:
        mult_perval = [l1 * l2 for l1 in list_int1]
        mult_perval = handle_carryover(mult_perval)
        
        #as we go from right to left
        list_of_list.insert(0, mult_perval)
    
    summed = [0]
    
    for pos, list_val in enumerate(list_of_list):
        porper_position = list_val + [0]*pos
        summed = add_two_list(summed, porper_position)
    return summed

def solution(x_pos, y_pos):
    """
    Arrangement of the triangle is like 1 bunny in row 1 then 2 bunny in 2nd row 
    So the nth row had n bunny so total bunnies are n*(n+1)/2(sum of 1 to n)

    Now any position is on a diagonal whose every element sum is x_pos + y_pos. Max bunny id of such diagonal is (x_pos + y_pos)*(x_pos +y_pos -1)//2

    To calculate id at a given position we do the following
    1. calculate the max bunny id till in the diagonal (x_pos + y_pos - 1)
    2. as the bunnies are stacked from x = 1 again we simply add the x_pos to the result of step 1
    """
    diag_id = x_pos + y_pos - 1 # by our constarint it should not overflow
    if diag_id & 1 == 0:
        int1 = diag_id >> 1
        int2 = diag_id - 1
    else:
        int1 = diag_id
        int2 = diag_id - 1
        int2 = int2 >> 1
    max_id = product(int1,int2)
    actual_id = add_two_list(max_id, integer_to_list(x_pos))
    return ''.join([str(i) for i in actual_id])

if __name__ == "__main__":
    print(solution(5,10))
    print(solution(3,2))
    print(solution(2,3))
    


