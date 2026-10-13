from DataStructures.Map import map_functions as mf
from DataStructures.List import array_list as al
from DataStructures.Map import map_entry as me
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
        prime (int, optional):Número primo utilizado para el cálculo del hash. Defaults to 109345121.
    
    Return:
        Tabla recien creada.
    """
    table = al.new_list()
    capacity = mf.next_prime(num_elements/load_factor)
    i = 0
    while i < capacity:
        al.add_last(table, me.new_map_entry(None, None))
        i += 1
    # Estructura map_linear_probing
    my_map = {
        'prime': prime,
        'capacity': capacity,
        'scale': 1, # random.randint
        'shift': 0, # random.randint
        'table': table,
        'current_factor': 0,
        'limit_factor': load_factor,
        'size': 0
    }
    return my_map

def put(my_map, key, value):
    """Agrega una nueva entrada llave-valor a la tabla de hash. Si la llave ya existe en la tabla, se actualiza el value de la entrada.
    Para agregar un nuevo elemento a la tabla, se realiza el siguiente procedimiento:
    Se calcula el hash de la llave, usando la función hash_value.
    Se busca la posición en la tabla con la función find_slot. Si la posición está ocupada, se busca la siguiente posición disponible.
    Se inserta la entrada en la tabla.
    Se actualiza el current_factor de la tabla si se agrega un nuevo elemento.
    Si el current_factor supera el limit_factor, se realiza un rehash de la tabla.
    Se retorna la tabla con el nuevo elemento agregado.

    Args:
        my_map (map_linear_probing): Tabla de simbolos a la cual se desea agregar el elemento.
        key (Any): Llave del elemento a agregar.
        value (Any): Valor del elemento a agregar.
    
    Returns:
        Tabla de simbolos con el nuevo elemento agregado.
    """
    # Se calcula el hash de la llave:
    hash_value = mf.hash_value(my_map,key)
    # Se busca la pocisión en la tabla:
    ocupied, index_avail = find_slot(my_map, key, hash_value)
    # Se inserta la entrada en la tabla:
    array_list = my_map['table']
    entry = al.get_element(array_list, index_avail)
    me.set_value(entry, value)
    me.set_key(entry, key)
    if not ocupied:
        my_map['size'] += 1
    # Se actualiza el current_factor:
    current_factor = my_map['size'] / my_map['capacity']
    my_map['current_factor'] = current_factor
    result = my_map
    # En caso de que la capacity suepere el limit_factor:
    if my_map['current_factor'] > my_map['limit_factor']:
        result = rehash(my_map)
    return result
    
def find_slot(my_map, key, hash_value):
    """Busca la posición en la tabla donde se debe insertar/encontrar una entrada con una llave dada.
    Utiliza el valor hash_value que tiene la posición inicial donde debería encontrase la key dada (parámetro).
    Si en esa posición está la key, se informa la posición donde se encontró. Si en esa posición no está la key y 
    esa posición no ha sido ocupada por otra pareja key-value, esa posición puede ser ocupada por la key dada. 
    Si en esa posición no está la key porque otra pareja key-value la ocupó, se debe buscar en la siguiente posición en la tabla.
    Utiliza las funciónes de validación is_available y comparación default_compare.

    Args:
        my_map (map_linear_probing): Tabla de simbolos en la que se desea buscar la posición.
        key (Any): Llave de la entrada que se desea buscar.
        hash_value (int): Valor del hash de la llave.

    Returns:
        bool, int: Retorna una tupla con dos valores. El primer valor es True si la key se encontró. De lo contrario es False. 
        Si el primer valor es True, el segundo valor es la posición en la tabla de hash donde la key se encontró. 
        Si el primer valor es False, el segundo valor es la posición en la tabla de hash que está disponible para agregar la key.
    """
    first_avail = None
    found = False
    ocupied = False
    while not found:
        if is_available(my_map["table"], hash_value):
                if first_avail is None:
                    first_avail = hash_value
                entry = al.get_element(my_map["table"], hash_value)
                if me.get_key(entry) is None:
                    found = True
        elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
                first_avail = hash_value
                found = True
                ocupied = True
        hash_value = (hash_value + 1) % my_map["capacity"]
    return ocupied, first_avail

def is_available(table, pos):
    
    entry = al.get_element(table, pos)
    if me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__":
        return True
    return False

def default_compare(key, entry):

    if key == me.get_key(entry):
        return 0
    elif key > me.get_key(entry):
        return 1
    return -1

def contains(my_map, key):
    """Valida si una llave dada se encuentra en la tabla de simbolos.

    Args:
        my_map (map_linear_probing): Tabla de simbolos en la que se desea buscar la llave.
        key (Any): Llave que se desea buscar en la tabla.
        
    Returns:
        bool: True si la llave se encuentra en la tabla, False en caso contrario.
    """
    hash_value = mf.hash_value(my_map, key)
    result, index = find_slot(my_map, key, hash_value)
    return result

def remove(my_map, key):
    """Elimina una entrada llave-valor de la tabla de símbolos asociada a una llave dada. 
    La entrada eliminada debe reemplazarse por la entrada llave-valor "__EMPTY__", "__EMPTY__"

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea eliminar la entrada.
        key (Any): Llave de la entrada que se desea eliminar.
        
    Returns:
        Tabla de simbolos sin la entrada asociada a la llave dada.
    """
    hash_value = mf.hash_value(my_map, key)
    ocupied, index = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = al.get_element(my_map['table'], index)
        me.set_value(entry,"__EMPTY__")
        me.set_key(entry, "__EMPTY__")
        my_map['size'] -= 1
        current_factor = my_map['size'] / my_map['capacity']
        my_map['current_factor'] = current_factor
    return my_map

def get(my_map, key):
    """Obtiene el valor asociado a una llave dada en la tabla de simbolos.

    Args:
        my_map (map_liear_probing): Tabla de simbolos en la que se desea buscar el valor.
        key (Any): Llave de la cual se desea obtener el valor.
        
    Returns:
        Valor asociado a la llave dada. Si la llave no se encuentra en la tabla, se retorna None.
    """
    hash_value = mf.hash_value(my_map, key)
    ocupied, index = find_slot(my_map, key, hash_value)
    if not ocupied:
        return None
    entry = al.get_element(my_map['table'], index)
    return me.get_value(entry)

def size(my_map):
    return my_map['size']

def is_empty(my_map):
    """Valida si la tabla de simbolos está vacía.

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea verificar si está vacía.
    
    Returns:
        True si la tabla está vacía, False en caso contrario.
    """
    if my_map['size'] == 0:
        return True
    else:
        return False
    
def key_set(my_map):
    """Obtiene la lista de llaves de la tabla de simbolos.

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea obtener el conjunto de llaves.
        
    Returns:
        Lista de llaves de la tabla de simbolos. (array_list)
    """
    result = al.new_list()
    for i in range(0, my_map['capacity']):
        entry = al.get_element(my_map['table'], i)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            al.add_last(result, me.get_key(entry))
    return result

def value_set(my_map):
    """Obtiene la lista de valores de la tabla de simbolos.

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea obtener el conjunto de valores.
        
    Returns:
        Lista de valores de la tabla de simbolos. (array_list)
    """
    result = al.new_list()
    for i in range(0, my_map['capacity']):
        entry = al.get_element(my_map['table'], i)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            al.add_last(result, me.get_value(entry))
    return result
    

def rehash(my_map):
    """Realiza un rehash de la tabla de simbolos.

    Args:
        my_map (map_linear_probing): Tabla de simbolos de la cual se desea realizar el rehash.
        
    Returns:
        Tabla de simbolos con el rehash realizado.
    """
    rehashed_map = new_map(2 * my_map['capacity'] * my_map['limit_factor'], my_map['limit_factor'], my_map['prime'])
    element = my_map['table']
    for i in range(0, my_map['capacity']):
        entry = al.get_element(element, i)
        if me.get_key(entry) is not None and me.get_key(entry) != "__EMPTY__":
            put(rehashed_map, me.get_key(al.get_element(element, i)), me.get_value(al.get_element(element, i)))
    return rehashed_map