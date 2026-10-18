- Comandos utilizados. 

docker compose up –build - d : sirve para construir y levantar los servicios de tu proyecto utilizando Docker Compose, dejándolos ejecutándose en segundo plano. 

git add .  : agrega todos los archivos nuevos, modificados y eliminados del directorio actual al área de preparación (staging), para incluirlos en el próximo commit.

git commit -m "Descripción" : guarda una versión de los cambios preparados en el historial local de Git. El texto entre comillas describe qué cambios se guardaron.

git push origin main : envía los commits locales a GitHub, a la rama main del repositorio remoto llamado origin.

docker stats : muestra en tiempo real el consumo de recursos de los contenedores de Docker. Te permite observar cuánta memoria RAM y CPU utiliza tu programa mientras se está ejecutando. 


- Arquitectura de Von Neumann y Contenedores

Recursos de la Arquitectura de Von Neumann utilizados:
  Memoria Principal (RAM):  Guarda el código ejecutable de Python/Django y las variables temporales de las peticiones.
  Unidad Central de Procesamiento (CPU): Ejecuta la Unidad de Control (instrucciones de Django) y la Unidad Aritmético-Lógica (ALU) para las conversiones y procesamiento de datos.
  Buses de Entrada/Salida (E/S): Los sockets de red por los que viajan los paquetes HTTP (puerto 8000).

¿Por qué el contenedor comparte el kernel del host?
A diferencia de una máquina virtual (que emula un hardware completo y corre un sistema operativo invitado completo con su propio kernel), un contenedor de Docker es una abstracción a nivel de proceso. Utiliza las características del sistema operativo host (como namespaces para aislamiento y cgroups para limitar RAM y CPU), compartiendo directamente el kernel del host. Esto reduce drásticamente el consumo de recursos y el tiempo de arranque.

Evidencia requerida. 

<img width="1069" height="94" alt="Captura de pantalla 2026-10-18 170545" src="https://github.com/user-attachments/assets/dc3ceef6-f8f0-44c6-841c-9c53aa672663" />
<img width="428" height="340" alt="image" src="https://github.com/user-attachments/assets/9ff83b83-5b4a-4993-b2ae-ac198ad68c13" />
<img width="321" height="144" alt="Captura de pantalla 2026-10-18 170731" src="https://github.com/user-attachments/assets/d87e1af2-9e99-40dd-9e1e-e95658f5dfdb" />

