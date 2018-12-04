# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:36:10 2018

@author: js_en
"""
import numpy as np
import nameop as op
#import cv2 as cv
#import pcl

class Tile:

    def __init__(self, fileordata, father=None, align=True):
        self.driver(fileordata)
        self.getProperties()
        if align == True:
            self.alignData()
        
        print('Init Completed')
            

    
    #---------------------------------------------------------
    # USER METHODS
    #---------------------------------------------------------
    
    # Cut a square pointcloud from the original
    def punch(self, origin, shape):
        a = self.data
        print(len(a[0]))
        b = self.rightBound( origin, shape, a)
        print(len(b[0]))
        c = self.leftBound( origin, shape, b)
        print(len(c[0]))
        d = self.upBound( origin, shape, c)
        print(len(d[0]))
        e = self.downBound( origin, shape, d)
        print(len(e[0]))
        return e
    
    # Rotate the entire point cloud about the z axis
    def rotZ(self, phi):
        xs = self.data[0]    # add if origin != 0
        ys = self.data[1]    # add if origin != 0
        rs = np.hypot(xs,ys)
        ths = np.arctan2(ys, xs)
        ths_new = np.add(ths, phi)
        xs_new = rs * np.cos(ths_new)
        ys_new = rs * np.sin(ths_new)
        self.data[0] = xs_new
        self.data[1] = ys_new
        
    # Rotate the entire point cloud about the y axis
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
        
    def saveFile(self, filepath=None, data=None):
        desc = self.name.desc
        dec = 5 # For rounding
        
        if data is None:
            data = np.array(self.data)
            size = self.size
            columns = self.columns
        else:
            data = data
            size = len(data[0])
            columns = len(data)
            
        if filepath == None:
            filepath = '%s.txt'%(desc)
        
        file_a = open(filepath,"w")
        
        data_new = []
        for i in range(columns):
            if i < 3:
                data_new.append(list(map(float, np.round(data[i,:], dec))))
            else:
                data_new.append(list(map(int, data[i,:])))
                
        for i in range(size):
            point = [dtype[i] for dtype in data_new]
            string = ' '.join(map(str, point))
            file_a.write(string + "\n")
        file_a.close()
        print('File Saved')
    
    def toImg(self):
        # Saves the data as an image using opencv
        pass
    
    #---------------------------------------------------------
    # INTERNAL METHODS
    #---------------------------------------------------------
    
    # Determines how data should be interpreted by the Tile
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
    
    # Calculates a set of properties for the tile    
    def getProperties(self):
        xs = self.data[0]
        ys = self.data[1]
        zs = self.data[2]
        self.maxxyz = np.array([max(xs), max(ys), max(zs)])
        self.minxyz = np.array([min(xs), min(ys), min(zs)])
        self.center = np.array([np.mean(xs), np.mean(ys), np.mean(zs)])
        self.stdev = np.std(ys)
        self.shape = (max(xs)-min(xs), max(zs)-min(zs) )
    
    # Reads and interprets columnar xyzirgb data       
    def readFile(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()            
            header = self.getHeader(lines)
            lines = lines[header:len(lines)]
            column = len(lines[0].split())
            self.columns = column
    
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
     
    # Gets the line lenght of the header so i can be dismissed
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
    
    # Vertical Right boundary for segmenting tile    
    def rightBound(self, origin, shape, data):
        d_new = []
        bound = origin[0] + shape[0]/2
        xs = data[0]
        for i in range(len(xs)):
            if xs[i] < bound:
                d = [dtype[i] for dtype in data]
                d_new.append(d)
        return np.transpose(d_new)
    
    # Vertical Left boundary for segmenting tile 
    def leftBound(self, origin, shape, data):
        d_new = []
        bound = origin[0] - shape[0]/2
        xs = data[0]
        for i in range(len(xs)):
            if xs[i] > bound:
                d = [dtype[i] for dtype in data]
                d_new.append(d)
        return np.transpose(d_new)
    
    # Horizontal Upper boundary for segmenting tile
    def upBound(self, origin, shape, data):
        d_new = []
        bound = origin[0] + shape[0]/2
        zs = data[2]
        for i in range(len(zs)):
            if zs[i] < bound:
                d = [dtype[i] for dtype in data]
                d_new.append(d)
        return np.transpose(d_new)
    
    # Horizontal Lower boundary for segmenting tile
    def downBound(self, origin, shape, data):
        d_new = []
        bound = origin[0] - shape[0]/2
        zs = data[2]
        for i in range(len(zs)):
            if zs[i] > bound:
                d = [dtype[i] for dtype in data]
                d_new.append(d)
        return np.transpose(d_new)
    


                    
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
    tile = Tile('lump_5ft_lvl3_inches.pts')
    
    smol = tile.punch((0,0), (12,12))
    tile_1 = Tile(smol, align=False)
    #tile.saveFile('smol_tile.txt', smol)
    #tile.saveFile('improved_save_2.txt')
    
    
    #tile = Tile('zeros.txt')
    #tile_1.saveFile()
