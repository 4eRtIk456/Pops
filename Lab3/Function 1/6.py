def reverse_words(sentence):
    return " ".join(sentence.split()[::-1])

s = input("Enter a sentence: ")
print(reverse_words(s))
