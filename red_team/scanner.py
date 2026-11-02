import subprocess
import re
ip_objetivo = "52.162.33.24"

def escaneo_basico(objetivo):
    resultado=subprocess.run(["nmap","-sS","-T4", objetivo], capture_output=True, text=True)
    return resultado.stdout

def escaneo_avanzado(objetivo):
    resultado=subprocess.run(["nmap","-A","-sV","-Pn","-T1",objetivo], capture_output=True, text=True)
    return resultado.stdout

def extraer_puertos(salida_nmap):
    patron= re.compile(r"^\d+/\w+\s+opeb+\s+\S+.*", re.MULTILINE)
    puertos= patron.findall(salida_nmap)
    return puertos

def guardar_reporte(objetivo, salida_basica, salida_avanzada):
    puertos_abiertos= extraer_puertos(salida_avanzada)
    with open("Reporte_escaneo.txt", "w", encoding="utf-8") as archivo:
        archivo.write(f"Reporte del escaneo \nObjetivo: {objetivo}\n")
        archivo.write("="*50+"\n\n")
        archivo.write("Resumen de puertos abiertos:\n")
        for puerto in puertos_abiertos:
            archivo.write(f" {puerto}\n")
        archivo.write("\n")
        
        archivo.write("Escaneo Basico(-sS)\n")
        archivo.write(salida_basica+"\n\n")
        archivo.write("Escaneo Avanzado(-A -sV -Pn -T1)")
        archivo.write(salida_avanzada+"\n")
    print("El reporte ha sido guardado en reporte_escaneo.txt")

if __name__=="__main__":
    print("Iniciando escaneo basico")
    salida_basica=escaneo_basico(ip_objetivo)
    print(salida_basica)
    
    print("Iniciando escaneo Avanzado")
    salida_avanzada=escaneo_avanzado(ip_objetivo)
    print(salida_avanzada)
    
    guardar_reporte(ip_objetivo,salida_basica,salida_avanzada)