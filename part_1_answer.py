# A. Given an array A of N integers, write a function missing_int(A) that returns the smallest positive integer (greater than 0) that does not occur in A.

# ○ A = [1, 3, 6, 4, 1, 2] should return 5
# ○ A = [1, 2, 3] should return 4
# ○ A = [-1, -1, -1, -5] should return 1
# ○ A = [1, 3, 6, 4, 1, 7, 8, 10] should return 2

def missing_int(A):

  num = 0

  for x in range(min(A), max(A)+1):

    if x not in A:
      num = x
      break
  
  else:

    num = max(A) + 1

  return 1 if min(A) < 0 and max(A) < 0 else num

print(missing_int([1, 3, 6, 4, 1, 7, 8, 10]))

# B. Write a function find_divisible(a, b, k) that accepts three integers: a, b and k, and returns the count of the numbers between a and b that are divisible by k
# ○ find_divisible(6,11,2) should return 3
# ○ find_divisible(0,11,2) should return 6

def find_divisible(a, b, k):

  count_div = 0

  for x in range(a,b+1):

    if (x % k) == 0:
      count_div += 1
  
  return count_div

print(find_divisible(6,11,2))

# C. Write a rotate(A, k) function which returns a rotated array A, k times; that is, each element of A will be shifted to the right k times

# ○ rotate([3, 8, 9, 7, 6], 3) returns [9, 7, 6, 3, 8]
# ○ rotate([0, 0, 0], 1) returns [0, 0, 0]
# ○ rotate([1, 2, 3, 4], 4) returns [1, 2, 3, 4]

def rotate(A, k):

  for i in range(0, k):

    temp = A[len(A)-1] 

    for j in range(len(A)-1, 0, -1):

      A[j] = A[j-1]

    A[0] = temp

  return A  

print(rotate([1, 2, 3, 4], 4))