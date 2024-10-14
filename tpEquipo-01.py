"""
-----------------------------------------------------------------------------------------------
Título: 
    Gestión Club Deportivo Primera
Fecha: 
    14/10/2024
Autores: 
    Gonzalez Grahl, Mariano (LU: 1060604)
    Borini, Daniel Augusto (LU: 1112803)
    Mastropierro, Lucas Matias (LU: 1157414)
    Contan, Guadalupe (LU: 1144964)

Descripción: 
    Trabajo Prático Obligatorio GRUPAL | Equipo 01 | Algoritmos y Estructuras de Datos 1 / Programación 1

Pendientes:
-----------------------------------------------------------------------------------------------
"""

#----------------------------------------------------------------------------------------------
# MÓDULOS
#----------------------------------------------------------------------------------------------
from datetime import datetime, timedelta
import random

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def iniciarClub(nombre, cap, socios):
    """
    Esta función lo que hace es inicializar los datos de un club, configurando su estructura, 
    capacidad total, sectores (general, platea, palco) y la cantidad de socios.

    Recibe:
    - nombre: string, el nombre del club.
    - cap: int, la capacidad total de asistentes en el estadio del club.
    - socios: int, la cantidad de socios que serán parte del club.

    Devuelve:
    - club: dict, un diccionario que contiene la estructura del club con su información de 
      capacidad, sectores y socios.
    - cap: int, la capacidad total del club.
    - socios: int, la cantidad de socios en el club.
    """
    filas = 10
    columnas = {
        "general": 20,
        "platea": 12,
        "palco": 5
    }
    club = {
        "nombre": nombre,
        "capacidad": cap,
        "sectores": {
            "general": {"capacidad": int(cap * 0.6), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["general"] for _ in range(filas)]},
            "platea": {"capacidad": int(cap * 0.3), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["platea"] for _ in range(filas)]},
            "palco": {"capacidad": int(cap * 0.1), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["palco"] for _ in range(filas)]},
        },
        "socios": {f"Socio {i + 1}": {"estado":True} for i in range(socios)},
        "historialPartidos": {},  
        "ventasTotales": {}  
    }
    
    return club, cap, socios

def generarPartidos(club, equiposArgentina,numPartidos):
    '''
    Función encargada de generar un conjunto de partidos aleatorios para un club ingresado, asignando fechas
     y equipos contra los cuales jugará, dentro de un tiempo predefinido (año actual).
    Entre fecha y fecha, habrá por lo menos 7 días de diferencia entre sí.

    Recibe:
    -club = diccionario. Contiene el historial de partidos.
    -equiposArgentina = lista. Lista con los nombres de los equipos de Argentina disponibles.
    -numPartidos= into. Número de partidos que se deben generar.

    Devuelve:
    -Modifica el diccionario "club" agregando partidos a historialPartidos. Asigna fecha y 
    equpos rivales.

    A tener en cuenta:
    -Si no hay equipos disponibles en la lista "equiposArgentina", se imprime mensaje de error y la funcion
    termina.
    -Filtra fechas a ingresar para que estén separadas por 7 días.
    -No permite repetisión de fechas a lo largo del año.
    '''
    if not equiposArgentina:
        print("No hay más equipos rivales disponibles.")
        return
    # Rango de fechas (desde el 1 de enero hasta el 31 de diciembre del año actual)
    fechaInicial = datetime(datetime.now().year, 1, 1)
    fechaFinal = datetime(datetime.now().year, 12, 31)
    delta = fechaFinal - fechaInicial  # Diferencia entre las fechas en días

    # Conjunto para asegurar que no haya fechas repetidas . SI USO SET(ES UN CONJUNTO. PUEDE MODIFICARSE PERO NO TIENE INDICES)
    fechasGeneradas = set() 
    ultimaFecha = fechaInicial

    for i in range(numPartidos):
        # Asegurarse de que el siguiente partido sea al menos 7 días después del anterior
        while True:
            # Generar entre 7 y 14 días adicionales de diferencia entre partidos
            diasAleatorios = random.randint(7, 14)
            fechaPartido = ultimaFecha + timedelta(days=diasAleatorios)
            fechaStr = fechaPartido.strftime("%d/%m/%Y")

            # Asegurarse de que la fecha no exceda el rango del año y no se repita
            if fechaStr not in fechasGeneradas and fechaPartido <= fechaFinal:
                fechasGeneradas.add(fechaStr)
                ultimaFecha = fechaPartido  # Actualizar última fecha utilizada
                break  # Salir del bucle al encontrar una fecha válida

        # Asignar un equipo rival aleatorio
        equipoRival = equiposArgentina[i % len(equiposArgentina)]
        club["historialPartidos"][fechaStr] = equipoRival  # Agregar partido al historial
    print("Partidos generados.")

