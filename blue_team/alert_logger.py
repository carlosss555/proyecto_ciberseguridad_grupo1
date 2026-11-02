#!/usr/bin/env python3

import logging
import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "blue_team_alerts.log")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def registrar_evento(mensaje, nivel="INFO"):

    nivel = nivel.upper()

    if nivel == "WARNING":
        logging.warning(mensaje)

    elif nivel == "ERROR":
        logging.error(mensaje)

    else:
        logging.info(mensaje)


def main():

    registrar_evento("Sistema de registro del Blue Team iniciado.")
    registrar_evento("Auditoría automática ejecutada.")
    registrar_evento(
        "Evento de prueba: actividad sospechosa detectada.",
        "WARNING"
    )

    print("Eventos registrados correctamente.")
    print(f"Archivo de log: {LOG_FILE}")


if __name__ == "__main__":
    main()
