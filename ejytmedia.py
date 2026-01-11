#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EJ.YTMedia - por Emmanuel Arroyo
Herramienta de terminal para descargar videos y audio de YouTube
Utiliza yt-dlp para máxima estabilidad y compatibilidad
"""

import os
import sys
import subprocess
import yt_dlp


def verificar_ffmpeg():
    """
    Verifica si FFmpeg está instalado en el sistema.
    
    Returns:
        bool: True si FFmpeg está disponible, False si no
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def verificar_permisos_carpeta(ruta):
    """
    Verifica si se puede crear/escribir en la carpeta especificada.
    
    Args:
        ruta: Ruta de la carpeta a verificar
    
    Returns:
        tuple: (puede_escribir, mensaje_error)
    """
    try:
        # Intentar crear la carpeta si no existe
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        
        # Verificar si se puede escribir
        archivo_prueba = os.path.join(ruta, '.test_write')
        with open(archivo_prueba, 'w') as f:
            f.write('test')
        os.remove(archivo_prueba)
        
        return True, ""
    except PermissionError:
        return False, f"Sin permisos para escribir en: {ruta}"
    except OSError as e:
        return False, f"Error al acceder a la carpeta: {e}"


def limpiar_pantalla():
    """Limpia la pantalla de la terminal según el sistema operativo."""
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')


def mostrar_titulo():
    """Muestra el título del programa."""
    titulo = r"""
    +===========================================================================+
    |                                                                           |
    |                         E J . Y T M e d i a                               |
    |                                                                           |
    |             Descarga videos y audio de YouTube facilmente                 |
    |                                                                           |
    +===========================================================================+
    |                   Desarrollado por: Emmanuel Arroyo                       |
    +===========================================================================+
    """
    print(titulo)


def mostrar_progreso(diccionario_progreso):
    """
    Función de callback para mostrar la barra de progreso durante la descarga.
    
    Args:
        diccionario_progreso: Diccionario con información del progreso de yt-dlp
    """
    if diccionario_progreso['status'] == 'downloading':
        # Obtener información del progreso
        total_bytes = diccionario_progreso.get('total_bytes') or diccionario_progreso.get('total_bytes_estimate', 0)
        bytes_descargados = diccionario_progreso.get('downloaded_bytes', 0)
        velocidad = diccionario_progreso.get('speed', 0)
        tiempo_restante = diccionario_progreso.get('eta', 0)
        
        if total_bytes > 0:
            # Calcular porcentaje
            porcentaje = (bytes_descargados / total_bytes) * 100
            
            # Construir barra de progreso visual
            ancho_barra = 40
            bloques_llenos = int(ancho_barra * porcentaje / 100)
            barra = '█' * bloques_llenos + '░' * (ancho_barra - bloques_llenos)
            
            # Formatear velocidad
            if velocidad:
                velocidad_texto = f"{velocidad / 1024 / 1024:.2f} MB/s"
            else:
                velocidad_texto = "Calculando..."
            
            # Formatear tiempo restante
            if tiempo_restante:
                minutos = int(tiempo_restante // 60)
                segundos = int(tiempo_restante % 60)
                tiempo_texto = f"{minutos:02d}:{segundos:02d}"
            else:
                tiempo_texto = "--:--"
            
            # Formatear tamaño
            mb_descargados = bytes_descargados / 1024 / 1024
            mb_totales = total_bytes / 1024 / 1024
            
            # Mostrar progreso en una sola línea (sobreescribiendo)
            sys.stdout.write(f'\r    📥 Progreso: [{barra}] {porcentaje:5.1f}% | '
                           f'{mb_descargados:.1f}/{mb_totales:.1f} MB | '
                           f'⚡ {velocidad_texto} | ⏱ {tiempo_texto}  ')
            sys.stdout.flush()
    
    elif diccionario_progreso['status'] == 'finished':
        sys.stdout.write('\n')
        print('    ✅ Descarga completada. Procesando archivo...')


def obtener_url():
    """
    Solicita al usuario la URL del video de YouTube.
    
    Returns:
        str: URL ingresada por el usuario
    """
    print("\n    ┌─────────────────────────────────────────────────────────────┐")
    print("    │               📎 INGRESA LA URL DEL VIDEO                   │")
    print("    └─────────────────────────────────────────────────────────────┘\n")
    
    url = input("    🔗 URL de YouTube: ").strip()
    return url


def obtener_formato():
    """
    Pregunta al usuario si desea descargar video o solo audio.
    
    Returns:
        str: 'video' o 'audio' según la elección del usuario
    """
    print("\n    ┌─────────────────────────────────────────────────────────────┐")
    print("    │               📦 SELECCIONA EL FORMATO                      │")
    print("    └─────────────────────────────────────────────────────────────┘\n")
    print("    [V] 🎬 Video (MP4 - Mejor calidad)")
    print("    [A] 🎵 Audio (MP3 - Solo música)\n")
    
    while True:
        opcion = input("    ➜ Tu elección (V/A): ").strip().upper()
        
        if opcion == 'V':
            return 'video'
        elif opcion == 'A':
            return 'audio'
        else:
            print("    ⚠️  Opción no válida. Por favor, ingresa 'V' para video o 'A' para audio.\n")


def obtener_opciones_descarga(formato, carpeta_destino):
    """
    Configura las opciones de yt-dlp según el formato seleccionado.
    
    Args:
        formato: 'video' o 'audio'
        carpeta_destino: Ruta de la carpeta donde se guardarán las descargas
    
    Returns:
        dict: Diccionario con las opciones de configuración para yt-dlp
    """
    # Crear carpeta de destino si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)
    
    # Opciones comunes con reintentos y mejor manejo de conexión
    opciones_base = {
        'outtmpl': os.path.join(carpeta_destino, '%(title)s.%(ext)s'),
        'progress_hooks': [mostrar_progreso],
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': False,
        # Evitar descargar playlists completas
        'noplaylist': True,  # Solo descarga el video individual
        # Opciones para evitar errores de timeout
        'retries': 10,  # Número de reintentos
        'fragment_retries': 10,  # Reintentos por fragmento
        'file_access_retries': 5,  # Reintentos de acceso a archivo
        'extractor_retries': 5,  # Reintentos del extractor
        'socket_timeout': 30,  # Timeout de socket en segundos
        'http_chunk_size': 10485760,  # Tamaño de chunk: 10MB (más estable)
        'continuedl': True,  # Continuar descargas parciales
        'noprogress': False,
        # Opciones adicionales de red
        'nocheckcertificate': True,
        'prefer_insecure': False,
        'geo_bypass': True,
    }
    
    if formato == 'video':
        # Configuración para descargar video en la mejor calidad
        opciones_base.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        })
    else:  # audio
        # Configuración para extraer solo el audio en MP3
        opciones_base.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    
    return opciones_base


