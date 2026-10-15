import time
import csv
csv.field_size_limit(2147483647)
import sys
default_limit = 1000
sys.setrecursionlimit(default_limit * 10)
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Map import map_entry as me


#  1. CATALOGO

def new_logic():
    """
    Crea el catalogo donde se almacenan la lista de pedidos y los mapas
    que usan los requerimientos.

    Llaves de los mapas (el valor siempre es una lista de pedidos):
        pedidos_por_pais          -> pais                 (Req 2 y Req 5)
        pedidos_por_mes           -> "YYYY-MM"            (Req 1)
        pedidos_por_fecha         -> "YYYY-MM-DD"         (Req 3)
        pedidos_por_producto_pais -> (producto, pais)     (Req 4)
        pedidos_por_producto      -> producto             (Req 6)
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
        "pedidos_por_pais": mlp.new_map(5, 0.5),
        "pedidos_por_mes": mlp.new_map(24, 0.5),
        "pedidos_por_fecha": mlp.new_map(730, 0.5),
        "pedidos_por_producto_pais": mlp.new_map(300, 0.5),
        "pedidos_por_producto": mlp.new_map(30, 0.5)
    }
    return catalog

#  CARGA DE DATOS

def load_data(catalog, filename):
    """
    Carga los datos del reto leyendo el CSV una sola vez.

    Por cada fila: crea el pedido, lo guarda en la lista principal,
    actualiza el reporte de carga y lo agrega a los mapas.

    Returns:
        tuple: (catalogo, reporte de carga)
    """
    start = get_time()
    with open(filename, encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=",")
        for row in reader:
            pedido = crear_pedido(row)
            al.add_last(catalog["pedidos"], pedido)
            actualizar_reporte_carga(catalog, pedido)
            agregar_pedido_a_mapas(catalog, pedido)

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
 
    Args:
        row (dict): Fila leida por csv.DictReader.
 
    Returns:
        dict: Pedido con sus campos ya convertidos (float, int, str).
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
    Actualiza los acumulados del reporte de carga con un pedido nuevo:
    pedido mas antiguo/reciente, Amount minimo/maximo y conteo por canal.
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

def agregar_a_mapa_lista(catalog, nombre_mapa, llave, pedido):
    """
    Agrega un pedido a la lista asociada a una llave dentro de un mapa del
    catalogo. Si la llave no existe, crea la lista y la inserta en el mapa.

    Args:
        catalog (dict): Catalogo con los mapas.
        nombre_mapa (str): Nombre del mapa dentro del catalogo.
        llave (Any): Llave bajo la cual se guarda el pedido.
        pedido (dict): Pedido a agregar.
    """
    mapa = catalog[nombre_mapa]
    lista = mlp.get(mapa, llave)
    if lista is None:
        lista = al.new_list()
        al.add_last(lista, pedido)
        # put puede devolver un mapa nuevo (rehash), por eso se reasigna
        catalog[nombre_mapa] = mlp.put(mapa, llave, lista)
    else:
        al.add_last(lista, pedido)

def agregar_pedido_a_mapas(catalog, pedido):
    """
    Agrega un pedido a todos los mapas de los requerimientos.
    Se llama una vez por pedido durante la carga. Costo: O(1) promedio.
    """
    # Req 1: llave "YYYY-MM"
    agregar_a_mapa_lista(catalog, "pedidos_por_mes", pedido["order_date"][:7], pedido)
    # Req 2 y Req 5: llave pais
    agregar_a_mapa_lista(catalog, "pedidos_por_pais", pedido["country"], pedido)
    # Req 3: llave "YYYY-MM-DD"
    agregar_a_mapa_lista(catalog, "pedidos_por_fecha", pedido["order_date"], pedido)
    # Req 4: llave (producto, pais)
    llave_prod_pais = (pedido["product"], pedido["country"])
    agregar_a_mapa_lista(catalog, "pedidos_por_producto_pais", llave_prod_pais, pedido)
    # Req 6: llave producto
    agregar_a_mapa_lista(catalog, "pedidos_por_producto", pedido["product"], pedido)
 
def total_pedidos(catalog):
    """
    Da el total de pedidos cargados.
    """
    return al.size(catalog["pedidos"])
 
def criterio_por_amount_descendente(pedido1, pedido2):
    """
    True si pedido1 va antes que pedido2: Amount descendente y,
    como desempate, Order_ID ascendente.
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
    Usa merge_sort: O(n log n) garantizado y no modifica catalog["pedidos"].
    """
    pedidos = catalog["pedidos"]
    ord_list = al.merge_sort(pedidos, criterio_por_amount_descendente)
    return ord_list
 
def first_last_5_pedidos(catalog):
    """
    Retorna una tupla (primeros_5, ultimos_5) tomada de la lista ordenada
    de manera descendente por Amount.
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

