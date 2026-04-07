#1. Рядки (Strings)
def len_str(text):
    return len(text)
print(len_str("Hello teacher!!!"))
print(len_str("My Homework!"))
def plus_str(str1, str2):
    return str1 + str2
print(plus_str("Hello", " world"))
print(plus_str("Men", " Power"))

#2. Числа (Int/float)
def sqr_num(num):
    return num ** 2
print(sqr_num(10))
print(sqr_num(100))

def sum_num(num1, num2):
    return num1 + num2
print(sum_num(1, 2))
print(sum_num(4, 5))
def div_remainder(a, b):
    if b == 0:
        return "Division by zero"
    integer_part = a//b
    remainder_part = a%b
    return integer_part, remainder_part
print(div_remainder(5, 2))
print(div_remainder(10, 0))

#3. Списки (Lists)
def average(numbers):
    return sum(numbers) / len(numbers)
print(average([1, 2, 3, 4, 5]))
print(average([9, 15]))
def common_el(list1, list2):
    result = []
    for el in list1:
        if el in list2:
            result.append(el)
    return result
print(common_el([1, 2, 3], [2, 3, 4]))

#4. Словники (Dictionaries)
def key_print(data):
    return list(data.keys())
my_dict = {"name" : "Oleksandr", "surname" : "Bychkov", "age" : 27}
print(key_print(my_dict))
def sum_dicts(dict1, dict2):
    return dict1 | dict2
dict1 = {"name": "Oleksandr", "surname": "Bychkov", "age" : 27}
dict2 = {"city": "Bucharest", "index": 7007,  "country" : "Romania"}
print(sum_dicts(dict1, dict2))

#5. Множини (Sets)
def union_sets(set1, set2):
    return set1.union(set2)
set1 = {1, 2, 3, 4, 5}
set2 = {6, 7, 8, 9}
print(union_sets(set1, set2))
def is_subset(set1, set2):
    return set1.issubset(set2)
set1 = {1, 2, 3}
set2 = {1, 2, 3, 4, 5, 6}
print(is_subset(set1, set2))

#6. Умовні вирази та цикли
def check_num(num):
    if num % 2 == 0:
        return True
    else:
        return False
print(check_num(5))
def get_number(numbers):
    result = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result
print(get_number([22, 31, 54, 12, 11, 99, 66]))

#7. лямбда-функція
check_even = lambda x: "парне" if x % 2 == 0 else "не парне"
print(check_even(4))
print(check_even(7))