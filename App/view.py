import sys
from App import logic
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from tabulate import tabulate


def new_logic():
    """
        Se crea una instancia del controlador
    """
    control = logic.new_logic()
    return control


def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def print_pedido(pedido):
    """
    Imprime los campos de un pedido que pide el reporte de carga.
    """
    print(f"  Order_ID: {pedido['order_id']} | Product: {pedido['product']} | "
          f"Country: {pedido['country']} | Channel: {pedido['channel']} | "
          f"Order_Date: {pedido['order_date']} | Boxes_Shipped: {pedido['boxes_shipped']} | "
          f"Price_per_Box: {pedido['price_per_box']:.2f} | Amount: {pedido['amount']:.2f}")


def print_lista_pedidos(lista):
    """
    Imprime todos los pedidos de un array_list.
    """
    for i in range(al.size(lista)):
        print_pedido(al.get_element(lista, i))


def print_pedidos_por_canal(mapa_canales):
    """
    Imprime el número de pedidos de cada canal guardado en el mapa.
    """
    canales = mlp.key_set(mapa_canales)
    for i in range(al.size(canales)):
        canal = al.get_element(canales, i)
        print(f"  {canal}: {mlp.get(mapa_canales, canal)}")

data_file = "Data/chocolate_sale_100_ptc.csv"

def load_data(control):
    """
    Carga los datos e imprime el reporte de la carga.
    """
    archivo = data_file
    control, reporte = logic.load_data(control, archivo)

    print("\n========== REPORTE DE CARGA ==========")
    print(f"Tiempo de ejecución: {reporte['tiempo_ms']:.2f} ms")
    print(f"Total de pedidos cargados: {reporte['total_pedidos']}")

    print("\nTotal de pedidos por canal:")
    print_pedidos_por_canal(reporte["pedidos_por_canal"])

    print("\nPedido con la fecha más antigua:")
    print_pedido(reporte["pedido_mas_antiguo"])
    print("\nPedido con la fecha más reciente:")
    print_pedido(reporte["pedido_mas_reciente"])

    print("\nPedido con el menor Amount:")
    print_pedido(reporte["pedido_min_amount"])
    print("\nPedido con el mayor Amount:")
    print_pedido(reporte["pedido_max_amount"])

    print("\nPrimeros 5 pedidos (Amount descendente):")
    print_lista_pedidos(reporte["primeros_5_amount"])
    print("\nÚltimos 5 pedidos (Amount descendente):")
    print_lista_pedidos(reporte["ultimos_5_amount"])
    print("======================================\n")

    return control

def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass


def datos_cargados(control):
    """
    Retorna True si ya se cargaron datos; si no, avisa al usuario.
    """
    if al.size(control["pedidos"]) == 0:
        print("\nPrimero debe cargar la información (opción 0).\n")
        return False
    return True


def imprimir_primeros_ultimos(pedidos, funcion_tabla):
    """
    Imprime todos los pedidos si son 20 o menos; si son mas, imprime
    solo los primeros 10 y los ultimos 10.

    Args:
        pedidos (array_list): Lista de pedidos ya ordenada.
        funcion_tabla (function): Recibe (pedidos, inicio, fin) y retorna la tabla en texto.
    """
    total = al.size(pedidos)
    if total > 20:
        print("\nPrimeros 10 pedidos:")
        print(funcion_tabla(pedidos, 0, 10))
        print("\nÚltimos 10 pedidos:")
        print(funcion_tabla(pedidos, total - 10, total))
    else:
        print("\nPedidos:")
        print(funcion_tabla(pedidos, 0, total))


# ---------------------------- Req 1 ----------------------------------

def tabla_pedidos_req1(pedidos, inicio, fin):
    filas = []
    for i in range(inicio, fin):
        p = al.get_element(pedidos, i)
        filas.append([p['order_id'], p['product'], p['country'], p['channel'],
                      p['order_date'], p['discount_pct'], f"{p['price_per_box']:.2f}",
                      p['boxes_shipped'], f"{p['amount']:.2f}"])
    encabezados = ["Order_ID", "Product", "Country", "Channel", "Order_Date",
                   "Discount_Pct", "Price_per_Box", "Boxes_Shipped", "Amount"]
    return tabulate(filas, headers=encabezados, tablefmt="grid")


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    anio = int(input("Año (YYYY): "))
    mes = int(input("Mes (1-12): "))
    # Usar la misma escala que tiene el CSV (verificar si es 0.15 o 15)
    desc_min = float(input("Descuento mínimo: "))
    desc_max = float(input("Descuento máximo: "))

    result = logic.req_1(control, anio, mes, desc_min, desc_max)

    print("\n========== REQUERIMIENTO 1 ==========")
    print(f"Tiempo de ejecución: {result['tiempo_ms']:.2f} ms")
    if result['total_pedidos'] == 0:
        print("No se encontraron pedidos para ese mes y rango de descuento.")
    else:
        resumen = [
            ["Total de pedidos que cumplieron el filtro", result['total_pedidos']],
            ["Monto total recaudado", f"{result['monto_total']:.2f}"],
            ["Promedio de Price_per_Box", f"{result['promedio_precio']:.2f}"],
            ["Promedio de Boxes_Shipped", f"{result['promedio_cajas']:.2f}"]
        ]
        print(tabulate(resumen, tablefmt="grid"))
        imprimir_primeros_ultimos(result['pedidos'], tabla_pedidos_req1)
    print("=====================================\n")


