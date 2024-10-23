"""
from os import path, walk, getcwd
import exiftool
from folium import Map, Marker, PolyLine
from datetime import datetime
from sys import argv
from math import log2
from collections import Counter
import hashlib
from json import loads
from PIL import Image
from re import findall
from pytsk3 import Img_Info, FS_Info, TSK_FS_META_TYPE_REG, TSK_FS_META_FLAG_UNALLOC
from log_viewer import procesar_logs
from traceroute import traceroute
"""
from os import path, walk, getcwd
import exiftool
from sys import argv




menu = """
-h                                                      Shows this text messagge

--ext-changed [directory]                               Verifies if the extension of a file in a directory was changed

--entropy [file path]                                   Analises the entropy and the redundancy of a file, This may detect some anti-forensic measure

--lsb [file path]                                       Decode a ocult message of a image

--hash [file path] [hash type]                          Calculates the hash of a specified file, default: MD5

--strings [directory] [min_length]                      Prints the strings on a file only if the strings are larger than the min_lenght

--recover-deleted [image]                               This function tries to recover deleted files from a image

--hexdump [file path]                                   Prints the hexdump of a file (the hex information and translated to ASCII utf-8 )

--analyze-sniffed [file path] [Image output]               Prints the connections that have been made based on sniffing a .pcap file and its variants, 
                                                        and also prints the number of requests between one IP and another, smth like:
                                                            192.168.0.1 <-> 192.168.0.4 85 requests
                                                            192.168.0.2 <-> 192.168.0.5 66 requests
                                                            192.168.0.3 <-> 192.168.0.6 2 requests

--analyze-log [file path]                               It represents the ADB logcat logs of an Android device on a 3-dimensional coordinate axis. 
                                                            X-axis: Unix time(ms)
                                                            Y-axis: PID
                                                            Z-axis: Importance (Info, warning, error and fatal)
                                                        Export the data using: adb logcat *:VIWEF > file.txt

--analyze-image [nº] [nombre del mapa a guardar.html]   nº = 1, Prints any possible editions in a image
                                                        nº = 2, Creates a .html map in which saves the geo-locations of the images
                                                        si nº = 3, Do both things

--trace-map [tracert path] [map file name]              Shows the path of a icmp from a "tracert -4 -h 30 example.com > output.txt" command, 
                                                            example.com: the path of the domain that you want to visualize
                                                            output.txt: The file name, this file has the output of the comand saved in it

                                                        if you dont write the [map file name], it would save the map in a file whose name is "tracert_map.html"
                                                            Note that the location of each point(node) of the visualized path is extracted by ipinfo.io, it uses IP GeoLocation.

--wav-analysis [wav file path]                          Shows the two-dimensional(
                                                                                X- Time(s)
                                                                                Y- Amplitude) a
                                                        and three-dimensional(
                                                                                X-Time(s)
                                                                                Y-Frecuency(Hz)
                                                                                Z-Intensity(dB)) 
                                                        graph representing the audio of a .wav file
                                                        Additionaly:
                                                            It shows the constellation diagram(that helps you to know if it's phase modulated).
                                                            And the fourier transform(To know if it is frecuency modulated) 
                                                        The intensity is calculated using the log10 of watts + 1e-18, this is done to avoid any calculation problems  
"""
def hexdump(file_path : str):
    with open(file_path, 'rb') as f:
        offset = 0
        while chunk := f.read(16):
            # Muestra el offset
            print(f"{offset:08x}  ", end='')

            # Muestra los bytes en formato hexadecimal
            hex_bytes = ' '.join(f"{byte:02x}" for byte in chunk)
            print(f"{hex_bytes:<48}", end=' ')

            # Muestra los caracteres imprimibles (o '.' si no es imprimible)
            ascii_rep = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk)
            print(f"|{ascii_rep}|")

            offset += len(chunk)

def recover_deleted(image_path : str):
    from pytsk3 import Img_Info, FS_Info, TSK_FS_META_TYPE_REG, TSK_FS_META_FLAG_UNALLOC
    """
    Intenta recuperar archivos eliminados en una imagen de disco o dispositivo.

    :param image_path: Ruta a la imagen de disco o dispositivo.
    """
    try:
        # Abre la imagen de disco o dispositivo
        img = Img_Info(image_path)
        fs = FS_Info(img)

        # Recorrer el directorio raíz
        directory = fs.open_dir(path="/")

        for file in directory:
            # Si el archivo tiene metadatos y es de tipo regular
            if file.info.meta and file.info.meta.type == TSK_FS_META_TYPE_REG:
                # Verificar si el archivo está eliminado
                if file.info.meta.flags == TSK_FS_META_FLAG_UNALLOC:
                    print(f"Recuperando archivo eliminado: {file.info.name.name.decode()}")

                    # Leer el contenido del archivo recuperado
                    file_data = file.read_random(0, file.info.meta.size)
                    output_file = f"recovered_{file.info.name.name.decode()}"
                    with open(output_file, 'wb') as recovered_file:
                        recovered_file.write(file_data)
                    print(f"Archivo recuperado y guardado como: {output_file}")

    except Exception as e:
        print(f"Error en la recuperación de archivos: {e}")


