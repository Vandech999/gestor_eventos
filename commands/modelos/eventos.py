from datetime import datetime
from modelos.utils import *
from modelos.clases import *
from commands.auth import Gestor
from Gestor_de_Eventos.menu import menu_loggeado, menu_gestor_de_eventos

ahora = datetime.now()
def agregar_fecha_evento():
        """
        Agregar fecha para Evento.
        Se usa dentro del menú de Gestión de Eventos, en el submenú de agregar evento.
        Se pide ingresar una fecha para el evento en formato %Y-%m-%d. Se verifica que no ingrese una fecha que ya pasó
        y luego también se verifica que ingrese la fecha en el formato requerido. Se agrega un except extra para capturar 
        posibles errores que no estén incluidos.
        """
        while True:
                try:
                        event_date = datetime.strptime(input("Ingrese la fecha del evento (YYYY-MM-DD): "), "%Y-%m-%d")
                        if event_date < ahora:
                                print("Error:La fecha ingresada ya pasó")
                                continue
                        return event_date
                except ValueError:
                        print("Formato invalido. Porfavor intente de nuevo.")
                        continue
                except Exception as e:
                        print("Ha ocurrido un error inesperado. Lo sentimos")
                        continue
def agregar_evento():
        """
        Agregar evento.
        Se le solicita al Gestor ingresar nombre para el Evento, con verificación de que no ingrese un nombre de menos de 3 letras.
        Se pide ingresar una localización para el Evento, verificando que sea de un minimo de 7 letras y un máximo de 70.
        Se usa agregar_fecha_evento() para conseguir una fecha para el evento.
        Se pide ingresar la capacidad para el evento, verificando que no se ingrese algo vacio o que no sea numero.
        Luego se verifica que no haya ingresado un numero menor o igual a 0.
        Finalmente se crea un objeto de clase Evento con los datos ingresados, y se usa el objeto Gestor (creado previamente)
        para agregar el evento a la lista de eventos que es parte del objeto.
        """
        event_name = input("Ingrese el nombre que le quiere dar al Evento: ")
        while not re.fullmatch(pattern_event_name,event_name):
                event_name = input("Nombre de Evento no valido. El nombre del evento debe tener minimo 3 letras y maximo 70.")
        event_location = input("Ingrese una localización para el Evento: ")
        while not re.fullmatch(pattern_event_location,event_location):
                event_location = input("Ubicación invalida. La localización puede tener minimo 7 letras y maximo 70")
        date_event = agregar_fecha_evento()
        while True:
                event_participants = input("Ingrese la capacidad maxima para el Evento: ")
                if event_participants == "":
                        event_participants= input("Ingrese una capacidad para el Evento: ")
                if not event_participants.isdigit():
                        event_participants = input("Ingrese un numero valido para el aforo del Evento: ")
                        continue
                aforo = int(event_participants)
                if aforo <= 0:
                        event_participants = input("Tiene que ingresar una cantidad mayor a 0: ")
                        continue
                break
        evento_completo = Evento(event_name,event_location,date_event,aforo,[])
        Gestor.agregar_evento(evento_completo)
        print("Evento agregado con exito!")

def eliminar_evento():
        """
        Eliminar evento.
        Se le solicita al Gestor ingresar el Evento que quiera eliminar, y si existe, se lo elimina de la lista de Eventos. Si el Evento que ingresa no existe
        se le pide que ingrese uno valido
        """
        while True:
                event_name = input("Introduzca el nombre del Evento a eliminar: ").strip()
                if Gestor.existe_evento(event_name):
                        confirmacion= input(f"Está seguro de eliminar el Evento {event_name}? (si/no)").strip().lower()
                        if confirmacion == "si":
                                Gestor.eliminar_evento(event_name)
                                print(f"Se ha eliminado el Evento {event_name}.")
                                break
                        elif confirmacion == "no":
                                print("Operación cancelada.")
                                break
                        else:
                                print("Respuesta invalida. Por favor escriba si o no")
                else:
                        print("Ese evento no existe. Intente nuevamente.")
def proximos_eventos():
        eventos = Gestor.listado_de_eventos()
        if eventos:
                for nombre in eventos:
                        print(f"Evento disponible: {nombre}")
        else:
                print("No hay ningún evento confirmado para el futuro cercano.")
                

