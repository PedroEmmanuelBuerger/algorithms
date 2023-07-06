def is_anagram(first_string, second_string):
    first_string = first_string.lower()
    second_string = second_string.lower()
    if len(first_string) < 1 and len(second_string) < 1:
        return first_string, second_string, False
    first_string = order_alphabet_string(first_string)
    second_string = order_alphabet_string(second_string)
    return first_string, second_string, first_string == second_string


def order_alphabet_string(string):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ordered_string = ""
    for letter in alphabet:
        if letter in string:
            ordered_string += letter * string.count(letter)
    return ordered_string
