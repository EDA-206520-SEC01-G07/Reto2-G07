from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
from DataStructures.List import single_linked_list as sll
import random

    # Implementación Map Linear Probing.

def new_map(num_elements, load_factor, prime = 109345121):
    """Crea una nueva tabla de hash (map) donde sus entradas llave-valor se inicializan con valores None-None.
    La tabla de simbolos es creada con los siguientes atributos:
    prime: Número primo usado para calcular el hash. Inicializado con el valor de prime y en caso de no ser dado, con el valor por defecto de 109345121.
    capacity: Tamaño de la tabla. Inicializado con el siguiente primo mayor a num_elements/ load_factor.
    scale: Número entero aleatorio entre 1 y prime- 1.
    shift: Número entero aleatorio entre 0 y prime- 1.
    table: Lista de tamaño capacity con las entradas de la tabla de tipo array_list. Inicializado con una lista donde cada elemento es una map_entry con llave y valor None.
    current_factor: Factor de carga actual de la tabla. Inicializado en 0.
    limit_factor: Factor de carga límite de la tabla antes de hacer un rehash. Inicializado con el valor de load_factor.
    size: Número de elementos en la tabla. Inicializado en 0.

    Args:
        num_elements (int): Número de elementos que se desean almacenar en la tabla.
        load_factor (float): Factor de carga límite de la tabla antes de hacer un rehash.
        prime (int, optional): Número primo utilizado para el cálculo del hash. Por defecto es 109345121.. Defaults to 109345121.
        
    Returns:
        Tabla recien creada.
    """
    capacity = mf.next_prime(num_elements / load_factor)
    table = al.new_list()
    i = 0
    while i < capacity:
        al.add_last(table, sll.new_list())
        i += 1
    my_map = {
        'prime': prime,
        'capacity': capacity,
        'scale': 1, # random.randint
        'shift': 0, # random.randint
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0,        
    }
    return my_map

def put(my_map, key, value):
    """Agrega una nueva entrada llave-valor a la tabla. Si la llave ya existe en la tabla, se actualiza el value de la entrada.
    Para agregar una nueva entrada se debe seguir los siguientes pasos:
    Calcular el hash de la llave, usando la función hash_value.
    Se busca la lista en la posición del hash en la tabla.
    Si la llave ya existe en la lista, se actualiza el valor de la entrada.
    Si la llave no existe en la lista, se agrega una nueva entrada al final de la lista.
    Se actualiza el current_factor de la tabla si se agrega una nueva entrada.
    Si el current_factor supera el limit_factor, se realiza un rehash de la tabla.
    Se retorna la tabla con la nueva entrada.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos a la cual se desea agregar un nuevo elemento.
        key (Any): Llave del nuevo elemento.
        value (Any): Valor del nuevo elemento.
    """
    # Calcular el hash de la llave:
    hash_value = mf.hash_value(my_map, key)
    # Buscar la pocisión del hash en la tabla:
    entry = my_map['table']
    if me.get_key(al.get_element(entry, hash_value)) is not None:
        sll.change_info(al.get_element(entry, hash_value), 0, me.new_map_entry(key, value))
    else:
        sll.add_last(al.get_element(entry, hash_value), me.new_map_entry(key, value))
    current_factor = my_map['size'] / my_map["capacity"]
    my_map['current_factor'] = current_factor
    result = my_map
    if my_map['current_factor'] > my_map['limit_factor']:
        result = rehash(my_map)
    return result
    

def default_compare(key, element):

    if (key == me.get_key(element)):
        return 0
    elif (key > me.get_key(element)):
        return 1
    return -1

def contains(my_map, key):
    """Verifica si una llave se encuentra en la tabla de simbolos.

    Args:
        my_map (map_separate chaining): Tabla de simbolos en la cual se desea verificar si la llave se encuentra.
        key (Any): Llave que se desea verificar si se encuentra en la tabla.

    Returns:
        bool: True si la llave se encuentra en la tabla, False en caso contrario.
    """
    table = my_map['table']
    found = False
    hash_value = mf.hash_value(my_map, key)
    single_ll = al.get_element(table, hash_value)
    node = single_ll['first']
    while node is not None and not found:
        if me.get_key(node['info']) == key:
            found = True
            return found
        node = node['next']
    return found

