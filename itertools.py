from itertools import repeat
from itertools import permutations
from itertools import dropwhile



# for i in repeat(2, 10):
#     print(i)



# values = ['Robber duck', 'Teapot', 'One Stock']

# repeat_list = list(zip(repeat("repeat", len(values)), values))

# for i, v in repeat_list:
#     print(f"{i}: {v}")



# xs = permutations("Python")
# for x in xs:
#     print(''.join(x))





# elems = ['a', 'b', 'c', 'd']
# size = 4

# params = permutations(elems, size)
# for perm in params:
#     print(perm)



# numbers = [1,3,4,5,8,2,7,6,9]

# filter_num = dropwhile(lambda x: x < 5 , numbers)

# print(list(filter_num))


# students = [('Jeffery', 60),('Gravvy', 85),('Ezekiel', 70),('Luna', 70)]
# print(students[1][1])


# filter_students = dropwhile(lambda student: student[1] < 75, students)

# filter_students = dropwhile(lambda student: student[1][1] < 75, students)  // TypeError: 'int' object is not subscriptable

# print(list(filter_students))




# from itertools import cycle
# # import random
# names = ['Jeffery', 'Gravvy', 'Ezekiel', 'Luna']

# developer_cycle = cycle(names)

# print('Code review:')

# for week in range(1, 53):
#     current = next(developer_cycle)
#     print(f'Week: {week} code review led by {current}')





# numbers = [1,10,3,4,5,8,2,7,6,9]

# filter_num = dropwhile(lambda x: x < 5 , numbers)
# filter_numtwo = list(filter(lambda x: x % 2 == 0, numbers))
# print(filter_numtwo)
# map= list(map(lambda x: x **2 , numbers))
# print(map)


# print(list(filter_num))
# for num in numbers:
#     print(num)
    
# print("---------------")    

# for num in range(len(numbers)):
#     print(numbers[num])    



# students = [('Jeffery', 60),('Gravvy', 85),('Ezekiel', 70),('Luna', 70)]
# print(students[1][1])

# filter_students = dropwhile(lambda student: student[1] < 75, students)

# filter_students = dropwhile(lambda student: student[1][1] < 75, students)  // TypeError: 'int' object is not subscriptable

# print(list(filter_students))


# from functools import reduce

# myList = [3,4,5,6,8]
# r = reduce(lambda x, y: x if x<y else y ,myList)
# print(r)


# for i in repeat("hello", 10):
    # print(i)




# values = ['Robber duck', 'Teapot', 'One Stock']
# valuestwo = ["tree", "shop", "branch"]
# valuethree = [122,44,66]

# result = zip(values, valuestwo, valuethree)
# data  = list(result)
# print(list(result))
# a,b,c = zip(data)
# print(a)
# print(b)
# print(c)

# newlist = [2,3,45,96,200,5,8,9]

# maxvalue = newlist[0]
# maxvalue_index = 0

# min_value = newlist[0]
# min_value_index = 0

# for i in range(len(newlist)):
#     if newlist[i] > maxvalue:
#         maxvalue = newlist[i]   
#         maxvalue_index = i
#     if newlist[i] < min_value:
#         min_value = newlist[i]
#         min_value_index = i


# print("maximum value: ",maxvalue)
# print("maximun value index: ",maxvalue_index)

# print("smallest value: ", min_value)
# print("smallest value index: ", min_value_index)




# small_element = 1
# for i in newlist:
#     if i < small_element:
#         small_element = i

# print(small_element)


# input --->
my_list = [
    {"name":"john", "age": 33, "address": "kolkata"},
    {"name":"david", "age": 40, "address": "kolkata"},
    {"name":"liam", "age": 31, "address": "kolkata"},
    {"name":"liam", "age": 31, "address": "kolkata"},
    {"name":"jack", "age": 23, "address": "kushmandi"},
    {"name":"peter", "age": 24, "address": "kushmandi"},
    {"name":"socker", "age": 24, "address": "kushmandi"},
    {"name":"jennie", "age": 24, "address": "kushmandi"}
] 

# output --> [{"address": "kolkata", "number_of_user": 3},{"address": "kushmandi", "number_of_user": 2}]

empty_list: list = []

my_dict: dict = {}
default_dict_if_user_not_found: dict = {}
my_dict_Two: dict = {}

user_count = 0
user_count_two = 0 

for iter in my_list:
    for key, value in iter.items():

        if value == "kolkata":
            user_count += 1
            my_dict[key] = value
            my_dict['number of user'] = user_count    

        if value == "kushmandi":
            user_count_two += 1
            my_dict_Two[key] = value
            my_dict_Two['number of user'] = user_count_two       



empty_list.append(my_dict)
empty_list.append(my_dict_Two)

result = empty_list
print(result)






nested_list = [[1,2,3,9], [4,5,6], [7,8,9]]

newlist = [num for sublist in nested_list for num in sublist if num % 2 == 0]


print(str(newlist))


numbers = [1,2,3,4,5,6,7,8,9,10]

answer = [ "Even" if num % 2 == 0 else "Odd" for num in numbers ]
print(answer)

rep = [i for i in repeat("debashis", 5)]
print(rep)
# print(len(nested_list[0]))

for i in range(len(nested_list[0])):
    print(nested_list[0][i], end ='-->\n')


my_string = "Longbook"

reversed_string = ''
for text in my_string:
    reversed_string = text + reversed_string 
    
print("Reversed string: ",reversed_string)



names = "Tea"
combination = permutations(names)
for xs in combination:
    print(''.join(xs))

from itertools import takewhile, groupby, count
# students = [('Jeffery', 860),('Gravvy', 85),('Ezekiel', 70),('Luna', 70)]

# filter_students = takewhile(lambda student: student[1] >= 80, students)
# print(list(filter_students))


students = [('Jeffery', 96),('Gravvy', 85),('Ezekiel', 70),('Luna', 70)]

sorted_student = sorted(students,key = lambda x: x[1])
grouping = groupby(sorted_student, lambda x: x[1])

for grade, group in grouping:
    print(f"Grade {grade}: {[student[0] for student in group]}") 

for number in count(start =1, step = 2):
    if number > 10:
        break
    print(number)

print()
for number in count(start =1, step = 1):
    if number % 2 == 0:
        print(number)
    if number > 10:
        break   



list_element = [3,4,5,7,22,44,6,776,9000,43]

largest_element = list_element[0]
index_position = 0

for i in range(len(list_element)):
    if list_element[i] > largest_element:
        largest_element = list_element[i]
        index_position = i+1

print("Largest element ",largest_element)
print("its index position ",index_position)


import itertools

for i in itertools.count(5,5):
    if i == 35:
        break
    print(i, end =' ')
print()


import itertools
count = 0
for i in itertools.cycle("ab"):
    i = i + "e"
    if count > 7:
        break
    
    print(i, end =" ")
    count += 1



l = ['Geeks', 'for', 'geeks']

iterators = itertools.cycle(l)

for i in range(3):
    print(next(iterators), end= " ")



l = [1, 2, 3]

iterators = itertools.cycle(l)

for i in range(6):
    print(next(iterators), end= " ")      