#Author: marktini   github.com/marktini
#Spirograph curve drawing program
#Version 1.0
#modified to Python3 by Robin Newman Dec 2018
#additions to allow export of x,y coords using OSC message
#with aid of pythonosc library
import math
import turtle
import random
import time
from euclidian import euclidianGCD
from frange import frange
from pythonosc import osc_message_builder
from pythonosc import udp_client



class Spirograph:
    #set radius of the spirograph toy (outer circle)
    def __init__ (self, R):
        self.R = R
        self.t = turtle.Turtle() #to be able to access turtle from different methods
    
    #set radius of the inner circle
    def setSmallCircle(self, r):
        self.r = r
    
    #set distance of pen from inner circle radius; set pen color
    def setPen(self, d, color='black', random=False):
        self.d = d
        self.color = color
        self.random = random
        
 
    #draw the spirograph given current settings
    def draw(self):
        
        #find greatest common denominator of r and R using Euclidian algorithm:
        gcd = euclidianGCD(self.r, self.R)
        #number of periods is the reduced numerator of the fraction r/R
        numPeriods = self.r/gcd
        numPetals = self.R/gcd
        #calculate constants for graphing
        print('Periods: ', numPeriods)
        print('Petals: ', numPetals)
        k = float(self.r)/self.R
        l = float(self.d)/self.r
        
        print('k=',self.r, '/',self.R, '=',k,' l=',self.d,'/',self.r,'=',l)
        
        #use the custom-made frange function to make a list of angles of given increment
        angleIncrement = 0.01 #the smaller angleIncrement, the more data points
        ptsPeriod = math.ceil(2*math.pi/angleIncrement)
        print("Points per Period: ", ptsPeriod)
        #frange function is an alternative to range(). The last argument specifies a decimal step
        angles = frange(0, 2*math.pi*numPeriods, angleIncrement)
        
        xCoordinates = []
        yCoordinates = []
        
        #calculate all the (x,y) points corresponding to parameters in the "angles" list
        for theta in angles: 
            thisX = self.R*((1-k)*math.cos(theta) + l*k*math.cos((1-k)/(k)*(theta)))
            thisY = self.R*((1-k)*math.sin(theta) + l*k*math.sin((1-k)/(k)*(theta)))                    
            xCoordinates.append(thisX)
            yCoordinates.append(thisY)
            
        print('Num data points: ', len(xCoordinates))
        
        t = self.t #for brevity in future references to the turtle
        screen= t.getscreen() #same as above
        screen.bgcolor("black")
        
        #name the canvas window
        title = "Spirograph with R= " + str(self.R) + ", r = "+str(self.r) + ", and d = " +str(self.d)
        screen.title(title)
        #for the first point, just move the pen without leaving trace
        t.up()
        t.goto(xCoordinates[0], yCoordinates[0])
        t.down()
        
        #speed up the drawing! update every 20 points. Change these parameters to vary speed
        screen.tracer(20)
        t.speed(6)
       
        
        randColors = False #if True, change up colors randomly with each period
        t.color(self.color)
        sender=udp_client.SimpleUDPClient("127.0.0.1",4559)
        pointsCount = 0
        for each in range(len(xCoordinates)):
            t.goto(xCoordinates[each], yCoordinates[each])
            pointsCount = pointsCount + 1
            #additonal section to export x.y coords using OSC message
            if (pointsCount % (numPetals*2) == 0):
                sender.send_message('/xcoord',xCoordinates[each])
            if (pointsCount % (numPetals*4) ==0):
                sender.send_message('/ycoord',yCoordinates[each])            
            #end of additional section
            if (randColors):
                if (pointsCount % ptsPeriod == 0):
                   red = random.random()
                   green = random.random()
                   blue = random.random()
                   t.color(red, green, blue)
        t.hideturtle()
        print("Done drawing this curve")        
        time.sleep(2)
        sender.send_message("/finished","done")
    
    #clear the drawing surface after "sec" seconds. Limit time to 2 min just in case
    def clear(self, sec):
        
        if sec > 2*60:#reset time in case it's too long 
            sec = 10
        
        time.sleep(sec)
        self.t.getscreen().reset() #now reset the screen 