def remove(my_map, key):
    """Elimina una entrada de la tabla de simbolos asociada a una llave dada.

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea eliminar una entrada.
        key (Any): Llave de la entrada que se desea eliminar.
        
    Returns:
        (map_separate_cahining): Tabla de simbolos con la entrada eliminada.
    """
    table = my_map['table']
    hash_value = mf.hash_value(my_map, key)
    single_ll = al.get_element(table, hash_value)
    node = single_ll['first']
    i = 0
    found = False
    while not found and node is not None:
        if me.get_key(node['info']) == key:
            sll.delete_element(single_ll, i)
            my_map['size'] -= 1
            current_factor = my_map['size'] / my_map['capacity']
            my_map['current_factor'] = current_factor
            found = True
        node = node['next']
        i += 1
    return my_map

def get(my_map, key):
    """Obtiene el valor asociado a una llave en la tabla de simbolos.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos de la cual se desea obtener el valor asociado a una llave.
        key (Any): Llave de la cual se desea obtener el valor asociado.
        
    Returns:
        Valor asociado a la llave en la tabla de simbolos.
    """
    table = my_map['table']
    hash_value = mf.hash_value(my_map, key)
    single_ll = al.get_element(table, hash_value)
    node = single_ll['first']
    found = False
    value = None
    while not found and node is not None:
        if me.get_key(node['info']) == key:
            found = True
            value = me.get_value(node['info'])
        node = node['next']
    return value

def size(my_map):
    """Obtiene la cantidad de elementos en la tabla de simbolos.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos de la cual se desea obtener la cantidad de elementos.
        
    Returns:
        (int): Cantidad de elementos en la tabla de simbolos.
    """
    return my_map['size']

def is_empty(my_map):
    """Verifica si la tabla de simbolos se encuentra vacia.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos de la cual se desea verificar si se encuentra vacia.
        
    Returns:
        (bool): True si la tabla se encuentra vacia, False en caso contrario.
    """
    empty = True
    if size(my_map) > 0:
        empty = False
    return empty

def key_set(my_map):
    """Obtiene la lista de llaves de la tabla de simbolos.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos de la cual se desea obtener el conjunto de llaves.
        
    Returns:
        (array_list): Lista de llaves de la tabla de simbolos.
    """
    result = al.new_list()
    table = my_map['table']
    for i in range(0, my_map['capacity']):
        single_ll = al.get_element(table, i)
        node = single_ll['first']
        while node is not None:
            key = me.get_key(node['info'])
            al.add_last(result, key)
            node = node['next']
    return result

def value_set(my_map):
    """Obtiene la lista de valores de la tabla de simbolos.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos de la cual se desea obtener el conjunto de valores.
        
    Returns:
        (array_list): Lista de valores de la tabla de simbolos.
    """
    result = al.new_list()
    table = my_map['table']
    for i in range(0, my_map['capacity']):
        single_ll = al.get_element(table, i)
        node = single_ll['first']
        while node is not None:
            value = me.get_value(node['info'])
            al.add_last(result, value)
            node = node['next']
    return result

def rehash(my_map):
    """Realiza un rehashing de la tabla de simbolos.
    Para realizar un rehash se debe seguir los siguientes pasos:
    Crear una nueva tabla map_separate_chaining con capacity que sea el siguiente primo al doble del capacity actual.
    Recorrer la tabla actual y reinsertar cada elemento en la nueva tabla.
    Asignar la nueva tabla como la tabla actual.
    Retornar la tabla nueva.

    Args:
        my_map (map_separate_chaining): Tabla de simbolos a la cual se le desea realizar un rehashing.
        
    Returns:
        Tabla de simbolos con un nuevo tamaño.
    """
    rehashed_map = new_map(2 * my_map['capacity'] * my_map['limit_factor'], my_map['limit_factor'], my_map['prime'])
    table = my_map['table']
    for i in range(0, my_map['capacity']):
        single_ll = al.get_element(table, i)
        node = single_ll['first']
        while node is not None:
            entry = node['info']
            rehashed_map = put(rehashed_map, me.get_key(entry), me.get_value(entry))
            node = node['next']
    return rehashed_map