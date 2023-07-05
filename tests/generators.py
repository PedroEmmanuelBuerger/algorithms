from functools import lru_cache
from random import choice, randint, shuffle
from typing import List, Tuple

import big_o

Schedule = Tuple[int, int]


def generate_schedules(
    quantity: int,
) -> Tuple[List[Schedule], int]:
    """Gera uma lista de cronogramas e um horário dentro de um dos cronogramas

    Um cronograma é uma tupla com o horário inicial e horário final.

    Parameters
    ----------
    quantity : int
        Quantidade de cronogramas gerados

    Returns
    -------
    Tuple[List[Schedule], int]
        Uma tupla com uma lista com `quantity` de cronogramas e um horário
        inicial de qualquer um dos cronogramas (aleatório)
    """
    schedule = [
        (x, x + randint(0, 3)) for x in big_o.datagen.integers(quantity, 1, 5)
    ]
    chosen_time_x = randint(1, 8)
    return schedule, chosen_time_x + randint(0, 3)


def generate_anagrams(size: int) -> Tuple[str, str]:
    """Gera duas palavras de determinado tamanho que são anagramas

    Anagramas são palavras onde as letras de uma podem formar a outra.

    Exemplo: ROMA e MORA são anagramas, pois reorganizando as letras de uma das
    palavras é possível formar a outra.

    Parameters
    ----------
    size : int
        Quantidade de caracteres em cada uma das palavras

    Returns
    -------
    Tuple[str, str]
        Duas palavras que são anagramas
    """
    first_string = big_o.datagen.strings(size)

    # * Este método é utilizado pois o shuffle opera inplace e a cópia de uma
    # * string não gera uma nova string, somente um ponteiro para a mesma ou
    # * seja: se `str1 = copy.copy(str2)` então `id(str1) == id(str2)` é True
    first_string_chars = list(first_string)
    shuffle(first_string_chars)
    second_string = "".join(first_string_chars)

    return first_string, second_string


def generate_palindromes(size: int) -> str:
    """Gera um palíndromo de um determinado tamanho

    Um palíndromo é uma palavra que pode ser lida igualmente de trás para
    frente.

    Parameters
    ----------
    size : int
        Tamanho do palíndromo a ser gerado

    Returns
    -------
    str
        Palíndromo
    """
    string = big_o.datagen.strings(size)
    mid = size // 2
    return string[:mid] + string[mid: size - mid] + string[mid - 1:: -1]


@lru_cache
def generate_integers(quantity: int) -> List[int]:
    """Gera quantidade informada de números inteiros aleatórios

    Os valores gerados são entre 1 e a `quantity` * 10, e ao menos
    uma das ocorrências é duplicada.

    A quantidade de números gerados é sempre pelo menos 2

    Parameters
    ----------
    quantity : int
        Quantidade de números a gerar

    Returns
    -------
    List[int]
        Lista de inteiros aleatórios
    """
    if quantity <= 1:
        quantity = 2

    result = []
    while len(result) < quantity - 1:
        num = randint(1, quantity * 10)
        if num not in result:
            result.append(num)

    result.append(choice(result))  # Adiciona item duplicado
    return result
