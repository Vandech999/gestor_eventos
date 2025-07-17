from commands.auth import auth_registrarse
from commands.auth import *
from commands.modelos.eventos import *
import random
import re

def menu_loggeado(codigo_usuario):
    """
    Menú al que accede el usuario una vez que pasó el inicio de sesión.
    Puede interactuar con todos los eventos disponibles, en los que está anotado y en los que no.
    Puede filtrar y ordenar eventos según ciertos criterios.
    Puede anotarse, desanotarse y confirmar asistencia a eventos.
    """
    while True:
        usuario = usuarios[codigo_usuario]["Usuario"]
        eventos = usuario.events_attended
        print(f"\tMenú de {usuario.name}")
        print("\tOpciones")
        print("1.Lista de Eventos")
        print("2.Lista de Eventos a los que asistiré")
        print("3.Filtrar Eventos")
        print("4.Ordenar Eventos")
        print("5.Asistir a Evento")
        print("6.Confirmar asistencia a Evento")
        print("7.Desanotarme de Evento")
        print("8.Salir")
        while True:
            op = input("Elija una opción: ")
            if op == "":
                op = input("Elija una opción (1-8): ")
                continue
            if not op.isdigit():
                op = input("Debe ingresar un numero: ")
                continue
            opcion = int(op)
            if opcion not in range(1,9):                       
                print("Opción invalida: Debe ser un número del 1 al 8.")
                continue
            break
        if opcion == 1:
            proximos_eventos()
        elif opcion == 2:
            usuario.mostrar_confirmaciones()
        elif opcion == 3:
            filtrar_eventos()
        elif opcion == 4:
            ordenar_eventos(usuario)
        elif opcion == 5:
            nombre = pedir_nombre_evento()
            usuario.go_to_an_event(nombre)
        elif opcion == 6:
            nombre_evento = pedir_nombre_evento()
            usuario.confirm_attendance(nombre_evento)
        elif opcion == 7:
            nombre = pedir_nombre_evento()
            usuario.not_going_event(nombre)
        elif opcion == 8:
            return





def menu_gestor_de_eventos():
    """
    Menú de Gestor de Eventos.
    Permite agregar,modificar,eliminar  eventos, 
    y también se puede ver una lista de los eventos que ya estén creados.
    """
    while True:
        print("\tMenú de Gestión de Eventos")
        print("\tOpciones")
        print("1.Agregar Evento")
        print("2.Modificar Evento")
        print("3.Eliminar Evento")
        print("4.Lista de Eventos")
        print("5.Administrar Evento")
        print("6.Salir")
        opcion = menu_opciones()
        if opcion == 1:
                agregar_evento()
        elif opcion == 2:
                modificar_evento()
        elif opcion == 3:
            eliminar_evento()
        elif opcion == 4:
            Gestor.listado_de_eventos()
        elif opcion == 5:
            administrar_eventos()
        elif opcion == 6:
            print("Volviendo al menú principal...")
            menu_principal()

def premenu_gestor_eventos():
    """
    Pre-menú para acceder al Gestor de Eventos.
    Se pide un código/contraseña que quien quiera acceder al gestor ya debe saber de antemano,
    Tiene 3 intentos para ingresarlo correctamente. En caso de fallar, el programa va a levantar un error 
    para evitar que se siga intentando acceder a este menú libremente.
    Si el codigo es ingresado exitosamente, se procede al menú para administar los eventos.
    """
    intentos = 0
    max_intentos = 3
    codigo = "GeEvo01"
    con = True
    while intentos < max_intentos:
        op = input("Ingrese código para poder ingresar al Gestor de Eventos: ")
        if op == "":
            print("No puede ingresar un valor vacío.")
            continue
        if op == codigo:
            menu_gestor_de_eventos()
            return
        else:
            intentos += 1
            print(f"Código incorrecto. Intento {intentos} de {max_intentos}")
    print("Ha superado la cantidad de intentos permitidos. Cerrando el programa....")
    raise ValueError("Acceso denegado")