#  REQUERIMIENTOS

#  Requerimiento 1: Pedidos por mes y rango de descuento

def criterio_req1(pedido1, pedido2):
    """
    True si pedido1 va antes que pedido2: Discount_Pct descendente,
    luego Amount descendente y luego Order_ID ascendente.
    """
    if pedido1["discount_pct"] > pedido2["discount_pct"]:
        return True
    elif pedido1["discount_pct"] < pedido2["discount_pct"]:
        return False
    elif pedido1["amount"] > pedido2["amount"]:
        return True
    elif pedido1["amount"] < pedido2["amount"]:
        return False
    else:
        return pedido1["order_id"] < pedido2["order_id"]

def filtrar_req1(catalog, anio, mes, desc_min, desc_max):
    """
    Obtiene del mapa los pedidos del mes y se queda con los que tienen
    Discount_Pct dentro del rango (extremos incluidos).
 
    Returns:
        tuple: (lista filtrada, suma de Amount, suma de Price_per_Box,
                suma de Boxes_Shipped)
    """
    llave = f"{anio}-{mes:02d}"
    candidatos = mlp.get(catalog["pedidos_por_mes"], llave)
    filtrados = al.new_list()
    suma_amount = 0
    suma_precio = 0
    suma_cajas = 0
    if candidatos is not None:
        for i in range(al.size(candidatos)):
            pedido = al.get_element(candidatos, i)
            if desc_min <= pedido["discount_pct"] and pedido["discount_pct"] <= desc_max:
                al.add_last(filtrados, pedido)
                suma_amount += pedido["amount"]
                suma_precio += pedido["price_per_box"]
                suma_cajas += pedido["boxes_shipped"]
    return filtrados, suma_amount, suma_precio, suma_cajas

def req_1(catalog, anio, mes, desc_min, desc_max):
    """
    Retorna el resultado del requerimiento 1: pedidos de un mes con
    Discount_Pct dentro de un rango (inclusivo).

    Complejidad: O(1) para el get del mes + O(k) para filtrar + O(k log k)
    para ordenar con merge_sort, donde k = pedidos del mes (k <= n).
    """
    start = get_time()
    filtrados, suma_amount, suma_precio, suma_cajas = filtrar_req1(catalog, anio, mes, desc_min, desc_max)
    total = al.size(filtrados)
    if total > 0:
        promedio_precio = suma_precio / total
        promedio_cajas = suma_cajas / total
    else:
        promedio_precio = 0
        promedio_cajas = 0
    filtrados = al.merge_sort(filtrados, criterio_req1)
    end = get_time()
    return {
        "tiempo_ms": delta_time(start, end),
        "total_pedidos": total,
        "monto_total": suma_amount,
        "promedio_precio": promedio_precio,
        "promedio_cajas": promedio_cajas,
        "pedidos": filtrados
    }

#  Requerimiento 2: Pedidos por pais y rango de cajas enviadas

def sort_crit_boxes_shipped(element_1, element_2):
    """
    Criterio de ordenamiento del Req 2: Boxes_Shipped ascendente, luego
    Order_Date descendente y luego Order_ID ascendente.

    Args:
        element_1 (dict): Primer pedido a comparar.
        element_2 (dict): Segundo pedido a comparar.

    Returns:
        bool: True si element_1 debe ir antes que element_2.
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
    """
    Filtra los pedidos del pais por rango de cajas enviadas y calcula los
    acumulados del requerimiento (sumas, conteo por producto y producto
    mas frecuente).

    Returns:
        tuple: (lista filtrada y ordenada, mapa producto -> conteo,
                suma de Marketing_Spend, suma de Amount,
                pedido del producto mas frecuente, conteo de ese producto)
    """
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
            # Conteo de pedidos por producto
            if pedidos_productos is None:
                conteo = 1
                mapa_productos = mlp.put(mapa_productos, pedido['product'], conteo)
            else:
                mapa_productos = mlp.put(mapa_productos, pedido['product'], pedidos_productos + 1)
            suma_marketing_spend += pedido['marketing_spend']
            suma_amount += pedido['amount']
            # Producto mas frecuente (desempate: nombre alfabeticamente menor)
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
    Retorna el resultado del requerimiento 2: pedidos de un pais con
    Boxes_Shipped dentro de un rango (inclusivo).
    """
    start_time = get_time()
    filtered_list, mapa_productos, suma_marketing_spend, suma_amount, producto_mas_frecuente, numero_pedidos_producto = filtrado_req2(catalog, country, min_boxes_shipped, max_boxes_shipped)

    # Numero total de pedidos que cumplieron el filtro
    pedidos_en_rango = al.size(filtered_list)

    # Numero de productos distintos en el rango
    cantidad_productos_distintos = mlp.size(mapa_productos)

    # Promedios de Marketing_Spend y Amount
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