def definirPrecios(club):
    '''
    Función encargada de definir los precios de las entradas en base a cada sector disponible
    (general, platea y palco) con valores ya predefinidos.

    Recibe:
    -club = diccionario. Contiene el historial de partidos.

    Devuelve:
    - Modifica el diccionario del club actualizando los precios de los sectores:
        - General: 500
        - Platea: 1000
        - Palco: 1500

    Después de actualizar los precios, imprime un mensaje indicando que los precios han sido 
    actualizados correctamente.
    '''
    precioGeneral = 500
    precioPlatea = 1000
    precioPalco = 1500

    club["sectores"]["general"]["precio"] = precioGeneral
    club["sectores"]["platea"]["precio"] = precioPlatea
    club["sectores"]["palco"]["precio"] = precioPalco
    print("Precios actualizados.")

def mostrarAsientos(sector, club):
    '''
    ######BORRAR#####
    '''
    asientos = club["sectores"][sector]["asientos"]
    print(f"\nAsientos disponibles en el sector {sector}:")
    for fila in asientos:
        print(" ".join(fila))
    
    return asientos

def seleccionarPartido(club):
    '''
    Función encargada de seleciconar un partido de la lista de partidos en realación al historial del club.
    Mostrará la lista numerada de partidos con sus respectivas fechas y rivales, solicitando la selección
    de alguno de ellos con el número correspondiente.

    Recibe:
    -club = diccionario. Contiene el historial de partidos.

    Devuelve:
    -fecha = string. Perteneciente al partido elegido.

    Si un usuario ingresa un número fuera del rango de opciones, se le pedirá que vuelva
    a seleccionar una opción, hasta ingresar finalmente un número valido.
    '''
    print("\n--- Seleccionar Partido ---")
    partidos = list(club["historialPartidos"].items())
    for i, (fecha, rival) in enumerate(partidos):
        print(f"{i + 1}. Fecha: {fecha}, Rival: {rival}")
    while True:
        partidoSeleccionado = int(input("Seleccione el número del partido: "))
        if 1 <= partidoSeleccionado <= len(partidos):
            return partidos[partidoSeleccionado - 1][0]  # Devuelve la fecha del partido correctamente
        else:
            print("Número inválido. Intente nuevamente.")

