import re
from datetime import datetime
import json
ahora = datetime.now()
pattern_email =r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
pattern_name = r"[A-Za-zÁÉÍÓÚÑáéíóúñ\s]{2,50}"
pattern_DNI = r"\d{7,8}"
pattern_event_name = r"[A-Za-zÁÉÍÓÚÑáéíóúñ\s]{3,70}"
pattern_event_location = r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s,]{7,70}$"

def pedir_nombre_evento():
        """
        Función para pedir nombre de Evento.
        Se usa en algunos menú.
        """
        while True:
                try:
                        nombre = input("Ingrese el nombre del evento: ").strip()
                        if not re.fullmatch(pattern_event_name, nombre):
                                raise ValueError("Nombre inválido. Debe tener entre 3 y 70 letras.")
                        return nombre
                except ValueError as e:
                        print(f"Error: {e}")

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

def guardar_usuarios_en_json(usuarios_dict : dict,ruta_archivo="usuarios.json"):
        """
        Función para guardar los datos de los usuarios registrados en un archivo JSON cuando terminan de registrarse.
        """
        with open(ruta_archivo,mode="w",encoding="utf-8") as archivo:
                json.dump(usuarios_dict,archivo,ensure_ascii=False,indent =4)