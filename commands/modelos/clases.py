from datetime import datetime
from commands.auth import Gestor
import csv
import os
import re
class GestorEventos:
    def __init__(self):
        self.ID = "GeEv01"
        self._eventos = {}
        self._participantes = []
    def agregar_evento(self,evento : object ):
        if isinstance(evento, Evento):
            self._eventos[evento.name] = {"Evento": evento}
        if evento.nombre in self._eventos:
            print("Ya existe un evento con ese nombre.")
        else:
            raise TypeError("Agregue un Evento válido.")
    def eliminar_evento(self,evento :object):
        if isinstance(evento, Evento):
            self._eventos.remove(evento)
        else:
            raise TypeError("No se ha podido eliminar el Evento")
    def listado_de_eventos(self):
        return list(self._eventos.keys())
    def existe_evento(self,nombre):
        return nombre in self._eventos
    def filter_by_name(self,name: str):
        name = name.lower()
        encontrados = []
        for evento_info in self._eventos.values():
            evento = evento_info["Evento"]
            if name in evento.nombre.lower():
                encontrados.append(evento)
        if encontrados:
            for e in encontrados:
                print(e)
        else:
            print("No se encontraron eventos con ese nombre.")
    def filter_by_location(self,location : str):
        location = location.lower()
        encontrados = []
        for evento_info in self._eventos.values():
            evento = evento_info["Evento"]
            if location in evento.location.lower():
                encontrados.append(evento)
        if encontrados:
            for e in encontrados:
                print(e)
        else:
            print("No se han encontrado eventos en esta localización.")
    def filter_by_date(self,date : datetime):
        encontrados = []
        for evento_info in self._eventos.values():
            evento = evento_info["Evento"]
            if evento.date() >= date:
                encontrados.append(evento)
        if encontrados:
            for e in encontrados:
                print(e)
        else:
            print("No se han encontrado eventos luego de esa fecha.")
    def filter_by_participants(self,participants : int):
        encontrados = []
        for evento_info in self._eventos.values():
            evento = evento_info["Evento"]
            if evento.max_participants >= participants:
                encontrados.append(evento)
        if encontrados:
            for e in encontrados:
                print(e)
        else:
            print("No se han encontrado Eventos que tengan un aforo mayor al ingresado.")
