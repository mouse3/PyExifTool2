
A forensic tool which is still in development, specializes in file change detection and other forensic uses.


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
                                                        Export the data using: adb logcat > file.txt

--analyze-image [nº] [nombre del mapa a guardar.html]   nº = 1, Prints any possible editions in a image
                                                        nº = 2, Creates a .html map in which saves the geo-locations of the images
                                                        si nº = 3, Do both things
                                                    si nº = 3, Do both things
```
### **Libraries imports**:
You will need:
```
	1-  Folium: pip install folium
	2-  Datetime:pip install DateTime
	3-  OS
	4-  SYS
	5-  pytsk
	6-  re
	7-  json
	8-  hashlib
	9-  collections
	10- math
	

	
```

#### **Be careful with:**
You shouldn't modify the .zip file because that's the module functions and its hard to repair it if you broke the file or modify it. So, you just need to modify and make changes in the .py file. The code is completely commented in Spanish but i will solve that as soon as possible

#### ***Help from the community:***
By the way, this repository is open to implement functions in the code (Like a new function or something like that) by a **Pull Request**
