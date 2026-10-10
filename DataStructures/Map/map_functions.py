    # Implementación TAD mapa.

import math as m
  
def is_prime(n):
    """Verifica si el número n dado es primo.

    Args:
        n (int): Número a verificar si es primo.

    Returns:
        bool: Verdadero si el número es primo, falso en caso contrario.
    """
    prime = True
    divisor = 2
    if n < 0:
        prime = False
        return prime
    sqrt = int(m.sqrt(n))
    if n == 0 or n == 1:
        prime = False
    while prime and divisor <= sqrt:
        calc = n % divisor
        if calc == 0:
            prime = False
        if divisor == 2:
            divisor += 1
        else:
            divisor += 2
    return prime

def next_prime(n):
    """Obtiene el siguiente número primo después del número n dado.

    Args:
        n (int): Número a partir del cual se desea obtener el siguiente número primo.

    Returns:
        int: Siguiente número primo después de n.
    """
    n = int(n)
    found = False
    num = n + 1
    while not found:
        if is_prime(num):
            found = True
        else:
            num += 1
    return num

def hash_value(my_table, key):
    """Calcula el hash para una llave dada, utitiizando el método:
    MAD: (abs(a * hash_key + b) % p) % m, donde:
    hash_key es el valor de la función nativa de Python hash() para la llave key.
    m es el tamaño de la tabla.
    p es un número primo mayor a m.
    a es entero aleatorio entre 1 y p-1.
    b es entero aleatorio entre 0 y p-1.

    Args:
        my_table (map_linear_probing / map_separate_chaining): Tabla en la que se desea calcular el hash.
        key (Any): Llave para la cual se desea calcular el hash.
        
    Returns:
    Valor del hash para la llave dada. (Que es un índice de la tabla).
    """
    m = my_table['capacity']
    p = my_table['prime']
    a = my_table['scale']
    b = my_table['shift']
    mad = (abs(a * hash(key) + b) % p) % m
    return mad