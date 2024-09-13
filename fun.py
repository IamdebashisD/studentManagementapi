my_list = [1, 2, 3, 4, 5]
print("before swapping",my_list)

# Using Multiple Assignment
my_list[0], my_list[-1] = my_list[-1], my_list[0]
print("after swapping Using Multiple Assignment",my_list)


# now swapping using temporary variable
# my_list[-1] =1, my_list[0] =5 
temp = my_list[-1]
my_list[-1] = my_list[0]
my_list[0] = temp
print("now swapping using temporary variable", my_list)

# swapping using addition and subtraction 
my_list[0] = my_list[0] + my_list[-1]
my_list[-1] = my_list[0] - my_list[-1]
my_list[0] = my_list[0] - my_list[-1]
print("Another swapping using addition and subtraction", my_list)


# swapping using XOR bitwise operator 
my_list[0] = my_list[0] ^ my_list[-1]
my_list[-1] = my_list[0] ^ my_list[-1]
my_list[0] = my_list[0] ^ my_list[-1]

print("Bitwise XOR operator swapping", my_list)




# number =  5

# if (number == 5):
#     number += 1
#     print('1')

#     if (number == 8):
#         print('2')

# else:
#     print('3')        


import re

txt = "heo planet"

#Search for a sequence that starts with "he", followed by 0 or 1  (any) character, and an "o":

x = re.findall("he.?o", txt)

for i in x:
    print(x)


if x:
    print("matches the pattern")
else:
    print("no matches found")    



scores: list[int] = [20, 23, 4, 52, 98, 66, 34,71, 35, 47, 100,]
# even:list = list()
# for score in scores:
#     if score % 2== 0:
#         even.append(score)

even:list = [score for score in scores if score % 2 == 0]

print("Even", even)  