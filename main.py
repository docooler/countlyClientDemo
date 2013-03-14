#!/usr/bin/python
#Author         : docooler
#Date           : 2013-03-10
#email          : yi01625@163.com

import urllib
import time
import threading
import json
import random
import config
#-----------------------------
#gt config file info 
#-----------------------------
def getConfig(cfg_filename):
    cfg = {}
    msg = config.ConfigMsg(cfg_filename)
    cfg['_server_url']   = msg.getServerURL()
    cfg['_app_key']      = msg.getApkKey()
    cfg['_sdk_version']  = msg.getSdkVersion()
    cfg['delay']         = msg.getUpdateDelayDurations()
    cfg['_os_version']   = msg.getOsVersion()
    cfg['_carrier']      = msg.getCarrier()
    cfg['_resolution']   = msg.getResolution()
    cfg['_devices_cm']   = msg.getDevices_cm()
    cfg['_locale']       = msg.getLocale()
    cfg['_updateTimes']  = msg.getUpdateTimes()
    cfg['_os_type']      = msg.getOsType()
    return cfg
    
class Demo():
    def __init__(self, devices_id, cfg):
        self._server_url  = cfg['_server_url']
        self._app_key     = cfg['_app_key']
        self._sdk_version = cfg['_sdk_version']
        self.delay        = cfg['delay'] 
        self._os_version  = cfg['_os_version']
        self._carrier     = cfg['_carrier']
        self._resolution  = cfg['_resolution']
        self._devices_cm  = cfg['_devices_cm']
        self._locale      = cfg['_locale'] 
        self._updateTimes = cfg['_updateTimes']
        self._os_type     = cfg['_os_type']
        self._devices_id  = devices_id
        self.c2dm_key     = 'none'
        

    def httpGet(self, url):
        try:
            #print "Get url is " + url
            f = urllib.urlopen(url)
            s = f.read()
            return s
        except IOError, e:
            print "Get http Data Error!"
            return None
        
    def genDeviceInfo(self):
        info = "{" + "\"" + "_device"         + "\"" + ":" + "\"" + random.choice(self._devices_cm) + "\""   \
                   + "," + "\"" + "_os"             + "\"" + ":" + "\"" + random.choice(self._os_type) + "\""   \
                   + "," + "\"" + "_os_version"     + "\"" + ":" + "\"" + random.choice(self._os_version) + "\""   \
                   + "," + "\"" + "_carrier"        + "\"" + ":" + "\"" + random.choice(self._carrier) + "\""      \
                   + "," + "\"" + "_resolution"        + "\"" + ":" + "\"" + random.choice(self._resolution) + "\""      \
                   + "," + "\"" + "_locale"         + "\"" + ":" + "\"" + random.choice(self._locale) + "\""      \
                   + "," + "\"" + "_app_version"    + "\"" + ":" + "\"" + "5.0" + "\""      \
                   + "}"
        return info
        
    def genBeginData(self):
        t    = time.time()
        self._begin_time = t
        self._last_time  = t
        data = "app_key=" + self._app_key + "&" + "device_id=" + self._devices_id \
               + "&" + "timestamp=" + str(t) + "&" + "sdk_version=" + random.choice(self._sdk_version) \
               + "&" + "begin_session=" + "1" + "&" + "metrics=" + self.genDeviceInfo()
        return data
        
    def beginSession(self):
        data = self.genBeginData()
        url = self._server_url + '/i?' + data
        #print "Get " + url
        s = self.httpGet(url)
        return s 
        
    def genUpdateData(self):
        t    = time.time() 
        duration = t - self._last_time
        self._last_time = t
        
        data = "app_key=" + self._app_key + "&" + "device_id=" + self._devices_id \
               + "&" + "sdk_version=" + random.choice(self._sdk_version) \
               + "&" + "c2dm_key="    + self.c2dm_key  \
               + "&" + "timestamp=" + str(t) + "&" + "session_duration=" + str(duration)
        return data
        
    def updateSession(self):
        data = self.genUpdateData()
        url  = self. _server_url + '/i?' + data
        s = self.httpGet(url)
        response = json.loads(s)
        if response['result'] == 'Push':
            if self.c2dm_key == 'none':
                self.c2dm_key = response['key']
            else:
                self.c2dm_key += ',' + response['key']
        return s

    def getDelay(self):
        return self.delay
        
    def genEndSession(self):
        t    = time.time()
        duration = t - self._begin_time
        data = "app_key=" + self._app_key + "&" + "device_id=" + self._devices_id \
               + "&" + "timestamp=" + str(t)    \
               + "&" + "end_session=" + "1"      \
               + "&" + "session_duration=" + str(duration)
        return data
               
    def endSession(self):
        data = self.genEndSession()
        url  = self. _server_url + '/i?' + data
        s = self.httpGet(url)
        return s
    
    def getUpdateTimes(self):
        return self._updateTimes
    

        

class phoneThread(threading.Thread):
    def __init__(self, threadname, agent , thread_id):  
        threading.Thread.__init__(self, name=threadname)  
        self._agent = agent 
        self._thread_id = thread_id
          
    def run(self):  
        self.threadFun(self._agent, self._thread_id)
        
    def threadFun(self, agent , thread_id):
        print str(thread_id) + "start"
        s = agent.beginSession()
        if s == None:
            print str(thread_id) + "'s Can't conect servers quit"
            #thread.exit_thread() 
            return
        for i in range(agent.getUpdateTimes()):
            time.sleep(agent.getDelay())
            text = agent.updateSession()
            if s == None:
                print "Can't conect servers quit"
                return
            print "the " + str(thread_id) + "\'s updateSession is :" + text
        text = agent.endSession()
        print str(thread_id) + "End"
        #thread.exit_thread() 
 
 
def test_run_by_config():
    msg = config.ConfigMsg('config.ini')
    start_uid = msg.getStartUid()
    user_num  = msg.getUserNum()
    cfg = getConfig('config.ini')
    
    for i in range(user_num):
        agent = Demo(str(start_uid), cfg)
        th = phoneThread(str(start_uid), agent, start_uid)
        th.start()
        time.sleep(0.1)
        if i%100 == 0:
            time.sleep(2)
        start_uid += 1
        print "now start user " + str(i+1)
    print 'test end !'
        
def test_always_run():
    cfg = getConfig('config.ini')
    i = 0
    
    while True:
        uid =  random.randint(500040001, 600040001)
        agent = Demo(str(uid), cfg)
        th = phoneThread(str(uid), agent, uid)
        th.start()
        time.sleep(0.1)
        if i%100 == 0:
            time.sleep(2)
        i += 1
        print "now start user " + str(i)
        
if __name__ == '__main__':
    #test_run_by_config()
    test_always_run()
        
   
    #text = s.genUpdateData()
    #print text
    
