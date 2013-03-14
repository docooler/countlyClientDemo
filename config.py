#!/usr/bin/python
#Author         : docooler
#Date           : 2013-03-11


#-------------------------------------
#setp1 Get INFO
#-------------------------------------
import ConfigParser
import sys

def genParserFd(file_name):
    try :
        configFile = open(file_name, 'r')
    except IOError:
        print(file_name + " is not found")
        print "please check wheather the file exist!!!"
        raw_input("press anykey to exit!")
        sys.exit()
        
    config = ConfigParser.ConfigParser()
    config.readfp(configFile)
    configFile.close()
    return config
    
class ConfigMsg():
    def __init__(self, file_name):
        self._file_name = file_name
        self._parserfd  = genParserFd(file_name)
    
    def readConfig(self, option, key):
        try:
            return self._parserfd.get(option, key)
        except ConfigParser.NoOptionError:
            print option + "no" + key 
            return None
        
    def getServerURL(self):
        return self.readConfig('SERVER_INFO', 'url')
    
    def getApkKey(self):
        return self.readConfig('SERVER_INFO', 'apk_key')
    
    def strToArr(self, text):
        ss = text.split(',')
        for i in range(len(ss)):
            ss[i] = ss[i].strip()
        return ss
        
    def getOsVersion(self):
        text =  self.readConfig('DEVICES_INFO', '_os_version')
        return self.strToArr(text)
    
    def getCarrier(self):
        text =  self.readConfig('DEVICES_INFO', '_carrier')
        return self.strToArr(text)
    
    def getOsType(self):
        text =  self.readConfig('DEVICES_INFO', '_os_type')
        return self.strToArr(text)
    
    def getResolution(self):
        text =  self.readConfig('DEVICES_INFO', '_resolution')
        return self.strToArr(text)
    
    def getDevices_cm(self):
        text =  self.readConfig('DEVICES_INFO', '_devices_cm')
        return self.strToArr(text)

    def getLocale(self):
        text =  self.readConfig('DEVICES_INFO', '_locale')
        return self.strToArr(text)
    
    def getSdkVersion(self):
        text =  self.readConfig('DEVICES_INFO', '_sdk_version')
        return self.strToArr(text)

    def getUpdateTimes(self):
        try:
            return self._parserfd.getint("CLIENT_CONFIG", "update_times")
        except ConfigParser.NoOptionError:
            return 6
    
    def getUpdateDelayDurations(self):
        try:
            return self._parserfd.getint("CLIENT_CONFIG", "update_delay_durantions")
        except ConfigParser.NoOptionError:
            return 60

    def getStartUid(self):
        try:
            return self._parserfd.getint("CLIENT_CONFIG", "start_uid")
        except ConfigParser.NoOptionError:
            return 40056000
        
    def getUserNum(self):
        try:
            return self._parserfd.getint("CLIENT_CONFIG", "user_num")
        except ConfigParser.NoOptionError:
            return 1000
    
if __name__ == '__main__':
    def printArr(arr):
        for i in arr:
            print i
            
    def test():
        msg = ConfigMsg('config.ini')
        print msg.getServerURL()
        text =  msg.getOsVersion()
        printArr(text)
        aa   = msg.getCarrier()
        printArr(aa)
        printArr(msg.getDevices_cm())
        printArr(msg.getLocale())
        printArr(msg.getOsVersion())
        printArr(msg.getOsType())
        printArr(msg.getSdkVersion())
        
    test()
            