
A Open-Source & Non-professional(not that much) forensic Tool which specializes in file change detection and other forensic uses.


### **Usage**:
```
-h                                                      Shows this text messagge

--ext-changed [directory]                               Verifies if the extension of a file in a directory was changed

--entropy [file path]                                   Analises the entropy and the redundancy of a file, This may detect some anti-forensic measure

--lsb [file path]                                       Decode a ocult message of a image

--hash [file path] [hash type]                          Calculates the hash of a specified file, default: MD5

--strings [directory] [min_length]                      Prints the strings on a file only if the strings are larger than the min_lenght

--recover-deleted [image]                               This function tries to recover deleted files from a image

--hexdump [file path]                                   Prints the hexdump of a file (the hex information and translated to ASCII utf-8 )

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
```
### **Libraries imports**:
You will need:
```
	1-  Folium(Map, Marker, PolyLine): pip install folium
	2-  Datetime(datetime):pip install DateTime
	3-  OS(path, walk, getcwd)
	4-  SYS(argv)
	5-  pytsk(Img_Info, FS_Info, TSK_FS_META_TYPE_REG, TSK_FS_META_FLAG_UNALLOC)
	6-  re(findall)
	7-  json(loads)
	8-  hashlib
	9-  collections(Counter)
	10- math(log2)
	11- numpy(max, abs, log10, arange, imag, real)
	12- matplotlib.pyplot(figure, plot, title, xlabel, ylabel, grid, show, scatter)
	14- scipy.io(wavfile)
	15- scipy.fft(ftt)
	16- scipy.signal(spectrogram)
	17-Plotly.graph_objects(Figure, Surface)
```

You can install all of this dependences using
```
pip install -r requirements.txt
```
Btw, the estimated size of all the files is around 94.7 MB

#### **Be careful with:**
You shouldn't modify the .zip file because that's the module functions and its hard to repair it. So, you just need to modify and make changes in the .py file. The code is completely commented in Spanish, but i'll fix it as soon as possible

#### ***Help from the community:***
By the way, this repository is open to implement functions in the code (Like a new function, optimization or something like that) by a **Pull Request**