def ventaEntradas(sector, cantidad, club, partido):
    '''
    Función encargada de realizar la venta de entradas para un sector específico de un club en un partido determinado.
    Verifica la disponibilidad de asientos, asigna asientos disponibles y actualiza las entradas vendidas 
    y las ventas totales para ese partido.

    Recibe:
    - sector = String. Nombre del sector donde se realizará la venta de entradas (general, platea, palco).
    - cantidad = Int. Cantidad de entradas que se desean vender.
    - club = Dict. El diccionario del club que contiene la información de los sectores, entradas vendidas, 
    y ventas totales.
    partido = String. Fecha del partido para el cual se están vendiendo las entradas.

    Devuelve:
    - No devuelve nada, pero actualiza la información de entradas vendidas y ventas totales en el diccionario 
      del club.

    Consideraciones:
    - Verifica que el sector ingresado sea válido.
    - La cantidad de entradas debe ser mayor que cero.
    - Asegura que haya suficientes asientos disponibles en el sector antes de realizar la venta.
    - Actualiza los asientos disponibles, marcándolos como ocupados ("X").
    - Imprime un mensaje con el total de la venta.
    - Si no hay suficientes asientos disponibles o se ingresa un sector inválido, muestra un mensaje de error.
    '''
    if sector in club["sectores"]:
        capacidad = club["sectores"][sector]["capacidad"]
        entradasVendidas = club["sectores"][sector]["entradasVendidas"]
        if cantidad <= 0 :
            print("La cantidad de entradas debe ser mayor a cero.")
            return
        
        if entradasVendidas + cantidad <= capacidad:
            asientos = club["sectores"][sector]["asientos"]
            asignados = 0
            for i in range(len(asientos)):
                for j in range(len(asientos[i])):
                    if asientos[i][j] == "O":
                        asientos[i][j] == "X"
                        asignados += 1
                        if asignados == cantidad:
                            break
                if asignados == cantidad:
                    break

            club["sectores"][sector]["entradasVendidas"] += cantidad
            total = cantidad * club["sectores"][sector]["precio"]

            if partido not in club["ventasTotales"]:
                club["ventasTotales"][partido] = {}
            if sector not in club["ventasTotales"][partido]:
                club["ventasTotales"][partido][sector] = 0
            club["ventasTotales"][partido][sector] += total

            print(f"Vendidas {cantidad} entradas para el partido del {partido} en {sector}. Total: ${total}")
            #mostrarAsientos(sector, club)
        else:
            print("No hay suficientes asientos disponibles.")
    else:
        print("Sector inválido.")

def mostrarHistorial(club):
    '''
    Función encargada de imprimir el historial de los partidos del club, mostrar fechas y
    los equipos rivales.

    Recibe:
    - club = Diccionario. El diccionario del club que contiene el historial de partidos.

    Devuelve:
    - Imprime la información del historial de partidos.

    Si el historial está vacio, no mostrará nada.
    '''
    print("Historial de partidos:")
    for fecha, rival in club["historialPartidos"].items():
        print(f"Fecha: {fecha}, Rival: {rival}")

def gestionDeEntradas(club):
    '''
    Función que gestiona el proceso de venta de entradas, como asi la visualización de los asientos disponibles por sector del estadio.
    Presentará un menú con opciones varias para ver los asientos disponibles y vender entradas, permitiendole al usuario seleccionar el partido,
    sector y cantidad de entradas a vender.

    Recibe:
    - club = Diccionario. El diccionario del club que contiene el historial de partidos.

    Devuelve:
    - No devuelve nada puntual, solamente ejecuta las acciones correspondientes a cada opción del menú.

    Funciones menú:
    - Opcion 1: Ver los asientos disponibles para cada sector en específico (ingresado por teclado).
    - Opcion 2: Vender entradas. Se le pide al usuario seleccionar un partido, sector y cantidad.
    - Opcion 0: Volver al menú principal, terminando con la gestión de entradas.

    Considerar:
    - Valida que el sector seleccionado sea válido. Si lo es, continua con el proceso de gestión.
    - Uso de la función "seleccionarPartido" para elegir partido.
    - Uso de la función "ventaEntradas" para procesar la venta.
    - Si el usuario ingresa una opción inválida, se le pide intentar nuevamente.
    '''
    while True:  
        print("\n--- Gestión de Entradas ---")
        print("1. Ver asientos disponibles")
        print("2. Vender entradas")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sector = input("Ingrese el sector (general, platea, palco): ")
            if sector in club["sectores"]:
                #mostrarAsientos(sector, club)
                print("Sector con asientos disponibles todavía.")
            else:
                print("Sector inválido.")

        elif opcion == "2":
            partido = seleccionarPartido(club)
            if partido:
                while True:
                    sector = input("Ingrese el sector (general, platea, palco): ")
                    if sector in club["sectores"]:
                        break
                    else:
                        print("Sector inválido. Por favor, elija entre 'general', 'platea' o 'palco'.")
                
                cantidad = validarEntero("Ingrese la cantidad de entradas a vender: ", 1)
                ventaEntradas(sector, cantidad, club, partido)
            else:
                print("Partido inválido.")
        elif opcion == "0":
            break

        else:
            print("Opción inválida.")


