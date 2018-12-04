# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:36:10 2018

@author: js_en
"""
import numpy as np
import nameop as op
#import pcl

class Tile:

    def __init__(self, fileordata, father=None, align=True):
        self.driver(fileordata)
        self.getProperties()
        if align == True:
            self.alignData()
        
        print('init done')
            

    
    #---------------------------------------------------------
    # USER METHODS
    #---------------------------------------------------------
    
    # Rotoate the cloud by angle theta on axis(x,y)
    def rotZ(self, phi, origin=(0,0)):
        xs = self.data[0]    # add if origin != 0
        ys = self.data[1]    # add if origin != 0
        rs = np.hypot(xs,ys)
        ths = np.arctan2(ys, xs)
        ths_new = np.add(ths, phi)
        xs_new = rs * np.cos(ths_new)
        ys_new = rs * np.sin(ths_new)
        self.data[0] = xs_new
        self.data[1] = ys_new
        
    def rotY(self, phi):
        xs = self.data[0]    # add if origin != 0
        zs = self.data[2]    # add if origin != 0
        rs = np.hypot(xs,zs)
        ths = np.arctan2(zs, xs)
        ths_new = np.add(ths, phi)
        xs_new = rs * np.cos(ths_new)
        zs_new = rs * np.sin(ths_new)
        self.data[0] = xs_new
        self.data[2] = zs_new
    
    def shiftXYZ(self, xyz):
        self.data[0] = np.array(self.data[0]) + xyz[0]
        self.data[1] = np.array(self.data[1]) + xyz[1]
        self.data[2] = np.array(self.data[2]) + xyz[2]
        
    def saveFile(self, filepath=None):
        desc = self.name.desc
        size = self.size
        data = np.array(self.data)
        dec = 5 # For rounding
        
        if filepath == None:
            filepath = '%s.txt'%(desc)
        
        file_a = open(filepath,"w") 
        for i in range(size):
            string = ' '.join(map(str, data[:,i]))
            file_a.write(string + "\n")
        file_a.close()
        print('File Saved')
    
    def toImg(self):
        # Saves the data as an image using opencv
        pass
    
    #---------------------------------------------------------
    # INTERNAL METHODS
    #---------------------------------------------------------
    
    def driver(self, fileordata):
        if isinstance(fileordata, str):
            self.filepath = fileordata
            self.name = op.NameOp(self.filepath)
#            self.ext = getExt(fileordata)
#            self.desc = getDesc(fileordata)
            self.data = self.readFile(fileordata)
        else:
            self.filepath = None
            self.ext = None
            self.desc = None
            self.data = fileordata
        
        self.size = len(self.data[0])
            
    def alignData(self):
        self.getProperties()
        self.rotZ(self.getRot())
        self.getProperties()
        self.shiftXYZ(-tile.center)
        self.name.addOperation('aligned')
    
    # Ge the rotation angle needed to ge the cloud to touch the YZ-plane
    def getRot(self, origin=(0,0)):     
        x = self.center[0]
        y = self.center[1]
        # create list of rotations
        th = np.arctan2(y, x)       # Make sure the xy order is correct
        th_mod = th % (2*np.pi)    # make list positive  
        
        phi = np.pi/2 - th_mod
        return phi
        
    def getProperties(self):
        xs = self.data[0]
        ys = self.data[1]
        zs = self.data[2]
        self.maxxyz = np.array([max(xs), max(ys), max(zs)])
        self.minxyz = np.array([min(xs), min(ys), min(zs)])
        self.center = np.array([np.mean(xs), np.mean(ys), np.mean(zs)])
        self.stdev = np.std(ys)
          
    def readFile(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()            
            header = self.getHeader(lines)
            lines = lines[header:len(lines)]
            
            column = len(lines[0].split())
    
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
            if column >= 7:
                self.r = [float(line.split()[4]) for line in lines]
                self.g = [float(line.split()[5]) for line in lines]
                self.b = [float(line.split()[6]) for line in lines]
                data.append(self.r)                
                data.append(self.g)                
                data.append(self.b)
        return np.array(data)
       
       
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
    


##############################################################################
    
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
        


        


    
if __name__ == "__main__":
    tile = Tile('lump_5ft_lvl3_inches.pts', align=False)
    tile.rotZ(35*np.pi/180)
    
    tile.saveFile('offset.txt')
    
    
    #tile = Tile('zeros.txt')
    #tile.saveFile()