def extract_strings(file_path : str, min_length : int):
    from re import findall
    """
    Extrae y devuelve todas las cadenas de texto legibles de un archivo binario.

    :param file_path: Ruta del archivo a analizar.
    :param min_length: Longitud mínima de las cadenas a extraer (por defecto es 4).
    :return: Una lista de cadenas legibles encontradas en el archivo.
    """
    # Convertir min_length a entero por si llega como string
    min_length = int(min_length)

    with open(file_path, "rb") as f:
        data = f.read()

    # Utiliza una expresión regular para encontrar secuencias de caracteres legibles
    pattern = rb'[\x20-\x7E]{%d,}' % min_length
    strings = findall(pattern, data)
    return [s.decode("utf-8", errors="ignore") for s in strings]

def verificar_extension_cambiada(ruta_directorio : str):
    cant_archivos_modif = 0
    with exiftool.ExifTool() as et:
        for carpeta_raiz, subcarpetas, archivos in walk(ruta_directorio):
            for archivo in archivos:
                ruta_completa = path.join(carpeta_raiz, archivo)
                
                # Ignorar ciertos archivos como los de 'exiftool_files'
                if 'exiftool_files' in ruta_completa:
                    continue  
                
                # Obtener la extensión del archivo actual
                extension_actual = path.splitext(archivo)[-1].lower().replace('.', '')
                
                try:
                    # Usar get_metadata en lugar de get_metadata_batch
                    metadata = et.get_metadata(ruta_completa)
                    
                    # Verificar si los metadatos contienen el tipo de archivo
                    if metadata:
                        tipo_archivo = metadata.get('File:FileTypeExtension', '').lower()
                        if extension_actual != tipo_archivo:
                            cant_archivos_modif += 1
                            print(f"El archivo '{ruta_completa}' tiene la extensión '.{extension_actual}' pero en los metadatos aparece como '.{tipo_archivo}'")
                except Exception as e:
                    print(f"No se pudieron obtener metadatos para '{ruta_completa}': {e}")
                    continue
        return cant_archivos_modif

def extract_lsb_message(image_path : str):
    from PIL import Image
    # Cargar la imagen
    image = Image.open(image_path)
    pixels = list(image.getdata())
    
    # Vamos a almacenar los bits del mensaje oculto
    hidden_bits = []
    
    for pixel in pixels:
        for color in pixel[:3]:  # Sólo RGB, ignorar el canal alfa si existe
            hidden_bits.append(color & 1)  # Extrae el bit menos significativo
    
    # Agrupar los bits en bytes (8 bits cada uno)
    hidden_message = ""
    for i in range(0, len(hidden_bits), 8):
        byte = hidden_bits[i:i+8]
        # Convertir de bits a un caracter (ASCII)
        hidden_message += chr(int("".join(map(str, byte)), 2))
    
    # Eliminar cualquier relleno nulo al final del mensaje
    hidden_message = hidden_message.split('\x00', 1)[0]
    
    return hidden_message


def detectar_edicion_imagen(ruta_imagen : str):
    from json import loads
    indicadores_edicion = {"Software": None, "CreateDate": None, "ModifyDate": None}
    
    with exiftool.ExifTool() as et:
        try:
            # Execute ExifTool command to retrieve metadata
            metadata_json = et.execute(b"-j", ruta_imagen.encode('utf-8'))
            metadata_list = loads(metadata_json)
            metadatos = metadata_list[0] if metadata_list else {}

            software = metadatos.get("Software")
            create_date = metadatos.get("CreateDate")
            modify_date = metadatos.get("ModifyDate")
            
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
            
        except Exception as e:
            print(f"Error obteniendo metadatos: {e}")
            return False, indicadores_edicion

def trazar_mapa(rutas_imagenes : str, nombre_mapa_guardar="mapa.html"):
    from folium import Map, Marker, PolyLine
    from datetime import datetime
    datos_imagenes = []
    with exiftool.ExifTool() as et:
        for ruta in rutas_imagenes:
            metadatos = et.get_metadata_batch(ruta)
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
        mapa = Map(location=[inicio["latitud"], inicio["longitud"]], zoom_start=12)
        puntos = [[dato["latitud"], dato["longitud"]] for dato in datos_imagenes]
        for punto in puntos:
            Marker(punto, popup=f"{punto}").add_to(mapa)
        PolyLine(puntos, color="blue", weight=2.5, opacity=1).add_to(mapa)
        mapa.save(nombre_mapa_guardar)
        print(f"Mapa guardado como {nombre_mapa_guardar}")
    else:
        print("No se encontraron datos de GPS para trazar en el mapa.")

def extraer_informacion_imagen(ruta_imagen : str, mode : int, nombre_mapa_guardar=None):
    if mode == 1:
        detectar_edicion_imagen(ruta_imagen)
    elif mode == 2:
        trazar_mapa([ruta_imagen], nombre_mapa_guardar)
    elif mode == 3:
        detectar_edicion_imagen(ruta_imagen)
        trazar_mapa([ruta_imagen], nombre_mapa_guardar)
    else:
        print("Error: Modo no válido. Consulte -h para la lista de comandos.")