def agregarSocio(club):
    '''
    Función encargada de agregar nuevos socios al club (uno a la vez), solicitando el nombre del socio al usuario e
    insertándolo en el diccionario de socios del club.

    Recibe:
    - club = Dict. Diccionario del club que contiene la información de los socios.

    Devuelve:
    - Actualiza el diccionario de socios del club ccon el nuevo socio agregado.

    Funciones:
    - Solicitar al usuario ingresar el nombre del nuevo socio.
    - Agregar el nuevo socio al diccionario 'club["socios"]', asignandole el valor "True" para indicar que está activo.
    - Imprimir el mensaje de que el socio fue agregado.

    No realiza ninguna validación con el nombre ingresado.
    '''
    nombreSocio = input("Ingrese el nombre del nuevo socio: ")
    club["socios"][nombreSocio] = True  # Agrega el socio al diccionario
    print(f"Socio {nombreSocio} agregado.")

def listarSocios(club):
    '''
    Función encargada de imprimir una lista de socios ACTIVOS del club. Los socios activos serán aquellos que posean el valor "True" en el diccionario.

    Recibe:
    - club = Dict. Diccionario del club que contiene la información de los socios.

    Devuelve:
    - Devuelve el diccionario del club, a fin de imprimir la lista activa de los socios.

    Funciones:
    - Itera sobre el diccionario 'club["socios"]' para encontrar los activos.
    - Imprime los socios activos en una lista.
    - No imprime socios cuyo estado sea "False".
    - Por default, todos los socios están inicialmente activos.
    '''
    print("Lista de socios activos:")
    
    # Itera sobre los socios en el diccionario
    for nombre, datos in club["socios"].items():
        # Verifica si el estado del socio es True
        if datos["estado"] == True:
            print(f"- {nombre}")
    
    return club

def borrarSocio(club):
    '''
    Función que nos permite borrar a un socio del club. Primero muestra la lista con los socios activos, pidiendo luego el
    ingreso del nombre del socio a eliminar.

    Recibe:
    - club = Dict. Diccionario del club que posee la información de los socios.

    Devuelve:
    - Actualiza la lista de socios, eliminando aquel que deseamos borrar.

    Funciones:
    - Llama a la función `listarSocios` para mostrar los socios activos antes de solicitar el nombre del socio a borrar.
    - Solicita al usuario que ingrese el nombre del socio que desea eliminar.
    - Verifica si el nombre ingresado existe en el diccionario de socios.
    - Si el socio existe, lo elimina del diccionario y muestra un mensaje confirmando la eliminación.
    - Si el socio no se encuentra, imprime un mensaje de error.

    Consideraciones:
    - Si no se encuentra el nombre del socio en el diccionario, no se realiza ninguna eliminación.
    '''
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a borrar: ")
    if nombreSocio in club["socios"]:
        del club["socios"][nombreSocio]  # Elimina el socio del diccionario
        print(f"Socio {nombreSocio} borrado.")
    else:
        print("Socio no encontrado.")

def modificarSocio(club):
    '''
    Función que permite modificar el nombre de un socio existente en el club, mostrando primero la lista de 
    socios activos y luego solicitando al usuario que ingrese el nombre del socio a modificar.

    Recibe:
    - club = Dict, el diccionario del club que contiene la información de los socios.

    Devuelve:
    - Actualiza el diccionario de socios con el nuevo nombre especificado.

    Funcionalidades:
    - Llama a la función `listarSocios` para mostrar los socios activos antes de solicitar el nombre del socio a modificar.
    - Solicita al usuario ingresar el nombre del socio que desea modificar.
    - Si el socio existe en el diccionario, solicita un nuevo nombre para el socio y actualiza el diccionario con el nuevo nombre.
    - Imprime un mensaje confirmando el cambio de nombre.
    - Si el socio no se encuentra en el diccionario, imprime un mensaje de error.

    Consideraciones:
    - El nombre del socio en el diccionario es reemplazado completamente por el nuevo nombre ingresado.
    - Si no se encuentra el nombre del socio en el diccionario, no se realiza ninguna modificación.
    '''
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a modificar: ")
    if nombreSocio in club["socios"]:
        nuevoNombre = input("Ingrese el nuevo nombre del socio: ")
        club["socios"][nuevoNombre] = club["socios"].pop(nombreSocio)  # Cambia el nombre del socio
        print(f"Socio {nombreSocio} modificado a {nuevoNombre}.")
    else:
        print("Socio no encontrado.")

