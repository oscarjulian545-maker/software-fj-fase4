"""Configuración del sistema de logging para registrar eventos y errores en archivo."""  # Documenta el módulo
import logging  # Importa el módulo estándar de registro de logs de Python
from pathlib import Path  # Importa Path para manejar rutas de archivos de forma segura


def configurar_logger(nombre_logger: str = "software_fj", archivo_log: str = "logs/sistema_software_fj.log") -> logging.Logger:
    """Configura y retorna un logger que escribe tanto en archivo como en consola."""  # Documenta la función
    ruta_log = Path(archivo_log)  # Convierte la ruta del log en un objeto Path
    ruta_log.parent.mkdir(parents=True, exist_ok=True)  # Crea la carpeta de logs si no existe

    logger = logging.getLogger(nombre_logger)  # Obtiene o crea la instancia del logger
    logger.setLevel(logging.INFO)  # Define el nivel mínimo de registro como INFO

    if not logger.handlers:  # Evita duplicar manejadores si la función se llama más de una vez
        formato = logging.Formatter(  # Define el formato legible de cada línea de log
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        manejador_archivo = logging.FileHandler(ruta_log, mode="a", encoding="utf-8")  # Crea manejador hacia archivo
        manejador_archivo.setLevel(logging.INFO)  # Registra INFO, WARNING, ERROR y CRITICAL en el archivo
        manejador_archivo.setFormatter(formato)  # Aplica el formato al archivo de logs

        manejador_consola = logging.StreamHandler()  # Crea manejador para mostrar salida en consola
        manejador_consola.setLevel(logging.INFO)  # Muestra eventos y errores en consola
        manejador_consola.setFormatter(formato)  # Aplica el formato a la consola

        logger.addHandler(manejador_archivo)  # Asocia el manejador de archivo al logger
        logger.addHandler(manejador_consola)  # Asocia el manejador de consola al logger

    return logger  # Retorna el logger configurado