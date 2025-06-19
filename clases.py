
class Alumno:
    def __init__(self, nombre, mac):
        self.nombre = nombre
        self.mac = mac

class Curso:
    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado
        self.alumnos = []
        self.servidores = []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def remover_alumno(self, alumno):
        if alumno in self.alumnos:
            self.alumnos.remove(alumno)

    def agregar_servidor(self, servidor):
        self.servidores.append(servidor)

class Servidor:
    def __init__(self, nombre, ip):
        self.nombre = nombre
        self.ip = ip
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

def main():
    # Objetos de cada clase :D
    alumno = Alumno("Juan Pérez", "AA:BB:CC:DD:EE:FF")
    servicio = Servicio("HTTP", "TCP", 80)
    servidor = Servidor("Servidor1", "192.168.1.10")
    curso = Curso("SDN", "Activo")

    # Métodos D:
    servidor.agregar_servicio(servicio)
    curso.agregar_alumno(alumno)
    curso.agregar_servidor(servidor)
    curso.remover_alumno(alumno)  

if __name__ == "__main__":
    main()
