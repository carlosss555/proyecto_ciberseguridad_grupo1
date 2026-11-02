#!/usr/bin/env python3

import os
import platform
import subprocess
from datetime import datetime


def ejecutar(comando):
    try:
        resultado = subprocess.run(
            comando,
            shell=True,
            capture_output=True,
            text=True
        )
        return resultado.stdout
    except Exception as error:
        return f"Error: {error}"


def main():

    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("=" * 60)
    print("BLUE TEAM - AUDITORÍA DEL SISTEMA")
    print("=" * 60)
    print(f"Fecha: {fecha}\n")

    print("[+] SISTEMA OPERATIVO")
    print(ejecutar("cat /etc/os-release"))

    print("[+] INFORMACIÓN DEL KERNEL")
    print(platform.platform())

    print("\n[+] HOSTNAME")
    print(platform.node())

    print("\n[+] USUARIOS DEL SISTEMA")
    print(ejecutar("cut -d: -f1 /etc/passwd"))

    print("\n[+] SERVICIOS ACTIVOS")
    print(ejecutar("systemctl list-units --type=service --state=running --no-pager"))

    print("\n[+] PUERTOS ABIERTOS")
    print(ejecutar("ss -tulpn"))

    print("\n[+] ESPACIO EN DISCO")
    print(ejecutar("df -h"))

    print("\n" + "=" * 60)
    print("AUDITORÍA FINALIZADA")
    print("=" * 60)


if __name__ == "__main__":
    main()
