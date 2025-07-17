from datetime import datetime
from .modelos.clases import *
import re
import random
from modelos.utils import *
from modelos.eventos import *

usuarios = dict()
dict_DNI = dict()
dict_email = dict()
Gestor = GestorEventos()




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
        usuario = Participante(name,edad,DNI,email, None,None)
        print(f"Usuario generado con exito! Su codigo de usuario es: {codigo} ")
        usuarios[codigo] = {"Usuario": usuario.to_dict(), "Contraseña":contraseña}
        dict_email[usuario.email] = usuario
        dict_DNI[usuario.DNI] = usuario
        guardar_usuarios_en_json(usuarios)
        return "Registro finalizado! Redirigiendo..."