class Evento:
    def __init__(self, nombre: str,location :str, date: datetime, max_participants : int, attendance : list):
        self.nombre = nombre
        self._location = location
        self._date = date
        self._attendance = []
        self.max_participants = max_participants
    def cambiar_nombre(self, nuevo_nombre : str):
        if isinstance(nuevo_nombre, str):
            self.nombre = nuevo_nombre
        else:
            raise ValueError("El nombre que ha introducido no es aceptable.")
    def cambiar_ubicacion(self, nueva_ubicacion):
        self._location = nueva_ubicacion
    def cambiar_fecha(self, nueva_fecha):
        if isinstance(nueva_fecha, datetime):
            self._date = nueva_fecha
        else:
            raise ValueError("Ha introducido una fecha invalida para el evento.")
    def agregar_participantes(self, participantes):
        if isinstance(participantes, object) or isinstance(participantes,list):
            self._attendance.append(participantes)
        else:
            raise ValueError("Error. Porfavor intente de nuevo.")
    def cambiar_aforo(self,nuevo_aforo):
        self.attendance = nuevo_aforo
    @property
    def attendance(self):
        return self._attendance
    @attendance.setter
    def attendance(self):
        if len(self.attendance) > self.max_participants:
            raise ValueError("Se ha superado la cantidad maxima de asistentes posibles a este evento.")
    def sort_by_name(self):
        try:
            print(sorted(self.attendance, key= lambda p:p.name))
        except Exception as e:
            raise ValueError("Error no identificado.")
    def sort_by_age(self):
        try:
            print(sorted(self.attendance,key=lambda p:p.age))
        except Exception as e:
            raise ValueError("Error no identificado.")
    def confirmed_attendance_list(self):
        print("Participantes que confirmaron asistencia:")
        for participante in self.attendance:
            if participante._attendance_confirmed.get(self, False):
                print(participante.name)
    def checking_attendance_list(self):
        print("Asistencia para el Evento:")
        for participante in self.attendance:
            confirmado = participante._attendance_confirmed.get(self, False)
            estado = "Sí" if confirmado else "No"
            print(f"Participante:{participante.name} -- Asistirá? {estado}")
    def not_confirmed_list(self):
        print("Participantes que NO confirmaron:")
        for participante in self.attendance:
            confirmado = participante._attendance_confirmed.get(self,False)
            if not confirmado:
                print(f"- {participante.nombre}")
    def generate_csv_report(self):
        file_name = re.sub(r'[^\w\s-]', '', self.name)
        file_name = file_name.replace(" ","_")
        file_name = f"modelos/reporte_{file_name}.csv"
        with open(file_name,mode="w",newline="",encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Nombre","Edad","DNI","Email","¿Asistirá?"])
            for p in self.attendance:
                writer.writerow([p.name,p.age,p.DNI,p.email, "Si" if p.attendance_confirmed else "No"])

class Participante:
    def __init__(self,name : str, age: int, DNI : str, email : str, attendance_confirmed : dict|None = None, events_attended : list|None = None):
        self.name = name
        self.age = age
        self._DNI = DNI
        self._email = email
        self._attendance_confirmed = attendance_confirmed if attendance_confirmed else {}
        self.events_attended = events_attended if events_attended else []
    @property
    def email(self):
        return self._email
    @property
    def DNI(self):
        return self._DNI
    def go_to_an_event(self, nombre_evento : str):
        if not Gestor.existe_evento(nombre_evento):
            return "El evento ingresado no existe."
        evento = Gestor._eventos[nombre_evento]["Evento"]
        if self in evento.attendance:
            return "Ya estás anotado en este evento."
        if len(evento.attendance) >= evento.max_participants:
            return "El evento ya alcanzó el máximo de participantes."
        evento._attendance.append(self)
        self.events_attended.append(evento)
        self._attendance_confirmed[evento] = False
        return f"Te has anotado al evento {evento.nombre}"
    def confirm_attendance(self, event_name : str):
        for evento in self.events_attended:
            if evento.nombre == event_name:
                self._attendance_confirmed[evento] = True
                print(f"Asistencia confirmada para el evento'{event_name}'. ")
                return
        print(f"No estás registrado en un evento llamado '{event_name}'.")
    def not_going_event(self, nombre_evento : str):
        if not Gestor.existe_evento(nombre_evento):
            return "El evento ingresado no existe."
        evento = Gestor._eventos[nombre_evento]["Evento"]
        if self not in evento.attendance:
            return "No estás anotado en este evento."
        self.events_attended.remove(evento)
        evento.attendance.remove(self)
        if evento in self._attendance_confirmed:
            del self._attendance_confirmed[evento]
        return f"Ya has sido desanotado del evento {evento.nombre}"
    def list_of_events(self):
        for evento in self.events_attended:
            print(evento.name)
    def conflicto_con_fechas(self, nuevo_evento : Evento):
        for evento in self.events_attended:
            if nuevo_evento._date == evento._date:
                return True
        return False
    def convertir_en_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "DNI": self.DNI,
            "email": self.email,
            "attendance_confirmed": self.attendance_confirmed,
            "events_attended": self.events_attended,
        }
    def mostrar_confirmaciones(self):
            for evento, confirmado in self._attendance_confirmed.items():
                estado = "Confirmado" if confirmado else "No confirmado"
                print(f"{evento.nombre} -> {estado}")
    def sort_events_alphabetical(self):
        if not self.events_attended:
            print("No estás anotado en ningún evento.")
            return
        eventos_ordenados = sorted(self.events_attended, key=lambda evento: evento.nombre.lower())
        for evento in eventos_ordenados:
            print(evento.nombre)
    def sort_events_by_date(self):
        if not self.events_attended:
            print("No estás anotado a ningún evento.")
            return
        eventos_ordenados = sorted(self.events_attended, key=lambda evento: evento._date)
        for evento in eventos_ordenados:
            print(f"{evento.nombre} - {evento._date.strftime('%Y-%m-%d')}")
    def sort_events_by_location(self):
        if not self.events_attended:
            print("No estás anotado a ningún evento.")
            return
        eventos_ordenados = sorted(self.events_attended, key= lambda evento: evento.location.lower())
        for evento in eventos_ordenados:
            print(f"{evento.nombre} - Ubicación: {evento.location}")
    def sort_events_by_max_participants(self):
        if not self.events_attended:
            print("No estás anotado a ningún evento.")
            return
        eventos_ordenados = sorted(self.events_attended, key= lambda evento: evento.max_participants)
        for evento in eventos_ordenados:
            print(f"{evento.nombre} - Aforo: {evento.max_participants}")


