from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR, ARP, sr1, send
from datetime import datetime


def analizar_paquete(paquete):
    """Revisa un paquete capturado e imprime sus datos más relevantes."""

    print("\n-----------------------------")
    print("Paquete Identificado")

    if IP in paquete:
        origen = paquete[IP].src
        destino = paquete[IP].dst

        print("IP de origen:", origen)
        print("IP de destino:", destino)

        # Caso TCP: nos interesa el puerto y las banderas (flags)
        if TCP in paquete:
            puerto = paquete[TCP].dport
            flags = paquete[TCP].flags

            print("Protocolo: TCP")
            print("Puerto destino:", puerto)
            print("Flags:", flags)

            # Una bandera SYN sola suele indicar intento de nueva conexión
            if flags == "S":
                print("ALERTA: Se detecto un paquete SYN")

        elif UDP in paquete:
            print("Protocolo: UDP")
            print("Puerto destino:", paquete[UDP].dport)

        # Si hay una consulta DNS, extraemos qué dominio se está resolviendo
        if DNS in paquete and paquete[DNS].qd:
            nombre = paquete[DNSQR].qname.decode(
                errors="ignore"
            )
            print("Consulta DNS:", nombre)

        # Puerto 80 sin cifrado, vale la pena marcarlo aparte
        if TCP in paquete and paquete[TCP].dport == 80:
            print(" Trafico HTTP sin cifrar detectado")

    elif ARP in paquete:
        print("Protocolo: ARP")
        print("IP de origen:", paquete[ARP].psrc)
        print("IP de destino:", paquete[ARP].pdst)

    # Dejamos un resumen de cada paquete como respaldo en disco
    with open("evidencia_trafico.txt", "a", encoding="utf-8") as archivo:
        archivo.write(str(paquete.summary()) + "\n")


def capturar_trafico():
    """Escucha la red por una cantidad de paquetes definida por el usuario."""

    cantidad = int(input("Cantidad de paquetes a capturar: "))

    print("\nIniciando captura de trafico...")
    print("Presione Ctrl + C para detener la captura.\n")

    try:
        paquetes = sniff(
            count=cantidad,
            prn=analizar_paquete,
            store=True
        )

        paquetes_path = "captura_trafico.pcap"

        # wrpcap guarda la captura en formato .pcap, para abrirla luego en Wireshark si hace falta
        from scapy.all import wrpcap
        wrpcap(paquetes_path, paquetes)

        print("\nCaptura finalizada.")
        print("Evidencia guardada en:", paquetes_path)

    except Exception as error:
        print("Error durante la captura:", error)


def generar_syn():
    """Arma y envía un único paquete SYN hacia el objetivo indicado."""

    ip_destino = input("Ingrese la IP de la VM Blue Team: ")
    puerto = int(input("Ingrese el puerto de prueba: "))

    print("\nEnviando paquete SYN de prueba...")

    try:
        # Armamos el paquete a mano: capa IP + capa TCP con la bandera SYN activa
        paquete = IP(dst=ip_destino) / TCP(
            dport=puerto,
            flags="S"
        )

        # sr1 manda el paquete y se queda esperando una sola respuesta
        respuesta = sr1(paquete, timeout=3, verbose=False)

        if respuesta:
            print("Respuesta recibida:")
            respuesta.show()
        else:
            print("No se recibio respuesta.")

    except Exception as error:
        print("Error al enviar el paquete:", error)


def menu():
    """Menu principal para elegir qué acción ejecutar."""

    while True:

        print("\n")
        print("     Análisis de Trafico")
        print("1. Capturar trafico de red")
        print("2. Generar paquete SYN de prueba")
        print("3. Salir")

        opcion = input("\nSeleccione una opcion: ")

        if opcion == "1":
            capturar_trafico()

        elif opcion == "2":
            generar_syn()

        elif opcion == "3":
            print("Finalizando programa...")
            break

        else:
            print("Opcion incorrecta. Intente nuevamente.")


menu()