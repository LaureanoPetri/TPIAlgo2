import json
import os

def guardarPartida(datos, nombrePartida, carpeta="partidasGuardadas"):
    # 1. Crear carpeta si no existe
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # 2. Nombre del archivo nuevo
    archivo = f"{nombrePartida}.json"
    ruta = os.path.join(carpeta, archivo)

    # 3. Guardar el diccionario como JSON
    with open(ruta, "w") as f:
        json.dump(datos, f, indent=4)

    print(f"Partida guardada en {ruta}")

def abrirArchivo(nombrePartida, carpeta="partidasGuardadas"):
    archivo = f"{nombrePartida}.json"
    ruta = os.path.join(carpeta, archivo)
    
    if os.path.exists(ruta):
        with open(ruta, "r") as f:
            datos = json.load(f)   # ✅ ahora sí le pasamos el archivo abierto
        return datos
    else:
        print("No existe el archivo", nombrePartida)

import os

def listarPartidas(carpeta="partidasGuardadas"):
    # Si la carpeta no existe, devolvemos lista vacía
    if not os.path.exists(carpeta):
        print("⚠️ No existe la carpeta de partidas")
        return []

    # Filtramos solo los archivos que terminen en .json
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".json")]

    # Sacamos la extensión .json y devolvemos solo el nombre
    partidas = [os.path.splitext(f)[0] for f in archivos]
    return partidas

# Ejemplo de uso
datos = {
    "jugador": "Laureano",
    "puntaje": 999,
    "vehiculos": 10
}
guardarPartida(datos, "partidaMati")
partidas=listarPartidas()
cont=0
for i in partidas:
    cont+=1
    print("partida: ", i)
nombre = input("elije la partida: ")

print(abrirArchivo(partidas[nombre]))
