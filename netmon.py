import re
import subprocess
import threading
import time

class CpInterfaceResultCode:
    UNKNOWN = 0
    FOUND = 1
    NOTFOUND = 2
    
class CpInterface:
    ResultCode = CpInterfaceResultCode.UNKNOWN
    RxBytes = 0
    TxBytes = 0
    InetAddress = ''
    PtP = ''
    Mask = ''
    

class NetMon(threading.Thread):

    def __init__(self, *args):
        self._target = self.task_handler
        self._args = args
        self.__lock = threading.Lock()
        self.closing = False # A flag to indicate thread shutdown
        threading.Thread.__init__(self)
   
        
        
    def run(self):
        self._target(*self._args)
        
    def task_handler(self):
        
        while not self.closing:
            self.net_mon()
            time.sleep(5)
            
            
    
    def net_mon(self): 
        # Check to see that interface exists
        if (self.query_interface('ppp0')):
            # Exctract interface metrics via ifconfig
            result = self.query_interface_ifconfig('ppp0')
        
            print 'Interface Results'
            print 'Result: %d' % result.ResultCode
            print 'RxBytes: %s' % result.RxBytes
            print 'TxBytes: %s' % result.TxBytes
            print 'InetAddress: %s' % result.InetAddress
            print 'PtP: %s' % result.PtP
            print 'Mask: %s' % result.Mask
        else:
            print 'Interface not found'


    def query_interface_ifconfig(self, interface):
            # Initialize new varialbe to hold results
        handle = CpInterface()
        
        output = subprocess.Popen(['ifconfig', interface], stdout=subprocess.PIPE).communicate()[0]
        
        handle.ResultCode = CpInterfaceResultCode.FOUND
        handle.RxBytes = re.findall('RX bytes:([0-9]*) ', output)[0]
        handle.TxBytes = re.findall('TX bytes:([0-9]*) ', output)[0]
        
        # Extract networking tuples
        tuple = re.findall( r'[0-9]+(?:\.[0-9]+){3}', output)
        handle.InetAddress = tuple[0]
        handle.PtP = tuple[1]
        handle.Mask = tuple[2]
    
        return handle
    
    def query_interface(self, interface):
        
        for line in open('/proc/net/dev', 'r'):
            if interface in line:
                return True
            
        return False
    
    # Alternative method for querying network interfaces
    # Not as detailed information is available as running ifconfig
    def query_interface_proc_net_dev_ex(self, interface):
        # Initialize new varialbe to hold results
        handle = CpInterface()
        
        for line in open('/proc/net/dev', 'r'):
            if interface in line:
                data = line.split('%s:' % interface)[1].split()
                #rx_bytes, tx_bytes = (data[0], data[8])
                handle.ResultCode = CpInterfaceResultCode.FOUND
                handle.RxBytes = data[0]
                handle.TxBytes = data[8]
            
        return handle

    def shutdown_thread(self):
        print 'shutting down CpLed...'
        self.__lock.acquire()
        self.closing = True
        self.__lock.release()

if __name__ == '__main__':
    
    netMon = NetMon()
    netMon.start()    
    
    while(netMon.isAlive()):
        time.sleep(.1)
        pass       
        
    print 'Exiting App...'
    exit()
    
    
    