def filtrar_eventos():
        eventos = Gestor.listado_de_eventos()
        while True:
            print("\t Filtrar Eventos")
            print("Filtrar por:")
            print("1.Nombre")
            print("2.Fecha")
            print("3.Ubicación")
            print("4.Aforo")
            print("5.Volver al Menú de Usuarios.")
            op = input("Elija la opción que desea: ")
            if op == "":
                op = input("Elija una opción (1-5): ")
                continue
            if not op.isdigit():
                op = input("Debe ingresar un numero: ")
                continue
            opcion = int(op)
            if opcion not in range(1,6):                       
                print("Opción invalida: Debe ser un número del 1 al 5.")
                continue
            break
        if opcion == 1:
                try:
                        nombre = input("Ingrese el nombre del evento: ")
                        if not nombre.strip():
                                raise ValueError("El nombre no puede estar vacío.")
                except ValueError as e:
                        print("Error:", e)
                Gestor.filterby_name(nombre)
        if opcion == 2:
                fecha_valida = agregar_fecha_evento()
                Gestor.filter_by_date(fecha_valida)
        if opcion == 3:
                while True:
                        try:
                                location = input("Ingrese la ubicación del evento (7 a 70 letras, espacios o comas): ")
                                if not re.fullmatch(pattern_event_location, location):
                                        raise ValueError("Ubicación inválida. Intente nuevamente.")
                                break
                        except ValueError as e:
                                print("Error:", e)
                Gestor.filter_by_location(location)
        if opcion == 4:
                while True:
                        try:
                                numero = int(input("Ingrese el número de aforo: "))
                                if numero <= 0:
                                        raise ValueError("El número debe ser mayor a 0.")
                                break  # Sale del bucle si está todo bien
                        except ValueError as e:
                                print("Error:", e)
                Gestor.filterby_participants(numero)
        if opcion == 5:
            menu_loggeado()
            

def modificar_evento():
        """
        Modificar eventos.
        Se pide que se ingrese el nombre del Evento a modificar, verificando que no se ingrese nada.
        Si se ingresa un nombre valido, se accede a un submenu de opciones donde se puede elegir que
        se desea modificar del Evento.
        """
        event_name = input("Introduzca el nombre del Evento a modificar: ").strip()
        while event_name == "":
                event_name = input("Ingrese el nombre de un Evento: ").strip()
        if Gestor.existe_evento(event_name):
                evento = Gestor._eventos[event_name]["Evento"]
                while True:
                        print("\t ¿Que desea Modificar?")
                        print("1. Nombre")
                        print("2. Fecha")
                        print("3. Ubicación")
                        print("4. Aforo máximo")
                        print("5. Salir del menú")
                        opciones = menu_opciones()
                        if opciones == 1:
                                try:
                                        while True:
                                                nuevo_nombre = input("Ingrese el nuevo nombre que le quiere dar al Evento: ")
                                                if nuevo_nombre == "":
                                                        nuevo_nombre = input("Ingrese el nuevo nombre que le quiere dar al Evento: ")
                                                else:
                                                        break
                                except Exception as e:
                                        raise KeyError("Error desconocido. Lo sentimos")
                                evento.cambiar_nombre(nuevo_nombre)
                                Gestor._eventos[nuevo_nombre] = Gestor._eventos.pop(event_name)
                                event_name = nuevo_nombre
                        elif opciones == 2:
                                fecha_nueva = agregar_fecha_evento()
                                evento.cambiar_fecha(fecha_nueva)
                        elif opciones == 3:
                                try:
                                        while True:
                                                nueva_ubicacion = input("Ingrese la nueva ubicación que quiere darle al Evento: ")
                                                if nueva_ubicacion == "":
                                                        nueva_ubicacion = input("Ingrese la nueva ubicación que quiere darle al Evento: ")
                                                        continue
                                                evento.cambiar_ubicacion(nueva_ubicacion)
                                except Exception as e:
                                        raise KeyError("Error desconocido. Lo sentimos")
                        elif opciones == 4:
                                try:
                                        while True:
                                                nuevo_aforo = input("Ingrese el nuevo aforo que quiere darle al Evento: ")
                                                if nuevo_aforo == "":
                                                        nuevo_aforo = input("Ingrese la nueva ubicación que quiere darle al Evento: ")
                                                        continue
                                                if nuevo_aforo < 0:
                                                        nuevo_aforo = input("No puede asignar un aforo menor a 0. Ingrese un aforo valido: ")
                                                        continue
                                except Exception as e:
                                        raise KeyError("Error desconocido. Lo sentimos")
                        elif opciones == 5:
                                menu_gestor_de_eventos()


def ordenar_eventos(usuario : Participante):
    while True:
        print("\tOrdenar Eventos")
        print("Ordenar por:")
        print("1.Orden Alfabetico")
        print("2.Fecha")
        print("3.Ubicación")
        print("4.Aforo")
        print("5.Salir")
        op = input("Elija la opción que desea: ")
        if op == "":
                op = input("Elija una opción (1-5): ")
                continue
        if not op.isdigit():
                op = input("Debe ingresar un numero: ")
                continue
        opcion = int(op)
        if opcion not in range(1,6):                       
                print("Opción invalida: Debe ser un número del 1 al 5.")
                continue
        break
        if opcion == 1:
        usuario.sort_events_alphabetical()
    if opcion == 2:
        usuario.sort_events_by_date()
    if opcion == 3:
        usuario.sort_events_by_location()
    if opcion == 4:
        usuario.sort_events_by_max_participants()
    if opcion == 5:
        return



def administrar_eventos():
        nombre_evento = pedir_nombre_evento
        evento = Gestor._eventos[nombre_evento]["Evento"]
        while True:
                print(f"\tAdministrar Evento {nombre_evento}")
                print("1.Registro Asistencia")