#  Requerimiento 3: Pedidos de una fecha y rango de costo total
 
def criterio_req3(pedido1, pedido2):
    """
    True si pedido1 va antes que pedido2: Amount descendente, luego
    Aporte comercial (Amount - Marketing_Spend) descendente y luego
    Order_ID ascendente.
    """
    aporte1 = pedido1["amount"] - pedido1["marketing_spend"]
    aporte2 = pedido2["amount"] - pedido2["marketing_spend"]
    if pedido1["amount"] > pedido2["amount"]:
        return True
    elif pedido1["amount"] < pedido2["amount"]:
        return False
    elif aporte1 > aporte2:
        return True
    elif aporte1 < aporte2:
        return False
    else:
        return pedido1["order_id"] < pedido2["order_id"]

def filtrar_req3(catalog, fecha, monto_min, monto_max):
    """
    Obtiene del mapa los pedidos de la fecha y se queda con los que tienen
    Amount dentro del rango (extremos incluidos).

    Returns:
        tuple: (lista filtrada, suma de Amount, suma de Marketing_Spend)
    """
    candidatos = mlp.get(catalog["pedidos_por_fecha"], fecha)
    filtrados = al.new_list()
    suma_amount = 0
    suma_marketing = 0
    if candidatos is not None:
        for i in range(al.size(candidatos)):
            pedido = al.get_element(candidatos, i)
            if monto_min <= pedido["amount"] and pedido["amount"] <= monto_max:
                al.add_last(filtrados, pedido)
                suma_amount += pedido["amount"]
                suma_marketing += pedido["marketing_spend"]
    return filtrados, suma_amount, suma_marketing

def req_3(catalog, fecha, monto_min, monto_max):
    """
    Retorna el resultado del requerimiento 3: pedidos de una fecha con
    Amount dentro de un rango (inclusivo).

    Complejidad: O(1) para el get de la fecha + O(k) para filtrar + O(k log k)
    para ordenar con merge_sort, donde k = pedidos de ese dia.
    """
    start = get_time()
    filtrados, suma_amount, suma_marketing = filtrar_req3(catalog, fecha, monto_min, monto_max)
    total = al.size(filtrados)
    filtrados = al.merge_sort(filtrados, criterio_req3)
    end = get_time()
    return {
        "tiempo_ms": delta_time(start, end),
        "total_pedidos": total,
        "monto_total": suma_amount,
        "marketing_total": suma_marketing,
        "aporte_total": suma_amount - suma_marketing,
        "pedidos": filtrados
    }

#  Requerimiento 4: Precio promedio de una combinacion Producto-Pais

def mejor_pedido_req4(pedido1, pedido2):
    """
    True si pedido1 es mejor que pedido2: mayor Amount; si empatan, menor
    Marketing_Spend; si persiste el empate, menor Order_ID.
    """
    if pedido1["amount"] > pedido2["amount"]:
        return True
    elif pedido1["amount"] < pedido2["amount"]:
        return False
    elif pedido1["marketing_spend"] < pedido2["marketing_spend"]:
        return True
    elif pedido1["marketing_spend"] > pedido2["marketing_spend"]:
        return False
    else:
        return pedido1["order_id"] < pedido2["order_id"]

