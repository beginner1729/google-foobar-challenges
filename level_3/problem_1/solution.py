class FracOps(object):
    """
    This class will help maintain the fractional protion of the solution
    just like floating/int multiplication addition and division is taken care of
    """
    def __init__(self, numerator, denominator):
        self.num = numerator
        self.den = denominator
        self.normalize()
        
    @staticmethod
    def gcd(int1, int2):
        greater = int1 if int1 >= int2 else int2
        smaller = int2 if int1 >= int2 else int1
        if smaller == 0 or greater == 0:
            return 1
        while(greater % smaller):
            temp = greater%smaller
            greater = smaller
            smaller = temp
        return smaller
    
    def normalize(self):
        gcd_val = self.gcd(self.num, self.den)
        self.num /= gcd_val
        self.den /= gcd_val
    
    def __add__(val1, val2):
        common_factor = (val1.den * val2.den) / val1.gcd(val1.den, val2.den)
        num1 = val1.num * (common_factor/val1.den)
        num2 = val2.num * (common_factor/val2.den)
        num_summed = num1 + num2
        return FracOps(num_summed, common_factor)
    
    def __sub__(val1, val2):
        new_frac = FracOps(val2.num * -1, val2.den)
        return val1 + new_frac
    
    def __mul__(val1, val2):
        num_prod = val1.num * val2.num
        den_prod = val1.den * val2.den
        return FracOps(num_prod, den_prod)
    
    def __div__(val1, val2):
        if val2.num==0:
            raise ZeroDivisionError("Zero fraction provided")
        new_frac = FracOps(val2.den, val2.num)
        return val1 * new_frac
    
    def common_den(self, list_fractions):
        lcm = 1
        final_nums = []
        for frac in list_fractions:
            den = frac.den if frac.num !=0 else 1
            lcm = lcm * den / self.gcd(lcm, den)
        final_nums = [int(frac.num * lcm/frac.den) for frac in list_fractions]
        return final_nums + [int(lcm)]

## matix inverse

def arrange_mat(mat):
    """
    Arranging the matrix into standard from 
                            | absorbing states | nonabsorbing states |
    absorbing states        |          I       |            0        |
    non absorbing states    |          R       |            Q        |
    
    returns the standard form and the number of absorpotion state
    """
    absorbing_states = []
    nonabsorbing_states = [] # as we start form s0
    if len(mat) ==1:
        return mat, 1
    for pos, row in enumerate(mat):
        if all([val == 0 for val in row]):
            absorbing_states.append(pos)
        else:
            nonabsorbing_states.append(pos)
    #print(absorbing_states, nonabsorbing_states)
    arranged = absorbing_states + nonabsorbing_states
    standard_from = []
    for r_pos in arranged:
        rearranged_row = [mat[r_pos][col] for col in arranged]
        standard_from.append(rearranged_row[:])
    return standard_from, len(absorbing_states)

def convert_frac(matrix):
    """
    Converts the fraction to fraction obj matrix
    """
    mat_frac = []
    for pos,row in enumerate(matrix):
        row_c = row[:]
        summed = sum(row)
        if summed == 0:
            row[pos] = 1
            summed = 1
        
        frac_row = [FracOps(count,summed) for count in row_c]
        mat_frac.append(frac_row[:])
    return mat_frac

def get_unitmatrix(dim_len):
    """
    Returns a fractional unti matrix with dim dim_len x dim_len
    """
    row = [FracOps(0,1)]*dim_len
    mat = []
    [mat.append(row[:]) for _ in range(dim_len)]
    for diag in range(dim_len):
        mat[diag][diag] = FracOps(1,1)
    return mat

def transpose_matrix(m):
    """
    matrix transposition
    """
    return map(lambda x: list(x), zip(*m))

def get_minor(m,i,j):
    """
    gets the minor matrix for the given position
    """
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def get_deternminant(m):
    """
    computes the determinant with a base case for 2 x 2
    """
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = FracOps(0,1)
    for c in range(len(m)):
        power_Val = FracOps(((-1)**(c)), 1)
        determinant += power_Val*m[0][c]*get_deternminant(get_minor(m,0,c))
    return determinant

