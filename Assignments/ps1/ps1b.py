###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    if target_weight ==0:
        return []
    eggs_added= []
    for i in egg_weights:
        test_eggs = []
        if target_weight-i >=0:
            test_eggs.append(i)
            if target_weight -i not in memo:
                sim = dp_make_weight(egg_weights, target_weight-i, memo)
                memo[target_weight -i] = sim
            else:
                sim = memo[target_weight -i]
            if sim != None:
                test_eggs += sim
        if len(test_eggs) > 0:
            eggs_added.append(test_eggs)
            
    if len(eggs_added)> 0:
        d = {}
        for i in eggs_added:
            if target_weight - sum(i) in d:
                d[target_weight - sum(i)].append(list(i))
            else:
                d[target_weight - sum(i)] = []
                d[target_weight - sum(i)].append(list(i))
        t = sorted(d)
        t_key = t[0]
        t = d[t_key]
        t.sort(key=len)
        memo[target_weight] = t[0]
        return t[0]
    else:
        []

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25,75,50,99)
    n = 6
    #print("Egg weights = (1, 5, 10, 25)")
    #print("n = 99")
    #print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print(dp_make_weight(egg_weights, n))