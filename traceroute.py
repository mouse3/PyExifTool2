def traceroute(archivo_tracert, nombre_mapa_guardar):
    ## IMPORTACIONES

    from requests import get
    from folium import Map, PolyLine, Marker
    from re import findall

    ## FIN DE IMPORTACIONES

    # Función para extraer todas las IPs (incluyendo privadas) de un archivo de texto
    def extraer_ips(archivo):
        with open(archivo, 'r', encoding='utf-16') as file:  # Especificar UTF-16 si es necesario
            texto = file.read()
            print("Contenido del archivo:\n", texto)  # Verificar el contenido
            # Expresión regular para capturar todas las IPs
            ips = findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', texto)
            #print("IPs extraídas:", ips)  # Verificar si se están extrayendo las IPs
            return ips

    # Función para obtener las coordenadas de una IP
    def get_ip_location(ip):
        try:
            response = get(f"https://ipinfo.io/{ip}/json")
            data = response.json()
            if "loc" in data:
                lat, lon = map(float, data["loc"].split(","))
                return (lat, lon)
        except Exception as e:
            print(f"Error obteniendo datos de la IP {ip}: {e}")
        return None

    # Obtener las coordenadas de todas las IPs
    locations = []
    ips = extraer_ips(archivo_tracert)
    ips.pop(0)
    print("IPs extraídas:", ips)
    for ip in ips:
        loc = get_ip_location(ip)
        if loc:
            locations.append((ip, loc))

    # Crear el mapa en folium
    if locations:
        # El primer nodo será el punto inicial del mapa
        start_coords = locations[0][1]
        mapa = Map(location=start_coords, zoom_start=4)

        # Añadir marcadores y líneas entre las ubicaciones
        for i, (ip, loc) in enumerate(locations):
            Marker(loc, popup=f"IP: {ip}").add_to(mapa)
            if i > 0:
                # Dibujar una línea entre el nodo anterior y el actual
                PolyLine([locations[i-1][1], loc], color="blue").add_to(mapa)

        # Guardar el mapa en un archivo HTML
        mapa.save(nombre_mapa_guardar)

        print("Mapa generado y guardado como 'tracert_map.html'")
    else:
        print("No se pudieron obtener las ubicaciones de las IPs.")