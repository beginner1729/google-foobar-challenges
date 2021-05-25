class IntegerCalculation(object):
    """
    Big integer class for handling 
    comparison operation, substraction, addition,
    long division
    """
    def __init__(self, str_int):
        ## left most bit is the most significant one
        self.int_arr = [int(i) for i in str_int]
        self.normalize()
    
    @staticmethod
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
    
    def normalize(self):
        """
        Removes all the initial zeroes to represent in the shortest form
        """
        new_ar = []
        non_zero_encountered = False
        for ele in self.int_arr:
            if (ele == 0) and (not non_zero_encountered):
                continue
            non_zero_encountered = True
            new_ar.append(ele)
        self.int_arr = new_ar
        # incase its a zero int
        if len(self.int_arr) == 0:
            self.int_arr = [0]

    def __gt__(self, arr_int):
        
        self.normalize()
        arr_int.normalize()
        if len(self.int_arr) > len(arr_int.int_arr):
            return True
        if len(self.int_arr) < len(arr_int.int_arr):
            return False
        for el1, el2 in zip(self.int_arr, arr_int.int_arr):
            if el1 > el2:
                return True
            if el1 < el2:
                return False
        return False
    
    def __ge__(self, arr_int):
        return self > arr_int or self == arr_int

    def __eq__(self, arr_int):
        self.normalize()
        arr_int.normalize()
        if len(self.int_arr) != len(arr_int.int_arr):
            return False
        for el1, el2 in zip(self.int_arr, arr_int.int_arr):
            if el1 != el2:
                return False
        return True
    
    def __sub__(self, arr_int):
        """
        Normal subtraction and carry over handling
        """
        self.normalize()
        arr_int.normalize()

        larger = self.int_arr
        smaller = arr_int.int_arr
        diff = len(larger) - len(smaller)
        if diff > 0:
            smaller = [0]*diff + smaller
        else:
            larger = [0]* abs(diff) + larger
        total_sum = []
        for val1, val2 in zip(larger, smaller):
            total_sum.append((val1 - val2))

        return IntegerCalculation(self.handle_carryover(total_sum))
    
    def __add__(self, arr_int):
        """
        Addition and carry over normalization
        """
        self.normalize()
        arr_int.normalize()

        larger = self.int_arr
        smaller = arr_int.int_arr
        diff = len(larger) - len(smaller)
        if diff > 0:
            smaller = [0]*diff + smaller
        else:
            larger = [0]* abs(diff) + larger
        total_sum = []
        for val1, val2 in zip(larger, smaller):
            total_sum.append((val1 + val2))

        return IntegerCalculation(self.handle_carryover(total_sum))

    def single_digitmult(self, digit):
        """
        Single digit multiplication
        """
        mult_result = [ele * digit for ele in self.int_arr]
        mult_result = self.handle_carryover(mult_result)

        return IntegerCalculation(mult_result)

    def divide_once(self,remainder):
        """
        As multiplication is a costly operation we try to estimate the multiple using
        the first three digits of divisor and dividend and generally get the estimate with only 
        3 try at max.
        And rest is simple subtraction and remainder carry
        """
        multiple = self.estimate_multiple(remainder)
        mul_val = self.single_digitmult(multiple)
        while remainder >= mul_val and multiple < 10:
            multiple += 1
            mul_val = self.single_digitmult(multiple)
        
        multiple -= 1 # so that we don't go beyond what is required
        mul_val = self.single_digitmult(multiple)
        remainder = remainder - mul_val
        return remainder, multiple

    def long_division(self, arr_int):
        """
        big int implementation of long division
        """
        pos = 0
        remainder = IntegerCalculation([0])
        quotient = []
        while True:
            try:
                remainder = IntegerCalculation(
                    (remainder.int_arr + [arr_int.int_arr[pos]]))
            except IndexError:
                # we have reached the end
                break
            if self > remainder:
                quotient.append(0)
                pos += 1
                continue
            remainder, multiple = self.divide_once(remainder)
            quotient.append(multiple)
            check_fordivision = False
            pos += 1
        
        return IntegerCalculation(quotient), remainder

    def estimate_multiple(self, numerator):
        """
        Actually estimates the multiple required for a certain iteration of the 
        division. normalize function always ensures we don't wound up with a zero division
        if zero was not explicitly passed, as we deal with positive integer so we don't bother with it
        """
        num = float("0." + ''.join([str(i) for i in numerator.int_arr[:3]]))
        den = float("0." + ''.join([str(i) for i in self.int_arr[:3]]))
        
        #increase the denominator so that we estimate lower that what is required
        den += 0.01

        div = num/den

        return int(div)

def solution(m,f):
    """
    This solution is kind of based on the Euclid's algorithm of computing the gcd

    At any point of time let there be m (Mach bombs) and f (Facula bombs), Now let m > f
    now the previous generation bombs is only m - f (Mach bombs) and f (Facula bombs).
    Same thing holds true if f and m's roles are reversed as the bomb increment process is symmetric.

    Now if m = q*f + r we can directly replace the next generation with the eventual generation, which is 
    r (Mach bombs) and f (Facula bombs) and add q to the number of generation.

    Its just like finding gcd where we keep track of the quoteint along with the remainder. And all happens in bigint. 
    """
    M_bomb = IntegerCalculation(m)
    F_bomb = IntegerCalculation(f)
    min_val = M_bomb if M_bomb < F_bomb else F_bomb
    max_val = M_bomb if M_bomb > F_bomb else F_bomb
    generation = IntegerCalculation([-1])
    # -1 as counting starts from 1,1 but while calculating we go all the way to zero
    
    while True:
        quotient, new_minval = min_val.long_division(max_val)
        new_minval.normalize()
        generation += quotient
        if len(new_minval.int_arr) and new_minval.int_arr[0] == 0:
            if len(min_val.int_arr) == 1 and min_val.int_arr[0] == 1:
                return ''.join([str(i) for i in generation.int_arr])
            return "impossible"
        
        max_val = min_val
        min_val = new_minval
    

if __name__ == "__main__":
    print(solution("124","8"))