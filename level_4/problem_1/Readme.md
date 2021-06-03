# Problem Statement and Constraints

## Distract the Trainers

The time for the mass escape has come, and you need to distract the bunny trainers so that the workers can make it out! Unfortunately for you, they're watching the bunnies closely. Fortunately, this means they haven't realized yet that the space station is about to explode due to the destruction of the LAMBCHOP doomsday device. Also fortunately, all that time you spent working as first a minion and then a henchman means that you know the trainers are fond of bananas. And gambling. And thumb wrestling.

The bunny trainers, being bored, readily accept your suggestion to play the Banana Games.

You will set up simultaneous thumb wrestling matches. In each match, two trainers will pair off to thumb wrestle. The trainer with fewer bananas will bet all their bananas, and the other trainer will match the bet. The winner will receive all of the bet bananas. You don't pair off trainers with the same number of bananas (you will see why, shortly). You know enough trainer psychology to know that the one who has more bananas always gets over-confident and loses. Once a match begins, the pair of trainers will continue to thumb wrestle and exchange bananas, until both of them have the same number of bananas. Once that happens, both of them will lose interest and go back to supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.

## Languages


To provide a Python solution, edit solution.py
To provide a Java solution, edit Solution.java

## Test cases

Your code should pass the following test cases.
Note that it may also be run against hidden test cases not shown here.

-- Python cases --
Input:
solution.solution(1,1)
Output:
    2

Input:
solution.solution([1, 7, 3, 21, 13, 19])
Output:
    0

# Solution
The problem is divided into two parts
1. detect if any two pairs are in infinite loop when two trainers are matched up
2. Pair up trainer in a optimal way so that most of them are matched up

__Solution of problem 1__ : Lets assume the two number are a and b to start with
Simple checks :
- if `a+b` is odd then we always have infinite loop for all numbers
- if `a == b`

With out loss of generality we assume a > b

If a+b is even, we concern ourselves with how much is the difference between a and b with that of (a+b)/2 which is (a-b)/2 lets name it d_1.Where _1 denotes the iteration number



Lets see an example :

- Iteration 1 : `(a,b)`
- Iteration 2 : `(a-b,2b)`, now here there can be 3 cases `(a+b)/2 < (a-b)/2 *2`, `(a+b)/2 > (a-b)/2 *2` and `(a+b)/2 == (a-b)/2 *2`


For the first case 
We see `(a+b)/2 + q = (a-b)/2*2`

`q = (a - 3b)/2` which is the difference of `a-b` or `2b` from `a+b`

Similarly for second case `q` comes out as `(3b-a)/2`

And for third case we see `a = 3b` substituting that in `(a-b)` we have `(a-b) = 2b`. Thus its the case where we have a finite loop.

Now if we see the pattern we can make out that 
- for iteration 1

    `abs(2*d_1 - ((a+b)/2)) % ((a+b)/2) = d_2`

    `2*d_1 - c_1*((a+b)/2) = d_2`


- for iteration 2

`abs(2*d_2 - ((a+b)/2))) % ((a+b)/2) = d_3`

`4*d_2 - c_2*((a+b/2)) = d_3`

and so on 

Now if its finite it means for some `n` we have `d_n = 0` meaning 

`(2^n) * d_1 = c_n * ((a+b)/2)`

thus `d_1` accounts all other prime factors of `((a+b)/2)` apart from `2`. If thats not the case we have infinite loop.


__Solution of Problem 2__ : Once its know for each pair of trainers that wether or not their thumb wrestling match go
in an infinite loop or not, all we need to do is pair them up in an optimal way so that we have least
number of trainers left out.
Lets consider the trainer to be nodes and there is an edge if they can be matched up in infinite loop.
Now finding the maximum possible pair of trainers is to find the max matching in a graph. We use Edmond's
Blossom Algorithm for it.
The code for matching was taken from https://www.ics.uci.edu/~eppstein/software.html