def get_matrix_inverse(m):
    """
    Computes the determinant with adj method
    """
    determinant = get_deternminant(m)
    negetive_one = FracOps(-1,1)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, negetive_one*m[0][1]/determinant],
                [negetive_one*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = get_minor(m,r,c)
            power_Val = FracOps(((-1)**(r+c)), 1)
            cofactorRow.append( power_Val * get_deternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose_matrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def mat_subtract(m1, m2):
    """
    subtract two matrix
    """
    deducted = []
    for row1, row2 in zip(m1, m2):
        deducted.append([i-j for i,j in zip(row1, row2)])
    return deducted

def frac_sum(iterable_fracs):
    """
    Sum of multiple fractions
    """
    zero_frac = FracOps(0,1)
    for frac in iterable_fracs:
        zero_frac += frac
    return zero_frac

def matmult(a,b):
    """
    matrix multiplication
    """
    zip_b = list(zip(*b))
    return [[frac_sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) 
             for col_b in zip_b] for row_a in a]

def solution(mat):
    """
    We use the idea of absorbing markov state to solve this problem
    some terms are as follows
    Absorbing state are the states in markov chain from where we cannot move to any other state
    Thus absorbing states have probability = 1 to itself.
    
    So first we arrange the prob matrix into standard format like 
                            | absorbing states | nonabsorbing states |
    absorbing states        |          I       |            0        |
    non absorbing states    |          R       |            Q        |
    where R is the sub matrix for probability states form non absorbing states to absorbing states.
    While Q is the sub matrix for state change proababilites with in non-absorbing states.
    Now all the elements in Q are one or less Q^n where n tends to infinity is 0 matrix.
    
    Using the property of adjacency matrix which is A^n gives the graph edges with in n path distance,
    we compute Q^n which is adjacency after n path travel. As n tends to infinity this basically
    gives all possible length path(including all cycles).
    
    So sum of all probability for all length path ( lets call it S) is 
    I + Q^1 + Q^2 + Q^3 ... 
    This is equal to (I - Q)^-1. Notice we need I as we assume all state to be a starting state
    as we have to start from a non absorbing state which is prob 1
    
    proof:
    S = I + Q^1 + Q^2 + Q^3 ... 
    S(I-Q) = I + Q^1 + Q^2 + Q^3 ...  - (Q^1 + Q^2 + Q^3 + Q^4 ...)
    S(I-Q) = I
    S = (I-Q)^-1
    
    hence non absorbing state to absorbing state via all possible path any number of time is SR
    which is (I-Q)^-1 * R
    """
    
    standard, num_absorption = arrange_mat(mat) # getting into standard form
    
    # check if zero is absorbing state
    row_zero = mat[0][:]
    if all([i==0 for i in row_zero]):
        result = [0] * num_absorption
        result[0] = 1
        result.append(1)
        return result
    
    mat_frac = convert_frac(standard) # get in fractional format this helps formatting

    nonnum_absorption = len(mat) - num_absorption

    q = [row[num_absorption:] for row in mat_frac[num_absorption:]] # submatrix Q
    r = [row[:num_absorption] for row in mat_frac[num_absorption:]] # submatrix R
    iq = get_unitmatrix(nonnum_absorption) # (I - Q)
    inv = get_matrix_inverse(mat_subtract(iq,q)) # (I - Q)^-1

    result = matmult(inv, r) # (I - Q)^-1 * R

    return FracOps(1,1).common_den(result[0]) # 0 th place will be for state 0
    
    
if __name__ =="__main__":
    mat = [
        [1, 2, 3, 0, 0, 0],
        [4, 5, 6, 0, 0, 0],
        [7, 8, 9, 1, 0, 0],
        [0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    print(solution(mat))
    mat = [
        [0]
    ]
    print(solution(mat))
    
    mat =[
        [0, 86, 61, 189, 0, 18, 12, 33, 66, 39],
        [0, 0, 2, 0, 0, 1, 0, 0, 0, 0],
        [15, 187, 0, 0, 18, 23, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    print(solution(mat))