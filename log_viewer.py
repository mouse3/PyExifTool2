from datetime import datetime
import plotly.graph_objects as go

def procesar_logs(archivo):
    eventos = []
    total_lineas = 0  # Inicializa el contador de líneas
    
    with open(archivo, encoding='utf-16') as fichero:
        for linea in fichero:
            linea = linea.replace('\x00', '').replace('\n', '')
            if not linea.strip():  # Ignorar líneas vacías
                continue
            if linea[1] == '-':
                continue
            total_lineas += 1  # Incrementa el contador de líneas
            
            partes = linea.split()
            fecha_hora = partes[0] + ' ' + partes[1]
            mes, dia = partes[0].split('-')
            hora, minuto, segundo = partes[1].split(':')
            centesima = segundo[3:6]  # Parte de los milisegundos
            
            PID1 = partes[2]
            PID2 = partes[3]
            nivel_log = partes[4]
            etiqueta = partes[5]
            mensaje = ' '.join(partes[6:])
            
            # Convertir la fecha a Unix timestamp
            presentDateStr = f'2024-{mes}-{dia} {hora}:{minuto}:{segundo}{centesima}'
            presentDate = datetime.strptime(presentDateStr, '%Y-%m-%d %H:%M:%S.%f')
            unix_time = datetime.timestamp(presentDate) * 1000
            
            eventos.append([unix_time, PID1, PID2, nivel_log, etiqueta, mensaje])
    
    print(f'Total de líneas: {total_lineas}')
    # Preparar datos para la gráfica 3D
    x_data = []
    y_data = []
    z_data = []
    colors = []
    hover_texts = []
    log_level_mapping = {
        'V': (1, 'cyan'),   # Información mas especifica
        'D': (2, 'green'),  # Debug
        'I': (3, 'blue'),   # Información
        'W': (4, 'yellow'), # Advertencia
        'E': (5, 'red'),    # Error
        'F': (6, 'black')   # Crítico
    }

    for sublista in eventos:
        x_data.append(float(sublista[0]))  # Tiempo UNIX en ms
        y_data.append(float(sublista[1]))  # PID en el eje Y
        hover_texts.append(f"UNIX: {sublista[0]}<br>PID: {sublista[1]}<br>{sublista[4]}<br>{sublista[5]}")  # Información para el hover
        if sublista[3] in log_level_mapping:
            z_data.append(log_level_mapping[sublista[3]][0])  # Nivel de log en el eje Y
            colors.append(log_level_mapping[sublista[3]][1])  # Colores según nivel de log

    # Crear una gráfica 3D de dispersión
    fig = go.Figure(data=[go.Scatter3d(
        x=x_data,  # Tiempo UNIX en el eje X
        y=y_data,  # Importancia (nivel de log) en el eje Y
        z=z_data,  # PID en el eje Z
        mode='markers',
        marker=dict(
            size=5,
            color=colors,  # Color según nivel de log
            opacity=0.8
        ),
        text= hover_texts,  # Texto de hover
        hoverinfo='text'
    )])

    # Actualizar el diseño del gráfico
    fig.update_layout(
        scene=dict(
            xaxis_title='Unix Time (ms)',
            yaxis_title='PID',
            zaxis_title='Log Importance'
        ),
        title='Log Events in 3D'
    )

    # Mostrar el gráfico
    fig.show()