# ---------------------------- Req 2 ----------------------------------

def tabla_pedidos_req2(pedidos, inicio, fin):
    """
    Construye las filas de la tabla del Req 2 para los pedidos entre las posiciones inicio y fin.
    """
    filas = []
    for i in range(inicio, fin):
        pedido = al.get_element(pedidos, i)
        filas.append([
            pedido['order_id'],
            pedido['product'],
            pedido['channel'],
            pedido['order_date'],
            pedido['boxes_shipped'],
            f"{pedido['price_per_box']:.2f}",
            f"{pedido['marketing_spend']:.2f}",
            f"{pedido['amount']:.2f}"
        ])
    encabezados = ["Order_ID", "Product", "Channel", "Order_Date",
                   "Boxes_Shipped", "Price_per_Box", "Marketing_Spend", "Amount"]
    return tabulate(filas, headers=encabezados, tablefmt="grid")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    pais = input("País: ").strip()
    minimo = int(input("Número mínimo de cajas enviadas: "))
    maximo = int(input("Número máximo de cajas enviadas: "))

    result = logic.req_2(control, pais, minimo, maximo)

    print("\n========== REQUERIMIENTO 2 ==========")
    print(f"Tiempo de ejecución: {result['tiempo_de_ejecución']:.2f} ms")

    total = result['numero_total_pedidos_cumplieron_filtro']
    if total == 0:
        print("No se encontraron pedidos para ese país y rango de cajas.")
    else:
        resumen = [
            ["Total de pedidos que cumplieron el filtro", total],
            ["Productos distintos en el resultado", result['cantidad_productos_distintos_en_rango']],
            ["Promedio de Marketing_Spend", f"{result['promedio_marketing_spend']:.2f}"],
            ["Promedio de Amount", f"{result['promedio_amount']:.2f}"],
            ["Producto más frecuente", result['producto_frecuente']['product']],
            ["Pedidos del producto más frecuente", result['numero_de_pedidos']]
        ]
        print(tabulate(resumen, tablefmt="grid"))

        pedidos = result['pedidos_filtrados']
        if total > 20:
            print("\nPrimeros 10 pedidos:")
            print(tabla_pedidos_req2(pedidos, 0, 10))
            print("\nÚltimos 10 pedidos:")
            print(tabla_pedidos_req2(pedidos, total - 10, total))
        else:
            print("\nPedidos:")
            print(tabla_pedidos_req2(pedidos, 0, total))
    print("=====================================\n")


# ---------------------------- Req 3 ----------------------------------

def tabla_pedidos_req3(pedidos, inicio, fin):
    filas = []
    for i in range(inicio, fin):
        p = al.get_element(pedidos, i)
        aporte = p['amount'] - p['marketing_spend']
        filas.append([p['order_id'], p['product'], p['country'], p['order_date'],
                      f"{p['marketing_spend']:.2f}", p['boxes_shipped'],
                      f"{p['amount']:.2f}", f"{aporte:.2f}"])
    encabezados = ["Order_ID", "Product", "Country", "Order_Date", "Marketing_Spend",
                   "Boxes_Shipped", "Amount", "Aporte comercial"]
    return tabulate(filas, headers=encabezados, tablefmt="grid")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    monto_min = float(input("Valor mínimo de costo total: "))
    monto_max = float(input("Valor máximo de costo total: "))

    result = logic.req_3(control, fecha, monto_min, monto_max)

    print("\n========== REQUERIMIENTO 3 ==========")
    print(f"Tiempo de ejecución: {result['tiempo_ms']:.2f} ms")
    if result['total_pedidos'] == 0:
        print("No se encontraron pedidos para esa fecha y rango de costo.")
    else:
        resumen = [
            ["Total de pedidos que cumplieron el filtro", result['total_pedidos']],
            ["Monto total recaudado", f"{result['monto_total']:.2f}"],
            ["Inversión total en mercadeo", f"{result['marketing_total']:.2f}"],
            ["Aporte comercial total", f"{result['aporte_total']:.2f}"]
        ]
        print(tabulate(resumen, tablefmt="grid"))
        imprimir_primeros_ultimos(result['pedidos'], tabla_pedidos_req3)
    print("=====================================\n")


