
import pygame
from pygame import *
import sys
import os


widthy = 800
heighty = 640
dead = False
half_widthy = int(widthy / 2)
half_heighty = int(heighty / 2)

DISPLAY = (widthy, heighty)

levels = list()

tileset_images = list()
tileset_block_width = 32
tileset_block_height = 32

platforms = None
entities = None
level_index = 0
player = None
camera = None
minimap_block_size = (3.0, 3.0)
door_wood_open_sound = None
door_wood_close_sound = None

def goto_level(dest_level_index, from_index = None, is_door = True):
    if is_door:
        if door_wood_open_sound is not None:
            door_wood_open_sound.play()
    load_level(levels[dest_level_index], dest_level_index, from_index, is_door)

def load_level(level, as_index, from_index = None, is_door = True):
    if is_door:
        if door_wood_close_sound is not None:
            door_wood_close_sound.play()
    # build the level
    global platforms, entities, player, camera, minimap_surface
    global minimap_block_size, level_index, is_first_spawn
    while len(platforms) > 0: platforms.pop()
    entities.empty()
    x = y = 0
    rows = cols = 0
    player.xvel = 0
    player.yvel = 0
    for row in level:
        cols = 0
        for col in row:
            if col == "P":
                p = Platform(x, y)
                platforms.append(p)
                entities.add(p)
            elif col == "E":
                e = ExitBlock(x, y)
                e.event_index = as_index + 1
                platforms.append(e)
                entities.add(e)
                if from_index is not None:
                    if from_index > as_index:
                        player.rect.left = x - player.rect.width - 1
            elif col == "B":
                e = ExitBlock(x, y)
                e.event_index = as_index - 1
                platforms.append(e)
                entities.add(e)
                if from_index is not None:
                    if from_index < as_index:
                        player.rect.left = x + 32 + 1
            x += 32
            cols += 1
        y += 32
        rows += 1
        x = 0

    total_level_width  = len(level[0])*32
    total_level_height = len(level)*32
    minimap_surface = Surface((cols*minimap_block_size[0], rows*minimap_block_size[1]))
    minimap_surface.convert()
    camera = Camera(simple_camera, total_level_width, total_level_height)
    entities.add(player)
    level_index = as_index
    #print("loaded level "+str(level_index)+" {"
    #    +"cols:"+str(cols)+"; "
    #    +"rows:"+str(rows)+"; "
    #    +"total_level_width:"+str(total_level_width)+"; "
    #    +"total_level_height:"+str(total_level_height)+"; "
    #    +"}")

