# Task_1_b Refactor homeworks from module 2 and 3 using functional approach with decomposition.

# Module 3
import re

s = """homEwork:
 tHis iz your homeWork, copy these Text to variable.

 You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

 it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.

 last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87."""


import re

# 1. Convert the text to lowercase and split it into lines
def lowercase_converter(s):
    return s.lower().split('\n')

# 2. Remove leading spaces from each line
def remover_leading_spaces(lines):
    return [line.lstrip() for line in lines]

# 3. Join the lines back into a single text with line breaks
def joiner_lines(lines):
    return '\n'.join(lines)

# 4. Split the text into sentences, keeping periods and colons at the end
def spliting_text_into_sentences(text):
    sentences = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            sentences.append('')
        else:
            parts = re.findall(r'.*?[.:](?=\s|$)', line)
            if parts:
                sentences.extend([p.strip() for p in parts])
            else:
                sentences.append(line)
    return sentences

# 5. Capitalize the first letter of each sentence (if not empty)
def capitalizer(sentences):
    return [sent.strip().capitalize() if sent.strip() else '' for sent in sentences]

# 6. Extract the header (first sentence)
def header_extractor(sentences):
    return sentences[0]

# 7. The rest is the body
def body_sentences_extractor(sentences):
    return sentences[1:]

# 8. Create a new sentence from the last word of each existing sentence
def new_sentence_creator(body_sentences):
    last_words = []
    for sent in body_sentences:
        words = re.findall(r"\b[\w']+\b", sent)
        if words:
            last_words.append(words[-1])
    return ' '.join(last_words).capitalize() + '.'

# 9. Insert the new sentence after the 4th sentence in the body
def inserter(body_sentences, new_sentence):
    result = body_sentences.copy()
    result.insert(4, new_sentence)
    return result

# 10. Join the body sentences into a single text, preserving empty lines
def joiner_body_sentences(body_sentences):
    final_body = ''
    for sent in body_sentences:
        if sent == '':
            final_body = final_body.rstrip() + '\n\n'
        else:
            final_body += sent + ' '
    return final_body.rstrip()

# 11. Replace "iz" with "is" (only if it is a separate word and not in quotes)
def replacer(text):
    return re.sub(r'(?<!“)\biz\b(?!“)', 'is', text, flags=re.IGNORECASE)

# 12. Count all whitespace characters in the original text and fixed text
def whitespaces_counter(original, fixed):
    return sum(1 for ch in original if ch.isspace()), sum(1 for ch in fixed if ch.isspace())

# FINAL RESULT
def final_result(s):
    # Step 1-3
    lower_lines = lowercase_converter(s)
    stripped_lines = remover_leading_spaces(lower_lines)
    text_lower = joiner_lines(stripped_lines)
    # Step 4-5
    sentences = spliting_text_into_sentences(text_lower)
    normalized_sentences = capitalizer(sentences)
    # Step 6-7
    header = header_extractor(normalized_sentences)
    body_sentences = body_sentences_extractor(normalized_sentences)
    # Step 8-9
    new_sentence = new_sentence_creator(body_sentences)
    body_with_new = inserter(body_sentences, new_sentence)
    # Step 10-11
    final_body = joiner_body_sentences(body_with_new)
    final_body = replacer(final_body)
    # Step 12-13
    whitespace_count_original_text, whitespace_count_fixed_text = whitespaces_counter(s, header + '\n' + final_body)
    # Step 14
    print(f'{header}\n{final_body}\n')
    print(f"Number of whitespace characters in original text: {whitespace_count_original_text}")
    print(f"Number of whitespace characters in fixed text: {whitespace_count_fixed_text}")

final_result(s)

