import re

def match_string(s):
    pattern = r"ab{2,3}$" 
    return bool(re.fullmatch(pattern, s))

test_strings = ["abb", "abbb", "ab", "a", "abbbb", "abbc"]
for s in test_strings:
    print(f"{s}: {match_string(s)}")