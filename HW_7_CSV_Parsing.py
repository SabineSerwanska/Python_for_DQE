import csv  # Import csv module for reading/writing CSV files

# Read all lines from the output file
with open('feed.txt', 'r', encoding='utf-8') as file:
    lines = []
    for line in file:
        lines.append(line)  # Add each line to the list

# Create one long string from all lines, convert to lowercase
s = ''.join(lines)  # Join all lines into a single string
s = s.replace('\n', ' ').lower()  # Replace newlines with spaces and convert to lowercase

# Remove all non-letter characters (keep spaces)
cleaned = ''.join([ch if ch.isalpha() or ch.isspace() else '' for ch in s])  # Clean string

# Split cleaned string into words
words_list = cleaned.split(' ')  # Split by spaces to get words
# print(words_list)  # Print list of words

# Count occurrences of each word
counter_dict = {}
for word in words_list:
    if word not in counter_dict and word != '':
        counter_dict[word] = 1  # Add new word to dictionary
    elif word in counter_dict:
        counter_dict[word] += 1  # Increment count for existing word

# print(counter_dict)  # Print word count dictionary

# Sort word count dictionary by value descending
counter_dict = dict(sorted(counter_dict.items(), key=lambda item: item[1], reverse=True))

# Prepare data for word-count CSV
data_words = []
for key, value in counter_dict.items():
    data_words_dict = {}
    data_words_dict['word'] = key  # Word
    data_words_dict['count'] = value  # Count
    data_words.append(data_words_dict)  # Add to list

print(data_words) # Print word statistics

# Write word-count CSV file
with open('word-count.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['word', 'count']  # CSV header
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write header
    writer.writerows(data_words)  # Write all word rows

# Prepare string for letter analysis (keep original case)
t = ''.join(lines)  # Join all lines into a single string
t = t.replace('\n', ' ')  # Replace newlines with spaces

# Remove all non-letter characters (keep spaces)
cleaned_t = ''.join([ch if ch.isalpha() or ch.isspace() else '' for ch in t])  # Clean string

# Count occurrences of each letter (case-sensitive)
counter_letter = {}
for l in cleaned_t:
    if l not in counter_letter and l != ' ':
        counter_letter[l] = 1  # Add new letter to dictionary
    elif l in counter_letter:
        counter_letter[l] += 1  # Increment count for existing letter

# Sort letter count dictionary by letter alphabetically
counter_letter = dict(sorted(counter_letter.items(), key=lambda item: item[0]))
# print(counter_letter)  # Print letter count dictionary

# Calculate total number of letters
list_values = []
for value in counter_letter.values():
    list_values.append(value)  # Add each letter count to list

sum_all_letters = sum(list_values)  # Sum all letter counts

# Prepare set of all unique letters in lowercase
list_letters = set([key.lower() for key in counter_letter.keys()])
# print(sorted(list_letters))  # Print sorted list of unique letters

# Prepare data for letter-count CSV
data_letters = []
for letter in sorted(list_letters):
    count_lower = counter_letter.get(letter, 0)  # Count of lowercase letter
    count_upper = counter_letter.get(letter.upper(), 0)  # Count of uppercase letter
    count_all = count_lower + count_upper  # Total count for this letter
    percentage = round(count_all / sum_all_letters * 100, 2)  # Percentage of all letters
    data_letters_dict = {
        'letter': letter,
        'count_all': count_all,
        'count_uppercase': count_upper,
        'percentage': percentage
    }
    data_letters.append(data_letters_dict)  # Add to list

print(data_letters)  # Print letter statistics

# Write letter-count CSV file
with open('letter-count.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']  # CSV header
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write header
    writer.writerows(data_letters)  # Write all letter rows

