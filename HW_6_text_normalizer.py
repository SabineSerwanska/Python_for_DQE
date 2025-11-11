import re

def text_normalizer(text):
    """
    Normalizes the text:
    - converts to lowercase,
    - removes leading spaces from each line,
    - splits into sentences and capitalizes the first letter of each sentence,
    - replaces 'iz' with 'is' (only as a separate word, not in quotes).
    """
    # 1. Convert to lowercase and remove leading spaces from each line
    lines = text.lower().split('\n')
    lines = [line.lstrip() for line in lines]
    text_lower = '\n'.join(lines)

    # 2. Split into sentences (keeping period/exclamation/question marks)
    sentences = re.split(r'([.!?])', text_lower)
    result = []
    if len(sentences) == 1:  # No punctuation found
        # Just capitalize the whole text and add to result
        normalized = sentences[0].strip().capitalize() + '.'
    else:
        for s in range(0, len(sentences) - 1, 2):
            sentence = sentences[s].strip().capitalize() + sentences[s + 1]
            result.append(sentence)
        normalized = ' '.join(result)

    # 3. Replace "iz" with "is" (only as a separate word, not in quotes)
    normalized = re.sub(r'(?<!“)\biz\b(?!“)', 'is', normalized, flags=re.IGNORECASE)

    return normalized