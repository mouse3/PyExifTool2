def wav_analysis(archivo_wav: str):
    ## IMPORTACIONES

    from numpy import max, abs, log10, arange, imag, real
    from matplotlib.pyplot import figure, plot, title, xlabel, ylabel, grid, show, scatter
    from scipy.io import wavfile
    from scipy.fft import fft
    from scipy.signal import spectrogram
    from plotly.graph_objects import Figure, Surface

    ## FIN DE IMPORTACIONES

    # Cargar el archivo de audio
    fs, data = wavfile.read(archivo_wav)

    # Si el audio es estéreo, convertir a mono
    if len(data.shape) == 2:
        data = data.mean(axis=1)

    # Normalizar el audio
    data = data / max(abs(data))

    # Espectrograma
    frequencies, times, Sxx = spectrogram(data, fs)

    # Convertir el espectrograma a escala logarítmica
    Sxx_log = 10 * log10(Sxx + 1e-18)  # Añadir un pequeño valor para evitar log(0)

    # Crear el gráfico 3D interactivo usando Plotly
    fig = Figure(data=[Surface(z=Sxx_log, x=times, y=frequencies)])

    # Configuración del gráfico
    fig.update_layout(
        title="3D Audio Spectrogram",
        scene=dict(
            xaxis_title='Time (s)',
            yaxis_title='Frequency (Hz)',
            zaxis_title='Intensity (dB)',
        ),
        autosize=False,
        width=900,
        height=700
    )

    # Mostrar el gráfico en el navegador
    fig.show()

    # Gráfico bidimensional: Tiempo vs Amplitud
    time = arange(0, len(data)) / fs
    figure(figsize=(12, 6))
    plot(time, data, label='Audio Amplitude')
    title('Two-dimensional Graph: Time vs Amplitude')
    xlabel('Time (s)')
    ylabel('Amplitude')
    grid(True)
    show(block=False)  # Mostrar el gráfico de amplitud en una ventana separada

    # Diagrama de constelación (I/Q)
    iq_data = fft(data)  # Transformada rápida de Fourier (FFT)
    iq_data = iq_data[:len(iq_data)//2]  # Solo la mitad positiva de las frecuencias

    figure(figsize=(6, 6))
    scatter(real(iq_data), imag(iq_data), color='blue', s=1)
    title('Constellation Diagram (I/Q)')
    xlabel('In-phase (Real)')
    ylabel('Quadrature (Imaginary)')
    grid(True)
    show(block=False)  # Mostrar el gráfico de constelación en otra ventana

    # Mantener la ejecución abierta para que todas las ventanas permanezcan abiertas
    show()  # Esto mantiene la interfaz abierta para interactuar con todas las ventanas