def descargar(url, opciones):
    """
    Ejecuta la descarga del video/audio.
    
    Args:
        url: URL del video de YouTube
        opciones: Diccionario con las opciones de yt-dlp
    
    Returns:
        bool: True si la descarga fue exitosa, False en caso contrario
    """
    print("\n    ┌─────────────────────────────────────────────────────────────┐")
    print("    │               ⬇️  INICIANDO DESCARGA...                      │")
    print("    └─────────────────────────────────────────────────────────────┘\n")
    
    try:
        # Configurar opciones para mostrar más información
        opciones['quiet'] = False
        opciones['no_warnings'] = False
        
        with yt_dlp.YoutubeDL(opciones) as descargador:
            print("    🔍 Conectando con YouTube...")
            # Descargar directamente (incluye obtener info)
            descargador.download([url])
            
        return True
        
    except yt_dlp.utils.DownloadError as error:
        print(f"\n    ❌ Error de descarga: {error}")
        return False
    except Exception as error:
        print(f"\n    ❌ Error: {error}")
        return False


def mostrar_resultado_exitoso(carpeta_destino):
    """Muestra un mensaje de éxito con la ubicación del archivo."""
    print("\n    ╔═══════════════════════════════════════════════════════════════╗")
    print("    ║           🎉 ¡DESCARGA COMPLETADA EXITOSAMENTE! 🎉            ║")
    print("    ╠═══════════════════════════════════════════════════════════════╣")
    print(f"    ║  📁 Archivo guardado en:                                      ║")
    print(f"    ║     {carpeta_destino:<55} ║")
    print("    ╚═══════════════════════════════════════════════════════════════╝\n")


def mostrar_error(mensaje_error):
    """Muestra un mensaje de error formateado."""
    print("\n    ╔═══════════════════════════════════════════════════════════════╗")
    print("    ║              ❌ ¡OCURRIÓ UN ERROR! ❌                          ║")
    print("    ╠═══════════════════════════════════════════════════════════════╣")
    print(f"    ║  {mensaje_error:<60} ║")
    print("    ╚═══════════════════════════════════════════════════════════════╝\n")


