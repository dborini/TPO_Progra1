"""
-----------------------------------------------------------------------------------------------
Título: 
    Gestión Club Deportivo Primera
Fecha: 
    14/10/2024 - 25/11/2024
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
import json
import re

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def iniciarClub(nombre, cap):
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
    try:
        filas = 10
        columnas = {
            "general": 20,
            "platea": 12,
            "palco": 5
        }
        
        # Verificar que la capacidad sea un número entero positivo
        if not isinstance(cap, int) or cap <= 0:
            raise ValueError("La capacidad del club debe ser un número entero positivo.")

        club = {
            "nombre": nombre,
            "capacidad": cap,
            "sectores": {
                "general": {"capacidad": int(cap * 0.6), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["general"] for _ in range(filas)]},
                "platea": {"capacidad": int(cap * 0.3), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["platea"] for _ in range(filas)]},
                "palco": {"capacidad": int(cap * 0.1), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["palco"] for _ in range(filas)]},
            },
            "historialPartidos": {},  
            "ventasTotales": {}  
        }

        return club, cap

    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def generarPartidos(club, equiposArgentina, numPartidos):
    '''
    Función encargada de generar un conjunto de partidos aleatorios para un club ingresado, asignando fechas
     y equipos contra los cuales jugará, dentro de un tiempo predefinido (año actual).
    Entre fecha y fecha, habrá por lo menos 7 días de diferencia entre sí.

    Recibe:
    -club = diccionario. Contiene el historial de partidos.
    -equiposArgentina = lista. Lista con los nombres de los equipos de Argentina disponibles.
    -numPartidos= int. Número de partidos que se deben generar.

    Devuelve:
    -Modifica el diccionario "club" agregando partidos a historialPartidos. Asigna fecha y 
    equipos rivales.

    A tener en cuenta:
    -Si no hay equipos disponibles en la lista "equiposArgentina", se imprime mensaje de error y la funcion
    termina.
    -Filtra fechas a ingresar para que estén separadas por 7 días.
    -No permite repetición de fechas a lo largo del año.
    '''
    try:
        if not equiposArgentina:
            raise ValueError("No hay más equipos rivales disponibles.")
        
        # Rango de fechas (desde el 1 de enero hasta el 31 de diciembre del año actual)
        fechaInicial = datetime(datetime.now().year, 1, 1)  # crea fecha inicial con el año actual y el mes 1 y día 1
        fechaFinal = datetime(datetime.now().year, 12, 31)  # crea fecha final con el año actual y el último día del año
        delta = fechaFinal - fechaInicial  # Diferencia entre las fechas en días

        # Conjunto para asegurar que no haya fechas repetidas
        fechasGeneradas = set()
        ultimaFecha = fechaInicial

        for i in range(numPartidos):
            # Asegurarse de que el siguiente partido sea al menos 7 días después del anterior
            while True:
                # Generar entre 7 y 14 días adicionales de diferencia entre partidos
                diasAleatorios = random.randint(7, 14)
                fechaPartido = ultimaFecha + timedelta(days=diasAleatorios)
                fechaStr = fechaPartido.strftime("%d/%m/%Y")  # Crea un formato string con formato de fecha

                # Asegurarse de que la fecha no exceda el rango del año y no se repita
                if fechaStr not in fechasGeneradas and fechaPartido <= fechaFinal:
                    fechasGeneradas.add(fechaStr)
                    ultimaFecha = fechaPartido  # Actualizar última fecha utilizada
                    break  # Salir del bucle al encontrar una fecha válida

            # Asignar un equipo rival aleatorio
            equipoRival = equiposArgentina[i % len(equiposArgentina)]
            club["historialPartidos"][fechaStr] = equipoRival  # Agregar partido al historial, como la fecha como key y el valor es el rival.

        print("Partidos generados.")

    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except KeyError as ke:
        print(f"Error de clave en el diccionario: {ke}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

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
    try:
        # Precios predefinidos
        precioGeneral = 500
        precioPlatea = 1000
        precioPalco = 1500

        # Verificación de la existencia de la estructura de sectores en el diccionario del club
        if "sectores" not in club:
            raise KeyError("La clave 'sectores' no se encuentra en el diccionario del club.")

        # Actualización de los precios para cada sector
        club["sectores"]["general"]["precio"] = precioGeneral
        club["sectores"]["platea"]["precio"] = precioPlatea
        club["sectores"]["palco"]["precio"] = precioPalco
        
        print("Precios actualizados.")

    except KeyError as ke:
        print(f"Error de clave: {ke}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def gestionDeEntradas(club):
    '''
    Función que gestiona el proceso de venta de entradas, como así la visualización de los asientos disponibles por sector del estadio.
    Presentará un menú con opciones varias para ver los asientos disponibles y vender entradas, permitiéndole al usuario seleccionar el partido,
    sector y cantidad de entradas a vender.

    Recibe:
    - club = Diccionario. El diccionario del club que contiene el historial de partidos.

    Devuelve:
    - No devuelve nada puntual, solamente ejecuta las acciones correspondientes a cada opción del menú.

    Funciones menú:
    - Opción 1: Ver los asientos disponibles para cada sector en específico (ingresado por teclado).
    - Opción 2: Vender entradas. Se le pide al usuario seleccionar un partido, sector y cantidad.
    - Opción 0: Volver al menú principal, terminando con la gestión de entradas.

    Considerar:
    - Valida que el sector seleccionado sea válido. Si lo es, continúa con el proceso de gestión.
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

        try:
            if opcion == "1":
                sector = input("Ingrese el sector (general, platea, palco): ")
                if sector in club["sectores"]:
                    mostrarAsientos(sector, club) # Descomentar si se necesita la visualización de asientos
                    print(f"Mostrando los asientos disponibles en el sector {sector}.")
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
                    
                    # Validar cantidad de entradas a vender
                    cantidad = validarEntero("Ingrese la cantidad de entradas a vender: ", 1)
                    ventaEntradas(sector, cantidad, club, partido)
                else:
                    print("No se seleccionó un partido válido.")

            elif opcion == "0":
                print("Volviendo al menú principal...")
                break

            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

def mostrarAsientos(sector, club):
    '''
    Función encargada de mostrar los asientos disponibles en un sector determinado del club.

    Recibe:
    - sector: string. El nombre del sector (general, platea, palco).
    - club: diccionario. Contiene la estructura del club y los asientos de cada sector.

    Devuelve:
    - asientos: lista. La lista de asientos del sector solicitado.
    '''
    try:
        # Verificar que el sector esté en los sectores del club
        if sector not in club["sectores"]:
            raise KeyError(f"El sector '{sector}' no existe en el club.")
        
        # Obtener la lista de asientos del sector
        asientos = club["sectores"][sector]["asientos"]
        
        # Imprimir los asientos disponibles
        print(f"\nAsientos disponibles en el sector {sector}:")
        for fila in asientos:
            print(" ".join(str(asiento) for asiento in fila))

        return asientos

    except KeyError as ke:
        print(f"Error de clave: {ke}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

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
    try:
        # Verificar si el sector existe en el club
        if sector in club["sectores"]:
            capacidad = club["sectores"][sector]["capacidad"]
            entradasVendidas = club["sectores"][sector]["entradasVendidas"]

            # Verificar que la cantidad de entradas sea válida
            if cantidad <= 0:
                print("La cantidad de entradas debe ser mayor a cero.")
                return

            # Verificar si hay suficientes asientos disponibles
            if entradasVendidas + cantidad <= capacidad:
                asientos = club["sectores"][sector]["asientos"]
                asignados = 0
                
                # Asignar los asientos a las entradas
                for i in range(len(asientos)):
                    for j in range(len(asientos[i])):
                        if asientos[i][j] == "O":  # Si el asiento está disponible
                            asientos[i][j] = "X"  # Marcar como ocupado
                            asignados += 1
                            if asignados == cantidad:
                                break
                    if asignados == cantidad:
                        break

                # Actualizar el número de entradas vendidas y ventas totales
                club["sectores"][sector]["entradasVendidas"] += cantidad
                total = cantidad * club["sectores"][sector]["precio"]

                if partido not in club["ventasTotales"]:
                    club["ventasTotales"][partido] = {}
                if sector not in club["ventasTotales"][partido]:
                    club["ventasTotales"][partido][sector] = 0
                club["ventasTotales"][partido][sector] += total

                print(f"Vendidas {cantidad} entradas para el partido del {partido} en {sector}. Total: ${total}")

            else:
                print("No hay suficientes asientos disponibles.")
        
        else:
            print("Sector inválido.")
    
    except KeyError as ke:
        print(f"Error de clave: {ke}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def seleccionarPartido(club):
    '''
    Función encargada de seleccionar un partido de la lista de partidos en relación al historial del club.
    Mostrará la lista numerada de partidos con sus respectivas fechas y rivales, solicitando la selección
    de alguno de ellos con el número correspondiente.

    Recibe:
    -club = diccionario. Contiene el historial de partidos.

    Devuelve:
    -fecha = string. Perteneciente al partido elegido.

    Si un usuario ingresa un número fuera del rango de opciones, se le pedirá que vuelva
    a seleccionar una opción, hasta ingresar finalmente un número valido.
    '''
    try:
        print("\n--- Seleccionar Partido ---")
        partidos = list(club["historialPartidos"].items())

        if not partidos:
            raise ValueError("No hay partidos disponibles en el historial.")

        for i, (fecha, rival) in enumerate(partidos):
            print(f"{i + 1}. Fecha: {fecha}, Rival: {rival}")

        while True:
            try:
                partidoSeleccionado = int(input("Seleccione el número del partido: "))
                if 1 <= partidoSeleccionado <= len(partidos):
                    return partidos[partidoSeleccionado - 1][0]  # Devuelve la fecha del partido correctamente
                else:
                    print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número entero.")

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def mostrarHistorial(club):
    '''
    Función encargada de imprimir el historial de los partidos del club, mostrar fechas y
    los equipos rivales.

    Recibe:
    - club = Diccionario. El diccionario del club que contiene el historial de partidos.

    Devuelve:
    - Imprime la información del historial de partidos.

    Si el historial está vacío, no mostrará nada.
    '''
    try:
        if club["historialPartidos"]:
            print("Historial de partidos:")
            for fecha, rival in club["historialPartidos"].items():
                print(f"Fecha: {fecha}, Rival: {rival}")
        else:
            print("No hay partidos registrados en el historial.")
    
    except KeyError:
        print("Error: El club no contiene un historial de partidos.")
    
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

def validarEdad(edad):
    """
    Función para verificar si la edad es un número válido y mayor que 0.
    """
    return validarEntero2(edad) and int(edad) > 0

def validarMail(email):
    """
    Función para verificar si un email tiene un formato válido.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def validarSexo(sexo):
    """
    Función para verificar si el sexo ingresado es válido ("masculino", "femenino").

    Recibe:
    - sexo: string. El sexo ingresado por el usuario.

    Devuelve:
    - True si el sexo es "masculino" o "femenino" (sin importar mayúsculas/minúsculas), de lo contrario False.
    """
    # Verificar si el valor ingresado es uno de los dos válidos
    if not sexo:  # Verifica si el campo está vacío
        print("El sexo no puede estar vacío.")
        return False
    
    return sexo.lower() in ['masculino', 'femenino']

