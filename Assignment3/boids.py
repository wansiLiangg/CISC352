# CISC352
# Assignment 3 Boids Problem
# Christina Hu  
# Derek Huang   
# Jie Niu       
# Wansi Liang   
# Xing Wang     

import random
from tkinter import *

#Variables definitions
Gwidth = 1024
Gheight = 768
Gboids = 50
GboidRadius = 3
Gspeed = 800
Gacceleration = 15
Gside = 500
GfromSide = 50

#Initialize a 2D vector
def twoDInitializer(input1, input2):
    return [float(input1), float(input2)]

#2D array addition
def pointAddition(input1, input2):
    return [float(input1[0] + input2[0]), float(input1[1] + input2[1])]

#2D array subtraction
def pointSubtraction(input1, input2):
    return [float(input1[0] - input2[0]), float(input1[1] - input2[1])]

#2D array division
def pointDivision(input1, input2):
    return [float(input1[0] / input2), float(input1[1] / input2)]

#Norm of a 2D array
def pointNorm(input):
    return (input[0] ** 2 + input[1] ** 2) ** 0.5

#Boid Initialization and rules
class Boid:

    #Initialize boid velocity and position
    def __init__(self):
        self.velocity = twoDInitializer(0, 0)
        self.position = twoDInitializer(*self.randNum())

    #Random boid position
    def randNum(self):
        if random.choice([True, False]):
            yCoordinate = random.randint(1, Gheight)
            if random.choice([True, False]):
                xCoordinate = -GfromSide
            else:
                xCoordinate = Gwidth + GfromSide
        else:
            xCoordinate = random.randint(1, Gwidth)
            if random.choice([True, False]):
                yCoordinate = -GfromSide
            else:
                yCoordinate = Gheight + GfromSide
        return xCoordinate, yCoordinate

    #Boid rule No.1 -- cohesion
    def rule1(self):
        vector = twoDInitializer(0, 0)
        for boid in Gboidsval:
            if boid is not self:
                vector = pointAddition(vector, boid.position)
        vector = pointDivision(vector, len(Gboidsval) - 1)
        return pointDivision(pointSubtraction(vector, self.position), 7.5)

    #Boid rule No.2 -- separation
    def rule2(self):
        vector = twoDInitializer(0, 0)
        for boid in Gboidsval:
            if boid is not self:
                if pointNorm(pointSubtraction(self.position, boid.position)) < 25:
                    vector = pointSubtraction(vector, pointSubtraction(boid.position, self.position))
        return vector

    #Boid rule No.3 -- alignment
    def rule3(self):
        vector = twoDInitializer(0, 0)
        for boid in Gboidsval:
            if boid is not self:
                vector = pointAddition(vector, boid.velocity)
        vector = pointDivision(vector, len(Gboidsval) - 1)
        return pointDivision(pointSubtraction(vector, self.velocity), 2)

    #Update boid velocity
    def newVelocity(self):
        vector1 = self.rule1()
        vector2 = self.rule2()
        vector12 = pointAddition(vector1, vector2)
        vector3 = self.rule2()
        self.temp = pointAddition(vector12, vector3)

    #Move boids to new position
    def move(self):
        self.velocity = pointAddition(self.velocity, self.temp)
        speedLimitation(self)
        self.position = pointAddition(self.position, pointDivision(self.velocity, 100))

#Build the GUI interface
def graph():
    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (Gwidth, Gheight, (root.winfo_screenwidth() - Gwidth) / 2, (root.winfo_screenheight() - Gheight) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    global Ggraph
    Ggraph = Canvas(root, width = Gwidth, height = Gheight, background='white')
    Ggraph.after(40, update)
    Ggraph.pack()

#Create boids on GUI
def draw():
    # Draw all boids.
    Ggraph.delete(ALL)
    for boid in Gboidsval:
        x1 = boid.position[0] - GboidRadius
        y1 = boid.position[1] - GboidRadius
        x2 = boid.position[0] + GboidRadius
        y2 = boid.position[1] + GboidRadius
        Ggraph.create_oval((x1, y1, x2, y2), fill = 'red')
    Ggraph.update()

#Create viewing boundaries on GUI
def collision(boid):
    if boid.position[0] < Gside:
        boid.velocity[0] += Gacceleration
    elif boid.position[0] > Gwidth - Gside:
        boid.velocity[0] -= Gacceleration
    if boid.position[1] < Gside:
        boid.velocity[1] += Gacceleration
    elif boid.position[1] > Gheight - Gside:
        boid.velocity[1] -= Gacceleration

#Move boids on GUI
def move():
    for boid in Gboidsval:
        collision(boid)
    for boid in Gboidsval:
        boid.newVelocity()
    for boid in Gboidsval:
        boid.move()

#Limit boids speed
def speedLimitation(boid):
    if pointNorm(boid.velocity) > Gspeed:
        boid.velocity = pointDivision(boid.velocity, pointNorm(boid.velocity) / Gspeed)

#Create boids variable
def boids():
    global Gboidsval
    Gboidsval = tuple(Boid() for boid in range(Gboids))

#Collision loop
def update():
    draw()
    move()
    Ggraph.after(40, update)

#Main function
def main():
    boids()
    graph()
    mainloop()

main()
