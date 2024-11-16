print('Lanternfly Extermination Co.')

from cmu_graphics import * 
import random


# SOUNDS NEEDED
# stomp, lanternfly rip splat, ohhhmuaaagawdddd for bang()


### CHARS

FLY_THRESHOLD = 3

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


    def update(self,x,y):
        self.cx,self.cy=x,y
        self.killZoneCX,self.killZoneCY=x,(y-(self.h/2)) + self.w/2

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
        self.color = 'gray'
        self.bTime = bTime # birth time bug time birth time
        self.age = 0 # 0 = young; 1 = old
        self.dx = 0
        self.dy = 0
        self.flightLen = 0
        self.alive = True


    def draw(self):
        if self.alive:
            drawCircle(self.cx,self.cy,self.size,fill=self.color)
        else:
            drawStar(self.cx,self.cy,self.size,20,fill='red')

    
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
    # for i in range(len(app.flies)-1)

    # checking for overlap (at least 2) 
    # 3: xyz
    # 4: xyz
    # 5: you lose immediately
    for i in range(len(app.flies)):
        for j in range(i + 1, len(app.flies)):
            fly1, fly2 = app.flies[i], app.flies[j]
            if fly1.alive and fly2.alive:  # check for alive
                distance = dist(fly1.cx, fly2.cx, fly1.cy, fly2.cy)
                if distance <= fly1.size + fly2.size:
                    # both death + produce new
                    fly1.alive = False
                    fly2.alive = False
                    app.flies.append(Fly(fly1.cx, fly1.cy, fly1.size))
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
    if app.counter <= 60:
        app. seanson = 'summer'
    elif app.counter > 60 and app.counter <= 120:
        app. seanson = 'fall'
    elif app.counter > 120 and app.counter <= 180:
        app. seanson = 'winter'

def checkGameStatue(app):
    # check game over 
    if app.aliveFly >= 15:
        app.gameOver == True
    elif app.season == 'winter' and app.aliveFly > 0:
        app.gameOver == True
    # check win
    if app.season != 'winter' and app.aliveFly == 0:
        app.win == True

########## batch import images #############
'''
# Get all files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

# Batch import and process images
images = []
for filename in image_files:
    img = Image.open(path).convert("RGBA")  # Ensure RGBA mode for transparency
    images.append(img)
'''

### DRAWING

def onAppStart(app):
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

def onStep(app):
    app.counter += 1/20
    seasonChange(app)

    for fly in app.flies:
        fly.move()
        fly.update(app)
        if fly.alive:
            app.aliveFly += 1    
    checkGameStatue(app)

    bang(app)
    
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
