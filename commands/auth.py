from datetime import datetime
from .modelos.clases import *
import re
import random

pattern_email =r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
pattern_name = r"[A-Za-zÁÉÍÓÚÑáéíóúñ\s]{2,50}"
pattern_DNI = r"\d{7,8}"
pattern_event_name = r"[A-Za-zÁÉÍÓÚÑáéíóúñ\s]{3,70}"
pattern_event_location = r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s,]{7,70}$"

ahora = datetime.now()
usuarios = dict()
dict_DNI = dict()
dict_email = dict()
Gestor = GestorEventos()

def proximos_eventos():
        eventos = Gestor.listado_de_eventos()
        if eventos:
                for nombre in eventos:
                        print(f"Evento disponible: {nombre}")
        else:
                print("No hay ningún evento confirmado para el futuro cercano.")
def pedir_email():
        """
        Función para pedir e-mail.
        Se usa a la hora de registrarse. Se valida a través de RegEx que el usuario ingrese un e-mail correcto.
        """
        while True:
                email = input("Ingrese su dirección de correo: ")
                if re.fullmatch(pattern_email,email):
                        break
                else:
                        print("Ha ingresado un correo invalido. Porfavor intentelo de nuevo.")
        return email
def pedir_DNI():
        """
        Función para pedir un DNI.
        Se usa a la hora de registrarse. Se valida mediante RegEx que ingrese el documento en el formato que pide el programa (solo números).
        """
        while True:
                DNI = input("Ingrese su numero de DNI (sin puntos o guiones separatorios): ")
                if re.fullmatch(pattern_DNI, DNI):
                        break
                else:
                        print("Ha ingresado el DNI de manera incorrecta. Porfavor intentelo de nuevo. ")
        return DNI
def pedir_edad():
        """
        Función para pedir la edad.
        Se usa a la hora de registrarse. Se le pide al usuario ingresar su fecha de nacimiento en formato
        YYYY-MM-DD asi se puede trabajar con datetime. Hay validación para que en caso de que la ingrese en un formato incorrecto,
        pueda seguir hasta ingresarla en el formato solicitado.
        Luego se usa datetime.now() para restarse con la fecha de nacimiento del usuario. Esta diferencia se divide en 365 para dar los años,
        y en caso de que el usuario sea menor de 18 años, el programa levanta un error para evitar que continue con el registro.
        """
        while True:
                try:
                        fecha_nacimiento = datetime.strptime(input("Ingrese su fecha de nacimiento (YYYY-MM-DD): "), "%Y-%m-%d")
                        break
                except ValueError:
                        print("Formato invalido. Porfavor intente de nuevo.")
                except Exception as e:
                        raise KeyError("Error no identificado.Lo sentimos mucho")
        diferencia = ahora - fecha_nacimiento
        edad = diferencia.days // 365
        if edad < 18:
                raise ValueError("Error: Tenés que ser mayor de 18 años para poder registrarte.")
        return edad

def auth_registrarse():
        """
        Función para registrarse.
        Se le pide al usuario que ingrese su nombre, y se valida con RegEx que no ingrese un nombre que tenga menos de 2 letras,
        ni tampoco uno de más de 50. Luego se llama a las funciones de pedir edad, y también a la función para pedir DNI.
        Con esta última, se hace una verificación dentro de un diccionario con los números de DNI de todos los usuarios para
        verificar que no esté ingresando un DNI que ya está en la base de datos. Lo mismo se hace con la función pedir email 
        a continuación.
        Finalmente, se le pide una contraseña al usuario, y se verifica que no ingrese vacio.
        Se le crea al usuario un codigo único de 7 digitos para el inicio de sesión, que contiene una verificación
        para evitar que haya un código de usuario duplicado.
        Para finalizar, usando la clase Participante se crea un objeto que contenga los datos del usuario,
        y este objeto se almacena en un diccionario usando como clave el codigo proporcionado anteriormente,
        y como valor se almacena el objeto Usuario y su contraseña.
        Adicionalmente, se almacenan su e-mail y DNI en un diccionario aparte como claves para facilitar la verificación
        de que  no haya un DNI o e-mail duplicado.
        """
        name = input("Ingrese su nombre: ")
        while not re.fullmatch(pattern_name,name):
            name = input("Error: Ha ingresado un nombre invalido. Porfavor ingrese un nombre con más de 2 letras y menos de 50: ")
        edad = pedir_edad()
        DNI = pedir_DNI()
        if DNI in dict_DNI:
                print("Ya existe un usuario con ese DNI.")
                return
        email = pedir_email()
        if email in dict_email:
                print("Error:Este e-mail ya está asignado a otra cuenta.")
                return
        while True:
                contraseña = input("Ingrese una contraseña: ")
                if contraseña == "":
                        print("Porfavor ingrese una contraseña.")
                else:
                        break
        while True:
                codigo = "".join(random.choices("0123456789", k=7))
                if codigo not in usuarios:
                        break
        Usuario = Participante(name,edad,DNI,email, None,None)
        print(f"Usuario generado con exito! Su codigo de usuario es: {codigo} ")
        usuarios[codigo] = {"Usuario": Usuario, "Contraseña":contraseña}
        dict_email[Usuario.email] = Usuario
        dict_DNI[Usuario.DNI] = Usuario
        return "Registro finalizado! Redirigiendo..."


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
                                print("Error:No puede agregar un evento que tenga una fecha pasada")
                        break
                except ValueError:
                        print("Formato invalido. Porfavor intente de nuevo.")
                        continue
                except Exception as e:
                        print("Ha ocurrido un error inesperado. Lo sentimos")
                        continue
        return event_date


def menu_opciones():
        """
        Menú opciones.
        Se hizo debido a que hay varios menús dentro del programa donde el usuario puede ingresar
        opciones del 1 al 5.
        return : opcion - Se le envia al menú desde donde se llama a esta función para que use el número de opción ingresado.
        """
        while True:
                op = input("Elija lo que desea modificar: ")
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
                return opcion

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








