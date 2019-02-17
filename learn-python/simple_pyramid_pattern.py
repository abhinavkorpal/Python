# Patterns can be printed in python using simple for loops. 
# First outer loop is used to handle number of rows and Inner nested loop is used to handle the number of columns. 
# Manipulating the print statements, different number patterns, alphabet patterns or star patterns can be printed.

# Python 3.x code to demonstrate star pattern 
# Function to demonstrate printing pattern 
def pypart(n): 
      
    # outer loop to handle number of rows 
    # n in this case 
    for i in range(0, n): 
      
        # inner loop to handle number of columns 
        # values changing acc. to outer loop 
        for j in range(0, i+1): 
          
            # printing stars 
            print("* ",end="") 
       
        # ending line after each row 
        print("\r") 
  
# Driver Code 
n = 5
pypart(n)

# Another Approach:
# Using List in Python 3, this could be done in a simpler way

def pypart1(m):
    myList = []
    for i in range(1,m+1):
        myList.append("* "*i)
    print("\n".join(myList))

m = 5
pypart1(m)


