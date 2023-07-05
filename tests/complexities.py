import json
from dataclasses import dataclass, field
from itertools import zip_longest
from statistics import mean, median, stdev
from timeit import repeat
from typing import Any, Callable, List, Optional, Union

import big_o
import matplotlib.pyplot as plt
import numpy as np

Times = List[Union[float, int]]
Sizes = List[int]

NOTATIONS = {
    big_o.complexities.Constant: "O(1)",
    big_o.complexities.Logarithmic: "O(log n)",
    big_o.complexities.Linear: "O(n)",
    big_o.complexities.Linearithmic: "O(n log n)",
    big_o.complexities.Quadratic: "O(n^2)",
    big_o.complexities.Cubic: "O(n^3)",
    big_o.complexities.Polynomial: "O(n^x)",
    big_o.complexities.Exponential: "O(2^n)",
}


@dataclass
class ComplexityInferenceData:
    """
    Parameters
    ----------
    função_analisada : Callable
        Função cuja complexidade será inferida
    função_de_geração : Callable[[int], List[Any]]
        Função que irá gerar entradas para a função analisada

        Ela deverá receber um inteiro, contendo o número de elementos a serem
        gerados para servir como entradas da função analisada

        O retorno dessa função deve ser, preferencialmente, uma lista de
        valores que levem o algoritmo da função analisada ao pior caso de
        complexidade de tempo
    ordens_de_grandeza : int, opcional
        Quantidade de ordens de grandeza das entradas geradas, começando de
        `ordem_inicial`, por padrão 4
    ordem_inicial : int, opcional
        Primeira ordem de grandeza à qual a `base_de_grandeza` será elevada.
        Sugere-se que esse valor não seja muito pequeno, visto que para
        tamanhos de entrada pequenos os tempos mensurados para a execução de
        algoritmos são imprecisos do ponto de vista de análise assintótica,
        por padrão 3
    base_de_grandeza : int, opcional
        Base da geração das ordens de grandeza das entradas: o número que é
        elevado a `ordens_de_grandeza` para definir a quantidade de elementos
        a serem gerados, por padrão 10
    quantidade_de_execuções : int, opcional
        Quantidade de vezes que a função analisada deve ser executada com a
        mesma entrada para medir o tempo total de todas as execuções

        Se a função for muito rápida, convém executar ela algumas milhares de
        vezes para a medição do tempo total de execução dessas milhares de
        vezes, de forma a ter um valor próximo de 1 segundo inteiro ou mais,
        visto que valores muito pequenos de tempo podem ser imprecisos

        Por padrão 10000
    vezes_a_repetir : int, opcional
        Quantidade de vezes a repetir a temporização, de forma a garantir
        picos de uso de CPU não irão atrapalhar a medição

        Por padrão 10
    """

    analyzed_function: Callable
    generation_function: Callable[[int], Any]
    order_of_magnitude: int = 4
    base_of_magnitude: int = 10
    execution_quantity: int = 10_000
    times_to_repeat: int = 10
    initial_order: int = 3


@dataclass
class MeasurementResults:
    registered_sizes: Sizes
    registered_times: Times
    registered_means: List[float] = field(default_factory=lambda: [])
    registered_deviations: List[float] = field(default_factory=lambda: [])


def measure_execution_times(
    data: ComplexityInferenceData,
) -> MeasurementResults:
    """Mede os tempos de execução de uma função

    O objetivo da função é inferir a melhor complexidade alcançada, visto que
    instabilidades no ambiente podem gerar complexidades maiores erroneamente

    `ordens_de_grandeza` e `base_de_grandeza` ditam o tamanho das entradas que
    a `função_analisada` vai receber, enquanto que `quantidade_de_execuções`,
    `ordens_de_grandeza` e `vezes_a_repetir` indicam quantas vezes a função
    será executada.

    Exemplo:
    Se a função for chamada com uma `função_analisada` que recebe uma lista de
    inteiros como parâmetro, uma `função_de_geração` que gera inteiros e recebe
    como parâmetro a quantidade de inteiros que irá gerar, `ordem_inicial` = 0
    `ordens_de_grandeza` = 5, `base_de_grandeza` = 2, `quantidade_de_execuções`
    = 100 e `vezes_a_repetir` = 3, a `função_de_geração` será chamada com os
    valores 2^0, 2^1, 2^2, 2^3 e 2^4 (a base 2, totalizando 5 ordens). Em cada
    uma dessas vezes, o resultado será passado para a `função_analisada`, que
    será chamada 300 vezes, sendo 3 vezes de 100, onde o tempo de execução dela
    por 100 vezes com a determinada entrada será mensurado, totalizando 3
    mensurações de tempo (ou seja, vai ser checado 3 vezes quanto tempo leva
    para executar a função 100 vezes com aquela entrada).

    Parameters
    ----------
    dados: DadosDeInferênciaDeComplexidade

    Returns
    -------
    tamanho_das_entradas, tempos_medidos: Tuple[Tamanhos, Tempos]
    """
    medians = []
    means = []
    standard_deviations = []
    input_sizes = [
        data.base_of_magnitude**order
        for order in range(
            data.initial_order, data.order_of_magnitude + data.initial_order
        )
    ]

    for input_size in input_sizes:
        inputs = data.generation_function(input_size)

        timer_result = repeat(
            lambda: data.analyzed_function(inputs),
            number=data.execution_quantity,
            repeat=data.times_to_repeat,
        )

        medians.append(median(timer_result))
        means.append(mean(timer_result))
        standard_deviations.append(stdev(timer_result))

    return MeasurementResults(
        registered_sizes=input_sizes,
        registered_times=medians,
        registered_means=means,
        registered_deviations=standard_deviations,
    )


