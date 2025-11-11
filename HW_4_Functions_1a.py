# Task_1_a Refactor homeworks from module 2 and 3 using functional approach with decomposition.

# Module 2 Task 1 and Task 2
import random      # import the random module for random numbers
import string      # import the string module for alphabet letters


def generate_dict():
    """Generate a dictionary with random lowercase letters as keys and random integers as values."""
    dictionary = {}                          # Initialize empty dictionary
    dict_length = random.randint(1, 26)      # Random number of keys (1–26)
    for _ in range(dict_length):             # Loop for each key-value pair
        random_key = random.choice(string.ascii_lowercase)  # Pick random letter as key
        random_value = random.randint(0, 100)               # Pick random integer as value
        dictionary[random_key] = random_value               # Add key-value to dictionary
    return dictionary                        # Return the generated dictionary

def generate_list_of_dicts():
    """Generate a list of random dictionaries."""
    data_list = []                           # Initialize empty list
    list_length = random.randint(2, 10)      # Random number of dictionaries (2–10)
    for _ in range(list_length):             # Loop for each dictionary
        data_list.append(generate_dict())    # Add generated dictionary to list
    return data_list                         # Return the list of dictionaries

def analyze_dicts(data_list):
    """
    Analyze the list of dictionaries:
    - Find the highest value for each key (best_val)
    - Store the dictionary number with the highest value (best_idx)
    - Count how many times each key appears (counts)
    """
    best_val = {}                            # Store highest value for each key
    best_idx = {}                            # Store dict number with highest value
    counts = {}                              # Store count of each key
    for i, d in enumerate(data_list, start=1):   # Loop through dictionaries with index
        for k, v in d.items():                   # Loop through key-value pairs
            counts[k] = counts.get(k, 0) + 1     # Increment key count
            if k not in best_val or v > best_val[k]:  # If new max value found
                best_val[k] = v                  # Update highest value
                best_idx[k] = i                  # Update dict number
    return best_val, best_idx, counts            # Return analysis results

def merge_dicts(best_val, best_idx, counts):
    """
    Merge the analyzed data into a single dictionary:
    - If a key appears only once, keep its name
    - If a key appears more than once, add the dictionary number with the highest value to the key name
    """
    result = {}                                # Initialize result dictionary
    for k in best_val:                         # Loop through all keys
        if counts[k] == 1:                     # If key appears only once
            result[k] = best_val[k]            # Keep original key name
        else:                                  # If key appears more than once
            result[f"{k}_{best_idx[k]}"] = best_val[k]  # Add dict number to key name
    return result                              # Return merged dictionary

# Main logic
data_list = generate_list_of_dicts()           # Generate list of random dictionaries
print("Generated list of dicts:", data_list)   # Print generated list

best_val, best_idx, counts = analyze_dicts(data_list)    # Analyze dictionaries
result = merge_dicts(best_val, best_idx, counts)         # Merge analysis results
print("Merged result:", result)                          # Print final merged dictionary


