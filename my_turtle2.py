# my_turtle2.py

import g,pygame,math,utils,buttons

def cls():
    g.tscreen.fill(utils.CREAM)
    for turtle in g.turtles: turtle.active=False
    g.running=False; buttons.clear()
    g.grid_on=False; g.turtles_on=True

def do():
    d=pygame.time.get_ticks()-g.ms
    if d>50:
        m=g.limit
        for i in range(6):
            t1=g.turtles[i]
            if t1.active:
                t1.running=True
                t2=t1.mate
                if t2==t1: #circle
                    if t1.angle==0: return # no circle if radius too small
                    if t1.angle==None: set_angle(t1)
                    t1.rt(t1.angle) # angle set in do_towards()
                else:
                    if t2.active:
                        towards(t1,t2)
                        connect(t1,t2)
                        if abs(t1.x-t2.x)<m and abs(t1.y-t2.y)<m:
                            t1.running=False
        for i in range(6):
            t1=g.turtles[i]
            if t1.active:
                if t1.running:
                    if t1.mate.active: t1.fd(g.step)
        g.ms=pygame.time.get_ticks()
        g.redraw=True

def draw():
    if g.turtles_on:
        for turtle in g.turtles:
            if turtle.active:
                imgr=pygame.transform.rotate(turtle.img,-turtle.h)
                x=g.txy[0]+turtle.x; y=g.txy[1]+turtle.y
                if x<g.x1: continue
                if x>g.x2: continue
                if y<g.y1: continue
                if y>g.y2: continue
                utils.centre_blit(g.screen,imgr,(x,y))

def towards(t1,t2):
    x1=t1.x; y1=t1.y; x2=t2.x; y2=t2.y
    dx=x2-x1; dy=y1-y2
    a=math.degrees(math.atan2(dx,dy))
    t1.h=a

def do_towards():
    for t1 in g.turtles:
        if t1.active:
            t2=t1.mate
            if t1!=t2:
                if t2.active: towards(t1,t2)
            else:
                if t1.angle==None: set_angle(t1)

def set_angle(t1):
    rad=radius(t1)
    if rad<5: t1.angle=0; return
    towards(t1,g.turtles[6]) # towards centre
    t1.lt(90)
    stp=g.step*g.unit # convert to pixel units cf radius
    t1.angle=math.degrees(math.asin(stp/2.0/rad))
    t1.rt(-t1.angle)
    t1.angle*=2.0
    t1.pen=True

def connect(t1,t2):
    x1=t1.x; y1=t1.y; x2=t2.x; y2=t2.y; colour=t1.colour
    if g.aaline:
        pygame.draw.aaline(g.tscreen,colour,(x1,y1),(x2,y2))
    else:
        pygame.draw.line(g.tscreen,colour,(x1,y1),(x2,y2))

def radius(t1):
    t2=g.turtles[6] # centre
    x1=t1.x; y1=t1.y; x2=t2.x; y2=t2.y
    dx=x1-x2; dy=y1-y2
    d=math.sqrt(dx*dx+dy*dy)
    return d

class Turtle:
    def __init__(self,colour,ind):
        self.colour=colour; self.ind=ind
        if ind<6:
            self.img=utils.load_image(str(ind)+'.png',True)
        self.home()
        self.active=False # in turtle screen
        self.running=False
        self.pen=False
        self.mate=self
        self.angle=None # for circle

    def home(self):
        self.x=g.side/2; self.y=self.x; self.h=0

    def fd(self,d):
        n=g.unit*d; rad=math.radians(self.h)
        x1=self.x; y1=self.y
        x2=x1+n*math.sin(rad); y2=y1-n*math.cos(rad)
        self.x=x2; self.y=y2
        if x1<0 or x1>g.side: return
        if x2<0 or x2>g.side: return
        if y1<0 or y1>g.side: return
        if y2<0 or y2>g.side: return
        if self.pen:
            if g.aaline:
                pygame.draw.aaline(g.tscreen,self.colour,(x1,y1),(x2,y2))
            else:
                pygame.draw.line(g.tscreen,self.colour,(x1,y1),(x2,y2))
            
    def bk(self,d):
        self.fd(-d)
        
    def rt(self,a):
        self.h+=a
        if self.h>=360: self.h-=360

    def lt(self,a):
        self.rt(-a)

    def put(self): # put turtle at mouse location
        x,y=g.pos; x0,y0=g.txy
        x-=x0; y-=y0
        if x<0 or x>g.side: self.active=False; return
        if y<0 or y>g.side: self.active=False; return
        self.x=x; self.y=y; self.active=True
        self.angle=None; self.h=0
    
       
        
