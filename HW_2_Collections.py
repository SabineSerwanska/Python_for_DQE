# Write a code, which will:
#
# 1. create a list of random number of dicts (from 2 to 10)
# dict's random numbers of keys should be letter,
# dict's values should be a number (0-100),
# example:[{'a': 5, 'b': 7, 'g': 11}, {'a': 3, 'c': 35, 'g': 42}]
import random      # import the random module for random numbers
import string      # import the string module for alphabet letters

data_list = []     # create an empty list to store dictionaries
list_length = random.randint(2, 10)   # choose random number of dictionaries (2–10)

for n in range(list_length):           # repeat for each dictionary
    dictionary = {}                    # create empty dictionary
    dict_length = random.randint(1, 26)  # choose random number of keys (1–26- numbers of letters in English alphabet)
    for k in range(dict_length):         # repeat for each key-value pair
        random_key = random.choice(string.ascii_lowercase)  # pick random lowercase letter as key
        random_value = random.randint(0, 100)               # pick random number (0–100) as value
        dictionary[random_key] = random_value               # add pair to dictionary
    data_list.append(dictionary)                            # add dictionary to main list

print(data_list)      # print the final list of dictionaries


# 2. get previously generated list of dicts and create one common dict:
#
# if dicts have same key, we will take max value, and rename key with dict number with max value
# if key is only in one dict - take it as is,
# example:{'a_1': 5, 'b': 7, 'c': 35, 'g_2': 42}

best_val = {}   # store the highest value for each key
best_idx = {}   # store the dictionary number with the highest value
counts = {}     # count how many times each key appears

for i, d in enumerate(data_list, start=1):   # loop through all dictionaries
    for k, v in d.items():                   # loop through key-value pairs
        counts[k] = counts.get(k, 0) + 1     # count each key occurrence
        if k not in best_val or v > best_val[k]:   # check if value is higher
            best_val[k] = v                  # save the new highest value
            best_idx[k] = i                  # save dictionary number

result = {}   # create final result dictionary

for k in best_val:                          # go through all keys
    if counts[k] == 1:                      # if key appeared only once
        result[k] = best_val[k]             # keep key name as it is
    else:                                   # if key appeared more than once
        result[f"{k}_{best_idx[k]}"] = best_val[k]  # add dictionary number to key name

print(result)   # print the final result

