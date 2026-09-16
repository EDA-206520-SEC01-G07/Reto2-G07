# Funciones de TAD Lista tipo Lista Simplemente Enlazada:
# - Creación, y manipulación.

from DataStructures.List.list_node import new_node


def new_list():
    """
    Crea una lista vacía basada en nodos encadenados.

    Returns:
        my_list: {'size': 0, 'first': None, 'last': None}
    """
    my_list = {
        "size":0,
        "first":None,
        "last":None
    }
    return my_list

def is_empty(my_list):
    """
    Indica si la lista no tiene elementos.
    """
    return my_list["size"] == 0

def size(my_list):
    """
    Retorna la cantidad de elementos de la lista.
    """
    return my_list["size"]

def add_first(my_list, element):
    """
    Agrega 'element' al inicio de la lista (nuevo primer nodo).
    """
    new_element = new_node(element)
    if not is_empty(my_list):
        actual = my_list["first"]
        my_list["first"] = new_element
        my_list["first"]["next"] = actual
    else:
        my_list["first"] = new_element
        my_list["last"] = new_element
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    """
    Agrega 'element' al final de la lista (nuevo último nodo).
    """
    new_element = new_node(element)
    if not is_empty(my_list):
        my_list["last"]["next"] = new_element
        my_list["last"] = new_element
    else:
        my_list["first"] = new_element
        my_list["last"] = new_element
    my_list["size"] += 1
    return my_list

def add_element(my_list, element, pos):
    """
    Inserta 'element' en la posición 'pos' (0-indexada), recorriendo la
    lista nodo a nodo hasta llegar a esa posición.
    """
    element_node = new_node(element)
    if pos > size(my_list):
        return IndexError("Position out of range.")
    elif pos == 0:
        return add_first(my_list,element)
    elif pos == size(my_list):
        my_list["last"]["next"] = element_node
        my_list["last"] = element_node
        return my_list
    else:
        actual_node = my_list["first"]
        change_next = None
        for i in range(0,my_list["size"]):
            if i == pos - 1:
                change_next = actual_node
            elif i == pos:
                element_node["next"] = actual_node
                change_next["next"] = element_node
            actual_node = actual_node["next"]
    my_list["size"] += 1
    return my_list

def first_element(my_list):
    """
    Retorna (sin eliminar) el primer elemento de la lista.
    """
    return my_list["first"]["info"]

def last_element(my_list):
    """
    Retorna (sin eliminar) el último elemento de la lista.
    """
    return my_list["last"]["info"]

def get_element(my_list, pos):
    """
    Retorna el elemento ubicado en la posición 'pos'.
    """
    if pos >= size(my_list):
        raise IndexError("Position out of range.")
    node = my_list["first"]
    i = 0
    found = False
    respuesta = None
    while i in range(0,size(my_list)) and not found:
        if i == pos:
            respuesta = node["info"]
            found = True
        node = node["next"]
        i += 1
    return respuesta

def delete_first(my_list):
    """
    Elimina y retorna el primer elemento de la lista.
    """
    if my_list["size"] == 0:
        raise IndexError("Position out of range.")
    elif my_list["size"] == 1:
        elemento = my_list["first"]
        my_list["first"] = None
        my_list["last"] = None
    else:
        elemento = my_list["first"]
        my_list["first"] = my_list["first"]["next"]
    my_list["size"] -= 1
    return elemento.pop("info")

def delete_last(my_list):
    """
    Elimina y retorna el último elemento de la lista.
    """
    if size(my_list) == 0:
        raise IndexError("Position out of range.")
    elif size(my_list) == 1:
        elemento = my_list["first"]
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"] -= 1
        return elemento.pop("info")
    else:
        element = None
        node = my_list["first"]
        previous = None
        for i in range(0,size(my_list)):
            if i == size(my_list) - 2:
                previous = node
            elif i == size(my_list) - 1:
                element = node
                my_list["last"] = previous
                previous["next"] = None
            node = node["next"]
        my_list["size"] -= 1
    return element.pop("info")