def validarEntero2(val):
    """
    Función para verificar si un valor es un número entero válido.

    Recibe:
    - val: El valor que se quiere verificar si es un entero.

    Devuelve:
    - True si el valor puede ser convertido a un entero, de lo contrario False.
    """
    try:
        # Intentar convertir el valor a un entero
        int(val)
        return True
    except ValueError:
        # Si ocurre un error en la conversión, no es un entero válido
        return False
    except TypeError:
        # Si el tipo de val no es compatible, también retorna False
        return False

def agregarSocio(rutaSocios):
    """
    Función para agregar un nuevo socio al club. Solicita los datos del socio y lo guarda en el archivo JSON.

    Recibe:
    - rutaSocios: la ruta del archivo JSON donde se almacenan los socios.

    Devuelve:
    - None. La función actualiza el archivo JSON con los nuevos datos.
    """
    # Solicitar los datos del nuevo socio
    print("\n--- Agregar Nuevo Socio ---")
      # Validar el DNI
    while True:
        dni = input("Ingrese el DNI del socio: ").strip()
        if not validarEntero2(dni):
            print("¡Error! El DNI debe ser un número entero.")
            continue
        # Verificar si el DNI ya existe en el archivo
        socios = cargarSocios(rutaSocios)
        if dni in socios:
            print("¡Error! Ya existe un socio con ese DNI.")
            continue
        break
    
    # Validar el nombre
    while True:
        nombre = input("Ingrese el nombre del socio: ").strip()
        if not nombre:
            print("¡Error! El nombre no puede estar vacío.")
        else:
            break
    
    # Validar el email
    while True:
        email = input("Ingrese el email del socio: ").strip()
        if not validarMail(email):
            print("¡Error! El email ingresado no es válido.")
        else:
            break

    # Validar la edad
    while True:
        edad = input("Ingrese la edad del socio: ").strip()
        if not validarEdad(edad):
            print("¡Error! La edad debe ser un número entero mayor a 0.")
        else:
            break
    
    # Validar el sexo
    while True:
        sexo = input("Ingrese el sexo del socio (masculino, femenino): ").strip().lower()
        if not validarSexo(sexo):
            print("¡Error! El sexo debe ser 'masculino', 'femenino'.")
        else:
            break
    # Estado inicial del socio es "activo"
    estado = "activo"
    
    # Crear el nuevo socio
    nuevoSocio = {
        "nombre": nombre,
        "email": email,
        "edad": edad,
        "sexo": sexo,
        "estado": estado
    }
    
    # Agregar el nuevo socio al diccionario de socios
    socios[dni] = nuevoSocio
    
    # Guardar los cambios en el archivo JSON 
    try:
        f = open(rutaSocios, mode='w', encoding='utf-8')  # Abrir archivo en modo escritura
        json.dump(socios, f, indent=4, ensure_ascii=False)  # Escribir el diccionario actualizado
        f.close()  # Cerrar el archivo manualmente
        print(f"\nSocio con DNI {dni} agregado exitosamente.")
    except Exception as e:
        print(f"Error al guardar el socio: {e}")