def main():
    global cameraX, cameraY, screen, dead, levels
    global entities, platforms, level_index, player, camera, tileset_images
    global minimap_surface, minimap_block_size
    global door_wood_open_sound, door_wood_close_sound
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    timer = pygame.time.Clock()
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    try:
        pygame.mixer.music.load(os.path.join('data',"117818__oatmealcrunch__a2backw.ogg"))
        pygame.mixer.music.play(-1)
        door_wood_open_sound = pygame.mixer.Sound(os.path.join('data','door-wood-open.wav'))  #load sound
        door_wood_close_sound = pygame.mixer.Sound(os.path.join('data','door-wood-close.wav'))  #load sound
    except:
        print("Problem loading sound files in "+os.path.join(os.getcwd(),"data"))
        #raise UserWarning, "could not load or play soundfiles in folder"+os.getcwd()

    up = down = left = right = running = False
    bg = Surface((32,32))
    bg.convert()
    bg.fill(Color("#3090C7"))
    entities = pygame.sprite.Group()
    player = Player(64, 64)
    platforms = []

    tileset_image = pygame.image.load(os.path.join('data',"DungeonCrawl_ProjectUtumnoTileset.png"))
    tileset_image.convert_alpha()
    tileset_images.append(tileset_image)
    print("loaded tileset")
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                                          E",
        "P                         PPPPPP   PPPPP  PP",
        "P                 PPPP                     P",
        "P                                          P",
        "P    PPPPPPPP                              P",
        "P                                          P",
        "P                          PPPPPPP         P",
        "P                 PPPPPP                   P",
        "P                                          P",
        "P         PPPPPPP                          P",
        "P                                          P",
        "P                     PPPPPP               P",
        "P                                          P",
        "P   PPPPPPPPPPP                            P",
        "P                                          P",
        "P                 PPPPPPPPPPP              P",
        "P                                          P",
        "P        PPPP                              P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    levels.append(level)
    level = [
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "B                                          P",
        "PP                                         P",
        "P       PPP                         PPP    P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "P                                  PPPP    P",
        "P                                          P",
        "P                                          P",
        "P                                          P",
        "P                        PPPPP             P",
        "P                                          P",
        "P                                          P",
        "P                  PPPP                    P",
        "P                                          P",
        "P                                          P",
        "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
    levels.append(level)
    
    
    load_level(levels[level_index], level_index, is_door=False)
    
    playing = True
    while playing:
        #timer.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                #pygame.quit()
                #sys.exit()
                playing = False
                
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    #pygame.quit()
                    #sys.exit()
                    playing = False
                    print("pressed K_ESCAPE")
                elif e.key == K_w or e.key == K_UP:
                    up = True
                elif e.key == K_s or e.key == K_DOWN:
                    down = True
                elif e.key == K_a or e.key == K_LEFT:
                    left = True
                elif e.key == K_d or e.key == K_RIGHT:
                    right = True
                elif e.key == K_SPACE:
                    running = True
                    
            elif e.type == KEYUP:
                if e.key == K_w or e.key == K_UP:
                    up = False
                elif e.key == K_s or e.key == K_DOWN:
                    down = False
                elif e.key == K_a or e.key == K_LEFT:
                    left = False
                elif e.key == K_d or e.key == K_RIGHT:
                    right = False
        
        # draw background
        for y in range(32):
            for x in range(32):
                screen.blit(bg, (x * 32, y * 32))

        camera.update(player)

        # update player, draw everything else
        activate_event = player.update(up, down, left, right, running, platforms)
        if activate_event >= 0:
            if activate_event == 0:
                goto_level(0, from_index = level_index)
            if activate_event == 1:
                goto_level(1, from_index = level_index)
            else:
                print("unknown event "+str(activate_event))
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        if minimap_surface is not None:
            #minimap_surface.fill((0,0,0,0))
            minimap_surface.fill((0,0,0,0))
            for e in entities:
                col=int(e.rect.left/32)
                row=int(e.rect.top/32)
                minimap_surface.fill((255,255,255,255),((col*minimap_block_size[0], row*minimap_block_size[1]),(minimap_block_size[0],minimap_block_size[1])))
                #minimap_surface.set_at( (col,row) , (255,255,255,255) )
            minimap_surface.set_alpha(128)
            screen.blit(minimap_surface, (0,0))
        else:
            print("Missing minimap surface")

        #pygame.display.update()
        timer.tick(60)
        pygame.display.flip()
    print("finished main")
    
    

#This is the class that controls where the scrolling stops for the player
class Camera(object):
    def __init__(self, camera_func, widthy, heighty):
        self.camera_func = camera_func
        #the width and height of the level, we want to stop scrolling at the edges of the level
        self.state = Rect(0, 0, widthy, heighty)

    #Method to re-calculate the position on the screen to apply the scrolling
    def apply(self, target):
        return target.rect.move(self.state.topleft)

    #Update camera position once per loop
    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def average_color_of_surface(s):
    color0 = 0
    color1 = 0
    color2 = 0
    deepcolor0 = 0
    deepcolor1 = 0
    deepcolor2 = 0
    #deepcolor3 = 0
    x = -1
    y = -1
    try:
        if s is not None:
            thisRect = s.get_rect()
            divisor = float(thisRect.width * thisRect.height)
            for y in range(0,thisRect.height):
                for x in range(0,thisRect.width):
                    thisColor = s.get_at((x,y))
                    deepcolor0 += thisColor[0]
                    deepcolor1 += thisColor[1]
                    deepcolor2 += thisColor[2]
            color0 = int(float(deepcolor0) / divisor + .5)
            color1 = int(float(deepcolor1) / divisor + .5)
            color2 = int(float(deepcolor2) / divisor + .5)
    except:
        print("Could not finish average_color_of_surface"+str(sys.exc_info())+" {location:("+str(x)+","+str(y)+")}")
    result = (color0, color1, color2)
    return result
#We just take the position of our target, and add half total screen size.
def simple_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return Rect(-l+half_widthy, -t+half_heighty, w, h)

#functions to ensure we don't scroll outside of level.
def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+half_widthy, -t+half_heighty, w, h
    l = min(0, l)                        # stop scrolling at the left edge
    l = max(-(camera.width-widthy), l)   # stop scrolling at the right edge
    t = max(-(camera.height-heighty), t) # stop scrolling at the bottom
    t = min(0, t)                        # stop scrolling at the top
    return Rect(l, t, w, h)

class Entity(pygame.sprite.Sprite):
    nav_color = None
    event_index = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        nav_color = (255,255,255,255)

def point_is_in_rect(x, y, rect):
    result = False
    if (x is not None) and (y is not None) and (rect is not None):
        if (x>=rect.left) and (x<rect.right):
            if (y>=rect.top) and (y<rect.bottom):
                result = True
    return result
collide_count = 0
class Player(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        self.stand_r_image = pygame.image.load(os.path.join('data',"turtley-r.png"))
        self.stand_l_image = pygame.image.load(os.path.join('data',"turtley-l.png"))
        self.stand_l_image.convert_alpha()
        self.stand_r_image.convert_alpha()
        self.image = self.stand_r_image
        self.nav_color = average_color_of_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect = Rect(x, y, 64, 64)

    def update(self, up, down, left, right, running, platforms):
        activate_event = -1
        if up:
            # only jump if on the ground
            if self.onGround: self.yvel -= 10
        if down:
            pass
        if running:
            self.xvel = 12
        if left:
            self.xvel = -8
            self.image = self.stand_l_image
        if right:
            self.xvel = 8
            self.image = self.stand_r_image
        if not self.onGround:
            # only accelerate with gravity if in the air
            self.yvel += 0.3
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0
        # increment in x direction
        self.rect.left += self.xvel
        # do x-axis collisions
        result = self.collide(self.xvel, 0, platforms)
        if result >= 0:
            activate_event = result
        # increment in y direction
        self.rect.top += self.yvel
        # assuming we're in the air
        self.onGround = False;
        # do y-axis collisions
        result = self.collide(0, self.yvel, platforms)
        if result >= 0:
            activate_event = result
        return activate_event

    def collide(self, xvel, yvel, platforms):
        global collide_count
        activate_event = -1
        for p in platforms:
            if p.event_index is not None:
                if xvel > 0:
                    try_x = self.rect.right + 1
                    try_y = self.rect.bottom - 1
                    #print("player at "+str(try_x)+","+str(try_y))
                    #print("  event on right at "+str(p.rect.left)+","+str(p.rect.top))
                    #print ("player bottom: "+str(self.rect.bottom)+" block bottom:"+ str(p.rect.bottom))
                    #print ("player right: "+str(self.rect.right)+" block left:"+ str(p.rect.left))
                    if point_is_in_rect(try_x, try_y, p.rect):
                        activate_event = p.event_index
                        #print("activate event")
                elif xvel < 0:
                    try_x = self.rect.left - 1
                    try_y = self.rect.bottom - 1
                    #print("player at "+str(try_x)+","+str(try_y))
                    #print("  event on left at "+str(p.rect.left)+","+str(p.rect.top))
                    if point_is_in_rect(try_x, try_y, p.rect):
                        activate_event = p.event_index
                        #print("activate event")
            if pygame.sprite.collide_rect(self, p):
                if isinstance(p, ExitBlock):
                    activate_event = p.event_index
                if xvel > 0:
                    self.rect.right = p.rect.left
                    collide_count += 1
                    #print("collide right "+str(collide_count))
                if xvel < 0:
                    self.rect.left = p.rect.right
                    collide_count += 1
                    #print("collide left "+str(collide_count))
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
        return activate_event


class Platform(Entity):
    def __init__(self, x, y):
        Entity.__init__(self)
        self.image = pygame.image.load(os.path.join('data',"block 4,18.png"))
        self.image.convert_alpha()
        #self.image.fill(Color("#DDDDDD"))
        self.rect = Rect(x, y, 32, 32)

    def update(self):
        pass

class ExitBlock(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        #tileset_images[1].
        self.image = Surface((32,32))
        self.image.convert_alpha()
        #NOTE: coordinates start at 0,0 for first block in tileset image
        self.image.blit(tileset_images[0], (-23*tileset_block_width, -11*tileset_block_height))
        #self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
    main()