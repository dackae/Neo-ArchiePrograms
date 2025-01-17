import os
from datetime import datetime

def obtener_info_archivo(ruta):
    stat = os.stat(ruta)
    return {
        "nombre": os.path.basename(ruta),
        "tamaño": stat.st_size,
        "modificado": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        "permisos": oct(stat.st_mode)[-3:]
    }

def ordenar_archivos(archivos, criterio='nombre'):
    if criterio == 'nombre':
        return sorted(archivos)
    elif criterio == 'tamaño':
        return sorted(archivos, key=lambda x: os.path.getsize(x))
    elif criterio == 'fecha':
        return sorted(archivos, key=lambda x: os.path.getmtime(x))