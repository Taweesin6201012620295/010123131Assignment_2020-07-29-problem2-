import pygame
import pygame.camera
from pygame.locals import *
import sys

# For windows 10, install VideoCapture 
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#videocapture

# Open Terminal in VSCode and run the following command
# $  pip install VideoCapture 

class Pos_rect():
    def __init__(self,tl,tr,rw,rh):
        self. tl = tl
        self. tr = tr
        self. rw = rw
        self. rh = rh
        self. Pos = (tl,tr,rw,rh)
    def Draw(self,I):
        self.I = I
        pygame.draw.rect(self.I,(82,200,220),self.Pos,1)
        surface.blit( self.I, (self.tl,self.tr,self.rw,self.rh), self.Pos)

def open_camera( frame_size=(1280, 720),mode='RGB'):
    pygame.camera.init()
    list_cameras = pygame.camera.list_cameras()
    print( 'Mumber of cameras found: ', len(list_cameras) )
    if list_cameras:
        # use the first camera found
        camera = pygame.camera.Camera(list_cameras[0], frame_size, mode )
        return camera 
    return None

#Click Black rect
def Cleck_rect(List_st,Pos):
    for p in List_st:
        if int(p.tl)< int(Pos[0]) < int(p.tl+p.rw) and int(p.tr) <int(Pos[1]) < int(p.tr+p.rh):
            return p
        else :
            pass

List_st = []
List_ch = []
scr_w, scr_h = 1000, 600

pygame.init()

camera = open_camera()

if camera:
    camera.start()
else:
    print('Cannot open camera')
    sys.exit(-1)

screen = pygame.display.set_mode((scr_w, scr_h))

surface = pygame.Surface( screen.get_size(), pygame.SRCALPHA )

M,N = 10,10
rw, rh = scr_w//M, scr_h//N
for i in range(M):
    for j in range(N): 
        e = Pos_rect(i*rw,j*rh,rw,rh)
        List_st.append(e)

img = None
is_running = True
while is_running:

    for t in List_st:
        t.Draw(surface)

    if len(List_ch) > 0 :
        for p in List_ch:
            p.Draw(img)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            is_running = False
            if img:
                # save the current image into the output file
                pygame.image.save( img, 'image.jpg' )
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            Deif = Cleck_rect(List_st,pos)

            if Deif == None :
                pass
            else :

                if Deif not in List_ch:
                    List_ch.append(Deif)
                else:
                    Deif2 = Cleck_rect(List_ch,pos)

        elif e.type == pygame.MOUSEBUTTONUP:
            pos1 = pygame.mouse.get_pos() 
            Deif3 = Cleck_rect(List_ch,pos1)

            if Deif3 in List_ch and Deif3 != Deif:
                Deif4 = Cleck_rect(List_ch,pos1)
                Deif2.Pos , Deif4.Pos = Deif4.Pos , Deif2.Pos

    # try to capture the next image from the camera 
    img = camera.get_image()
    if img is None:
        continue

    # get the image size
    img_rect = img.get_rect()
    img_w, img_h = img_rect.w, img_rect.h

    # write the surface to the screen and update the display
    screen.blit( surface, (0,0) )
    pygame.display.update()

# close the camera
camera.stop()

print('Done....')