import time
import csv
csv.field_size_limit(2147483647)
from DataStructures.List import array_list as al

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "pedidos": al.new_list()
    }
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    with open(filename, encoding = "utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter = ",")
        for row in reader:
            pedido = {
                "order_id": row["Order_ID"],
                "product": row["Product"],
                "country": row["Country"],
                "channel": row["Channel"],
                "order_date": row["Order_Date"],
                "discount_pct": float(row["Discount_Pct"]),
                "price_per_box": float(row["Price_per_Box"]),
                "marketing_spend": float(row["Marketing_Spend"]),
                "boxes_shipped": int(row["Boxes_Shipped"]),
                "amount": float(row["Amount"])
            }
            al.add_last(catalog["pedidos"], pedido)
    return catalog


# Funciones de consulta sobre el catálogo

def total_pedidos(catalog):
    """
    Da el total de pedidos cargados.
    """
    return al.size(catalog["pedidos"])

def total_pedidos_por_canal(catalog):
    """
    Retorna un diccionario {canal: cantidad_de_pedidos}.
    """
    pedidos = catalog["pedidos"]
    if al.size(pedidos) == 0:
        raise Exception("No hay pedidos cargados!")
    result = {}
    for i in range(0, al.size(pedidos)):
        pedido = al.get_element(pedidos, i)
        canal = pedido["channel"].lower().strip()
        if canal not in result:
            result[canal] = 1
        else:
            result[canal] += 1
    return result

def fecha_mas_antigua(catalog):
    """
    Retorna el pedido con la fecha más antigua.
    """
    pedidos = catalog["pedidos"]
    if al.size(pedidos) == 0:
        raise Exception(f"No hay pedidos cargados!")
    pedido_antiguo = None
    for i in range(0, al.size(pedidos)):
        pedido = al.get_element(pedidos, i)
        if pedido_antiguo is None:
            pedido_antiguo = pedido
        elif pedido["order_date"].strip() < pedido_antiguo["order_date"].strip():
            pedido_antiguo = pedido
    return pedido_antiguo

def fecha_mas_reciente(catalog):
    """
    Retorna el pedido con la fecha más reciente.
    """
    pedidos = catalog["pedidos"]
    if al.size(pedidos) == 0:
        raise Exception(f"No hay pedidos cargados!")
    pedido_reciente = None
    for i in range(0, al.size(pedidos)):
        pedido = al.get_element(pedidos, i)
        if pedido_reciente is None:
            pedido_reciente = pedido
        elif pedido["order_date"].strip() > pedido_reciente["order_date"].strip():
            pedido_reciente = pedido
    return pedido_reciente
    
def mayor_amount(catalog):
    """Retorna el pedido con mayor amount.
    """
    pedidos = catalog["pedidos"]
    if al.size(pedidos) == 0:
        raise Exception(f"No hay pedidos cargados!")
    pedido_mayor = None
    for i in range(0, al.size(pedidos)):
        pedido = al.get_element(pedidos, i)
        if pedido_mayor is None:
            pedido_mayor = pedido
        elif pedido_mayor["amount"] < pedido["amount"]:
            pedido_mayor = pedido
    return pedido_mayor

def menor_amount(catalog):
    """Retorna el pedido con menor amount.
    """
    pedidos = catalog["pedidos"]
    if al.size(pedidos) == 0:
        raise Exception(f"No hay pedidos cargados!")
    pedido_menor = None
    for i in range(0, al.size(pedidos)):
        pedido = al.get_element(pedidos, i)
        if pedido_menor is None:
            pedido_menor = pedido
        elif pedido_menor["amount"] > pedido["amount"]:
            pedido_menor = pedido
    return pedido_menor

def criterio_por_amount_descendente(pedido1, pedido2):
    """
    True si pedido1 va antes que pedido2: orden descendente por Amount,
    con Order_ID ascendente como desempate.
    """
    if pedido1["amount"] > pedido2["amount"]:
        return True
    elif pedido1["amount"] < pedido2["amount"]:
        return False
    else:
        return pedido1["order_id"] < pedido2["order_id"]

def ord_pedidos_amount(catalog):
    """
    Retorna la lista de pedidos ordenada de manera descendente por Amount.
    """
    pedidos = catalog["pedidos"]
    ord_list = al.quick_sort(pedidos, criterio_por_amount_descendente)
    return ord_list

def first_last_5_pedidos(catalog):
    """
    Retorna una tupla (primeros_5, ultimos_5) de la lista ordenada
    descendente por Amount.
    """
    ord_list = ord_pedidos_amount(catalog)
    total = al.size(ord_list)
    if 5 < total:
        n = 5
    else:
        n = total
    primeros = al.sub_list(ord_list, 0, n)
    ultimos = al.sub_list(ord_list, total - n, n)
    return (primeros, ultimos)

    # Requerimientos del Reto:
    
def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
