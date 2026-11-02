#!/usr/bin/env python3

from scapy.all import sniff, IP, TCP
from collections import defaultdict
from datetime import datetime
from alert_logger import registrar_evento

conteo_conexiones = defaultdict(int)


def analizar_paquete(paquete):

    if paquete.haslayer(IP) and paquete.haslayer(TCP):

        ip_origen = paquete[IP].src
        puerto_destino = paquete[TCP].dport

        conteo_conexiones[ip_origen] += 1

        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"IP: {ip_origen} -> Puerto: {puerto_destino}"
        )

        # Detección simple de múltiples conexiones
        if conteo_conexiones[ip_origen] > 20:

            mensaje = (
                f"ALERTA: Posible actividad sospechosa "
                f"desde {ip_origen}. "
                f"Múltiples conexiones detectadas."
            )

            print("\n[!] " + mensaje)

            registrar_evento(mensaje, "WARNING")

            conteo_conexiones[ip_origen] = 0


def main():

    print("=" * 60)
    print("BLUE TEAM - SNIFFER DE DEFENSA")
    print("Monitoreando tráfico de red...")
    print("Presiona CTRL+C para detener.")
    print("=" * 60)

    registrar_evento("Sniffer de defensa iniciado.")

    sniff(
        filter="tcp",
        prn=analizar_paquete,
        store=False
    )


if __name__ == "__main__":
    main()