def inactivarSocio(club):
    '''
    Esta función permite inactivar (False) a un socio en el club, cambiando su estado a `False`. Primero muestra
    la lista de socios activos y luego solicita al usuario que ingrese el nombre del socio a inactivar.

    Recibe:
    - club = Dict, el diccionario del club que contiene la información de los socios.

    Devuelve:
    - No devuelve nada, pero actualiza el estado del socio en el diccionario cambiándolo a `False`.

    Funcionalidades:
    - Llama a la función `listarSocios` para mostrar los socios activos antes de solicitar el nombre del socio a inactivar.
    - Solicita al usuario ingresar el nombre del socio que desea inactivar.
    - Si el socio existe en el diccionario, cambia el valor de `"estado"` a `False` para marcar al socio como inactivo.
    - Imprime un mensaje confirmando la inactivación del socio.
    - Si el socio no se encuentra en el diccionario, imprime un mensaje de error.

    Consideraciones:
    - Si el nombre del socio no se encuentra en el diccionario, no se realiza ninguna modificación.
    '''
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a inactivar: ")
    if nombreSocio in club["socios"]:
        club["socios"][nombreSocio]["estado"] = False
        print(f"El socio {nombreSocio} ha sido inactivado.")
    else:
        print("Socio no encontrado.")

def listarSociosInactivos(club):
    '''
    Función que imprime una lista de los socios inactivos del club. Los socios inactivos son aquellos cuyo estado 
    está marcado como `False` en el diccionario de socios.

    Recibe:
    - club = Dict, el diccionario del club que contiene la información de los socios.

    Devuelve:
    - Devuelve el diccionario del club, aunque su propósito principal es imprimir la lista de socios inactivos.

    Funcionalidades:
    - Itera sobre el diccionario `club["socios"]` para encontrar aquellos socios cuyo estado es `False`.
    - Imprime los nombres de los socios inactivos.

    Consideraciones:
    - No imprime a los socios cuyo estado sea `True`.
    - Se asume que el diccionario de cada socio contiene una clave `"estado"` que indica si el socio está inactivo.
    '''
    print("Lista de socios inactivos:")
    
    # Itera sobre los socios en el diccionario
    for nombre, datos in club["socios"].items():
        # Verifica si el estado del socio es False
        if datos["estado"] == False:
            print(f"- {nombre}")
    
    return club

def gestionDeSocios(club):
    '''
    Esta función proporciona un menú interactivo para la gestión de socios del club. Permite al usuario agregar, listar, 
    borrar, modificar, inactivar socios, así como listar los socios inactivos.

    Recibe:
    - club = dict, el diccionario del club que contiene la información de los socios.

    Devuelve:
    - No devuelve nada. Esta función es un bucle interactivo que permite la gestión de los socios del club.

    Funciones:
    - Muestra un menú con varias opciones:
        1. Agregar socio: Llama a la función `agregarSocio` para añadir un nuevo socio al club.
        2. Listar socios: Llama a la función `listarSocios` para mostrar los socios activos.
        3. Borrar socio: Llama a la función `borrarSocio` para eliminar un socio del club.
        4. Modificar socio: Llama a la función `modificarSocio` para cambiar el nombre de un socio existente.
        5. Inactivar socio: Llama a la función `inactivarSocio` para marcar a un socio como inactivo.
        6. Listar socios inactivos: Llama a la función `listarSociosInactivos` para mostrar una lista de los socios inactivos.
        0. Volver al menú principal: Sale del bucle y regresa al menú principal.
    - Maneja entradas inválidas mostrando un mensaje de error cuando el usuario selecciona una opción no válida.
    - El bucle continúa hasta que el usuario seleccione la opción de volver al menú principal (opción "0").

    Consideraciones:
    - Asegura que las funciones relacionadas con la gestión de socios sean llamadas según la selección del usuario.
    - Valida que el usuario ingrese opciones correctas del menú antes de proceder con la acción correspondiente.
    '''
    while True:
        print("\n--- Gestión de Socios ---")
        print("1. Agregar socio")
        print("2. Listar socios")
        print("3. Borrar socio")
        print("4. Modificar socio")
        print("5. Inactivar socio")
        print("6. Listar socios inactivos")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregarSocio(club)

        elif opcion == "2":
            listarSocios(club)

        elif opcion == "3":
            borrarSocio(club)

        elif opcion == "4":
            modificarSocio(club)

        elif opcion == "5":
            inactivarSocio(club)
        elif opcion == "6":
            listarSociosInactivos(club)
        elif opcion == "0":
            break

        else:
            print("Opción inválida.")

