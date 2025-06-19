import requests
import yaml

FLOODLIGHT_URL = "http://10.20.12.161:8080"

class Alumno:
    def __init__(self, nombre, codigo, mac):
        self.nombre = nombre
        self.codigo = codigo
        self.mac = mac

class Curso:
    def __init__(self, codigo, nombre, estado, alumnos=None, servidores=None):
        self.codigo = codigo
        self.nombre = nombre
        self.estado = estado
        self.alumnos = alumnos if alumnos else []
        self.servidores = servidores if servidores else []

    def agregar_alumno(self, alumno):
        self.alumnos.append(alumno)

    def remover_alumno(self, alumno):
        if alumno in self.alumnos:
            self.alumnos.remove(alumno)

    def agregar_servidor(self, servidor):
        self.servidores.append(servidor)

class Servidor:
    def __init__(self, nombre, ip, servicios=None):
        self.nombre = nombre
        self.ip = ip
        self.servicios = servicios if servicios else []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

class Servicio:
    def __init__(self, nombre, protocolo, puerto):
        self.nombre = nombre
        self.protocolo = protocolo
        self.puerto = puerto

def crear_conexion():
    cod_alumno = input("Código del alumno: ")
    nombre_servicio = input("Servicio (ej: ssh): ").lower()
    nombre_servidor = input("Servidor (ej: Servidor 1): ")

    alumno = next((a for a in alumnos if a.codigo == cod_alumno), None)
    servidor = next((s for s in servidores if s.nombre == nombre_servidor), None)

    if not alumno or not servidor:
        print("Alumno o servidor no encontrado.")
        return

    autorizado = False
    for curso in cursos:
        if curso.estado == "DICTANDO" and cod_alumno in curso.alumnos:
            for srv in curso.servidores:
                if srv["nombre"] == nombre_servidor and nombre_servicio in srv["servicios_permitidos"]:
                    autorizado = True

    if not autorizado:
        print("Alumno NO autorizado para acceder al servicio.")
        return

    # Buscar servicio en objeto servidor
    servicio_obj = next((x for x in servidor.servicios if x.nombre == nombre_servicio), None)

    if servicio_obj:
        mac_src = alumno.mac
        ip_dst = servidor.ip
        protocolo = servicio_obj.protocolo
        puerto = servicio_obj.puerto
        success = insertar_flows(mac_src, ip_dst, protocolo, puerto)
        print("Conexión creada." if success else "Error al insertar flow.")
    else:
        print("Servicio no encontrado.")

#Punto de conexión de un host
def get_attachment_points(mac_address):
    url = f"{FLOODLIGHT_URL}/wm/device/"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for host in data:
            if mac_address.lower() in [m.lower() for m in host.get("mac", [])]:
                aps = host.get("attachmentPoint", [])
                if aps:
                    punto = aps[0]
                    return punto["switchDPID"], punto["port"]
                else:
                    print(f"La MAC {mac_address} no tiene attachmentPoint.")
        print(f"La MAC {mac_address} no fue encontrada.")
    else:
        print(f"[{response.status_code}]")
        print(f"Respuesta: {response.text}")
    
    return None, None

def listar_alumnos():
    for a in alumnos:
        print(f"{a.codigo} - {a.nombre} - {a.mac}")


def listar_cursos():
    for c in cursos:
        print(f"{c.codigo} - {c.nombre} [{c.estado}]")

def listar_servidores():
    for s in servidores:
        print(f"{s.nombre} - {s.ip}")
        for srv in s.servicios:
            print(f"   > {srv.nombre} [{srv.protocolo}:{srv.puerto}]")

def importar_datos(ruta_archivo):
    with open(ruta_archivo, 'r') as file:
        data = yaml.safe_load(file)

    alumnos = [Alumno(**a) for a in data.get('alumnos', [])]

    cursos = []
    for c in data.get('cursos', []):
        cursos.append(Curso(
            nombre=c['nombre'],
            estado=c['estado'],
            alumnos=c['alumnos'],
            servidores=c['servidores'],
            codigo=c['codigo']
        ))

    servidores = []
    for s in data.get('servidores', []):
        servicios = [Servicio(**serv) for serv in s['servicios']]
        servidores.append(Servidor(s['nombre'], s['ip'], servicios))

    return alumnos, cursos, servidores

def leer_nombres_servidores():
    with open('datos.yaml', 'r') as archivo:
        datos = yaml.safe_load(archivo)

        servidores = datos.get('servidores', [])
        print("Servidores:")
        for servidor in servidores:
            print(servidor.get('nombre'))

def insertar_flows(mac_src, ip_dst, protocolo, puerto):
    dpid, port = get_attachment_points(mac_src)
    if not dpid:
        print("No se pudo determinar el punto de conexión.")
        return False

    flow = {
        "switch": dpid,
        "name": f"flow_{mac_src}_{ip_dst}_{puerto}",
        "priority": "32768",
        "eth_type": "0x0800",
        "ipv4_dst": ip_dst,
        "eth_src": mac_src,
        "ip_proto": "0x06" if protocolo.lower() == "tcp" else "0x11",
        "tp_dst": str(puerto),
        "active": "true",
        "actions": f"output={port}"  
    }
    response = requests.post(f"{FLOODLIGHT_URL}/wm/staticflowpusher/json", json=flow)
    return response.status_code == 200



def get_route(src_dpid, src_port, dst_dpid, dst_port):

    url = f"{FLOODLIGHT_URL}/wm/topology/route/{src_dpid}/{src_port}/{dst_dpid}/{dst_port}/json"
    response = requests.get(url)

    if response.status_code == 200:
        ruta = response.json()
        
        return [(hop["switch"], hop["port"]["portNumber"]) for hop in ruta]
    return []




def menu():
    while True:
        print("####################################################")
        print("Network Policy manager de la UPSM")
        print("####################################################")
        print("\n--- MENÚ ---")
        print("1. Importar ")
        print("2. Exportar")
        print("3. Cursos")
        print("4. Alumnos")
        print("5. Servidores")
        print("6. Políticas")
        print("7. Conexiones")
        print("0. Salir")
        opc = input("Seleccione: ")

        if opc == "1":
            ruta = input("Ruta del archivo YAML: ")
            global alumnos, cursos, servidores
            alumnos, cursos, servidores = importar_datos(ruta)
        elif opc == "3":
            listar_cursos()
        elif opc == "4":
            listar_alumnos()
        elif opc == "5":
            listar_servidores()
        elif opc == "7":
            crear_conexion()
        elif opc == "0":
            break

if __name__ == "__main__":
    menu()