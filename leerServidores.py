import yaml

def leer_nombres_servidores():
    with open('datos.yaml', 'r') as archivo:
        datos = yaml.safe_load(archivo)

        servidores = datos.get('servidores', [])
        print("Servidores:")
        for servidor in servidores:
            print(servidor.get('nombre'))

if __name__ == "__main__":
    leer_nombres_servidores()