# ---------------------------- Req 4 ----------------------------------

def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    producto = input("Producto: ").strip()
    pais = input("País: ").strip()

    result = logic.req_4(control, producto, pais)

    print("\n========== REQUERIMIENTO 4 ==========")
    print(f"Tiempo de ejecución: {result['tiempo_ms']:.2f} ms")
    if result['total_pedidos'] == 0:
        print("No se encontraron pedidos para esa combinación Producto-País.")
    else:
        resumen = [
            ["Total de pedidos que cumplieron el filtro", result['total_pedidos']],
            ["Promedio de Price_per_Box", f"{result['promedio_precio']:.2f}"],
            ["Promedio de Discount_Pct", f"{result['promedio_descuento']:.2f}"],
            ["Promedio de Marketing_Spend", f"{result['promedio_marketing']:.2f}"],
            ["Promedio de Boxes_Shipped", f"{result['promedio_cajas']:.2f}"]
        ]
        print(tabulate(resumen, tablefmt="grid"))

        filas = []
        top_2 = result['top_2']
        for i in range(al.size(top_2)):
            p = al.get_element(top_2, i)
            filas.append([p['order_id'], p['channel'], p['order_date'],
                          p['boxes_shipped'], f"{p['amount']:.2f}"])
        print("\nPedidos de mayor Amount:")
        print(tabulate(filas, headers=["Order_ID", "Channel", "Order_Date",
                                       "Boxes_Shipped", "Amount"], tablefmt="grid"))
    print("=====================================\n")


# ---------------------------- Req 5 ----------------------------------

def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    print("\nEl requerimiento 5 aún no está implementado.\n")


# ---------------------------- Req 6 ----------------------------------

def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    n = int(input("Número N de países: "))
    producto = input("Producto: ").strip()
    fecha_ini = input("Fecha inicial (YYYY-MM-DD): ").strip()
    fecha_fin = input("Fecha final (YYYY-MM-DD): ").strip()

    result = logic.req_6(control, n, producto, fecha_ini, fecha_fin)

    print("\n========== REQUERIMIENTO 6 ==========")
    print(f"Tiempo de ejecución: {result['tiempo_ms']:.2f} ms")
    if result['total_pedidos'] == 0:
        print("No se encontraron pedidos para ese producto y rango de fechas.")
    else:
        resumen = [
            ["Total de pedidos que cumplieron el filtro", result['total_pedidos']],
            ["Países diferentes encontrados", result['total_paises']],
            ["Amount total", f"{result['amount_total']:.2f}"],
            ["Marketing_Spend total", f"{result['marketing_total']:.2f}"]
        ]
        print(tabulate(resumen, tablefmt="grid"))

        filas = []
        top = result['top_paises']
        for i in range(al.size(top)):
            c = al.get_element(top, i)
            filas.append([c['country'], c['pedidos'], f"{c['amount']:.2f}",
                          f"{c['marketing']:.2f}", c['cajas'],
                          f"{c['precio_promedio']:.2f}", f"{c['eficiencia']:.4f}"])
        print("\nTop países por eficiencia de mercadeo:")
        print(tabulate(filas, headers=["Country", "Pedidos", "Amount total",
                                       "Marketing_Spend total", "Boxes_Shipped total",
                                       "Price_per_Box promedio", "Eficiencia"],
                       tablefmt="grid"))
    print("=====================================\n")


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    global control
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if not inputs.strip().isdigit():
            print("Opción errónea, vuelva a elegir.\n")
        else:
            opcion = int(inputs)
            if opcion == 0:
                print("Cargando información de los archivos ....\n")
                # Se crea un catálogo nuevo para no duplicar datos si se carga dos veces
                control = new_logic()
                data = load_data(control)
            elif opcion == 7:
                working = False
                print("\nGracias por utilizar el programa")
            elif opcion >= 1 and opcion <= 6:
                if datos_cargados(control):
                    if opcion == 1:
                        print_req_1(control)
                    elif opcion == 2:
                        print_req_2(control)
                    elif opcion == 3:
                        print_req_3(control)
                    elif opcion == 4:
                        print_req_4(control)
                    elif opcion == 5:
                        print_req_5(control)
                    elif opcion == 6:
                        print_req_6(control)
            else:
                print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()