def informeDeVentas(club):
    '''
    Esta función genera un informe detallado de las ventas de entradas del club, tanto en total como por partido y sector.

    Recibe:
    - club = dict, el diccionario del club que contiene información sobre las ventas y partidos.

    Devuelve:
    - No devuelve nada. La función imprime directamente el informe de ventas.

    Funciones:
    - Comprueba si existen ventas registradas. Si no hay ventas, imprime un mensaje y termina la función.
    - Calcula e imprime el total de ventas de todos los partidos combinados.
    - Desglosa las ventas por partido y sector, mostrando el total de ventas por partido, y el detalle de las ventas por sector (general, platea, palco) para cada partido.
    - Si un partido no tiene ventas registradas, lo indica con un mensaje.

    Consideraciones:
    - El informe solo incluye partidos que tienen registros de ventas en el diccionario `club["ventasTotales"]`.
    - Las ventas totales incluyen todas las entradas vendidas para cada sector de un partido.
    - Maneja el caso en el que no hay ventas registradas en absoluto mostrando un mensaje adecuado.
    '''
    print("\n--- Informe de Ventas ---")

    # Si no hay ventas registradas, mostramos un mensaje
    if not club["ventasTotales"]:
        print("No hay ventas registradas.")
        return

    # Ventas totales de todos los partidos
    totalGeneral = 0
    for partido, ventas_por_sector in club["ventasTotales"].items():
        totalPartido = sum(ventas_por_sector.values())
        totalGeneral += totalPartido

    print(f"\nVentas Totales de Todos los Partidos: ${totalGeneral}")

    # Detalle de ventas por partido y por sector
    print("\n--- Detalle de Ventas por Partido ---")
    for fecha, rival in club["historialPartidos"].items():
        if fecha in club["ventasTotales"]:
            ventasPartido = club["ventasTotales"][fecha]
            totalPartido = sum(ventasPartido.values())
            
            print(f"\nPartido: {fecha} contra {rival}")
            print(f"Ventas totales del partido: ${totalPartido}")
            
            for sector, ventas in ventasPartido.items():
                print(f"  Sector: {sector}, Ventas: ${ventas}")
        else:
            print(f"\nPartido: {fecha} contra {rival}")
            print(f"No hay ventas registradas para este partido.")

def gestionDePartidos(club):
    '''
    Función gestiona el menú de operaciones relacionadas con los partidos del club, permitiendo al usuario mostrar, agregar o eliminar partidos.

    Recibe:
    - club = Dict, el diccionario del club que contiene el historial de partidos.

    Devuelve:
    - No devuelve nada. La función se basa en un bucle que permite al usuario interactuar con el sistema de gestión de partidos.

    Funcionalidades:
    - Muestra el historial de partidos almacenados en el club cuando se selecciona la opción correspondiente.
    - Permite agregar nuevos partidos al club.
    - Permite eliminar partidos existentes del historial del club.
    - El usuario puede volver al menú principal seleccionando la opción "0".
    - Maneja la entrada de opciones inválidas con un mensaje de error y vuelve a solicitar una opción válida.

    Consideraciones:
    - La función utiliza un bucle `while` para mantener el menú activo hasta que el usuario seleccione la opción de salir ("0").
    - Se basa en otras funciones (`mostrarHistorial`, `agregarPartido`, `eliminarPartido`) para realizar las operaciones correspondientes.
    - Asegura una interacción fluida y valida las opciones seleccionadas por el usuario.
    '''
    while True:
        print("\n--- Gestión de Partidos ---")
        print("1. Mostrar historial de partidos")
        print("2. Agregar partido")
        print("3. Eliminar partido")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrarHistorial(club)

        elif opcion == "2":
            agregarPartido(club)

        elif opcion == "3":
            eliminarPartido(club)

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")

