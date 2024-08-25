import os
import exiftool
import folium
from datetime import datetime
from sys import argv

menu = """
-h                                                      Muestra este bloque de texto
--ext-changed                                           Verifica si la extension de un archivo en el directorio ha cambiado
--analyze-image [nº] [nombre del mapa a guardar.html]   si nº = 1, Arroja posibles ediciones en la imagen. No hace falta poner el nombre del mapa
                                                        si nº = 2, Crea un .html con una ruta en cuanto los metadatos GPS de la imagen
                                                        si nº = 3, Hace ambas cosas
"""

def verificar_extension_cambiada(ruta_directorio):
    cant_archivos_modif = 0
    with exiftool.ExifTool() as et:
        for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_directorio):
            for archivo in archivos:
                ruta_completa = os.path.join(carpeta_raiz, archivo)
                if 'exiftool_files' in ruta_completa:
                    continue  # Saltar este archivo
                extension_actual = os.path.splitext(archivo)[-1].lower().replace('.', '')
                try:
                    metadata = et.get_metadata(ruta_completa)
                    tipo_archivo = metadata.get('File:FileTypeExtension', '').lower()
                    if extension_actual != tipo_archivo:
                        cant_archivos_modif += 1
                        print(f"El archivo '{ruta_completa}' tiene la extensión '.{extension_actual}' pero en los metadatos aparece como '.{tipo_archivo}'")
                except Exception as e:
                    print(f"No se pudieron obtener metadatos para '{ruta_completa}': {e}")
                    continue
        return cant_archivos_modif


def detectar_edicion_imagen(ruta_imagen):
    indicadores_edicion = {"Software": None, "CreateDate": None, "ModifyDate": None}
    with exiftool.ExifTool() as et:
        metadatos = et.get_metadata(ruta_imagen)
        software = metadatos.get("EXIF:Software")
        create_date = metadatos.get("EXIF:CreateDate")
        modify_date = metadatos.get("EXIF:ModifyDate")
        if software:
            indicadores_edicion["Software"] = software
        if create_date and modify_date and create_date != modify_date:
            indicadores_edicion["CreateDate"] = create_date
            indicadores_edicion["ModifyDate"] = modify_date
        edicion_detectada = any(indicadores_edicion.values())
        if edicion_detectada:
            print("Posible edición detectada:")
            print(indicadores_edicion)
        else:
            print("No se detectaron indicios claros de edición en la imagen.")
        return edicion_detectada, indicadores_edicion

def trazar_mapa(rutas_imagenes, nombre_mapa_guardar="mapa.html"):
    datos_imagenes = []
    with exiftool.ExifTool() as et:
        for ruta in rutas_imagenes:
            metadatos = et.get_metadata(ruta)
            gps_latitude = metadatos.get("EXIF:GPSLatitude")
            gps_longitude = metadatos.get("EXIF:GPSLongitude")
            gps_latitude_ref = metadatos.get("EXIF:GPSLatitudeRef")
            gps_longitude_ref = metadatos.get("EXIF:GPSLongitudeRef")
            fecha_hora = metadatos.get("EXIF:DateTimeOriginal") or metadatos.get("EXIF:CreateDate")
            if gps_latitude and gps_longitude and fecha_hora:
                lat = gps_latitude if gps_latitude_ref == "N" else -gps_latitude
                lon = gps_longitude if gps_longitude_ref == "E" else -gps_longitude
                fecha_hora = datetime.strptime(fecha_hora, "%Y:%m:%d %H:%M:%S")
                datos_imagenes.append({"ruta": ruta, "latitud": lat, "longitud": lon, "fecha_hora": fecha_hora})
    datos_imagenes.sort(key=lambda x: x["fecha_hora"])
    if datos_imagenes:
        inicio = datos_imagenes[0]
        mapa = folium.Map(location=[inicio["latitud"], inicio["longitud"]], zoom_start=12)
        puntos = [[dato["latitud"], dato["longitud"]] for dato in datos_imagenes]
        for punto in puntos:
            folium.Marker(punto, popup=f"{punto}").add_to(mapa)
        folium.PolyLine(puntos, color="blue", weight=2.5, opacity=1).add_to(mapa)
        mapa.save(nombre_mapa_guardar)
        print(f"Mapa guardado como {nombre_mapa_guardar}")
    else:
        print("No se encontraron datos de GPS para trazar en el mapa.")

def extraer_informacion_imagen(ruta_imagen, mode, nombre_mapa_guardar=None):
    if mode == 1:
        detectar_edicion_imagen(ruta_imagen)
    elif mode == 2:
        trazar_mapa([ruta_imagen], nombre_mapa_guardar)
    elif mode == 3:
        detectar_edicion_imagen(ruta_imagen)
        trazar_mapa([ruta_imagen], nombre_mapa_guardar)
    else:
        print("Error: Modo no válido. Consulte -h para la lista de comandos.")

if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == '-h':
            print(menu)
        elif argv[1] == '--ext-changed':
            ruta_directorio = argv[2] if len(argv) >= 3 else os.getcwd()
            cant_archivos_modif = verificar_extension_cambiada(ruta_directorio)
            print("Cantidad de archivos modificados: ", cant_archivos_modif)
        elif argv[1] == '--analyze-image':
            if len(argv) >= 4:
                ruta_imagen = argv[2]
                mode = int(argv[3])
                nombre_mapa_guardar = argv[4] if len(argv) > 4 else "mapa.html"
                extraer_informacion_imagen(ruta_imagen, mode, nombre_mapa_guardar)
            else:
                print("Error: Parámetros insuficientes. Consulte -h para la lista de comandos.")
        else:
            print("Comando no reconocido. Use '-h' para ver la lista de comandos.")
    else:
        print("Use 'python exiftool2.py -h' para más información.")
