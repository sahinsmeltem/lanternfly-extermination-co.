from cmu_graphics import * 
import random
from PIL import Image
import os, pathlib


# SOUNDS NEEDED
# stomp, lanternfly rip splat, ohhhmuaaagawdddd for bang()


### CHARS

MATURE_THRESHOLD = 3
DEAD_THRESHOLD = 10

class Foot:
    def __init__(self,cx,cy,app):
        self.cx,self.cy=cx,cy # this is mouse coordinates
        self.w=60
        self.h=100
        self.color='pink'
        self.hype=0
        self.stomping=False

        self.killZoneCX = self.cx
        self.killZoneCY = (self.cy-(self.h/2)) + self.w/2
        self.killZoneSz = self.w/2 * 0.75

        #### import foot images ####
        self.img1 = Image.open("images/shoeFf1.png")
        self.img2 = Image.open("images/shoeNb1.png")
        self.img3 = Image.open("images/shoeNike1.png")
        
        self.imageWidth,self.imageHeight = self.img1.width,self.img1.height
        

        self.img1 = CMUImage(self.img1)
        self.img2 = CMUImage(self.img2)
        self.img3 = CMUImage(self.img3)
        
    
    def draw(self,app): 
        drawCircle(self.killZoneCX,self.killZoneCY,self.killZoneSz,fill=None,border='blue')
        scaledWidth, scaledHeight = (self.imageWidth // 5, self.imageHeight // 5)
        if app.season == 'spring':
            img = self.img3
            drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
        elif app.season == 'summer':
            img = self.img1
            drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
        elif app.season == 'fall':
            img = self.img2
            drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
        else:
            img = self.img2
            drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')


    def update(self,x,y):
        self.cx,self.cy=x,y
        self.killZoneCX,self.killZoneCY=x,(y-(self.h/2)) + self.w/2

    


class Fly:
    def __init__(self, cx, cy, bTime):
        self.cx = cx
        self.cy = cy
        self.size = 12
        self.color = 'gray'
        self.bTime = bTime # birth time bug time birth time
        self.age = 0 # 0 = young; 1 = old
        self.dx = 0
        self.dy = 0
        self.flightLen = 0
        self.alive = True

        self.situation = 'young'
        

        #### import fly images ####
        self.img1 = Image.open("images/lanternfly1.png")
        self.imageWidth,self.imageHeight = self.img1.width,self.img1.height
        
        self.img2 = Image.open("images/lanternfly2.png")
        self.imageWidth,self.imageHeight = self.img2.width,self.img2.height

        self.img3 = Image.open("images/lanternfly3.png")
        self.imageWidth,self.imageHeight = self.img2.width,self.img2.height

        self.imgSplat = Image.open("images/lanternflySplat.png")
        self.imageWidth,self.imageHeight = self.img2.width,self.img2.height

        self.img1 = CMUImage(self.img1)
        self.img2 = CMUImage(self.img2)
        self.img3 = CMUImage(self.img3)
        self.imgSplat = CMUImage(self.imgSplat)
        

    def draw(self):
        if self.alive:
            if self.situation == 'mature':
                angle = random.randrange(-30, 30)
                img = self.img2
                scaledWidth, scaledHeight = (self.imageWidth // 5, self.imageHeight // 5)
                drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center', rotateAngle=angle)
            elif self.situation == 'young':
                img = self.img1
                scaledWidth, scaledHeight = (self.imageWidth // 5, self.imageHeight // 5)
                drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
        else:
            if self.situation == 'natural dead':
                img = self.img3
                scaledWidth, scaledHeight = (self.imageWidth // 5, self.imageHeight // 5)
                drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
            elif self.situation == 'stomped':
                img = self.imgSplat
                scaledWidth, scaledHeight = (self.imageWidth // 5, self.imageHeight // 5)
                drawImage(img, self.cx, self.cy, width=scaledWidth, height=scaledHeight, align='center')
            

    
    def move(self):
        if not self.alive:
            self.dx=0
            self.dy=0
        elif self.flightLen % 10 == 0:
            self.dx = random.randint(-5,5)
            self.dy = random.randint(-5,5)
        
            

    def update(self,app):
        if app.counter-self.bTime > MATURE_THRESHOLD: 
            self.situation = 'mature'
        elif app.counter-self.bTime > DEAD_THRESHOLD: 
            self.alive = False
            self.situation = 'natural dead'
        # circle of life check
        bang(app)
        
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



def bang(app): # i.e., flies bangin... sorry
    for i in range(len(app.flies)):
        for j in range(i + 1, len(app.flies)):
            fly1, fly2 = app.flies[i], app.flies[j]
            if fly1.alive and fly2.alive:  # check for alive
                distance = dist(fly1.cx, fly2.cx, fly1.cy, fly2.cy)
                if distance <= fly1.size + fly2.size:
                    # both death + produce new
                    fly1.alive = False
                    fly2.alive = False

                    newFlycx = (fly1.cx + fly2.cx) / 2
                    newFlycy = (fly1.cy + fly2.cy) / 2
                    app.flies.append(Fly(newFlycx, newFlycy, app.counter))
                    
                    print("bang!")

                    

### UTILS
def dist(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def stompEvaluation(app):
    for fly in app.flies: # !!! POTENTIAL BUG 
        if fly.alive:
            distance = dist(fly.cx, fly.cy, app.foot.killZoneCX, app.foot.killZoneCY)
            if distance <= (fly.size + app.foot.killZoneSz):
                # fly.die()
                fly.alive=False # rip
                fly.situation = 'stomped'
                print('1 fly down')
            ############################################
            ############## yuki add sth here ###########
            ############## copy paste next lines #######
            else: # if not a perfect stomp
                if ((fly.cx+fly.size)>(app.foot.killZoneCX-app.foot.w/2) or
                    (fly.cx-fly.size)<(app.foot.killZoneCX+app.foot.w/2) or
                    (fly.cy+fly.size)>(app.foot.killZoneCY-app.foot.h/2) or
                    (fly.cy-fly.size)<(app.foot.killZoneCY+app.foot.h/2)):
                    fly.age += 50 # accelerate bug death

def seasonChange(app):
    if 3 <= app.counter <= 6:
        app.season = 'summer'
    elif app.counter > 6 and app.counter <= 9:
        app.season = 'fall'
    elif app.counter > 9 and app.counter <= 12:
        app.season = 'winter'

def checkGameStatus(app):
    # # check game over 
    # if app.aliveFly >= 15:
    #     app.gameOver == True
    # elif app.season == 'winter' and app.aliveFly > 0:
    #     app.gameOver == True
    # # check win
    # if app.season != 'winter' and app.aliveFly == 0:
    #     app.win == True

     # check game over 
    # if app.aliveFly >= 100:
    #     app.gameOver = True
    #     app.win = False
    # elif app.season == 'winter' and app.aliveFly > 0:
    #     app.gameOver = True
    #     app.win = False
    # check win
    if app.season != 'winter' and app.aliveFly < 3:
        app.gameOver = True
        app.win = True
        print('should be over, you won')

def drawBg(app):
    bg1 = Image.open("images/bg/bgSpring.png")    
    bg1 = CMUImage(bg1)

    bg2 = Image.open("images/bg/bgSummer.png")    
    bg2 = CMUImage(bg2)

    bg3 = Image.open("images/bg/bgFall.png")    
    bg3 = CMUImage(bg3)

    bg4 = Image.open("images/bg/bgWinter.png")    
    bg4 = CMUImage(bg4)


    if app.season == 'spring':
        drawImage(bg1,app.width/2, app.height/2, width=app.width, height=app.height, align = 'center')
    elif app.season == 'summer':
        drawImage(bg2,app.width/2, app.height/2, width=app.width, height=app.height, align = 'center')
    elif app.season == 'fall':
        drawImage(bg3,app.width/2, app.height/2, width=app.width, height=app.height, align = 'center')
    else:
        drawImage(bg4,app.width/2, app.height/2, width=app.width, height=app.height, align = 'center')                    


def reset(app):
    app.foot=Foot(app.width/2,app.height/2,app)
    app.flies = [ ]
    app.counter = 0 
    for i in range(10):
        app.flies.append(Fly(random.randint(0,app.width),random.randint(0,app.height),app.counter))
    app.width = 400
    app.height = 400
    app.stepsPerSecond = 20 # default is 30?
    app.aliveFly = 0
    app.gameOver = False
    app.win = False
    app.season = 'spring'
    app.reset=False


def onAppStart(app):
    reset(app)
    app.welcomeScreen=True

def onStep(app):
    app.counter += 1/20
    seasonChange(app)

    
    if app.reset:
        reset(app)

    ct=0
    for fly in app.flies:
        fly.move()
        fly.update(app)
        if fly.alive:
            ct+=1
    app.aliveFly = ct
    checkGameStatus(app)

    bang(app)
    
def onKeyPress(app,key):
    if key=='space':
        # app.foot.hype+=1
        app.foot.stomping=True
        # play stomp sound
        stompEvaluation(app)
        # print(f"stomp registered{'!'*app.foot.hype}")
    if key=='r':
        app.reset = True

def onKeyRelease(app,key):
    if key=='space':
        app.foot.stomping=False

def onMouseMove(app,mx,my):
    app.foot.update(mx,my)


# def redrawAll(app):
#     if not app.gameOver:
#         drawBg(app)
#         for fly in app.flies:
#             fly.draw()
#         app.foot.draw(app)
#     else:
#         reset(app)


def redrawAll(app): #LESLIE CHANGED THIS FUNCTION ENTIRELY
    if app.gameOver:
        if app.win:
            drawLabel('YES, YOU DID IT.', 200, 170, size=40, bold=True, font='impact', fill='black')
        else:
            drawLabel('YOU FAILED US.', 200, 170, size=40, bold=True, font='impact', fill='black')
            drawLabel('GAME OVER', 200, 200, size=44, bold=True, font='arial', fill='black')
        drawLabel('press r to restart', 200, 385, size=15, bold=True, font='arial', fill='black')    
        
    else:
        drawBg(app) # draw bg based on season
        if app.welcomeScreen and app.counter<1:
            drawLabel('Lanternfly Stomper 4000'.upper(), 200, 200, size=33, bold=True, font='impact', fill='black')
            drawLabel(f'move mouse to position foot'.upper(), 200, 325, size=15, bold=True, font='arial', fill='black')
            drawLabel(f'press space to stomp'.upper(), 200, 345, size=15, bold=True, font='arial', fill='black')
            
            drawLabel(f'starting in {3-int(app.counter)}...'.upper(), 200, 385, size=15, bold=True, font='arial', fill='black')
        else:
            for fly in app.flies:
                fly.draw()
            app.foot.draw(app)


def main():
    runApp()
main()