def req_4(catalog, producto, pais):
    """
    Retorna el resultado del requerimiento 4: estadisticas de la combinacion
    Producto-Pais y los 2 pedidos de mayor Amount.
 
    Complejidad: O(1) para el get de la llave (producto, pais) + O(k) para
    recorrer el grupo una sola vez (sumas y top 2), donde k = pedidos de la
    combinacion. No hace falta ordenar: el top 2 se mantiene en una pasada.
    """
    start = get_time()
    candidatos = mlp.get(catalog["pedidos_por_producto_pais"], (producto, pais))
    suma_precio = 0
    suma_descuento = 0
    suma_marketing = 0
    suma_cajas = 0
    primero = None
    segundo = None
    total = 0
    if candidatos is not None:
        total = al.size(candidatos)
        for i in range(total):
            pedido = al.get_element(candidatos, i)
            suma_precio += pedido["price_per_box"]
            suma_descuento += pedido["discount_pct"]
            suma_marketing += pedido["marketing_spend"]
            suma_cajas += pedido["boxes_shipped"]
            # Se mantienen los dos mejores pedidos
            if primero is None or mejor_pedido_req4(pedido, primero):
                segundo = primero
                primero = pedido
            elif segundo is None or mejor_pedido_req4(pedido, segundo):
                segundo = pedido
    top_2 = al.new_list()
    if primero is not None:
        al.add_last(top_2, primero)
    if segundo is not None:
        al.add_last(top_2, segundo)
    if total > 0:
        promedio_precio = suma_precio / total
        promedio_descuento = suma_descuento / total
        promedio_marketing = suma_marketing / total
        promedio_cajas = suma_cajas / total
    else:
        promedio_precio = 0
        promedio_descuento = 0
        promedio_marketing = 0
        promedio_cajas = 0
    end = get_time()
    return {
        "tiempo_ms": delta_time(start, end),
        "total_pedidos": total,
        "promedio_precio": promedio_precio,
        "promedio_descuento": promedio_descuento,
        "promedio_marketing": promedio_marketing,
        "promedio_cajas": promedio_cajas,
        "top_2": top_2
    }

#  Requerimiento 5: Top N productos por recaudo (pais y rango de fechas)

def sort_crit_recaudo_total(element1, element2):
    if element1['total_amount'] > element2['total_amount']:
        return True
    elif element1['total_amount'] < element2['total_amount']:
        return False
    elif element1['total_boxes'] > element2['total_boxes']:
        return True
    elif element1['total_boxes'] < element2['total_boxes']:
        return False
    elif element1['product'].casefold() < element2['product'].casefold():
        return True
    else:
        return False

def filtrado_req5(catalog, country, initial_date, final_date):
    mapa = catalog['pedidos_por_pais']
    array_list = mlp.get(mapa, country)
    mapa_productos = mlp.new_map(100, 0.5)
    recaudo_total_filtro = 0
    pedidos_en_filtro = 0
    if array_list is None:
        return (mapa_productos, recaudo_total_filtro, pedidos_en_filtro)
    for i in range(0, al.size(array_list)):
        pedido = al.get_element(array_list, i)
        order_date = pedido['order_date']
        if order_date.strip() >= initial_date.strip() and order_date.strip() <= final_date.strip():
            pedidos_en_filtro += 1
            recaudo_total_filtro += pedido['amount']
            producto_en_mapa = mlp.get(mapa_productos, pedido['product'])
            if producto_en_mapa is None:
                info = {
                    'product': pedido['product'],
                    'num_pedidos': 1,
                    'total_boxes': pedido['boxes_shipped'],
                    'total_amount': pedido['amount'],
                    'suma_price_per_box': pedido['price_per_box'],
                    'suma_discount': pedido['discount_pct'],
                    'total_marketing': pedido['marketing_spend'],
                }
                mapa_productos = mlp.put(mapa_productos, pedido['product'], info)
            else:
                producto_en_mapa['num_pedidos'] += 1
                producto_en_mapa['total_boxes'] += pedido['boxes_shipped']
                producto_en_mapa['total_amount'] += pedido['amount']
                producto_en_mapa['suma_price_per_box'] += pedido['price_per_box']
                producto_en_mapa['suma_discount'] += pedido['discount_pct']
                producto_en_mapa['total_marketing'] += pedido['marketing_spend']
    return (mapa_productos, recaudo_total_filtro, pedidos_en_filtro)

def req_5(catalog, N, country, initial_date, final_date):
    """
    Retorna el resultado del requerimiento 5
    """
    start_time = get_time()
    mapa_productos, recaudo_total_filtro, pedidos_en_filtro = filtrado_req5(catalog, country, initial_date, final_date)
    values = mlp.value_set(mapa_productos)
    
    ordered_products = al.quick_sort(values, sort_crit_recaudo_total)
    if N >= mlp.size(mapa_productos):
        top = al.sub_list(ordered_products, 0, mlp.size(mapa_productos))
    else:
        top = al.sub_list(ordered_products, 0, N)
    for i in range(0, al.size(top)):
        registro = al.get_element(top, i)
        registro['promedio_price_per_box'] = registro['suma_price_per_box'] / registro['num_pedidos']
        registro['promedio_discount_pct'] = registro['suma_discount'] / registro['num_pedidos']
    result = {
        'tiempo_ejecucion': None,
        'num_total_pedidos_filtro': pedidos_en_filtro,
        'num_productos_diferentes': mlp.size(mapa_productos),
        'total_recaudo_pedidos_filtrados': recaudo_total_filtro,
        'productos_top': top
        
    }
    end_time = get_time()
    result['tiempo_ejecucion'] = delta_time(start_time, end_time)
    return result

