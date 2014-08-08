import time

if __name__ == '__main__':
    
    print "Setting up watchdog..."
    wd = open("/dev/watchdog", "w+")
    print "Watchdog active..."
    while True:
        input = raw_input(">> ")
                # Python 3 users
                # input = input(">> ")
        if input == 'exit' or input == 'EXIT':
            print "Exiting app"
            break
        else:
            wd.write("keep-alive")
            print "sending keep-alive..."
            
        time.sleep(.5)
        
    wd.close()
    exit()
    
    
        