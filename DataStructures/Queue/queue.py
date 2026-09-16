from DataStructures.List import array_list as lt


def new_queue():
    """
    Crea una cola vacía.

    Returns:
        my_queue: una nueva cola vacía (reutiliza la estructura de lt.new_list()).
    """
    return lt.new_list()

def enqueue(my_queue, element):
    """
    Añade 'element' al final de la cola.

    Parameters:
        my_queue (queue): la cola a la que se añadirá el elemento.
        element (Any): el elemento a añadir.
    Returns:
        my_queue: la cola con el elemento añadido.
    """
    return lt.add_last(my_queue,element)

def dequeue(my_queue):
    """
    Elimina y retorna el primer elemento de la cola (el más antiguo).

    Returns:
        Any: el elemento que estaba de primero en la cola.
    """
    return lt.delete_first(my_queue)

def peek(my_queue):
    """
    Retorna (sin eliminar) el primer elemento de la cola.
    """
    return lt.first_element(my_queue)

def is_empty(my_queue):
    """
    Indica si la cola está vacía.
    """
    return False if lt.size(my_queue) > 0 else True

def size(my_queue):
    """
    Retorna la cantidad de elementos en la cola.
    """
    return lt.size(my_queue)