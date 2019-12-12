__author__ = 'max'

import re
MAX_CHAR_LENGTH = 45
NUM_CHAR_PAD = 2

# Regular expressions used to normalize digits.
# DIGIT_RE = re.compile(br"\d")
DIGIT_RE = re.compile(r"\d")    # 2to3

def get_token(pos_tagged):
    tagged_list = pos_tagged.split('|')
    token = list()
    for tagged in tagged_list:
        #print(tagged)
        if '//' in tagged:  # //SP
            tok = '/'
        else:
            tok, _ = tagged.split('/')
        token.append(tok)
    token = ''.join(token)
    return token