def entropy(file_path : str):
    from math import log2
    from collections import Counter
    # Leer el archivo en modo binario
    with open(file_path, 'rb') as file:
        data = file.read()
    #Full mathematics here
    # Calculates the frecuency of each byte of the data 
    frecuency = Counter(data)
    
    # Calculates the probability of each byte 
    length = len(data)
    probabilities = [frec / length for frec in frecuency.values()]
    
    # Calculates the entropy using the Shannons' formula 
    entropie = -sum(p * log2(p) for p in probabilities)

    ###### Redundancy
    redundancy = 1 - entropie/(log2(255)) #255 possible symbols(on a byte)
    return entropie, redundancy


def calculate_hash(file_path :str, algorithm : str):
    import hashlib
    # Initialize the hash object
    hash_func = getattr(hashlib, algorithm)()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

if __name__ == '__main__':
    if len(argv) > 1:
        if argv[1] == '-h':
            print(menu)
        elif argv[1] == '--ext-changed':
            ruta_directorio = argv[2] if len(argv) >= 3 else getcwd()
            cant_archivos_modif = verificar_extension_cambiada(ruta_directorio)
            print("Cantidad de archivos modificados: ", cant_archivos_modif)
        elif argv[1] == '--entropy':
            file_path = argv[2]
            entropie, redundancy = entropy(file_path)
            print(f'The entropy of the file is {entropie:.6f} bit by byte')
            print(f"The redundancy of the file is {redundancy:.6f}")
            if entropie == 0:
                print("The entropy level is so low")
            elif 0 < entropie <= 2:
                print("The entropy level is Low")
            elif 2 < entropie <= 4:
                print("The entropy level is Low-medium")
            elif 4 < entropie <= 6:
                print("The entropy level is Medium")
            elif 6 < entropie <= 7.5:
                print("The entropy level is Medium-high")
            elif 7.5 < entropie < 8:
                print("The entropy level is high, Is so possible that there was applied a forensic evasion technique.")
            elif entropie >= 8:
                print("The entropy level i high af. This is imposible")
        elif argv[1] == '--lsb':
            if len(argv) > 1:
                image_path = argv[2]
                text = extract_lsb_message(image_path)
                print("Ocult message:" + text)
        elif argv[1] == '--strings':
            if len(argv) == 4:
                file_path = argv[2]
                n_string = argv[3]
                strings = extract_strings(file_path, n_string)
                for string in strings:
                    print(string)
            else: 
                print("Error: Parámetros insuficientes. Consulte -h para la lista de comandos.")
        elif argv[1] == '--hash':
            print("hashlib supports: sha1, sha224, sha256, sha384, sha512, sha3_224 \nsha3_256, sha3_384, sha3_512, shake128, shake256, blake2b, blake2s and md5 \n")
            if len(argv) == 4:
                file_path = argv[2]
                algorithm = argv[3]
                file_hash = calculate_hash(file_path, algorithm)
            elif len(argv) == 3:
                file_path = argv[2]
                algorithm = "sha1"
                file_hash = calculate_hash(file_path, algorithm)
            else:
                print("Error: Parámetros insuficientes. Consulte -h para la lista de comandos.")
            print(f"The hash {algorithm.upper()} of the file is: {file_hash}")
        elif argv[1] == '--recover-deleted':
            if len(argv) == 3:
                directory = argv[2]
                recover_deleted(directory)
        elif argv[1] == '--analyze-log':
            from log_viewer import procesar_logs
            if len(argv) == 3:
                directory = argv[2] if len(argv) >= 3 else getcwd()
                procesar_logs(directory)
        elif argv[1] == '--hexdump':
            if len(argv) == 3:
                directory = argv[2] if len(argv) >= 3 else getcwd()
                hexdump(directory)
        elif argv[1] == '--analyze-image':
            if len(argv) >= 4:
                ruta_imagen = argv[3]
                mode = int(argv[2])
                nombre_mapa_guardar = argv[4] if len(argv) > 4 else "mapa.html"
                extraer_informacion_imagen(ruta_imagen, mode, nombre_mapa_guardar)
            else:
                print("Error: Parámetros insuficientes. Consulte -h para la lista de comandos.")
        elif argv[1] == '--trace-map':
            from traceroute import traceroute
            if len(argv)  >= 3:
                archivo_traceado = argv[2] 
                nombre_mapa_guardar = argv[3] if len(argv) > 3 else "tracert_map.html"
                traceroute(archivo_traceado, nombre_mapa_guardar)
        elif argv[1] == '--wav-analysis':
            from wav_analysis import wav_analysis
            if len(argv) == 3:
                wav_file = argv[2] if len(argv) >= 3 else getcwd()
                wav_analysis(wav_file)
        elif argv[1] == '--analyze-sniffed':
            from pcap import pcap_to_image
            pcap_file = argv[2]
            output_image = argv[3]
            pcap_to_image(pcap_file, output_image)
        else:
            print("Comando no reconocido. Use '-h' para ver la lista de comandos.")
    else:
        print(menu)
