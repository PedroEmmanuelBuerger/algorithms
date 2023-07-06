def is_anagram(first_string, second_string):
    first_string = first_string.lower()
    second_string = second_string.lower()
    first_string = order_alphabet_string(first_string)
    second_string = order_alphabet_string(second_string)
    return first_string, second_string, first_string == second_string


def order_alphabet_string(string):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ordered_string = ""
    for letter in alphabet:
        if letter in string:
            ordered_string += letter
    return ordered_string


print(is_anagram("pedra", "perdaaa"))