from mlphon import PhoneticAnalyser
from MLTranslit import ml_to_en

t = ml_to_en()
mlphon = PhoneticAnalyser()


def split_ipa(ml_ipa):
    """
    Function to split the IPA representation of a Malayalam word into individual phonemes
    :param ml_ipa: string, IPA representation of word. Example: akai̯t̪aʋamaːja
    :return: the split IPA as a string. Example: a k ai̯ t̪ a ʋ a m aː j a
    """
    ipa_split = []   # Initialize an empty list to store the split IPA
    idx = 0   # Initialize an index variable to keep track of the current position in the split IPA list
    for ch in ml_ipa[0]:   # Iterate over the characters of the IPA representation
        # if character is " ̪ "[1] or "ː", concatenate the character to the last element of ipa_split
        if ch == ' ̪ '[1] or ch == "ː":
            ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        # check if character is '̯'
        elif ch == '̯':
            # handle special cases where a single phoneme comrpises of multiple characters. Eg: "au̯" is one phoneme
            if ipa_split[idx-1] in ['u', 'i'] and ipa_split[idx-2] == 'a':
                ipa_split[idx-2] = ipa_split[idx-2] + ipa_split[idx-1] + ch + ' '
                ipa_split = ipa_split[:-1]
                idx -= 1
            else:
                ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        # if character is is "ɨ" and the last element of ipa_split is "r", add character to ipa_split
        elif ch == "ɨ" and ipa_split[idx-1] == "r":
            ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        # check if the character is "ʃ"
        elif ch == "ʃ":
            # if character occurs at the beginning of the IPA representation, add character to ipa_split
            if idx == 0:
                ipa_split.append(ch)
                idx += 1
            # the last element of ipa_split is " ͡ "[1], concatenate the last two elements and the current character to the second last element (before space).
            elif ipa_split[idx-1] == ' ͡ '[1]:
                ipa_split[idx-2] = ipa_split[idx-2] + ' ͡ '[1] + ch + ' '
                ipa_split = ipa_split[:-1]
                idx -= 1
        # check if the character is "ʰ" or "ʱ"
        elif ch == "ʰ" or ch == "ʱ":
            # if the last element of ipa_split is more than one character, it replaces space with the current character
            if len(ipa_split[idx-1]) > 1:
                ipa_split[idx-1] = ipa_split[idx-1][:-1] + ch + ' '
            # else add character to ipa_split
            else:
                ipa_split[idx-1] = ipa_split[idx-1] + ch + ' '
        # if none of the conditions are met, append the current character to ipa_split
        else:
            ipa_split.append(ch)
            idx += 1
    # if constituent phoneme has only one character, append a space character. Eg., "a" -> "a "
    ipa_split = [ch + ' ' if len(ch) == 1 else ch for idx, ch in enumerate(ipa_split)]
    ipa_split = ''.join(ipa_split)   # Join all characters in the list to form a single string
    ipa_split = ipa_split.rstrip()   # Remove trailing whitespaces, if any
    return ipa_split


def get_ipa(input_words):
    """
    Function that generates IPA representation for a Malayalam word or a list of Malayaalam words.
    :param input_words: a string or a list of strings of Malayalam word(s)
    :return: a dictionary, with <malayalam_word>:<space seperated IPA representation> as the key-value pair
    """
    ipa = {}    # Initialize an empty dictionary to store the word-IPA pairs
    # Assign input to mlwords depending on datatype (string vs list of strings)
    mlwords = [''.join(input_words.split())] if isinstance(input_words, str) else input_words
    ml_ipa = ''
    for word in mlwords:
        try:
            # If current word has a valid IPA representation in mlphon library, use it as the IPA representation
            ml_ipa = mlphon.grapheme_to_phoneme(word)
        except ValueError:
            # Else, concatenate IPA representation of constituent letters
            ml_ipa[0] = ''.join([mlphon.grapheme_to_phoneme(letter)[0] for letter in word])
        ipa[word] = ' '.join(split_ipa(ml_ipa).split())
    return ipa
