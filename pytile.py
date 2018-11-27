# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:36:10 2018

@author: js_en
"""
import numpy as np
import math as ma
#import pcl

class Tile:

    def __init__(self, fileordata, father=None):
        self.driver(fileordata)
        self.alignData()
        self.getProperties()
        print('init done')
            
        #self.readFile(filepath)s 
    def driver(self, fileordata):
        if isinstance(fileordata, str):
            self.filepath = fileordata
            self.ext = self.getExt(fileordata)
            self.desc = self.getDesc(fileordata)
            self.data = self.readFile(fileordata)
        else:
            self.filepath = None
            self.ext = None
            self.desc = None
            self.data = fileordata
        
        self.size = len(self.data[0])
            
    def alignData(self):
        self.getProperties()
        #if self.properties ~= aligned properties
        
        #self.rotate()
        self.data = self.data
        
    # Rotoate the cloud by angle theta on axis(x,y)
    def rotateZ(self, phi, origin=(0,0)):
        x = self.data[0]    # add if origin != 0
        y = self.data[1]    # add if origin != 0
        r = np.hypot(x,y)
        th = np.arctan2[x, y]
        th_new = np.add(th,phi)
        x_new = r * np.cos(th_new)
        y_new = r * np.sin(th_new)
        self.data[0] = x_new
        self.data[1] = y_new
    
    # Ge the rotation angle needed to ge the cloud to touch the YZ-plane
    def getRot(self, origin=(0,0)):     
        x = self.data[0]
        y = self.data[1]
        # create list of rotations
        th = np.arctan2[x, y]       # Make sure the xy order is correct
        th_pos = [element % 360 for element in th]    # make list positive         
        
        phi = np.pi - max(th_pos)
        return phi
        
        
    def getProperties(self):
        data = self.data
        self.maxxyz = [max(data[0]), max(data[1]), max(data[2])]
        self.minxyz = [min(data[0]), min(data[1]), min(data[2])]
        
    
    def saveFile(self):
        desc = self.desc
        size = self.size
        data = np.array(self.data)
        dec = 5 
        
        file_a = open("%s.txt"%(desc),"w") 
        for i in range(size):
            string = ' '.join(map(str, data[0:3, i]))
            file_a.write(string + "\n")
        file_a.close()
        print('File Saved')
    
    
    def getFilename(self, filepath):
        pathlist = filepath.split('/')
        size = len(pathlist)        
        filename = pathlist[size-1]
        return filename
        
    def getExt(self, filepath):
        filename = self.getFilename(filepath)
        namelist = filename.split('.')
        size = len(namelist)
        ext = namelist[size-1]
        return ext
        
    def getDesc(self, filepath):
        filename = self.getFilename(filepath)
        namelist = filename.split('.')
        size = len(namelist)
        namelist = namelist[0:size-1]
        desc = '.'.join(namelist) 
        return desc
        
    def readFile(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()            
            header = self.getHeader(lines)
            lines = lines[header:len(lines)]
            
            column = len(lines[0].split())
            print(column)
            data = []            
            if column >= 3:
                self.x = [float(line.split()[0]) for line in lines]
                self.y = [float(line.split()[1]) for line in lines]                
                self.z = [float(line.split()[2]) for line in lines]
                data.append(self.x)                
                data.append(self.y)                
                data.append(self.z)
            if column >= 4:
                self.i = [float(line.split()[3]) for line in lines]
                data.append(self.i)
            if column == 7:
                self.r = [float(line.split()[4]) for line in lines]
                self.g = [float(line.split()[5]) for line in lines]
                self.b = [float(line.split()[6]) for line in lines]
                data.append(self.r)                
                data.append(self.g)                
                data.append(self.b)
        return data
       
       
    def getHeader(self, lines):
        key = True
        header = 0        
        while key == True:
            cols = len(lines[header].split())
            if cols >= 3:
                key = False
            else:
                header = header + 1
        return header
        
    def filtering(self):
        pass
    
class Point:
    
    def __init__(self):
        self.x = None
        self.y = None
        self.z = None
        self.i = None
        self.r = None
        self.g = None
        self.b = None
        
class Stamp:
    
    def __init__(self, center, size, rotation):
        pass
    
    def genBoundUp(self):
        #y = mx+b
        pass
    
    

# Unimplimented Functions
        
def writeFile(self, filename, data):
    string = str(data)        
    file_a = open("file_data/%d_%s.txt" %(self.file_num, filename),"a")  
    file_a.write(string + "\n")
    file_a.close()
    
def readFileNum(self):
    file_a = open("_log/memory_file.txt","r")
    number = int(file_a.read()) + 1
    file_a.close()
   
    file_a = open("_log/memory_file.txt","w")
    file_a.write(str(number))    
    file_a.close()

    return number


def addOperation(self, string):
    if self.desc != None:
        desc = self.desc.split('_')
        desc.append(string)
        self.desc = '_'.join(desc)
    else:
        self.desc = string
        


    
if __name__ == "__main__":
    tile = Tile('lump_5ft_lvl3_inches.pts')
    #tile = Tile('zeros.txt')
    #tile.saveFile()