def cargarSocios(rutaSocios):
    """
    Carga los socios desde el archivo JSON y los retorna.

    Recibe:
    - ruta = str, la ruta del archivo JSON que contiene la información de los socios.

    Devuelve:
    - dict, el diccionario de socios cargados desde el archivo JSON.
    """
    try:
        f = open(rutaSocios, mode='r', encoding='utf-8')  # Abrir el archivo en modo lectura
        socios = json.load(f)  # Cargar los datos JSON
        f.close()  # Cerrar el archivo manualmente
        
        return socios
    except FileNotFoundError:
        print(f"Error: El archivo {rutaSocios} no se encuentra.")
    except json.JSONDecodeError:
        print(f"Error: El archivo {rutaSocios} no tiene el formato correcto de JSON.")
    except Exception as e:
        print(f"Error inesperado al cargar los socios: {e}")
    return {}

def listarSocios(rutaSocios):
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
    try:
        socios = cargarSocios(rutaSocios)  # Cargar los socios desde el archivo JSON
    
        if not socios:  # Verificar si el archivo no se cargó correctamente
            print("No se pudieron cargar los socios.")
            return

        print(f"{'DNI':<12} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Sexo':<10} {'Estado':<10} {'Celular':<15}")
        print("-" * 90)
    
        for dni, datos in socios.items():
            try:
                # Verificar si el estado del socio es "activo"
                if datos["estado"] == "activo":
                    celular = datos.get('celular', 'No disponible')  # Obtener el celular si está disponible
                    print(f"{dni:<12} {datos['nombre']:<20} {datos['email']:<30} {datos['edad']:<5} {datos['sexo']:<10} {'Activo':<10} {celular:<15}")
            except KeyError as e:
                print(f"Faltan datos en el registro del socio con DNI {dni}: {e}")
    
    except FileNotFoundError as e:
        print("Error: No se encontró el archivo de socios:", e)
    except OSError as e:
        print("Error al intentar abrir el archivo:", e)
    except ValueError as e:
        print("Error al procesar el archivo de socios (posiblemente esté mal formado):", e)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

