from cmu_graphics import * 
import random
from PIL import Image
import os, pathlib

# SOUNDS NEEDED + IMAGES
# stomp, lanternfly rip splat, ohhhmuaaagawdddd for bang()
#########################################
############ IMAGES & SOUNDS ############
#########################################


#########################################
################# CHARS #################
#########################################
FLY_THRESHOLD = 3

class Foot:
    def __init__(self,cx,cy,app):
        self.cx,self.cy = cx,cy # this is mouse coordinates
        self.w = 60
        self.h = 100
        self.color = 'pink'
        self.hype = 0
        self.stomping = False

        self.killZoneCX = self.cx
        self.killZoneCY = (self.cy-(self.h/2)) + self.w/2
        self.killZoneSz = self.w/2 * 0.75


    def update(self,x,y):
        self.cx,self.cy=x,y
        self.killZoneCX,self.killZoneCY = x,(y-(self.h/2)) + self.w/2

    def draw(self,app):
        # left,top=self.cx-(self.w/2),self.cy-(self.h/2)
        # drawRect(left,top,self.w,self.h,fill=self.color)
        
        drawCircle(self.killZoneCX,self.killZoneCY,self.killZoneSz,fill=None,border='blue')
        if not self.stomping:
            drawRect(self.cx,self.cy,self.w,self.h,fill=self.color,align='center',opacity=50)
        else:
            drawRect(self.cx,self.cy,self.w,self.h,fill=self.color,align='center',border='hotpink',borderWidth=10,opacity=50)


class Fly:
    def __init__(self, cx, cy, bTime):
        self.cx = cx
        self.cy = cy
        self.size = 12
        self.color = 'lightgray'
        self.bTime = bTime # birth time bug time birth time
        self.age = 0 # 0 = young; 1 = old
        self.dx = 0
        self.dy = 0
        self.flightLen = 0
        self.alive = True

        self.image1 = Image.open("images/lanternfly2.png")
        self.imageWidth1,self.imageHeight1 = self.image1.width,self.image1.height
        self.image1 = CMUImage(self.image1)

        self.image2 = Image.open("images/lanternfly1.png")
        self.imageWidth2,self.imageHeight2 = self.image2.width,self.image2.height
        self.image2 = CMUImage(self.image2)


    def draw(self):
        if self.alive:
            angle = random.randrange(-30,30)
            scaledWidth1, scaledHeight1 = (self.imageWidth1//5,self.imageHeight1//5)
            drawImage(self.image1,self.cx,self.cy, width=scaledWidth1, height=scaledHeight1, align = 'center', rotateAngle=angle)
            # drawCircle(self.cx,self.cy,self.size,fill=self.color)
        else:
            # drawStar(self.cx,self.cy,self.size,20,fill='red')
            scaledWidth2, scaledHeight2 = (self.imageWidth2//5,self.imageHeight2//5)
            drawImage(self.image2,self.cx,self.cy, width=scaledWidth2, height=scaledHeight2, align = 'center')

    
    def move(self):
        if not self.alive:
            self.dx=0
            self.dy=0
        elif self.flightLen % 10 == 0:
            self.dx = random.randint(-5,5)
            self.dy = random.randint(-5,5)
        
            

    def update(self,app):
        if app.counter-self.bTime > FLY_THRESHOLD: 
            self.age=1
            self.color='brown'
        # circle of life check

        # bounds check
        if (self.cx - (self.size / 2) <= 0):
            self.cx = (self.size / 2)
        elif (self.cx + (self.size / 2) >= app.width):
            self.cx = app.width - (self.size / 2)
        if (self.cy - (self.size / 2) <= 0):
            self.cy = (self.size / 2)
        elif (self.cy + (self.size / 2) >= app.height):
            self.cy = app.height - (self.size / 2)
        
        self.cx += self.dx
        self.cy += self.dy
        self.flightLen += 1

def checkForIntersections(app):
    # Iterate through all pairs of flies to check for intersections
    for i in range(len(app.flies)):
        for j in range(i + 1, len(app.flies)):
            fly1, fly2 = app.flies[i], app.flies[j]
            if fly1.alive and fly2.alive:  # check for alive
                distance = dist(fly1.cx, fly1.cy, fly2.cx, fly2.cy)
                if distance <= (fly1.size + fly2.size):
                    return fly1, fly2
    return None, None


def bang(app, fly1, fly2): # i.e., flies bangin... sorry
    # for i in range(len(app.flies)-1)

    # checking for overlap (at least 2) 
    # 3: xyz
    # 4: xyz
    # 5: you lose immediately
    
    # both death + produce new
    fly1.alive = False
    fly2.alive = False

    newFlycx = (fly1.cx + fly2.cx) / 2
    newFlycy = (fly1.cy + fly2.cy) / 2
    app.flies.append(Fly(newFlycx, newFlycy, app.counter))

    print("bang!")


#########################################
################# UTILS #################
#########################################
def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def stompEvaluation(app):
    for fly in app.flies: # !!! POTENTIAL BUG 
        if fly.alive:
            distance = dist(fly.cx, fly.cy, app.foot.killZoneCX, app.foot.killZoneCY)
            if distance <= (fly.size + app.foot.killZoneSz):
                # fly.die()
                fly.alive=False # rip
                print('1 fly down')
            
            ######### yuki added sth here ########### - CHECK!
            else: # if not a perfect stomp
                if ((fly.cx+fly.size)>(app.foot.killZoneCX-app.foot.w/2) or
                    (fly.cx-fly.size)<(app.foot.killZoneCX+app.foot.w/2) or
                    (fly.cy+fly.size)>(app.foot.killZoneCY-app.foot.h/2) or
                    (fly.cy-fly.size)<(app.foot.killZoneCY+app.foot.h/2)):
                    fly.age += 50 # accelerate bug death


#########################################
################ DRAWING ################
#########################################

def onAppStart(app):
    app.foot=Foot(app.width/2,app.height/2,app)
    app.flies = [ ]
    app.counter = 0 
    for i in range(10):
        app.flies.append(Fly(random.randint(0,app.width),random.randint(0,app.height),app.counter))
    app.width = 400
    app.height = 400
    app.stepsPerSecond = 20 # default is 30?


def onStep(app):
    app.counter += 1/20

    for fly in app.flies:
        fly.move()
        fly.update(app)
    
    fly1, fly2 = checkForIntersections(app)

    if fly1 and fly2 != None and fly2.alive == True and fly2.alive == True:
        bang(app, fly1, fly2)

    

    
def onKeyPress(app,key):
    if key=='space':
        # app.foot.hype+=1
        app.foot.stomping=True
        # play stomp sound
        stompEvaluation(app)
        # print(f"stomp registered{'!'*app.foot.hype}")

def onKeyRelease(app,key):
    if key=='space':
        app.foot.stomping=False

def onMouseMove(app,mx,my):
    app.foot.update(mx,my)


def redrawAll(app):
    for fly in app.flies:
        fly.draw()
    app.foot.draw(app)
    




def main():
    runApp()
main()

