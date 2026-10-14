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

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


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


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 1:
            print_req_1(control)

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