def infer_complexity(
    input_sizes: Sizes, measured_times: Times
) -> big_o.complexities.ComplexityClass:
    """Infere a complexidade assintótica de tempo de uma função

    Parameters
    ----------
    dados: DadosDeInferênciaDeComplexidade

    Returns
    -------
    big_o.complexities.ComplexityClass
        Provável complexidade temporal da função, na forma de subclasse da
        ComplexityClass da biblioteca big_o
    """
    likely_complexity, _ = big_o.infer_big_o_class(
        # ! A big_o exige que `ns` seja um array numpy para as transformadas
        ns=np.array(input_sizes),
        time=measured_times,
    )

    if likely_complexity is None or not isinstance(
        likely_complexity, big_o.complexities.ComplexityClass
    ):
        raise ValueError(
            "Complexidade inferida não é subclasse das complexidades da lib"
            " big_o"
        )

    return likely_complexity


def register_data(
    data: ComplexityInferenceData,
    results: MeasurementResults,
    likely_complexity: big_o.complexities.ComplexityClass,
    id_: int = 1,
) -> str:
    result_data = {
        "funcao_analisada": data.analyzed_function.__name__,
        "funcao_de_geracao": data.generation_function.__name__,
        "ordens_de_grandeza": data.order_of_magnitude,
        "base_de_grandeza": data.base_of_magnitude,
        "quantidade_de_execucoes": data.execution_quantity,
        "vezes_a_repetir": data.times_to_repeat,
        "pontos_medidos": list(
            zip_longest(
                results.registered_sizes,
                results.registered_times,
                results.registered_means,
                results.registered_deviations,
            )
        ),
        "provavel_complexidade": f"{likely_complexity}",
    }

    complete_path = _generate_file_path(data.analyzed_function, id_)

    with open(f"{complete_path}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(result_data))

    return f"{id_}".zfill(3)


def plot_chart(
    data: ComplexityInferenceData,
    results: MeasurementResults,
    likely_complexity: Optional[big_o.complexities.ComplexityClass] = None,
    id_: int = 1,
):
    complete_path = _generate_file_path(data.analyzed_function, id_)
    plt.plot(results.registered_sizes, results.registered_times, "bo-")
    plt.plot(results.registered_sizes, results.registered_means, "ro:")
    # plt.plot(results.tamanhos, results.desvios, "ro.")
    plt.xlabel(
        f"Tamanho das entradas: de "
        f"{data.base_of_magnitude}^{data.initial_order} a "
        f"{data.base_of_magnitude}"
        f"^{data.initial_order + data.order_of_magnitude}"
    )
    plt.ylabel(
        f"Tempo medido: {data.times_to_repeat} vezes de "
        f"{data.execution_quantity} execuções"
    )
    plt.title(
        f"{data.analyzed_function.__name__}\n"
        f"{likely_complexity or 'Complexidade não medida'}"
    )
    plt.savefig(f"{complete_path}.png")
    plt.close()


def _generate_file_path(função_analisada: Callable, id_: int):
    path = "tests/results"
    # nome_do_arquivo = f"{int(time.time())}.{função_analisada.__name__}"
    file_name = f"{função_analisada.__name__} - "
    file_name += f"{id_}".zfill(3)
    return f"{path}/{file_name}"
