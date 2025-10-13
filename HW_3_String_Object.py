s = """homEwork:
 tHis iz your homeWork, copy these Text to variable.



 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""



import re


# 1. Normalize the text to have consistent letter casing
normalized_text = s.lower()
# Spiting sentence
sentences = re.split(r'(?<=\.)', normalized_text)  # Split only by dot
normalized_sentences = [sentence.strip().capitalize() for sentence in sentences]  # Capitalize each sentence and remove whitespice from end
final_normalized_text = ' '.join(normalized_sentences)

# 2. Creating new sentence from last words
last_words = []
for sentence in normalized_sentences:
    words = sentence.strip().split()
    if words:  # if sentence is empty
        last_words.append(words[-1])  # add last word
last_words_not_dot = [element[:-1] if element.endswith('.') else element for element in last_words]


last_words_not_dot[0] = last_words_not_dot[0].capitalize()


new_sentence = ' '.join(last_words_not_dot) # join words in sentence


final_text_with_new_sentence = final_normalized_text + '' + new_sentence + '.'

# 3. Change from "iZ" to "is"
fixed_text = re.sub(r'\biz\b', 'is', final_text_with_new_sentence, flags=re.IGNORECASE)

# 4. Count all whitespace
whitespace_count = sum(1 for char in fixed_text if char.isspace())

# 5. Print result
print(fixed_text)
print(f'Number of whitespace characters: {whitespace_count}')

