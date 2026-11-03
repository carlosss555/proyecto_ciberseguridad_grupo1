1. Objetivo del ataque

En este informe se van a documentar las actividades realizadas por el equipo de Red Team 
como parte del proyecto de Ciberseguridad del curso de programacion avanzada: 
El objetivo principal fue evaluar el nivel de exposición y seguridad de la máquina virtual asignada al equipo de Blue Team, desplegada en Microsoft Azure, mediante técnicas controladas de reconocimiento, análisis de tráfico e intentos de acceso no autorizado.

La máquina objetivo corresponde a una VM Ubuntu Linux ubicada en la dirección IP Publica 
52.162.33.24.

2. Metodología empleada

Para el desarrollo del ataque seguimos una metodología estructurada en tres fases: reconocimiento, análisis de tráfico e intento de acceso.

Fase 1 - Reconocimiento (scanner.py): Se desarrolló un script en Python que 
automatiza el uso de Nmap mediante el módulo subprocess, con el fin de identificar 
los puertos abiertos y servicios activos en la VM objetivo. Se ejecutaron dos tipos 
de escaneo: uno SYN básico (-sS) para una identificación rápida de puertos, y uno 
avanzado (-A -sV -Pn -T1) para obtener versiones de servicios, detección de sistema 
operativo y un perfil más detallado del objetivo, priorizando el sigilo mediante 
temporización lenta (-T1). El script genera automáticamente un reporte en texto con 
el resumen de puertos abiertos encontrados.

Fase 2 - Análisis de tráfico (packet_attack.py): Utilizando la librería Scapy, se 
capturó y analizó el tráfico de red relacionado con la VM objetivo, con el propósito 
de identificar protocolos en uso, patrones de comunicación y posibles vectores de 
ataque adicionales.

Fase 3 - Intento de acceso (ssh_brute.py): Se desarrolló un script basado en la 
librería paramiko para realizar un ataque de diccionario contra el servicio SSH de 
la VM objetivo, con el fin de evaluar la robustez de las credenciales configuradas 
y la existencia de políticas de bloqueo ante múltiples intentos fallidos.

Cada una de estas fases fue documentada mediante capturas de pantalla y registros 
de salida, los cuales se incluyen como evidencia en la sección correspondiente de 
este informe.

3. Resultados

3.1 Escaneo de puertos (scanner.py)

Se ejecutaron ambos escaneos (básico y avanzado) contra la IP 52.162.33.24. El 
escaneo básico (-sS) completó en 11.67 segundos, mientras que el escaneo avanzado 
(-A -sV -Pn -T1), debido a su temporización sigilosa, tardó aproximadamente 1251 
segundos (cerca de 21 minutos).

Resultado: se identificó únicamente el puerto 22/tcp abierto, correspondiente al 
servicio SSH, ejecutando OpenSSH 9.6p1 sobre Ubuntu Linux (protocolo 2.0). Los 
999 puertos restantes analizados se reportaron como filtrados (no-response), lo 
cual indica la presencia de un firewall o Network Security Group (NSG) configurado 
por el equipo de Blue Team, limitando significativamente la superficie de ataque 
expuesta.

Debido a la falta de puertos cerrados detectables, Nmap no logró determinar con 
certeza el sistema operativo mediante fingerprinting (OS fingerprint not ideal), 
aunque la información del servicio SSH confirmó que se trata de un sistema Linux 
basado en el kernel de Linux (CPE: cpe:/o:linux:linux_kernel).

4. Evidencias
Scanner.py
![alt text](escaneo1.png)
![alt text](escaneo2.png)

5. Reflexión sobre la eficacia del Blue Team



6. Recomendaciones de mejora
