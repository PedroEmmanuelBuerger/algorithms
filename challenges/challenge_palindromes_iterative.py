def is_palindrome_iterative(word):
    if len(word) == 0:
        return False
    reverse_Word = ''
    for i in range(len(word)):
        reverse_Word += word[len(word)-1-i]
    return reverse_Word == word
