import requests

#Pregunta 4 SDN - 20212591

#Aquí consideré ya la IP 
FLOODLIGHT_URL = "http://10.20.12.161:8080"

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

# Consulta de la ruta
def get_route(src_dpid, src_port, dst_dpid, dst_port):

    url = f"{FLOODLIGHT_URL}/wm/topology/route/{src_dpid}/{src_port}/{dst_dpid}/{dst_port}/json"
    response = requests.get(url)

    if response.status_code == 200:
        ruta = response.json()
        # DPID y puerto de cada paso
        return [(hop["switch"], hop["port"]["portNumber"]) for hop in ruta]
    return []

if __name__ == "__main__":
    #Prueba :D

    # MAC de origen
    mac_origen = "fa:16:3e:55:70:7a"
    dpid_src, port_src = get_attachment_points(mac_origen)
    print(f"Origen: Switch {dpid_src}, Puerto {port_src}")

    # MAC de destino
    mac_destino = "fa:16:3e:40:75:d4"
    dpid_dst, port_dst = get_attachment_points(mac_destino)
    print(f"Destino: Switch {dpid_dst}, Puerto {port_dst}")

    if dpid_src and dpid_dst:
        ruta = get_route(dpid_src, port_src, dpid_dst, port_dst)
        print("Ruta: ")
        for hop in ruta:
            print(f"  → Switch {hop[0]}, Puerto {hop[1]}")
    else:
        print("No se pudo obtener el punto de conexión de uno o ambos hosts.")