def borrarSocio(rutaSocios):
    """
    Función para eliminar un socio del club. Solicita el DNI del socio a eliminar y lo elimina del archivo JSON.
    """
    print("\n--- Borrar Socio ---")
    
    # Solicitar el DNI del socio a eliminar
    while True:
        dni = input("Ingrese el DNI del socio a eliminar: ").strip()
        
        # Validar que el DNI sea un número entero
        if not validarEntero2(dni):
            print("¡Error! El DNI debe ser un número entero.")
            continue
        
        # Cargar los socios desde el archivo
        socios = cargarSocios(rutaSocios)
        
        # Verificar si el socio con el DNI ingresado existe
        if dni not in socios:
            print(f"¡Error! No existe un socio con el DNI {dni}.")
            continue
        
        # Si existe, salir del bucle
        break
    
    # Eliminar el socio con el DNI ingresado
    try:
        del socios[dni]
        print(f"Socio con DNI {dni} eliminado exitosamente.")
        
        # Guardar los cambios en el archivo JSON
        f = open(rutaSocios, mode='w', encoding='utf-8')  # Abrir archivo en modo escritura
        json.dump(socios, f, indent=4, ensure_ascii=False)  # Guardar el diccionario actualizado
        f.close()  # Cerrar el archivo manualmente
    except Exception as e:
        print(f"Error al eliminar el socio: {e}")

