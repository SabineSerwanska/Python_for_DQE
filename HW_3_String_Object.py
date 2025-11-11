import re

s = """homEwork:
 tHis iz your homeWork, copy these Text to variable.

 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


# 1. Convert the text to lowercase and split it into lines
lower_lines = s.lower().split('\n')
# print(f'lower_lines {lower_lines} \n')

# 2. Remove leading spaces from each line
stripped_lines = [line.lstrip() for line in lower_lines]
# print(f'stripped_lines: {stripped_lines}')

# 3. Join the lines back into a single text with line breaks
text_lower = '\n'.join(stripped_lines)
# print(f'text_lower: {text_lower}\n')

# 4. Split the text into sentences, keeping periods and colons at the end
sentences = []
for line in text_lower.split('\n'):
    line = line.strip()  # Remove leading/trailing spaces from the line
    if not line:
        sentences.append('')  # Keep empty lines as separators
    else:
        # Find all sentence parts ending with a period or colon
        parts = re.findall(r'.*?[.:](?=\s|$)', line)
        if parts:
            sentences.extend([p.strip() for p in parts])  # Add found sentences
        else:
            sentences.append(line)  # Add the line if no sentence end found

# print(sentences)
# print(f'sentences: {sentences} \n')

# 5. Capitalize the first letter of each sentence (if not empty)
normalized_sentences = [sent.strip().capitalize() if sent.strip() else '' for sent in sentences ]
# print(f'normalized sentence: {normalized_sentences} \n')

# 6. Extract the header (first sentence)
header = normalized_sentences[0]  # "Homework:"
# 7. The rest is the body
body_sentences = normalized_sentences[1:]
# print(f'header {header}')
# print(f'body {body_sentences} \n')

# 8. Create a new sentence from the last word of each existing sentence
last_words = []
for sent in body_sentences:
    words = re.findall(r"\b[\w']+\b", sent)  # Find all words in the sentence
    if words:
        last_words.append(words[-1])  # Add the last word
new_sentence = ' '.join(last_words).capitalize() + '.'  # Join last words and capitalize
# print(f'lista {last_words} \n')
# print(f'new_sentence {new_sentence}')

# 9. Insert the new sentence after the 4th sentence in the body
body_sentences.insert(4, new_sentence)

# 10. Join the body sentences into a single text, preserving empty lines
final_body = ''
for sent in body_sentences:
    if sent == '':
        final_body = final_body.rstrip() + '\n\n'  # Remove space before new line, add double line break
    else:
        final_body += sent + ' '  # Add sentence and a space

final_body = final_body.rstrip()  # Remove the last space

# print(f'final_body {final_body} \n')

# 11. Replace "iz" with "is" (only if it is a separate word and not in quotes)
final_body = re.sub(r'(?<!“)\biz\b(?!“)', 'is', final_body, flags=re.IGNORECASE)
# print(f'final_body {final_body} \n')

# 12. Count all whitespace characters in the original text
whitespace_count_original_text = sum(1 for ch in s if ch.isspace())
# 13. Count all whitespace characters in the fixed text (header + body)
whitespace_count_fixed_text = sum(1 for ch in (header + '\n' + final_body) if ch.isspace())

# 14. Print the final result
print(f"{header}\n{final_body}\n")
print(f"Number of whitespace characters in original text: {whitespace_count_original_text}")
print(f"Number of whitespace characters in fixed text: {whitespace_count_fixed_text}")

