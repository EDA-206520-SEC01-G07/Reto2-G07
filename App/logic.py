import time
import csv
csv.field_size_limit(2147483647)
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_entry as me


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
        },
        # Mapas de los requerimientos
        "pedidos_por_pais": mlp.new_map(5, 0.5)
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
            # mapa req 1:
            
            # mapa req 2:
            pedidos_pais = mlp.get(catalog['pedidos_por_pais'], pedido['country'])
            if pedidos_pais is None:
                lista = al.new_list()
                al.add_last(lista, pedido)
                catalog['pedidos_por_pais'] = mlp.put(catalog['pedidos_por_pais'], pedido['country'], lista)
            else:
                al.add_last(pedidos_pais, pedido)
            # mapa req 3:
            
            # mapa req 4:
            
            # mapa req 5:
            
            # mapa req 6:
                
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

    # Funciones Auxiliares Requerimiento 2:

def sort_crit_boxes_shipped(element_1, element_2):
    """Es el sort criteria para organizar ascendentemente por boxes_shipped la lista filtrada de el req2.

    Args:
        element_1 (Any): Primer elemento a comparar
        element_2 (Any): Segundo elemento a comparar

    Returns:
        bool: True si var1 es < var2
    """
    if element_1['boxes_shipped'] < element_2['boxes_shipped']:
        return True
    elif element_1['boxes_shipped'] > element_2['boxes_shipped']:
        return False
    elif element_1['order_date'].strip() > element_2['order_date'].strip():
        return True
    elif element_1['order_date'].strip() < element_2['order_date'].strip():
        return False
    if element_1['order_id'] < element_2['order_id']:
        return True
    else:
        return False

def filtrado_req2(catalog, country, min_boxes_shipped, max_boxes_shipped):
    mapa = catalog['pedidos_por_pais']
    array_list = mlp.get(mapa, country)
    filtered_list = al.new_list()
    mapa_productos = mlp.new_map(100, 0.5)
    suma_marketing_spend = 0
    suma_amount = 0
    producto_mas_frecuente = None
    conteo_produ_frecuente = None
    if array_list is None:
        return (filtered_list, mapa_productos, suma_marketing_spend, suma_amount, producto_mas_frecuente, conteo_produ_frecuente)
    for i in range(0, al.size(array_list)):
        pedido = al.get_element(array_list, i)
        boxes_shipped_pedido = pedido['boxes_shipped']
        if min_boxes_shipped <= boxes_shipped_pedido and max_boxes_shipped >= boxes_shipped_pedido:
            pedidos_productos = mlp.get(mapa_productos, pedido['product'])
            al.add_last(filtered_list, pedido)
            if pedidos_productos is None:
                conteo = 1
                mapa_productos = mlp.put(mapa_productos, pedido['product'], conteo)
            else:
                mapa_productos = mlp.put(mapa_productos, pedido['product'], pedidos_productos + 1)
            suma_marketing_spend += pedido['marketing_spend']
            suma_amount += pedido['amount']
            if producto_mas_frecuente is None:
                producto_mas_frecuente = pedido
                conteo_produ_frecuente = mlp.get(mapa_productos, pedido['product'])
            else:
                if conteo_produ_frecuente < mlp.get(mapa_productos, pedido['product']):
                    producto_mas_frecuente = pedido
                    conteo_produ_frecuente = mlp.get(mapa_productos, pedido['product'])
                elif conteo_produ_frecuente == mlp.get(mapa_productos, pedido['product']):
                    if producto_mas_frecuente['product'].casefold() > pedido['product'].casefold():
                        producto_mas_frecuente = pedido
                        conteo_produ_frecuente = mlp.get(mapa_productos, pedido['product']) 
        
    filtered_list = al.quick_sort(filtered_list, sort_crit_boxes_shipped)
    return (filtered_list, mapa_productos, suma_marketing_spend, suma_amount, producto_mas_frecuente, conteo_produ_frecuente)

def req_2(catalog, country, min_boxes_shipped, max_boxes_shipped):
    """
    Retorna el resultado del requerimiento 2
    """
    start_time = get_time()
    filtered_list, mapa_productos, suma_marketing_spend, suma_amount, producto_mas_frecuente, numero_pedidos_producto = filtrado_req2(catalog, country, min_boxes_shipped, max_boxes_shipped)
    
    # Número total de pedidos que cumplieron el filtro.
    pedidos_en_rango = al.size(filtered_list)
    
    # Número de productos distintos en el rango.
    cantidad_productos_distintos = mlp.size(mapa_productos)
    
    # Promedio Marketing Spend y Amount
    if pedidos_en_rango > 0:
        promedio_marketing_spend = suma_marketing_spend / pedidos_en_rango
        promedio_amount = suma_amount / pedidos_en_rango
    else:
        promedio_marketing_spend = 0
        promedio_amount = 0
    
    result = {
        'tiempo_de_ejecución': None,
        'numero_total_pedidos_cumplieron_filtro': pedidos_en_rango,
        'cantidad_productos_distintos_en_rango': cantidad_productos_distintos,
        'promedio_marketing_spend': promedio_marketing_spend,
        'promedio_amount': promedio_amount,
        'producto_frecuente': producto_mas_frecuente,
        'numero_de_pedidos': numero_pedidos_producto,
        'pedidos_filtrados': filtered_list,
    }
    end_time = get_time()
    result['tiempo_de_ejecución'] = delta_time(start_time, end_time)
    return result


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