def modificarSocio(rutaSocios):
    """
    Función para modificar los datos de un socio del club.
    Se puede modificar el nombre o el estado (activo/inactivo) del socio.
    """
    print("\n--- Modificar Socio ---")
    
    # Solicitar el DNI del socio a modificar
    while True:
        dni = input("Ingrese el DNI del socio a modificar: ").strip()
        
        # Validar que el DNI sea un número entero
        if not validarEntero2(dni):
            print("¡Error! El DNI debe ser un número entero.")
            continue
        
        # Cargar los socios desde el archivo
        socios = cargarSocios(rutaSocios)
        
        # Verificar si el socio con el DNI ingresado existe
        if dni not in socios:
            print(f"¡Error! No existe un socio con el DNI {dni}.")
            continue
        
        # Si existe, salir del bucle
        break
    
    # Mostrar los datos actuales del socio
    socio = socios[dni]
    print(f"\nDatos actuales del socio {dni}:")
    print(f"Nombre: {socio['nombre']}")
    print(f"Email: {socio['email']}")
    print(f"Edad: {socio['edad']}")
    print(f"Sexo: {socio['sexo']}")
    print(f"Estado: {socio['estado']}")
    print(f"Celular: {socio['celular']}")
    
    # Opción de modificar el nombre del socio
    nuevoNombre = input("\nIngrese el nuevo nombre (dejar vacío para no modificar): ").strip()
    if nuevoNombre:
        socio['nombre'] = nuevoNombre
    
    # Opción de modificar el estado del socio (activo o inactivo)
    while True:
        nuevoEstado = input("\nIngrese el nuevo estado (activo/inactivo): ").strip().lower()
        if nuevoEstado not in ['activo', 'inactivo']:
            print("¡Error! El estado debe ser 'activo' o 'inactivo'.")
        else:
            socio['estado'] = nuevoEstado
            break
    
    # Actualizar los datos en el archivo
    try:
        socios[dni] = socio  # Actualizar el socio en el diccionario
        
        # Guardar los cambios en el archivo JSON
        f = open(rutaSocios, mode='w', encoding='utf-8')  # Abrir archivo en modo escritura
        json.dump(socios, f, indent=4, ensure_ascii=False)  # Guardar el diccionario actualizado
        f.close()  # Cerrar el archivo manualmente
        
        print(f"Socio con DNI {dni} actualizado exitosamente.")
    except Exception as e:
        print(f"Error al modificar el socio: {e}")

