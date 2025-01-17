import os
import psutil

def obtener_espacio_disco(ruta):
    usage = psutil.disk_usage(ruta)
    return {
        "total": usage.total,
        "usado": usage.used,
        "libre": usage.free,
        "porcentaje": usage.percent
    }

def listar_unidades_montadas():
    return psutil.disk_partitions()

def es_root():
    return os.geteuid() == 0