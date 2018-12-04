# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 19:08:19 2018

@author: robotics
"""
class NameOp:
    
    def __init__(self, filepath):
        self.original = self.getFilename(filepath)
        self.ext = self.getExt(filepath)
        self.desc = self.getDesc(filepath)
    
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
    
    def addOperation(self, string):
        if self.desc != None:
            desc = self.desc.split('_')
            desc.append(string)
            self.desc = '_'.join(desc)
        else:
            self.desc = string
            
    def readFileNum(self):
        file_a = open("_log/counter.txt","r")
        number = int(file_a.read()) + 1
        file_a.close()
        file_a = open("_log/counter.txt","w")
        file_a.write(str(number))    
        file_a.close()
        return number
    
if __name__ == "__main__":
    pass