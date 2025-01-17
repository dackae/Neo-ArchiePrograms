import os
import shutil
from pathlib import Path

def listar_archivos(directorio):
    return os.listdir(directorio)

def copiar_archivo(origen, destino):
    shutil.copy2(origen, destino)

def mover_archivo(origen, destino):
    shutil.move(origen, destino)

def eliminar_archivo(ruta):
    if os.path.isfile(ruta):
        os.remove(ruta)
    elif os.path.isdir(ruta):
        shutil.rmtree(ruta)

def crear_directorio(ruta):
    os.makedirs(ruta, exist_ok=True)

def enviar_a_papelera(ruta):
    destino = os.path.expanduser("~/.local/share/Trash/files")
    shutil.move(ruta, destino)

def montar_unidad(dispositivo, punto_montaje):
    os.system(f"mount {dispositivo} {punto_montaje}")

def desmontar_unidad(punto_montaje):
    os.system(f"umount {punto_montaje}")
