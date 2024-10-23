import matplotlib.pyplot as plt
import networkx as nx
from scapy.all import rdpcap, IP

def pcap_to_image(pcap_file, output_image):
    try:
        # Leer el archivo PCAP
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"An error has ocurred when reading the file PCAP: {e}")
        return
    
    # Crear un grafo
    G = nx.Graph()

    # Contar las conexiones
    connection_count = {}

    # Extraer IPs y agregar conexiones al grafo
    for packet in packets:
        # Verificar que el paquete tenga capas IP
        if IP in packet:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            
            # Añadir arista al grafo
            G.add_edge(src_ip, dst_ip)

            # Contar las conexiones
            connection = (src_ip, dst_ip)
            connection_count[connection] = connection_count.get(connection, 0) + 1

    # Encontrar la conexión más frecuente
    max_connection = max(connection_count, key=connection_count.get)
    max_count = connection_count[max_connection]

    # Imprimir la conexión con más peticiones
    print(f"the connection with the most requests is {max_connection[0]} <-> {max_connection[1]} {max_count} requests.") 

    # Imprimir todas las conexiones
    print("\nList of conections and requests:")
    for (src, dst), count in connection_count.items():
        print(f"{src} <-> {dst} {count} requests")

    # Dibujar el grafo
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)  # Posiciones para todos los nodos
    node_sizes = [G.degree(n) * 100 for n in G.nodes()]

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue')

    # Dibujar aristas
    edges_color = ['red' if edge == max_connection else 'lightgray' for edge in G.edges()]
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color=edges_color)

    # Dibujar etiquetas
    nx.draw_networkx_labels(G, pos, font_size=10)

    # Guardar la imagen
    plt.title('Conections IPs')
    plt.axis('off')
    plt.savefig(output_image + ".png", format='PNG')
    plt.close()