def delete_element(my_list, pos):
    """
    Elimina y retorna el elemento ubicado en la posición 'pos'.
    """
    if size(my_list) == 0:
        raise IndexError("Position out of range.")
    elif pos >= size(my_list):
        raise IndexError("Position out of range.")
    elif size(my_list) == 1:
        elemento = my_list["first"]
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"] -= 1
        return elemento.pop("info")
    elif pos == 0:
        return delete_first(my_list)
    del_element = None
    node = my_list["first"]
    i = 0
    found = False
    previous = None
    while i in range(0,size(my_list)) and not found:
        if i == pos - 1:
            previous = node
        elif i == pos:
            del_element = node
            previous["next"] = node["next"]
            found = True
        i += 1
        node = node["next"]
    my_list["size"] -= 1
    return del_element.pop("info")

def is_present(my_list, element, cmp_function):
    """
    Busca 'element' recorriendo la lista y usando 'cmp_function' para
    comparar. Retorna la posición (0-indexada) o -1 si no está presente.
    """
    resultado = -1
    node = my_list["first"]
    for i in range(0,size(my_list)):
        if cmp_function(element,node["info"]) == 0:
            resultado = i
            return resultado
        node = node["next"]
    return resultado

def change_info(my_list, pos, new_info):
    """
    Cambia la información del nodo ubicado en la posición 'pos'.
    """
    if size(my_list) == 0:
        raise IndexError("Position out of range.")
    elif pos >= size(my_list):
        raise IndexError("Position out of range.")
    i = 0
    found = False
    node = my_list["first"]
    while i in range(0,size(my_list)) and not found:
        if i == pos:
            node["info"] = new_info
            found = True
        node = node["next"]
        i += 1
    return my_list

def exchange(my_list, pos1, pos2):
    """
    Intercambia la información de los nodos en las posiciones 'pos1' y
    'pos2'.
    """
    if size(my_list) == 0:
        raise IndexError("Position out of range.")
    elif size(my_list) == 1:
        raise IndexError("Position out of range.")
    node = my_list["first"]
    for i in range(0,size(my_list)):
        if i == pos1:
            change1 = node
        if i == pos2:
            change2 = node
        node = node["next"]
    temp = change1["info"]
    change_info(my_list,pos1,change2["info"])
    change_info(my_list,pos2,temp)
    return my_list

def sub_list(my_list, pos, num_elements):
    """
    Retorna una nueva lista encadenada con 'num_elements' elementos de
    'my_list', comenzando en la posición 'pos'.
    """
    new = new_list()
    node = my_list["first"]
    for i in range(0,size(my_list)):
        if i >= pos and i < pos + num_elements:
            element = node["info"]
            add_last(new,element)
        node = node["next"]
    return new

# Funciones de Ordenamiento:

def default_sort_criteria(element_1, element_2):
    """
    Parameters:
        element_1 (any) - Primer elemento a comparar.
        element_2 (any) - Segundo elemento a comparar.
    Returns:
        True si el primer elemento es menor que el segundo, False en caso contrario.
    Return type:
        bool
    """
    is_sorted = False
    if element_1 < element_2:
        is_sorted = True
    return is_sorted
 
def shell_sort(my_list, sort_crit=default_sort_criteria):
    """
    Parameters:
            my_list (list) - Lista sobre la que se va a ordenar.

            sort_crit (function) - Función de comparación de dos elementos.
    Returns:
        my_list ordenada.
    Return type:
        list
    """
    n = size(my_list)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = get_element(my_list, i)
            j = i
            while j >= gap and sort_crit(temp, get_element(my_list, j - gap)):
                change_info(my_list, j, get_element(my_list, j - gap))
                j -= gap
            change_info(my_list, j, temp)
        gap //= 2
    return my_list
 
def insertion_sort(my_list, sort_crit=default_sort_criteria):
    """Ordena una lista utilizando el algoritmo de ordenamiento Insertion Sort.
    
        Args:
            my_list (array_list ): Lista a ordenar.
            sort_crit (function): Función de comparación.
            
        Return type:
            Lista orenada.
        """
    for i in range(0,size(my_list)):
            ordenado = False
            if i != 0:
                j = i - 1
                element1 = get_element(my_list, j + 1)
                element2 = get_element(my_list,j)
                while j >= 0 and not ordenado:
                    if sort_crit(element2, element1) is False:
                        exchange(my_list, j, j + 1)
                        j -= 1
                        if j >= 0:
                            element1 = get_element(my_list, j + 1)
                            element2 = get_element(my_list, j)
                    else:
                        ordenado = True
    return my_list

