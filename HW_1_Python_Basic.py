# Task_1 Create list of 100 random numbers from 0 to 1000
import random                                       # import module random

numbers = []                                        # creating empty list with all optional num

for i in range(0, 1001):                            # populate list using loop for
    numbers.append(i)

# numbers = list(range(1001))                       # creating list in one line


random_list = []                                    # creating empty list for result

while len(random_list) < 100:                       # populate list using while loop
    num = random.choice(numbers)
    if num not in random_list:                      # ensure no duplicate
        random_list.append(num)                     # adding num to list with result

# random_list = random.sample(range(1001), 100)    # generate result using existing method (in random module) in one line

# print(random_list)                                 # checking result
# print(len(random_list))                            # checking result


# Task_2 Sort list from min to max(without using sort())
sorted_list = []                                    # create empty list for sorted elements

for i in range(len(random_list)):                   # using for loop for iterating tru all indexs in list
    a = min(random_list)                            # finding min number in list
    sorted_list.append(a)                           # adding min number to sorted list
    random_list.remove(a)                           # removing min element from list

# print(sorted_list)                                # checking result


# Task_3 Calculate average for even and odd numbers
even_num = []                                      # create empty list for even numbers
odd_num = []                                       # create empty list for even numbers

for i in sorted_list:                              # for loop for adding even/odd elements to list
    if i % 2 == 0:
        even_num.append(i)
    else:
        odd_num.append(i)

even_num = [x for x in sorted_list if x % 2 == 0]   # the same as loop but using list comprehension
odd_num = [x for x in sorted_list if x % 2 != 0]    # the same as loop but using list comprehension

avg_even = sum(even_num) / len(even_num)            # calculate avg for even numbers
avg_odd = sum(odd_num) / len(odd_num)               # calculate avg for odd numbers

print(avg_even)                                    # print result
print(avg_odd)                                     # print result






