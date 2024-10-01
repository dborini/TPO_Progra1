from datetime import datetime, timedelta

#----------------------------------------------------------------------------------------------
# FUNCIONES
#----------------------------------------------------------------------------------------------
def iniciarClub(nombre, cap, socios):
    filas = 10
    columnas = {
        "general": 20,
        "platea": 8,
        "palco": 2
    }
    club = {
        "nombre": nombre,
        "capacidad": cap,
        "sectores": {
            "general": {"capacidad": int(cap * 0.6), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["general"] for _ in range(filas)]},
            "platea": {"capacidad": int(cap * 0.3), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["platea"] for _ in range(filas)]},
            "palco": {"capacidad": int(cap * 0.1), "entradasVendidas": 0, "precio": 0, "asientos": [["O"] * columnas["palco"] for _ in range(filas)]},
        },
        "socios": {},  # Cambiado a diccionario
        "historialPartidos": {},  # Cambiado a diccionario
        "ventasTotales": {}  # Cambiado a diccionario
    }
    
    # Inicializa los socios en un diccionario
    for i in range(socios):
        club["socios"][f"Socio {i + 1}"] = True  # `True` indica que el socio está activo

    return club, cap, socios

def generarPartidos(club, equiposArgentina):
    if not equiposArgentina:
        print("No hay más equipos rivales disponibles.")
        return

    fechaInicial = datetime(datetime.now().year, 1, 1)
    for i in range(52):  # 52 semanas en un año
        fechaPartido = fechaInicial + timedelta(weeks=i)
        equipoRival = equiposArgentina[i % len(equiposArgentina)]
        club["historialPartidos"][fechaPartido.strftime("%d/%m/%Y")] = equipoRival  # Agregado como diccionario

    print("Partidos generados para todo el año.")

def mostrarHistorial(club):
    print("Historial de partidos:")
    for fecha, rival in club["historialPartidos"].items():
        print(f"Fecha: {fecha}, Rival: {rival}")

def definirPrecios(club):
    precioGeneral = int(input("Ingrese el precio de la entrada general: "))
    precioPlatea = int(input("Ingrese el precio de la platea: "))
    precioPalco = int(input("Ingrese el precio del palco: "))

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
                sector = input("Ingrese el sector (general, platea, palco): ")
                cantidad = int(input("Ingrese la cantidad de entradas a vender: "))
                ventaEntradas(sector, cantidad, club, partido)
            else:
                print("Partido inválido.")

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")

def seleccionarPartido(club):
    print("\n--- Seleccionar Partido ---")
    for i, (fecha, rival) in enumerate(club["historialPartidos"].items()):
        print(f"{i + 1}. Fecha: {fecha}, Rival: {rival}")
    partido_seleccionado = int(input("Seleccione el número del partido: ")) - 1
    fechas = list(club["historialPartidos"].keys())
    return fechas[partido_seleccionado] if 0 <= partido_seleccionado < len(fechas) else None

def ventaEntradas(sector, cantidad, club,partido):
    if sector in club["sectores"]:
        capacidad = club["sectores"][sector]["capacidad"]
        entradasVendidas = club["sectores"][sector]["entradasVendidas"]

        if entradasVendidas + cantidad <= capacidad:
            asientos = club["sectores"][sector]["asientos"]
            for _ in range(cantidad):
                for i in range(len(asientos)):
                    for j in range(len(asientos[i])):
                        if asientos[i][j] == "O":
                            asientos[i][j] = "X"
                            break
                    else:
                        continue
                    break

            club["sectores"][sector]["entradasVendidas"] += cantidad
            total = cantidad * club["sectores"][sector]["precio"]
            # Actualiza las ventas totales como un diccionario
            if sector not in club["ventasTotales"]:
                club["ventasTotales"][sector] = 0
            club["ventasTotales"][sector] += total
            
            print(f"Vendidas {cantidad} entradas para el partido del {partido} en {sector}. Total: ${total}")
            mostrarAsientos(sector, club)
        else:
            print("No hay suficientes asientos disponibles.")
    else:
        print("Sector inválido.")

def agregarSocio(club):
    nombre_socio = input("Ingrese el nombre del nuevo socio: ")
    club["socios"][nombre_socio] = True  # Agrega el socio al diccionario
    print(f"Socio {nombre_socio} agregado.")

def listarSocios(club):
    print("Lista de socios:")
    for socio in club["socios"]:
        print(f"- {socio}")

def borrarSocio(club):
    listarSocios(club)
    nombre_socio = input("Ingrese el nombre del socio a borrar: ")
    if nombre_socio in club["socios"]:
        del club["socios"][nombre_socio]  # Elimina el socio del diccionario
        print(f"Socio {nombre_socio} borrado.")
    else:
        print("Socio no encontrado.")

def modificarSocio(club):
    listarSocios(club)
    nombre_socio = input("Ingrese el nombre del socio a modificar: ")
    if nombre_socio in club["socios"]:
        nuevo_nombre = input("Ingrese el nuevo nombre del socio: ")
        club["socios"][nuevo_nombre] = club["socios"].pop(nombre_socio)  # Cambia el nombre del socio
        print(f"Socio {nombre_socio} modificado a {nuevo_nombre}.")
    else:
        print("Socio no encontrado.")
def gestionDeSocios(club):
    while True:
        print("\n--- Gestión de Socios ---")
        print("1. Agregar socio")
        print("2. Listar socios")
        print("3. Borrar socio")
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
        elif opcion == "0":
            break

        else:
            print("Opción inválida.")

def informeDeVentas(club):
    print("\n--- Informe de Ventas ---")
    if not club["ventasTotales"]:
        print("No hay ventas registradas.")
        return

    for sector, total in club["ventasTotales"].items():
        print(f"Sector: {sector}, Ventas Totales: ${total}")

def agregarPartido(club):
    fecha_str = input("Ingrese la fecha del partido (dd/mm/yyyy): ")
    rival = input("Ingrese el equipo rival: ")
    
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
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
            print("-------------------------")
            print("\n--- Menú Principal ---")
            print("1. Iniciar Club Deportivo")
            print("2. Gestión de entradas")
            print("3. Gestión de socios")
            print("4. Informe de ventas")
            print("5. Historial de partidos")
            print("6. Agregar partido")
            print("7. Eliminar Partido")
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

            capacidad = int(input("Ingrese la capacidad del estadio: "))
            numSocios = int(input("Ingrese el numero de socios iniciales: "))
            club, capacidad, socios = iniciarClub(nombreClub, capacidad, numSocios)
            definirPrecios(club)
            generarPartidos(club, equiposArgentina)
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
                informeDeVentas(club)
            else:
                print("Primero debe iniciar un club.")
        elif opcion == "5":   # Opción 5
            if club is not None:
                mostrarHistorial(club)
        elif opcion == "6":   # Opción 6
            if club is not None:
                agregarPartido(club)
            else:
                print("Primero debe iniciar un club.")
        elif opcion == "7":
            if club is not None:
                eliminarPartido(club)
            else:
                print("Primero debe iniciar un club.")

        input("\nPresione ENTER para volver al menú.")
        print("\n\n")

# Punto de entrada al programa
if __name__ == "__main__":
    main()