# Requerimiento 6

def criterio_req6(pais1, pais2):
    """
    True si pais1 va antes que pais2: eficiencia descendente, luego Amount
    total descendente y luego Country ascendente.
    Recibe los acumuladores de pais (diccionarios), no pedidos.
    """
    if pais1["eficiencia"] > pais2["eficiencia"]:
        return True
    elif pais1["eficiencia"] < pais2["eficiencia"]:
        return False
    elif pais1["amount"] > pais2["amount"]:
        return True
    elif pais1["amount"] < pais2["amount"]:
        return False
    else:
        return pais1["country"] < pais2["country"]


def acumular_paises_req6(catalog, producto, fecha_ini, fecha_fin):
    """
    Obtiene del mapa los pedidos del producto, filtra por rango de fechas y
    acumula por pais en un mapa temporal (llave: pais, valor: acumulador).

    Returns:
        tuple: (mapa de paises, total pedidos, Amount total, Marketing_Spend total)
    """
    candidatos = mlp.get(catalog["pedidos_por_producto"], producto)
    paises = mlp.new_map(30, 0.5)
    total_pedidos = 0
    amount_total = 0
    marketing_total = 0
    if candidatos is not None:
        for i in range(al.size(candidatos)):
            pedido = al.get_element(candidatos, i)
            fecha = pedido["order_date"]
            if fecha_ini <= fecha and fecha <= fecha_fin:
                acumulador = mlp.get(paises, pedido["country"])
                if acumulador is None:
                    acumulador = {
                        "country": pedido["country"],
                        "pedidos": 0,
                        "amount": 0,
                        "marketing": 0,
                        "cajas": 0,
                        "suma_precio": 0,
                        "precio_promedio": 0,
                        "eficiencia": 0
                    }
                    paises = mlp.put(paises, pedido["country"], acumulador)
                acumulador["pedidos"] += 1
                acumulador["amount"] += pedido["amount"]
                acumulador["marketing"] += pedido["marketing_spend"]
                acumulador["cajas"] += pedido["boxes_shipped"]
                acumulador["suma_precio"] += pedido["price_per_box"]
                total_pedidos += 1
                amount_total += pedido["amount"]
                marketing_total += pedido["marketing_spend"]
    return paises, total_pedidos, amount_total, marketing_total


def req_6(catalog, n, producto, fecha_ini, fecha_fin):
    """
    Retorna el resultado del requerimiento 6: los N paises con mayor eficiencia
    de mercadeo (suma Amount / suma Marketing_Spend) para un producto y un
    rango de fechas.

    Complejidad: O(1) para el get del producto + O(k) para filtrar y acumular
    por pais + O(c log c) para ordenar los c paises con merge_sort
    (c = numero de paises, pequeño y independiente de n).
    """
    start = get_time()
    paises, total_pedidos, amount_total, marketing_total = acumular_paises_req6(
        catalog, producto, fecha_ini, fecha_fin)

    # Solo entran al ranking los paises con Marketing_Spend total > 0
    acumulados = mlp.value_set(paises)
    ranking = al.new_list()
    for i in range(al.size(acumulados)):
        acumulador = al.get_element(acumulados, i)
        if acumulador["marketing"] > 0:
            acumulador["eficiencia"] = acumulador["amount"] / acumulador["marketing"]
            acumulador["precio_promedio"] = acumulador["suma_precio"] / acumulador["pedidos"]
            al.add_last(ranking, acumulador)

    ranking = al.merge_sort(ranking, criterio_req6)

    # Top N (si N es mayor a los paises disponibles, se muestran todos)
    top_n = al.new_list()
    i = 0
    while i < n and i < al.size(ranking):
        al.add_last(top_n, al.get_element(ranking, i))
        i += 1

    end = get_time()
    return {
        "tiempo_ms": delta_time(start, end),
        "total_pedidos": total_pedidos,
        "total_paises": mlp.size(paises),
        "amount_total": amount_total,
        "marketing_total": marketing_total,
        "top_paises": top_n
    }


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