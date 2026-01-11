# EJ.YTMedia

Herramienta de terminal para descargar videos y audio de YouTube de forma sencilla y rápida.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20Mac-lightgrey.svg)

## Características

- **Descarga de Video** - Formato MP4 en la mejor calidad disponible
- **Descarga de Audio** - Extrae audio en formato MP3 a 320kbps
- **YouTube Shorts** - Soporta descarga de Shorts
- **Barra de Progreso** - Visualiza el progreso de la descarga en tiempo real
- **Reintentos Automáticos** - Maneja errores de conexión automáticamente
- **Verificación de FFmpeg** - Detecta si FFmpeg está instalado antes de convertir
- **Interfaz en Español** - Diseñada completamente en español

## Requisitos

- Python 3.7 o superior
- FFmpeg (requerido para conversión a MP3)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Emmanuel-man/EJ.YTMedia.git
cd EJ.YTMedia
```

### 2. Instalar dependencias

```bash
pip install yt-dlp
```

### 3. Instalar FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Windows:**
Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html) y agrega al PATH.

**Mac:**
```bash
brew install ffmpeg
```

## Uso

```bash
python ejytmedia.py
```

### Flujo del programa:

1. Ingresa la URL del video de YouTube
2. Selecciona el formato: `V` para video o `A` para audio
3. Espera a que termine la descarga

Los archivos se guardan en: `~/Descargas/EJ-YTMedia/`

## Capturas de Pantalla

```
+===========================================================================+
|                                                                           |
|                         E J . Y T M e d i a                               |
|                                                                           |
|             Descarga videos y audio de YouTube facilmente                 |
|                                                                           |
+===========================================================================+
|                   Desarrollado por: Emmanuel Arroyo                       |
+===========================================================================+
```

## Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Haz fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

**Emmanuel Arroyo** - [GitHub](https://github.com/Emmanuel-man)

---

⭐ Si te fue útil, considera darle una estrella al repositorio.
