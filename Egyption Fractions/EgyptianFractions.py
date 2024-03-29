#Language: Python

#Description: This program is a function that uses the greedy strategy to determine a set of distinct (i.e. all different) Egyptian 
#fractions that sum to numerator/denominator. The assumptions in this program are that the numerator and denominator are positive integers 
#as well as the numerator is less than or equal to denominator. The function 1) prints a readable "equation" showing the result and
#2) returns a list of Egyptian fraction denominators.

def egypt1(numerator,denominator):
    x = 2
    result = []
    print("{}/{} = ".format(numerator,denominator), end = " ")
    while(numerator != 0):
        if((numerator * x) >= denominator):
            result.append(x)
            numerator = (numerator * x) - denominator
            denominator = denominator * x
        x += 1
      
    print("1/{} ".format(result[0]),end="")
    i = 1 
    while i < len(result):
        print("+ 1/{}".format(result[i]), end=" ")
        i += 1
    print ()
    return result
