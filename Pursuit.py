#!/usr/bin/python
# Pursuit.py
"""
    Copyright (C) 2011  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,sys,buttons,load_save
import my_turtle2
try:
    import gtk
except:
    pass

class Pursuit:

    def __init__(self):
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py

    def display(self):
        g.screen.fill(g.bgd)
        g.screen.blit(g.tscreen,g.txy)
        if g.grid_on:
            g.screen.blit(g.grid,g.txy)
            if g.grid_nos:
                g.screen.blit(g.x_nos,g.x_nos_xy)
                g.screen.blit(g.y_nos,g.y_nos_xy)
                x,y=g.txy
                utils.display_number(0,(x,y+g.side),g.font2)
        pygame.draw.rect(g.screen,(0,0,150),(g.txy,(g.side,g.side)),2)
        my_turtle2.draw()
        self.panel()
        buttons.draw()

    def panel(self):
        x,y=g.panel_xy
        for ind in range(6):
            g.screen.blit(g.panel_imgl[ind],(x,y+g.panel_offset))
            if ind==g.carry_ind or g.turtles[ind].active:
                g.screen.blit(g.grey,(x,y+g.panel_offset))
            indr=g.turtles[ind].mate.ind
            g.screen.blit(g.panel_imgr[indr],(x+g.panel_dx,y))
            g.screen.blit(g.arrow,(x+g.arrow_dx,y+g.arrow_dy))
            y+=g.panel_dy

    def check_panell(self):
        x,y=g.panel_xy; img=g.panel_imgl[0]
        for ind in range(6):
            if utils.mouse_on_img(img,(x,y+g.panel_offset)):
                g.carry_ind=ind
                g.turtles[ind].active=False
                return True
            y+=g.panel_dy
        return False

    def check_panelr(self,left_click=True):
        x,y=g.panel_xy; img=g.panel_imgr[0]
        for ind in range(6):
            if utils.mouse_on_img(img,(x+g.panel_dx,y)):
                g.turtles[ind].angle=None # reset circle
                if left_click:
                    self.inc(ind); return True
                else:
                    self.dec(ind); return True
            y+=g.panel_dy
        return False

    def check_active(self):
        img=g.turtles[0].img
        for i in range(6):
            ind=5-i
            t=g.turtles[ind]
            if t.active:
                x=g.txy[0]+t.x; y=g.txy[1]+t.y
                if utils.mouse_on_img1(img,(x,y)):
                    t.active=False; g.carry_ind=ind; return True
        return False
                
    def inc(self,ind):
        m=g.turtles[ind].mate.ind+1
        if m==6: m=0
        g.turtles[ind].mate=g.turtles[m]

    def dec(self,ind):
        m=g.turtles[ind].mate.ind-1
        if m<0: m=5
        g.turtles[ind].mate=g.turtles[m]

    def do_click(self):
        if g.carry_ind!=None:
            g.turtles[g.carry_ind].put(); g.carry_ind=None; return True
        if self.check_active(): return True
        if self.check_panell(): return True
        if self.check_panelr(): return True
        return False

    def do_button(self,bu):
        if bu=='cls': my_turtle2.cls()
        elif bu=='run': g.running=not g.running
        elif bu=='grid': g.grid_on=not g.grid_on
        elif bu=='hide': g.turtles_on=not g.turtles_on

    def do_key(self,key):
        if key==pygame.K_n: g.grid_nos=not g.grid_nos; return
        if key==pygame.K_v: g.version_display=not g.version_display; return
        if key in g.NUMBERS:
            ind=g.NUMBERS[key]-1
            if g.carry_ind==None:
                g.carry_ind=ind; g.turtles[ind].active=False; return
            if g.carry_ind!=ind:
                g.turtles[g.carry_ind].active=False; g.carry_ind=ind
                g.turtles[ind].active=False

    def buttons_setup(self):
        cx=g.sx(3.7); cy=g.sy(16.4); dx=g.sy(3.6); dy=g.sy(3.3)
        buttons.Button('cls',(cx,cy)); cx+=dx
        buttons.Button('run',(cx,cy)); cx-=dx; cy+=dy
        buttons.Button('grid',(cx,cy)); cx+=dx
        buttons.Button('hide',(cx,cy))

    def flush_queue(self):
        flushing=True
        while flushing:
            flushing=False
            if self.journal:
                while gtk.events_pending(): gtk.main_iteration()
            for event in pygame.event.get(): flushing=True

    def run(self):
        g.init()
        if not self.journal: utils.load()
        my_turtle2.cls()
        load_save.retrieve()
        self.buttons_setup()
        if self.canvas<>None: self.canvas.grab_focus()
        ctrl=False
        pygame.key.set_repeat(600,120); key_ms=pygame.time.get_ticks()
        going=True
        while going:
            if self.journal:
                # Pump GTK messages.
                while gtk.events_pending(): gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT: # only in standalone version
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos=event.pos
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==1:
                        if self.do_click():
                            my_turtle2.do_towards()
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                    if event.button==3: # right click
                        self.check_panelr(False)
                        my_turtle2.do_towards()
                    self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    # throttle keyboard repeat
                    if pygame.time.get_ticks()-key_ms>110:
                        key_ms=pygame.time.get_ticks()
                        if ctrl:
                            if event.key==pygame.K_q:
                                if not self.journal: utils.save()
                                going=False; break
                            else:
                                ctrl=False
                        if event.key in (pygame.K_LCTRL,pygame.K_RCTRL):
                            ctrl=True; break
                        self.do_key(event.key); g.redraw=True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl=False
            if not going: break
            if g.running: my_turtle2.do()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                if g.carry_ind!=None:
                    utils.centre_blit(g.screen,g.turtles[g.carry_ind].img,g.pos)
                g.screen.blit(g.pointer,g.pos)
                pygame.display.flip()
                g.redraw=False
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((1024,768),pygame.FULLSCREEN)
    game=Pursuit()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