def preguntar_continuar():
    """
    Pregunta al usuario si desea realizar otra descarga.
    
    Returns:
        bool: True si desea continuar, False si desea salir
    """
    print("    ┌─────────────────────────────────────────────────────────────┐")
    print("    │         ¿Deseas realizar otra descarga?                     │")
    print("    └─────────────────────────────────────────────────────────────┘\n")
    
    respuesta = input("    ➜ Continuar (S/N): ").strip().upper()
    return respuesta == 'S'


def validar_url(url):
    """
    Valida que la URL ingresada sea una URL de YouTube válida.
    
    Args:
        url: URL a validar
    
    Returns:
        tuple: (es_valida, mensaje_error)
    """
    if not url:
        return False, "No ingresaste ninguna URL."
    
    dominios_validos = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    
    es_youtube = any(dominio in url.lower() for dominio in dominios_validos)
    
    if not es_youtube:
        return False, "La URL no parece ser de YouTube."
    
    return True, ""


def main():
    """Función principal que ejecuta el programa."""
    # Definir carpeta de destino para las descargas
    carpeta_destino = os.path.join(os.path.expanduser('~'), 'Descargas', 'EJ-YTMedia')
    
    continuar = True
    
    while continuar:
        try:
            # Limpiar pantalla y mostrar título
            limpiar_pantalla()
            mostrar_titulo()
            
            # Solicitar URL
            url = obtener_url()
            
            # Validar URL
            es_valida, mensaje_error = validar_url(url)
            if not es_valida:
                mostrar_error(mensaje_error)
                input("    Presiona ENTER para intentar de nuevo...")
                continue
            
            # Solicitar formato
            formato = obtener_formato()
            
            # Verificar FFmpeg si se seleccionó audio
            if formato == 'audio' and not verificar_ffmpeg():
                print("\n    ╔═══════════════════════════════════════════════════════════════╗")
                print("    ║           ⚠️  FFMPEG NO ESTÁ INSTALADO ⚠️                       ║")
                print("    ╠═══════════════════════════════════════════════════════════════╣")
                print("    ║  FFmpeg es necesario para convertir a MP3.                    ║")
                print("    ║                                                               ║")
                print("    ║  Instálalo con:                                               ║")
                print("    ║    Ubuntu/Debian: sudo apt install ffmpeg                     ║")
                print("    ║    Windows: descarga desde ffmpeg.org                         ║")
                print("    ║    Mac: brew install ffmpeg                                   ║")
                print("    ╚═══════════════════════════════════════════════════════════════╝\n")
                input("    Presiona ENTER para continuar...")
                continue
            
            # Verificar permisos de carpeta
            puede_escribir, error_permisos = verificar_permisos_carpeta(carpeta_destino)
            if not puede_escribir:
                mostrar_error(error_permisos)
                input("    Presiona ENTER para continuar...")
                continue
            
            # Configurar opciones de descarga
            opciones = obtener_opciones_descarga(formato, carpeta_destino)
            
            # Ejecutar descarga
            exito = descargar(url, opciones)
            
            if exito:
                mostrar_resultado_exitoso(carpeta_destino)
            else:
                mostrar_error("No se pudo completar la descarga.")
            
            # Preguntar si desea continuar
            continuar = preguntar_continuar()
            
        except KeyboardInterrupt:
            # El usuario presionó Ctrl+C
            print("\n\n    👋 ¡Hasta luego! Gracias por usar EJ.YTMedia.\n")
            break
            
        except yt_dlp.utils.DownloadError as error:
            error_texto = str(error)
            
            if "Unable to download" in error_texto or "HTTP Error" in error_texto:
                mostrar_error("Error de conexión. Verifica tu internet.")
            elif "Video unavailable" in error_texto:
                mostrar_error("El video no está disponible o es privado.")
            elif "Private video" in error_texto:
                mostrar_error("El video es privado.")
            else:
                mostrar_error(f"Error: {error_texto[:50]}...")
            
            continuar = preguntar_continuar()
            
        except Exception as error:
            mostrar_error(f"Error inesperado: {str(error)[:45]}...")
            continuar = preguntar_continuar()
    
    # Mensaje de despedida
    limpiar_pantalla()
    print(r"""
    +===========================================================================+
    |                                                                           |
    |                  GRACIAS POR USAR EJ.YTMedia!                             |
    |                                                                           |
    |                  Desarrollado por: Emmanuel Arroyo                        |
    |                                                                           |
    |     Si te fue util, considera compartirlo.                                |
    |     Para reportar errores, crea un issue en el repositorio.               |
    |                                                                           |
    +===========================================================================+
    """)


if __name__ == "__main__":
    main()