def inactivarSocio(rutaSocios):
    """
    Función para inactivar a un socio del club.
    Cambia el estado de 'activo' a 'inactivo' de un socio existente.
    """
    print("\n--- Inactivar Socio ---")
    
    # Solicitar el DNI del socio a inactivar
    while True:
        dni = input("Ingrese el DNI del socio a inactivar: ").strip()
        
        # Validar que el DNI sea un número entero
        if not validarEntero2(dni):
            print("¡Error! El DNI debe ser un número entero.")
            continue
        
        # Cargar los socios desde el archivo
        socios = cargarSocios(rutaSocios)
        
        # Verificar si el socio con el DNI ingresado existe
        if dni not in socios:
            print(f"¡Error! No existe un socio con el DNI {dni}.")
            continue
        
        # Si existe, salir del bucle
        break
    
    # Verificar si el socio ya está inactivo
    socio = socios[dni]
    if socio['estado'] == 'inactivo':
        print(f"El socio con DNI {dni} ya está inactivo.")
    else:
        # Cambiar el estado a inactivo
        socio['estado'] = 'inactivo'
        try:
            socios[dni] = socio  # Actualizar el socio en el diccionario
            
            # Guardar los cambios en el archivo
            f = open(rutaSocios, mode='w', encoding='utf-8')  # Abrir archivo en modo escritura
            json.dump(socios, f, indent=4, ensure_ascii=False)  # Guardar el diccionario actualizado
            f.close()  # Cerrar el archivo manualmente
            
            print(f"Socio con DNI {dni} inactivado exitosamente.")
        except Exception as e:
            print(f"Error al inactivar el socio: {e}")

def listarSociosInactivos(rutaSocios):
    """
    Función que lista todos los socios inactivos del club.
    Filtra los socios cuyo estado es 'inactivo' y los muestra en consola.
    """
    try:
        print("\n--- Listar Socios Inactivos ---")
        
        # Cargar los socios desde el archivo JSON
        socios = cargarSocios(rutaSocios)
        
        # Verificar si no hay socios cargados
        if not socios:
            print("No hay socios registrados o no se pudo cargar el archivo.")
            return

        # Mostrar encabezado de la tabla
        print(f"{'DNI':<12} {'Nombre':<20} {'Email':<30} {'Edad':<5} {'Sexo':<10} {'Estado':<10} {'Celular':<15}")
        print("-" * 90)
        
        encontrado = False  # Variable para verificar si se encuentran socios inactivos
        
        for dni, datos in socios.items():
            try:
                # Filtrar y mostrar solo los socios inactivos
                if datos.get("estado") == "inactivo":
                    celular = datos.get('celular', 'No disponible')  # Obtener el celular si está disponible
                    print(f"{dni:<12} {datos['nombre']:<20} {datos['email']:<30} {datos['edad']:<5} {datos['sexo']:<10} {'Inactivo':<10} {celular:<15}")
                    encontrado = True
            except KeyError as e:
                print(f"Faltan datos en el registro del socio con DNI {dni}: {e}")
        
        if not encontrado:
            print("No hay socios inactivos en el sistema.")
    
    except FileNotFoundError as e:
        print("Error: No se encontró el archivo de socios:", e)
    except OSError as e:
        print("Error al intentar abrir el archivo:", e)
    except ValueError as e:
        print("Error al procesar el archivo de socios (posiblemente esté mal formado):", e)
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