def selection_sort(my_list, sort_crit=default_sort_criteria):
    """
    Ordena los elementos de my_list utilizando el algoritmo Selection Sort.

    Parameters:
        my_list (list) - Lista sobre la que se va a ordenar.
        sort_crit (function) - Función de comparación de dos elementos.
    Returns:
        my_list ordenada.
    Return type:
        list
    """
    n = size(my_list)
    for i in range(0, n - 1):
        min_index = i
        elem_min = get_element(my_list, min_index)
        for j in range(i + 1, n):
            elem_j = get_element(my_list, j)
            if sort_crit(elem_j, elem_min):
                min_index = j
                elem_min = elem_j
        if min_index != i:
            exchange(my_list, i, min_index)
    return my_list

# Funciones de Ordenamiento Recursivas (Single Linked List):
def merge_sort(my_list, sort_crit = default_sort_criteria):
    if size(my_list) == 1 or size(my_list) == 0:
        return my_list
    # División entera entre 2 listas.
    mid = size(my_list) // 2
    first_half = sub_list(my_list,0,mid)
    second_half = sub_list(my_list,mid, size(my_list) - mid)
    
    ord_first_half = merge_sort(first_half, sort_crit)
    ord_second_half = merge_sort(second_half, sort_crit)
    return merge(ord_first_half, ord_second_half,sort_crit)

def merge(ord_first_half, ord_second_half, sort_crit = default_sort_criteria):
    result = new_list()
    i = 0
    j = 0
    while i < size(ord_first_half) and j < size(ord_second_half):
        if sort_crit(get_element(ord_first_half,i), get_element(ord_second_half,j)):
            add_last(result,get_element(ord_first_half,i))
            i += 1
        elif sort_crit(get_element(ord_second_half,j),get_element(ord_first_half,i)):
            add_last(result,get_element(ord_second_half,j))
            j += 1
        else:
            add_last(result,get_element(ord_first_half,i))
            add_last(result,get_element(ord_second_half,j))
            i += 1
            j += 1
            
    while i < size(ord_first_half):
        add_last(result,get_element(ord_first_half,i))
        i += 1
    while j < size(ord_second_half):
            add_last(result,get_element(ord_second_half,j))
            j += 1
    return result

# Quick Sort Single Linked List.

def quick_sort(my_list, sort_crit = default_sort_criteria):
    """Ordena una lista utilizando el algoritmo recursivo de ordenamiento Quick Sort.

    Se selecciona un elemento como pivote y se colocan los elementos menores a la izquierda y los mayores a la derecha de este elemento pivote.

    Si la lista es vacía o tiene un solo elemento, se retorna la lista original.
    """
    # Lista tiene 1 elemento.
    if size(my_list) <= 1:
        return my_list
    # Tiene más elementos.
    pivot = get_element(my_list,size(my_list) - 1)
    i = -1
    j = 0
    while j < size(my_list) - 1:
        # Elemento      
        if sort_crit(get_element(my_list,j), pivot):
            i += 1
            exchange(my_list,j,i)
            j += 1
        else:
            j += 1
    delete_last(my_list)
    add_element(my_list,pivot,i + 1)
    first_half = sub_list(my_list, 0, i + 1)
    second_half = sub_list(my_list,i + 2, (size(my_list) - 1) - (i + 1))
    
    ord_first_half = quick_sort(first_half,sort_crit)
    ord_second_half = quick_sort(second_half,sort_crit)
    
    result = new_list()
    k = 0
    while k < size(ord_first_half):
        add_last(result, get_element(ord_first_half, k))
        k += 1
    add_last(result, pivot)
    k = 0
    while k < size(ord_second_half):
        add_last(result, get_element(ord_second_half, k))
        k += 1
    return result