def iniciar_sesion():
    """
    Menú para iniciar sesión.
    Se le pide al usuario que ingrese el código único que se le da a la hora de registrarse,
    y luego tiene 3 intentos para ingresar su contraseña. En caso de fallar, se le devuelve al menú de usuarios,
    si se procede con el inicio de sesión, se lo envía a la interfaz de usuarios.
    """
    intentos_codigo = 0
    intentos_max = 3
    while intentos_codigo < intentos_max:
        checkear_codigo = input("Ingrese su código de Usuario: ")
        if checkear_codigo not in usuarios:
            intentos_codigo += 1
            print(f"Código inválido. Intento {intentos_codigo} de {intentos_max}")
            continue
        intentos_contraseña = 0
        while intentos_contraseña < intentos_max:
            contraseña = input("Ingrese su contraseña: ")
            if contraseña == usuarios[checkear_codigo]["Contraseña"]:
                print(f"¡Bienvenido {usuarios[checkear_codigo]['Usuario'].name}!")
                menu_loggeado(checkear_codigo)
                return checkear_codigo
            else:
                intentos_contraseña += 1
                print(f"Contraseña incorrecta. Intento {intentos_contraseña} de {intentos_max}")
        print("Ha superado el número máximo de intentos de contraseña. Volviendo al menú de usuarios.")
        return  
    print("Ha superado el número máximo de intentos de código. Saliendo...")
    return 


def registrarse():
    """
    Menú de registro.
    Primero se le pregunta al usuario si quiere regresar al menú de usuarios en caso de que se haya equivocado a la hora de acceder
    y ya tenga una cuenta. Si no, se procede a auth_registrarse() donde se procede con el registro de la cuenta.
    """
    while True:
        op = input("Desea volver al menu de usuario? si/no: ").strip().lower()
        if op == "":
            print("Error: No se puede ingresar un valor vacio")
            continue
        if op == "si":
            menu_usuario()
            break
        if op  == "no":
            auth_registrarse()
            break
        else:
            op = input("Ingrese una opción valida (Si/No): ")


def menu_usuario():
    """
    Menú para los usuarios.
    Se les permite ingresar a su cuenta o Registrarse.
    """
    con = True
    while con == True:
        print("\t Menú de Usuarios")
        print("\tQue desea hacer?")
        print("1.Ingresar a mi cuenta")
        print("2.Registrarme")
        print("3.Volver al menú principal")
        op = input("Seleccione una opción: ")
        if op == "": 
            print("Tiene que ingresar un valor.")
            continue
        if not op.isdigit():
            print("Tiene que ingresar un numero.")
            continue
        opcion = int(op)
        if opcion == 1:
            iniciar_sesion()
        elif opcion == 2:
            registrarse()
        elif opcion == 3:
            menu_principal()
    pass

def menu_principal():
    """
    Menú principal:
    Interfaz a la que accede el usuario cuando ejecute el programa.
    Permite navegar al resto de menus. 
    Se vuelve a él cuando el usuario quiera salir de algún otro menú.
    """
    con = True
    while con == True:
        print("\t Menu Principal")
        print("\t Opciones:")
        print("1.Acceder al Gestor de Eventos")
        print("2. Ingresar/Registrarse")
        print("3. Cerrar programa")
        
        op = input("Elija a que menú desea ir: ")
        if op == "":
                print("Tiene que ingresar un valor.")
                continue
        if not op.isdigit():
                print("Tiene que ingresar un numero.")
                continue
        opcion = int(op)
        if opcion == 1:
            premenu_gestor_eventos()
        elif opcion == 2:
            menu_usuario()
        elif opcion == 3:
            con = False
            break
        
        else:
            print("Opcion incorrecta: Elija una opción valida.")

menu_principal()