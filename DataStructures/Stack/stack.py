from DataStructures.List import single_linked_list as sll

def new_stack():
    """Crea una nueva pila vacía.
    """
    return sll.new_list()

def push(my_stack, element):
    """Añade el elemento element al tope de la pila my_stack.

    Args:
        my_stack (stack): La pila a la que se le añadirá el elemento.
        element (Any): El elemento que se añadirá a la pila.
        
    Returns:
        La pila con el elemento añadido. (stack)
    """
    return sll.add_first(my_stack,element)

def pop(my_stack):
    """Elimina y retorna el elemento en el tope de la pila my_stack no vacía.

    Si la pila está vacía, se lanza un error: EmptyStructureError: stack is empty.

    Args:
        my_stack (stack): La pila de la que se eliminará el elemento.
        
    Returns:
        Elemento retirado de la pila. (Any)
    """
    return sll.delete_first(my_stack)

def is_empty(my_stack):
    """Verifica si la pila my_stack está vacía.

    Args:
        my_stack (stack): La pila a verificar.
    
    Returns:
        True si la pila está vacía, de lo contrario False.
    """
    return False if sll.size(my_stack) > 0 else True

def top(my_stack):
    """Retorna sin eliminar el elemento en el tope de la pila my_stack.
    Si la pila está vacía, se lanza un error: EmptyStructureError: stack is empty.

    Args:
        my_stack (stack): La pila de la que se retornará el elemento.
    
    Returns:
        Elemento en el tope de la pila. (any)
    """
    if size(my_stack) > 0:
        return sll.first_element(my_stack) 
    else:
        raise Exception('EmptyStructureError: stack is empty')

def size(my_stack):
    """Retorna el número de elementos en la pila my_stack.

    Args:
        my_stack (stack): La pila de la que se retornará el tamaño.
    
    Returns:
        Número de elementos en la pila. (int)
    """
    return sll.size(my_stack)