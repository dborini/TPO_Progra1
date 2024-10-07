from datetime import datetime, timedelta
import random
#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def iniciarClub(nombre, cap, socios):
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
    precioGeneral = 500
    precioPlatea = 1000
    precioPalco = 1500

    club["sectores"]["general"]["precio"] = precioGeneral
    club["sectores"]["platea"]["precio"] = precioPlatea
    club["sectores"]["palco"]["precio"] = precioPalco
    print("Precios actualizados.")

def mostrarAsientos(sector, club):
    asientos = club["sectores"][sector]["asientos"]
    print(f"\nAsientos disponibles en el sector {sector}:")
    for fila in asientos:
        print(" ".join(fila))
    
    return asientos

def seleccionarPartido(club):
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
            mostrarAsientos(sector, club)
        else:
            print("No hay suficientes asientos disponibles.")
    else:
        print("Sector inválido.")
def mostrarHistorial(club):
    print("Historial de partidos:")
    for fecha, rival in club["historialPartidos"].items():
        print(f"Fecha: {fecha}, Rival: {rival}")




def gestionDeEntradas(club):
    while True:  
        print("\n--- Gestión de Entradas ---")
        print("1. Ver asientos disponibles")
        print("2. Vender entradas")
        print("0. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sector = input("Ingrese el sector (general, platea, palco): ")
            if sector in club["sectores"]:
                mostrarAsientos(sector, club)
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
    nombreSocio = input("Ingrese el nombre del nuevo socio: ")
    club["socios"][nombreSocio] = True  # Agrega el socio al diccionario
    print(f"Socio {nombreSocio} agregado.")

def listarSocios(club):
    print("Lista de socios activos:")
    
    # Itera sobre los socios en el diccionario
    for nombre, datos in club["socios"].items():
        # Verifica si el estado del socio es True
        if datos["estado"] == True:
            print(f"- {nombre}")
    
    return club

def borrarSocio(club):
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a borrar: ")
    if nombreSocio in club["socios"]:
        del club["socios"][nombreSocio]  # Elimina el socio del diccionario
        print(f"Socio {nombreSocio} borrado.")
    else:
        print("Socio no encontrado.")

def modificarSocio(club):
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a modificar: ")
    if nombreSocio in club["socios"]:
        nuevoNombre = input("Ingrese el nuevo nombre del socio: ")
        club["socios"][nuevoNombre] = club["socios"].pop(nombreSocio)  # Cambia el nombre del socio
        print(f"Socio {nombreSocio} modificado a {nuevoNombre}.")
    else:
        print("Socio no encontrado.")
def inactivarSocio(club):
    listarSocios(club)
    nombreSocio = input("Ingrese el nombre del socio a inactivar: ")
    if nombreSocio in club["socios"]:
        club["socios"][nombreSocio]["estado"] = False
        print(f"El socio {nombreSocio} ha sido inactivado.")
    else:
        print("Socio no encontrado.")
def listarSociosInactivos(club):
    print("Lista de socios inactivos:")
    
    # Itera sobre los socios en el diccionario
    for nombre, datos in club["socios"].items():
        # Verifica si el estado del socio es False
        if datos["estado"] == False:
            print(f"- {nombre}")
    
    return club

def gestionDeSocios(club):
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
    fechaStr = input("Ingrese la fecha del partido (dd/mm/yyyy): ")
    rival = input("Ingrese el equipo rival: ")
    
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
    print("\n--- Eliminar Partido ---")
    partido = seleccionarPartido(club)
    if partido:
        del club["historialPartidos"][partido]
        print(f"Partido del {partido} eliminado.")
    else:
        print("Partido inválido.")

def validarEntero(mensaje,minimo=None,maximo=None):
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
    #-------------------------------------------------
    # Inicialización de variables
    #----------------------------------------------------------------------------------------------
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
    #----------------------------------------------------------------------------------------------
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