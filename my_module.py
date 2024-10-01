# from random import randint

# def random_list():
#     num_list = list()
#     for i in range(10):
#         num_list.append(randint(0, 100))
#     print("list of random number", num_list )

# if __name__ == '__main__':
#     random_list()        



# scores: list[int] = [20, 23, 4, 52, 98, 66, 34,71, 35, 47, 100,]
# # even:list = list()
# # for score in scores:
# #     if score % 2== 0:
# #         even.append(score)

# even:list = [score for score in scores if score % 2 == 0]

# print("Even", even)        
                    

# scores: dict[str, int] = {"Josh": 85, "Chuck": 75, "Charlie": 90, "David": 72, "Annie": 58}
# for keys in scores:
#     print(keys, scores[keys])
# l = {keys: value for keys, value in scores.items()}
# print(l)




# chai_types: dict[str, str] = {'Masala' : 'Spicy', 'Ginger' : 'Zesty', 'Green' : 'Mild'}

# print(chai_types.get('Gingery'))
# chai_types['Green'] = 'Fresh'

# print(chai_types)

# if 'Masala' in chai_types:
#     print("I have Masala chai")




# scores: dict[str, int] = {"Josh": 85, "Chuck": 75, "Charlie": 90, "David": 72, "Annie": 58}

# results = {}
# for student, score in scores.items():
#     if scores[student] >= 60:
#         results[student] = "Pass"
#     else:
#         results[student] = "Fail"

# results = {student: ("Passed" if score >= 60 else "Failed") for student, score in scores.items()}
# print("Result:", results)


# def function_1(numbers: list[int]) -> list[int]:
#     even = list()
#     for n in numbers:
#         if n % 2== 0:
#             even.append(n)
#     return even        

# numbers: list[int] = [20, 23, 4, 52, 98, 66, 34,71, 35, 47, 100,]
# output = function_1(numbers)
# print(output)



# def function_2(scores: list[str, int]) -> dict[str, str]:
#     results = {}
#     for student, score in scores.items():
#         if score >= 70:
#             results[student] = "Pass"
#         else:
#             results[student] = "Fail"
#     return results        

# scores: dict[str, int] = {"Josh": 85, "Chuck": 75, "Charlie": 90, "David": 72, "Annie": 58}
# output = function_2(scores)
# print(output)



def add_items(item, items = None) -> list[int]:
    if items == None:
        items = []
    if type(item) == int:
        items.append(item)
        return items
    else:
        return ValueError('method only takes integer number')

print(add_items(1))
print(add_items(2))
print(add_items(8))
print(add_items('hujhgugh'))



scores: dict[str: int] = {"Josh": 85, "Chuck": 75, "Charlie": 90, "David": 72, "Annie": 58}

results = {}
for student, score in scores.items():
    if scores[student] >= 60:
        results[student] = "Pass"
    else:
        results[student] = "Fail"
print("Results", results)


result = {student: ("pass" if scores[student] >= 60 else "Fail") for student, score in scores.items()} # dictionary comprehension
print("Result:",result)

import json
x = '{"name": "John", "age": 30, "married": true, "divorced": false, "children": ["Ann","Billy"], "pets": null, "cars": [{"model": "BMW 230", "mpg": 27.5}, {"model": "Ford Edge", "mpg": 24.1}]}'
y = json.loads(x)
print(y)
