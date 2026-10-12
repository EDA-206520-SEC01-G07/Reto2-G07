import time
import csv
csv.field_size_limit(2147483647)
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "pedidos": al.new_list(),
        "reporte_carga": {
            "pedido_mas_antiguo": None,
            "pedido_mas_reciente": None,
            "pedido_max_amount": None,
            "pedido_min_amount": None,
            "pedidos_por_canal": mlp.new_map(3, 0.5)
        }
        # Mapas de los requerimientos
    }
    return catalog

# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start = get_time()
    with open(filename, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            pedido = crear_pedido(row)
            al.add_last(catalog["pedidos"], pedido)
            actualizar_reporte_carga(catalog, pedido)
            # agregar_pedido_a_mapas(catalog, pedido)
    primeros, ultimos = first_last_5_pedidos(catalog)
    end = get_time()

    acumulado = catalog["reporte_carga"]
    reporte = {
        "tiempo_ms": delta_time(start, end),
        "total_pedidos": total_pedidos(catalog),
        "pedidos_por_canal": acumulado["pedidos_por_canal"],
        "pedido_mas_antiguo": acumulado["pedido_mas_antiguo"],
        "pedido_mas_reciente": acumulado["pedido_mas_reciente"],
        "pedido_min_amount": acumulado["pedido_min_amount"],
        "pedido_max_amount": acumulado["pedido_max_amount"],
        "primeros_5_amount": primeros,
        "ultimos_5_amount": ultimos
    }
    return catalog, reporte

def crear_pedido(row):
    """
    Convierte una fila del CSV en un pedido con los tipos correctos.
    """
    return {
        "order_id": row["Order_ID"].strip(),
        "product": row["Product"].strip(),
        "country": row["Country"].strip(),
        "channel": row["Channel"].strip(),
        "order_date": row["Order_Date"].strip(),
        "discount_pct": float(row["Discount_Pct"]),
        "price_per_box": float(row["Price_per_Box"]),
        "marketing_spend": float(row["Marketing_Spend"]),
        "boxes_shipped": int(row["Boxes_Shipped"]),
        "amount": float(row["Amount"])
    }


def actualizar_reporte_carga(catalog, pedido):
    """
    Actualiza los acumulados del reporte de carga con un pedido nuevo.
    """
    reporte = catalog["reporte_carga"]

    antiguo = reporte["pedido_mas_antiguo"]
    if antiguo is None or pedido["order_date"] < antiguo["order_date"]:
        reporte["pedido_mas_antiguo"] = pedido

    reciente = reporte["pedido_mas_reciente"]
    if reciente is None or pedido["order_date"] > reciente["order_date"]:
        reporte["pedido_mas_reciente"] = pedido

    maximo = reporte["pedido_max_amount"]
    if maximo is None or pedido["amount"] > maximo["amount"]:
        reporte["pedido_max_amount"] = pedido

    minimo = reporte["pedido_min_amount"]
    if minimo is None or pedido["amount"] < minimo["amount"]:
        reporte["pedido_min_amount"] = pedido

    canales = reporte["pedidos_por_canal"]
    cantidad = mlp.get(canales, pedido["channel"])
    if cantidad is None:
        cantidad = 0
    reporte["pedidos_por_canal"] = mlp.put(canales, pedido["channel"], cantidad + 1)

def total_pedidos(catalog):
    """
    Da el total de pedidos cargados.
    """
    return al.size(catalog["pedidos"])

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
