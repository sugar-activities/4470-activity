# g.py - globals
import pygame,utils,my_turtle2,grid_surface

app='Pursuit'; ver='1.0'
ver='1.1'
# panel
ver='1.2'
# n -> x,y co-ords
ver='1.3'
# grey right turtle
ver='21'
ver='22'
# flush_queue() doesn't use gtk on non-XO

UP=(264,273)
DOWN=(258,274)
LEFT=(260,276)
RIGHT=(262,275)
CROSS=(259,120)
CIRCLE=(265,111)
SQUARE=(263,32)
TICK=(257,13)
NUMBERS={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4,\
           pygame.K_5:5,pygame.K_6:6}

def init(): # called by run()
    global redraw
    global screen,w,h,font1,font2,clock
    global factor,offset,imgf,message,version_display
    global pos,pointer
    redraw=True
    version_display=False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70,0,70))
    pygame.display.flip()
    w,h=screen.get_size()
    if float(w)/float(h)>1.5: #widescreen
        offset=(w-4*h/3)/2 # we assume 4:3 - centre on widescreen
    else:
        h=int(.75*w) # allow for toolbar - works to 4:3
        offset=0
    factor=float(h)/24 # measurement scaling factor (32x24 = design units)
    imgf=float(h)/900 # image scaling factor - all images built for 1200x900
    clock=pygame.time.Clock()
    if pygame.font:
        t=int(40*imgf); font1=pygame.font.Font(None,t)
        t=int(60*imgf); font2=pygame.font.Font(None,t)
    message=''
    pos=pygame.mouse.get_pos()
    pointer=utils.load_image('pointer.png',True)
    pygame.mouse.set_visible(False)
    
    # this activity only
    global pattern,side,tscreen,txy,aaline,unit,turtles,turtles_on,running,ms
    global limit # how close
    global x1,x2,y1,y2 # turtle screen limits
    global panel_xy,panel_dy,panel_imgl,panel_dx,panel_imgr,panel_offset
    global carry_ind,grid,grid_on,grid_step,step
    global arrow,arrow_dx,arrow_dy
    global bgd,x_nos,y_nos,x_nos_xy,y_nos_xy,grid_nos,grey
    pattern=1 # not used
    side=int(sy(20.5)+.5)
    tscreen=pygame.Surface((side,side))
    txy=(sx(11),sy(.5))
    aaline=True
    try:
        pygame.draw.aaline(tscreen,utils.BLACK,(1,1),(2,2))
    except:
        aaline=False
    unit=sy(.03)
    turtles=[]; ind=0
    for colour in\
        (utils.RED,utils.GREEN,utils.BLUE,utils.ORANGE,\
         utils.CYAN,utils.MAGENTA,utils.WHITE):
        turtle=my_turtle2.Turtle(colour,ind)
        turtles.append(turtle); ind+=1
    for ind in range(6):
        j=ind+1
        if ind==5: j=0
        turtles[ind].mate=turtles[j]
    turtles_on=True
    running=False
    ms=pygame.time.get_ticks()
    limit=sy(.5) # how close
    d=turtles[0].img.get_width()/2
    x1,y1=txy; x2=x1+side; y2=y1+side
    x1+=d; y1+=d; x2-=d; y2-=d
    panel_xy=sx(1.2),sy(1.2); panel_dy=sy(2.2); panel_imgl=[]
    for ind in range(6):
        img=utils.load_image(str(ind)+'.png',True,'right')
        panel_imgl.append(img)
    panel_dx=sy(7); panel_imgr=[]
    for ind in range(6):
        img=utils.load_image(str(ind)+'.png',True,'up')
        panel_imgr.append(img)
    panel_offset=sy(.4)
    carry_ind=None
    t=100
    grid_step=16
    grid=grid_surface.grid(grid_step,grid_step,side,(t,t,t))
    grid_on=False
    step=10 # turtle step each cycle (in turtle units)
    arrow=utils.load_image('arrow.png',True)
    arrow_dx,arrow_dy=sx(2.4),sy(.6)
    bgd=(192,255,255)
    s=side/grid_step
    x_nos=pygame.Surface((side+s,s))
    x_nos.fill(utils.WHITE); x_nos.set_colorkey(utils.WHITE)
    y_nos=pygame.Surface((s+sy(.2),side+s))
    y_nos.fill(utils.WHITE); y_nos.set_colorkey(utils.WHITE)
    x,y=txy; x_nos_xy=(x-s/2,y+side-sy(.2)); y_nos_xy=(x-s-sy(.2),y-sy(.95))
    x=s/2; y=x
    for n in range(1,grid_step+1):
        x+=s; utils.display_number2(x_nos,n,(x,y),font1)
    x=s/2; y=x
    for i in range(grid_step):
        n=16-i
        utils.display_number3(y_nos,n,(x,y),font1); y+=s
    grid_nos=False
    grey=utils.load_image('grey.png',True)
    
def sx(f): # scale x function
    return f*factor+offset

def sy(f): # scale y function
    return f*factor
