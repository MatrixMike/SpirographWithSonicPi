#spiroOSCserver.py by Robin Newman, December 2018. (use python3)
from pythonosc import osc_server
from pythonosc import dispatcher
import argparse
import time
import os
from Spirograph import Spirograph

cwd = os.getcwd() #current directory

def oscTest(unused_addr,args,data):
    print("data received",data)
def drawIt(unused_addr,args,r,sr,d,col):
   s="/usr/local/bin/python3 "+cwd+"/spiroRun.py -r "+r+" -sr "+sr+" -d "+d+" -col '"+col+"'"
   os.system(s)

       
if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-ip",
        default = '127.0.0.1', help="The ip of this computer")
        parser.add_argument("-sp",
        default = '127.0.0.1', help="The ip of the computer running Sonic Pi")
        #This is the port on which the server listens. Usually 8000 is OK
        #but you can specify a different one
        parser.add_argument("--port",
            type=int, default=8000, help="The port to listen on")
        args=parser.parse_args()
        spip=args.sp
        #######dispatchers which handle incoming osc calls. They pass the data received on to
        ####### the routine following the OSC address. eg "/setAll" calls oscSetAll with data cname and id
        ####### All routines can send optional message back to Sonic Pi if id param is > -1 (default),sender
        ####### steps, wait_ms and id all have default values if omitted
        dispatcher = dispatcher.Dispatcher()

        dispatcher.map("/test",oscTest,"data") #for testing purposes only
        dispatcher.map("/draw",drawIt,"r","sr","d","col")
        #now setup sender to return OSC messages to Sonic Pi
        print("Sonic Pi on ip",spip)
 #sender set up for specified IP
        #Now set up and run the OSC server
        server = osc_server.ThreadingOSCUDPServer(
            (args.ip, args.port), dispatcher)
        print("Serving on {}".format(server.server_address))
        #run the server "forever" (till stopped by pressing ctrl-C)
        server.serve_forever()
    except  KeyboardInterrupt:
        print("exiting program")