def agregarPartido(club):
    '''
    Esta función permite agregar un nuevo partido al historial del club, solicitando al usuario la fecha y el equipo rival.

    Recibe:
    - club = Dict, el diccionario del club que contiene el historial de partidos.

    Devuelve:
    - No devuelve nada. La función modifica el historial de partidos del club.

    Funcionalidades:
    - Solicita al usuario la fecha del partido en formato "dd/mm/yyyy" y el nombre del equipo rival.
    - Convierte la fecha ingresada a un objeto `datetime` para validar su formato.
    - Comprueba si ya existe un partido registrado en la misma fecha; si es así, notifica al usuario.
    - Si la fecha es válida y no existe un partido registrado, agrega el nuevo partido al historial del club.
    - Maneja errores de formato en la fecha, informando al usuario en caso de que se ingrese un formato inválido.

    Consideraciones:
    - Utiliza `strptime` de la biblioteca `datetime` para convertir la fecha de cadena a un objeto `datetime`.
    - Proporciona mensajes claros al usuario sobre el estado de la operación (ya existente, agregado o error de formato).
    '''
    fechaStr = input("Ingrese la fecha del partido (dd/mm/yyyy): ")
    rival = input("Ingrese el equipo rival: ")
    
    #Uso de try - except para validar el ingreso de la fecha.
    try:
        fecha = datetime.strptime(fechaStr, "%d/%m/%Y")
        if fecha.strftime("%d/%m/%Y") in club["historialPartidos"]:
            print("Ya existe un partido en esa fecha.")
        else:
            club["historialPartidos"][fecha.strftime("%d/%m/%Y")] = rival
            print(f"Partido agregado: {fecha.strftime('%d/%m/%Y')} contra {rival}.")
    except ValueError:
        print("Formato de fecha inválido. Intente nuevamente.")

def eliminarPartido(club):
    '''
    Función que nos permite eliminar un partido del historial del club, seleccionando el partido a eliminar.

    Recibe:
    - club = Dict, el diccionario del club que contiene el historial de partidos.

    Devuelve:
    - No devuelve nada. La función modifica el historial de partidos del club.

    Funcioness:
    - Muestra un mensaje indicando que se está eliminando un partido.
    - Utiliza la función `seleccionarPartido` para permitir al usuario elegir qué partido desea eliminar.
    - Si se selecciona un partido válido, lo elimina del historial de partidos del club y notifica al usuario.
    - En caso de que el partido no sea válido, muestra un mensaje correspondiente.

    Consideraciones:
    - Depende de la función `seleccionarPartido` para obtener la fecha del partido que se desea eliminar.
    - Proporciona un mensaje claro al usuario sobre el estado de la operación (eliminado o inválido).
    '''
    print("\n--- Eliminar Partido ---")
    partido = seleccionarPartido(club)
    if partido:
        del club["historialPartidos"][partido]
        print(f"Partido del {partido} eliminado.")
    else:
        print("Partido inválido.")

