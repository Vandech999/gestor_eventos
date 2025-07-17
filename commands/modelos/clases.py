from datetime import datetime
class GestorEventos:
    def __init__(self):
        self.ID = "GeEv01"
        self._eventos = []
        self._participantes = []
    def agregar_evento(self,evento : object ):
        if isinstance(evento, Evento):
            self._eventos.append(evento)
        else:
            raise TypeError("Agregue un Evento válido.")
    def eliminar_evento(self,evento :object):
        if isinstance(evento, Evento):
            self._eventos.remove(evento)
        else:
            raise TypeError("No se ha podido eliminar el Evento")
    def listado_de_eventos(self):
        for evento in self._eventos:
            print(evento)
        pass

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
    def go_to_an_event(self, evento : Evento):
        if self in evento.attendance:
            return "Ya estás anotado en este evento."
        if len(evento.attendance) >= evento.max_participants:
            return "El evento ya alcanzó el máximo de participantes."
        evento._attendance.append(self)
        self.events_attended.append(evento)
        self._attendance_confirmed[evento] = False
        return f"Te has anotado al evento: {evento.nombre}"
    def confirm_attendance(self, evento: Evento):
        if evento in self.events_attended:
            self._attendance_confirmed[evento] = True
        else:
            raise ValueError("No estás registrado en este evento.")
    def not_going_event(self, event : Evento):
        if self in event.attendance:
            event._attendance.remove(self)
        else:
            raise ValueError("No está registrado para este evento.")
    def list_of_events(self):
        for evento in self.events_attended:
            print(evento.name)
    def conflicto_con_fechas(self, nuevo_evento : Evento):
        for evento in self.events_attended:
            if nuevo_evento._date == evento._date:
                return True
        return False
    def mostrar_confirmaciones(self):
            for evento, confirmado in self._attendance_confirmed.items():
                estado = "Confirmado" if confirmado else "No confirmado"
                print(f"{evento.nombre} -> {estado}")
