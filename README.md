
A forensic tool which is still in development, specializes in file change detection and other forensic uses.


### **Usage**:
```
python3 PyExifTool.py:

-h Shows this text block

--ext-changed Verifies if the extension of a file in a directory was changed

--analyze-image [nº] [name of the map to save.html] 

nº = 1, Prints any possible editions in a image

nº = 2, Creates a .html map in which saves the geo-locations of the images 

nº = 3, Do both things 
```

### **Libraries imports**:
You will need:
```
	1-Folium: pip install folium
	2-Datetime:pip install DateTime
	3-OS
	4-SYS
```

#### **Be careful with:**
You shouldn't modify the .zip file because that's the module functions and its hard to repair it if you broke the file or modify it. So, you just need to modify and make changes in the .py file. The code is completely commented in Spanish but i will solve that as soon as possible

#### ***Help from the community:***
By the way, this repository is open to implement functions in the code (Like a new function or something like that) by a **Pull Request**
