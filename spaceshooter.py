import sys, pygame, math
from pygame.locals import *
import time
import pygame.time
import pygame.font
import pygame.image
import collision
import draw
from draw_call import *
import entity
import background
import input
from shape import *
from random import randint
from pygame.time import Clock

from gl_texture import GL_Texture

import entity_control
import texture_control

from camera import Camera


clock = 0

game_dimensions = width, height = 0, 0

#entities = None

camera = None
player_id = None

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init():
    global clock, game_dimensions, width, height, camera, player_id

    pygame.init()

    clock = 0

    game_dimensions = width, height = 640, 480

    draw.init(width, height)

    camera = Camera(width, height)

    entity_control.init()

    player_ship = GL_Texture('graphics\\ship.tif')

    bullet1 = GL_Texture('graphics\\bullet_6x6.tif')
    target1 = GL_Texture('graphics\\target_30x30.tif')
    dust1 = GL_Texture('graphics\\layers\\dust_640x480_1.tif')
    dust2 = GL_Texture('graphics\\layers\\dust_640x480_2.tif')
    dust3 = GL_Texture('graphics\\layers\\dust_800x800_1.tif')
    planet1 = GL_Texture('graphics\\layers\\planet_154x154_1.tif')
    planet2 = GL_Texture('graphics\\layers\\planet_40x40_1.tif')
    starfield = GL_Texture('graphics\\layers\\starfield_640x480_1.tif')
    test = GL_Texture('graphics\\layers\\test_400x400.tif')

    entities = {}
    shape = Polygon([Pnt(0,-15),Pnt(10,15), Pnt(-10,15)], Pnt())
    player_id = entity_control.register(entity.Player(player_ship, shape, 0.0005, 0.2, 0.005, bullet1))

    shape = Circle(15)
    entity_control.register(entity.Enemy(target1, shape, Pnt(300, 300), None))

    entity_control.register(background.Background_scrolling(dust1, 0.5, 4))
    entity_control.register(background.Background_scrolling(dust2, 1.0, 3))
    entity_control.register(background.Background_scrolling(dust3, 2.0, 3))
    entity_control.register(background.Background_object(Pnt(0, 0), planet1, 4, 2))
    entity_control.register(background.Background_object(Pnt(0, 0), planet2, 6, 1))
    entity_control.register(background.Background_scrolling(starfield, 20, 0))

    for e in entity_control.yield_entities():
        e.set_camera(camera)
    
    


init()

count = 0
#main loop
done = False
fps_clock = Clock()
delta = 0
player_move = Pnt()
debug = False
while not done:
    clock = pygame.time.get_ticks()
    mx, my = pygame.mouse.get_pos()
    input.mpos = Pnt(mx, my)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            #print event.key
            if event.key == 96:
                debug = not debug
            #W
            if event.key == 119:
                input.player_move.y += -1
            #S
            if event.key == 115:
                input.player_move.y += 1
            #A
            if event.key == 97:
                input.player_move.x += -1
            #D
            if event.key == 100:
                input.player_move.x += 1
        if event.type == pygame.KEYUP:
            #W
            if event.key == 119:
                input.player_move.y += 1
            #S
            if event.key == 115:
                input.player_move.y += -1
            #A
            if event.key == 97:
                input.player_move.x += 1
            #D
            if event.key == 100:
                input.player_move.x += -1
        if event.type == pygame.MOUSEBUTTONDOWN:
            input.player_shoot = True
        if event.type == pygame.MOUSEBUTTONUP:
            input.player_shoot = False

    #update loop

    for e in entity_control.yield_entities():
        e.update(delta)


    #collisions

    e_list = [e for e in entity_control.yield_entities()]

    type_map = {'background':0, 'player': 1, 'enemy':2, 'bullet':4}

    for i in range(len(e_list)-1):
        for j in range(i+1, len(e_list)):
            e1 = e_list[i]
            e2 = e_list[j]
            tc = type_map[e1.type]+type_map[e2.type]
            collision_pnt = None
            if tc == 6:
                collision_pnt = collision.shape_collide(e1.get_shape_proper(), e2.get_shape_proper())
            if collision_pnt:
                e1.collide(e2.id, collision_pnt)
                e2.collide(e1.id, collision_pnt)

    entity_control.kill_finalize()

    player = entity_control.entity_dict[player_id]
    camera.set_pos(player.pos-player.velocity*delta)
    
    #draw loop

    draw_list = Draw_Call_List()

    for e in entity_control.yield_entities():
        draw_list.append(e.draw(debug))

    draw.draw_loop(draw_list)
              
    #draw.draw_text(str(clock/1000.0), (0,0), 255, 255, 255)
    #draw.draw_text(str(fps_clock.get_fps()), (40,0), 255, 255, 255)
    #draw.draw_text(str(map(int, player.pos.tuple())), (0,30), 255, 255, 255)

    #draw.draw_text(str(input.player_move), (0,15), 255, 255, 255)

    print fps_clock.get_fps()

    delta = fps_clock.get_time()
    fps_clock.tick()
    
    #draw.flip()

pygame.quit()