def validarEntero(mensaje,minimo=None,maximo=None):
    '''
    Función que valida que la entrada del usuario sea un número entero dentro de un rango específico.

    Recibe:
    - mensaje: str, el mensaje que se mostrará al usuario para solicitar la entrada.
    - minimo: int, valor mínimo permitido (opcional).
    - maximo: int, valor máximo permitido (opcional).

    Devuelve:
    - int, el valor entero ingresado por el usuario, validado dentro del rango especificado.

    Funcionalidades:
    - Muestra un mensaje al usuario solicitando la entrada.
    - Verifica que la entrada contenga solo dígitos y que se pueda convertir a un entero.
    - Comprueba si el valor está dentro de los límites especificados (mínimo y máximo, si se proporcionan).
    - Si la entrada es válida, la devuelve. Si no, muestra un mensaje de error y vuelve a solicitar la entrada.

    Consideraciones:
    - Utiliza el método `isdigit()` para asegurar que la entrada sea numérica.
    - Proporciona retroalimentación clara al usuario sobre la validez de su entrada y los requisitos del rango.
    '''
    while True:
        entrada = input(mensaje)
        if entrada.isdigit():  # Verifica que solo se ingresen dígitos
            valor = int(entrada)
            if (minimo is None or valor >= minimo) and (maximo is None or valor <= maximo):
                return valor
            else:
                print(f"Por favor, ingrese un valor entre {minimo} y {maximo}.")
        else:
            print("Por favor, ingrese un número válido.")


#----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
#----------------------------------------------------------------------------------------------
def main():
    #--------------------------------------------------
    # Inicialización de variables
    #--------------------------------------------------
    equiposArgentina = [
        "River Plate", "Boca Juniors", "Racing Club", "Independiente",
        "San Lorenzo", "Huracán", "Vélez Sarsfield", "Argentinos Juniors",
        "Estudiantes de La Plata", "Gimnasia y Esgrima La Plata", "Lanús",
        "Banfield", "Talleres", "Belgrano", "Godoy Cruz", "Colón",
        "Unión", "Newell's Old Boys", "Rosario Central", "Atlético Tucumán",
        "Central Córdoba", "Sarmiento", "Platense", "Barracas Central",
        "Instituto"
    ]

    #-------------------------------------------------
    # Bloque de menú
    #-------------------------------------------------
    club = None  # Inicializa club como None

    while True:
        opciones = 7
        while True:
            print("---------------------------------------")
            print("--------GESTION CLUB DEPORTIVO---------")
            print("---------------------------------------")
            print("\n--- Menú Principal ---")
            print("1. Iniciar Club Deportivo")
            print("2. Gestión de entradas")
            print("3. Gestión de socios")
            print("4. Gestion de partidos")
            print("5. Informe de ventas")
            print("-------------------")
            print("0. Salir del programa")
            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:  # Ajusta el rango de opciones
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0":  # Opción salir del programa
            print("FIN DEL PROGRAMA")
            exit()

        elif opcion == "1":   # Opción 1
            while True:
                nombreClub = input("Ingrese el nombre del club: ")
                if nombreClub in equiposArgentina:
                    equiposArgentina.remove(nombreClub)
                    break
                else:
                    print("No existe ese equipo en el sistema. Intente nuevamente.")

            capacidad = validarEntero("Ingrese la capacidad del estadio: ", 1)
            numSocios = validarEntero("Ingrese el número de socios iniciales: ", 0)
            numPartidos = validarEntero("Ingrese la cantidad de partidos del torneo: ", 1)

            club, capacidad, socios = iniciarClub(nombreClub, capacidad, numSocios)
            definirPrecios(club)
            generarPartidos(club, equiposArgentina,numPartidos)
            print(f"Nombre del club: {club['nombre']}")
            print(f"Capacidad del estadio: {capacidad}")
            print(f"Socios iniciales: {numSocios}")

        elif opcion == "2":   # Opción 2
            if club is not None:
                gestionDeEntradas(club)
            else:
                print("Primero debe iniciarl el club.")
        elif opcion == "3":   # Opción 3
            if club is not None:
                gestionDeSocios(club)
            else:
                print("Primero debe iniciar un club.")

        elif opcion == "4":   # Opción 4
            if club is not None:
                gestionDePartidos(club)
            else:
                print("Primero debe iniciar un club.")
        elif opcion == "5":   # Opción 5
            if club is not None:
                informeDeVentas(club)
            else:
                print("Primero debe iniciar un club.")
        

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")

# Punto de entrada al programa
if __name__ == "__main__":
    main()