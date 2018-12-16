
#function that finds greatest common divisor using Euclidian algorithm. 
#For math description of the algorithm, visit https://en.wikipedia.org/wiki/Euclidean_algorithm
def euclidianGCD(a, b):
    #check if either of the inputs is zero
    if (a==0 or b==0):
        if (a==0 and b!=0):
            return b
        elif (a!=0 and b==0):
            return a
        else:#if both are zero
            print("Cannot return a common divisor when both inputs are zero. Return None.")
            return None
    else:#if neither input is zero
        a_new = abs(a-b)
        b_new = min(a, b)
      
        while (a_new != b_new):
            this_a = a_new
            this_b = b_new
            
            a_new = abs(this_a - this_b)
            b_new = min(this_a, this_b)
        
        return a_new #alternatively, might return b_new since they are the same thing with a_new