def gestionDeSocios(rutaSocios):
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
            agregarSocio(rutaSocios)
            
        elif opcion == "2":
            listarSocios(rutaSocios)

        elif opcion == "3":
            borrarSocio(rutaSocios)
            
        elif opcion == "4":
            modificarSocio(rutaSocios)
            
        elif opcion == "5":
            inactivarSocio(rutaSocios)
            
        elif opcion == "6":
            listarSociosInactivos(rutaSocios)
            
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
    try:
        print("\n--- Informe de Ventas ---")
        
        # Verificar si hay ventas registradas
        if not club.get("ventasTotales"):
            print("No hay ventas registradas.")
            return

        # Ventas totales de todos los partidos
        totalGeneral = 0
        for partido, ventas_por_sector in club["ventasTotales"].items():
            try:
                totalPartido = sum(ventas_por_sector.values())
                totalGeneral += totalPartido
            except (TypeError, AttributeError) as e:
                print(f"Error al calcular las ventas del partido {partido}: {e}")
                continue

        print(f"\nVentas Totales de Todos los Partidos: ${totalGeneral}")

        # Detalle de ventas por partido y por sector
        print("\n--- Detalle de Ventas por Partido ---")
        for fecha, rival in club.get("historialPartidos", {}).items():
            try:
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
            except KeyError as e:
                print(f"Error en los datos del partido {fecha} contra {rival}: {e}")
            except TypeError as e:
                print(f"Error al procesar las ventas del partido {fecha} contra {rival}: {e}")
    
    except KeyError as e:
        print(f"Error en la estructura del diccionario del club: clave faltante {e}")
    except TypeError as e:
        print(f"Error: El parámetro 'club' no tiene el formato esperado: {e}")
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

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
from datetime import datetime

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
    - Valida que el equipo rival no sea el mismo que el club local.
    '''
    fechaStr = input("Ingrese la fecha del partido (dd/mm/yyyy): ")
    rival = input("Ingrese el equipo rival: ")

    # Validar el ingreso de la fecha
    try:
        fecha = datetime.strptime(fechaStr, "%d/%m/%Y")

        # Verificar si el equipo rival es el mismo que el club local
        nombreClub = club.get("nombre", "Tu club")  # Asumimos que el nombre del club está en club["nombre"]
        if rival.strip().lower() == nombreClub.strip().lower():
            print("No puedes agregar un partido contra tu propio equipo.")
            return

        # Verificar si ya existe un partido en esa fecha
        if fecha.strftime("%d/%m/%Y") in club["historialPartidos"]:
            print("Ya existe un partido en esa fecha.")
        else:
            # Agregar el nuevo partido al historial
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

    Funciones:
    - Muestra un mensaje indicando que se está eliminando un partido.
    - Utiliza la función `seleccionarPartido` para permitir al usuario elegir qué partido desea eliminar.
    - Si se selecciona un partido válido, lo elimina del historial de partidos del club y notifica al usuario.
    - En caso de que el partido no sea válido, muestra un mensaje correspondiente.

    Consideraciones:
    - Depende de la función `seleccionarPartido` para obtener la fecha del partido que se desea eliminar.
    - Proporciona un mensaje claro al usuario sobre el estado de la operación (eliminado o inválido).
    '''
    try:
        print("\n--- Eliminar Partido ---")
        
        # Seleccionar partido
        partido = seleccionarPartido(club)
        if not partido:
            print("No se seleccionó un partido válido.")
            return
        
        # Intentar eliminar el partido del historial
        try:
            del club["historialPartidos"][partido]
            print(f"Partido del {partido} eliminado.")
        except KeyError:
            print(f"Error: El partido seleccionado ({partido}) no existe en el historial.")
    
    except KeyError as e:
        print(f"Error: Clave faltante en el diccionario del club: {e}")
    except TypeError as e:
        print(f"Error: Parámetro 'club' con formato incorrecto: {e}")
    except Exception as e:
        print("Ocurrió un error inesperado:", e)

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

    # Archivo JSON de la entidad socios
    # Clave principal: DNI del socio
    rutaSocios = r"C:\Users\danie\OneDrive\Documentos\Licenciatura\1- Algoritmos y Estructuras de Datos1\2C-2024\TPO-Grupal\ClubRepo\TPO_Progra1\EntregaFinal\socios.json"

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
            numPartidos = validarEntero("Ingrese la cantidad de partidos del torneo: ", 1)

            club, capacidad = iniciarClub(nombreClub, capacidad)
            definirPrecios(club)
            generarPartidos(club, equiposArgentina,numPartidos)
            print(f"Nombre del club: {club['nombre']}")
            print(f"Capacidad del estadio: {capacidad}")
            

        elif opcion == "2":   # Opción 2
            if club is not None:
                gestionDeEntradas(club)
            else:
                print("Primero debe iniciar el club.")
        elif opcion == "3":   # Opción 3
            if club is not None:
                gestionDeSocios(rutaSocios)
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