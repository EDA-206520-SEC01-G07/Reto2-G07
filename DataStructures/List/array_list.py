# Funciones de TAD Lista tipo Array:
# - Creación, y manipulación.

def new_list():
    """
    Crea una lista vacía basada en arreglo.

    Returns:
        my_list: una nueva lista vacía.
        Ejemplo esperado: new_list() -> {'elements': [], 'size': 0}
    """
    my_list = {
        'elements': [],
        'size': 0
    }
    return my_list


def is_empty(my_list):
    """
    Indica si la lista no tiene elementos.

    Parameters:
        my_list (list): la lista a examinar.
    Returns:
        bool: True si la lista está vacía, False en caso contrario.
    """
    return True if my_list["size"] == 0 else False


def size(my_list):
    """
    Retorna la cantidad de elementos almacenados en la lista.
    """
    return my_list["size"]


def add_first(my_list, element):
    """
    Agrega 'element' al inicio de la lista.

    Parameters:
        my_list (list): la lista sobre la que se agrega.
        element (Any): el elemento a agregar.
    Returns:
        my_list: la lista actualizada.
    """
    actual = None
    new = None
    if size(my_list) == 0:
        my_list["elements"].append(element)
    else:
        for i in range(0,size(my_list)):
            if i > 0:
                actual = my_list["elements"][i]
                my_list["elements"][i] = new
                new = actual
            elif i == 0:
                new = my_list["elements"][i]
                my_list["elements"][0] = element
        my_list["elements"].append(new)
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    """
    Agrega 'element' al final de la lista.
    """
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list


def add_element(my_list, element, pos):
    """
    Inserta 'element' en la posición 'pos', desplazando los
    elementos que estén desde esa posición en adelante.
    """
    actual = None
    new = None
    if size(my_list) == 0:
        my_list["elements"].append(element)
    elif pos == size(my_list):
        my_list["elements"].append(element)
    else:
        for i in range(0,size(my_list)):
            if i == pos:
                new = my_list["elements"][i]
                my_list["elements"][i] = element
            elif i > pos:
                actual = my_list["elements"][i]
                my_list["elements"][i] = new
                new = actual
        my_list["elements"].append(new)
    my_list["size"] += 1
    return my_list


def first_element(my_list):
    """
    Retorna (sin eliminar) el primer elemento de la lista.
    """
    return my_list["elements"][0]


def last_element(my_list):
    """
    Retorna (sin eliminar) el último elemento de la lista.
    """
    return my_list["elements"][-1]


def get_element(my_list, pos):
    """
    Retorna el elemento que está en la posición 'pos' (0-indexada).
    """
    return my_list["elements"][pos]


def delete_first(my_list):
    """
    Elimina y retorna el primer elemento de la lista.
    """
    primer_elemento = my_list["elements"].pop(0)
    my_list["size"] -= 1
    return primer_elemento


def delete_last(my_list):
    """
    Elimina y retorna el último elemento de la lista.
    """
    ult_elemento = my_list["elements"].pop()
    my_list["size"] -= 1
    return ult_elemento


def delete_element(my_list, pos):
    """
    Elimina y retorna el elemento ubicado en la posición 'pos'.
    """
    element = my_list["elements"].pop(pos)
    my_list["size"] -= 1
    return my_list


def is_present(my_list, element, cmp_function):
    """
    Busca 'element' dentro de la lista usando 'cmp_function' para comparar.

    Parameters:
        cmp_function (function): función que recibe (element, elemento_de_la_lista)
            y retorna 0 si son iguales (misma convención que 'cmp' clásico).
    Returns:
        int: la posición (0-indexada) donde se encontró el elemento, o -1
             si no está presente.
    """
    resultado = -1
    for i in range(0,size(my_list)):
        valor = cmp_function(element,my_list["elements"][i])
        if valor == 0:
            resultado = i
            return resultado
    return resultado


def change_info(my_list, pos, new_info):
    """
    Cambia la información almacenada en la posición 'pos' por 'new_info'.
    """
    my_list["elements"][pos] = new_info
    return my_list


def exchange(my_list, pos1, pos2):
    """
    Intercambia los elementos ubicados en las posiciones 'pos1' y 'pos2'.
    """
    info2 = my_list["elements"][pos2]
    info1 = my_list["elements"][pos1]
    change_info(my_list,pos1,info2)
    change_info(my_list,pos2,info1)
    return my_list


def sub_list(my_list, pos, num_elements):
    """
    Retorna una nueva lista con 'num_elements' elementos de 'my_list',
    comenzando en la posición 'pos'.
    """
    result_list = new_list()
    for i in range(pos, pos + num_elements):
        result_list["elements"].append(my_list["elements"][i])
        result_list["size"] += 1
    return result_list

# Funciones de Ordenamiento Iterativas:

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

def shell_sort(my_list, sort_crit = default_sort_criteria):
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

def insertion_sort(my_list, sort_crit = default_sort_criteria):
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
                        element2 = get_element(my_list, j)
                        element1 = get_element(my_list, j + 1)
                else:
                    ordenado = True
    return my_list

def selection_sort(my_list, sort_crit = default_sort_criteria):
    """
    Ordena los elementos de my_list usando el algoritmo Selection Sort.

    Parameters:
        my_list (list): la lista a ordenar.
        sort_crit (function): función de comparación; retorna True si el
            primer elemento debe ir antes que el segundo.
    Returns:
        my_list: la lista ordenada.
    """
    n = size(my_list)
    for i in range(0, n - 1):
        min_index = i
        for j in range(i + 1, n):
            elem_j = get_element(my_list, j)
            elem_min = get_element(my_list, min_index)
            if sort_crit(elem_j, elem_min):
                min_index = j
        if min_index != i:
            exchange(my_list, i, min_index)
    return my_list

# Funciones de Ordenamiento Recursivas (Array List):
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

# Quick Sort Array.

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