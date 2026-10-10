    # Implementación TAD Mapa.

def new_map_entry(key, value):
    """Crea una nueva entrada (de tipo map_entry) de una tabla con una llave y un valor dados.

    Args:
        key (Any): Llave de la entrada.
        value (Any): Valor de la entrada.
    
    Returns:
        Entrada de una tabla.
    """
    return {'key': key, 'value': value}

def set_key(my_entry, key):
    """Establece un valor nuevo a la key de una entrada recibida.

    Args:
        my_entry (map_entry): Entrada a modificar.
        key (Any): Llave nueva de la entrada.
        
    Returns:
        Entrada con la llave modificada.
    """
    my_entry['key'] = key
    return my_entry

def set_value(my_entry, value):
    """Establece un valor nuevo al value de una entrada recibida.

    Args:
        my_entry (map_entry): Entrada a modificar.
        value (Any): Valor nuevo de la entrada.
        
    Returns:
        Entrada con el valor modificado.
    """
    my_entry['value'] = value
    return my_entry

def get_key(my_entry):
    """Obtiene la llave key de una entrada recibida.

    Args:
        my_entry (map_entry): Entrada de la cual se desea obtener la llave.
        
    Returns:
        Llave de la entrada.
    """
    return my_entry['key']

def get_value(my_entry):
    """Obtiene el valor value de una entrada recibida.

    Args:
        my_entry (map_entry): Entrada de la cual se desea obtener el valor.
        
    Returns:
        Valor de la entrada.
    """
    return my_entry['value']