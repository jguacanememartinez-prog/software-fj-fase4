"""
registro.py
Configuración del archivo de logs donde se registran eventos y errores.
"""
import logging
import os

# Carpeta y archivo donde se guardará el log
CARPETA_LOGS = "logs"
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "software_fj.log")


def configurar_logger():
    """Crea (o reutiliza) el logger principal del sistema y lo devuelve."""
    # Creamos la carpeta de logs si no existe
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    # Obtenemos el logger con nombre propio
    logger = logging.getLogger("software_fj")
    # Evitamos duplicar manejadores si la función se llama más de una vez
    if logger.handlers:
        return logger
    # Registramos todos los niveles (DEBUG en adelante)
    logger.setLevel(logging.DEBUG)
    # Formato: fecha, nivel, módulo y mensaje
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(module)-10s | %(message)s"
    )
    # Manejador que escribe en el archivo (UTF-8 para tildes)
    manejador = logging.FileHandler(ARCHIVO_LOG, mode="w", encoding="utf-8")
    manejador.setFormatter(formato)
    logger.addHandler(manejador)
    return logger


# Logger compartido por todos los módulos
log = configurar_logger()
