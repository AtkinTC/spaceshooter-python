import sys, pygame
from pygame.locals import *
import pygame.font
import pygame.image
import pygame.transform
from shape import *
import math

w, h = 320,240
screen = None
font = None

tile = None

image_dict = {}
image_dict_large = -1

camera = None

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def init(width=320, height=240):
    global screen, w, h, font, tile, camera
    w = width
    h = height
    screen = pygame.display.set_mode((w,h))
    screen.fill((0,0,0))
    pygame.font.init()
    font = pygame.font.SysFont(None, 15)
    camera = Pnt()

def get_dimensions():
    return Pnt(w,h)

def camera_translate(pnt):
    global camera
    camera = camera+pnt

def camera_set(pnt):
    global camera
    camera = pnt

def camera_align(pnt):
    return pnt - camera + Pnt(w/2,h/2)

def get_camera():
    return camera

def load_image(name, alpha=False):
    global image_dict, image_dict_large
    im = pygame.image.load(name)
    if alpha:
        im = im.convert_alpha(screen)
    else:
        im = im.convert(screen)

    id = 0
    while id in image_dict:
        id += 1
    image_dict_large = max(image_dict_large, id)
    image_dict[id] = im
    return id

def draw_image(id, pos, area=None, angle=0, cam=True):
    im = image_dict.get(id, None)
    
    if im:
        if angle:
            d = (im.get_width()*2, im.get_height()*2)
            im = pygame.transform.smoothscale(im, d)
            im = pygame.transform.rotate(im, angle)
            d = (im.get_width()/2, im.get_height()/2)
            im = pygame.transform.smoothscale(im, d)

        pos = pos-Pnt(im.get_width(),im.get_height())/2
        if cam:
            pos = camera_align(pos)
        screen.blit(im, pos.tuple(), area)

def fill(x, y, w, h, r, g, b):
    screen.fill((r,g,b),(x,y,w,h))

def draw_shape(shape, rgb, cam=True):
    if shape.type == 'poly':
        draw_shape_polygon(shape, rgb, cam)
    elif shape.type == 'circle':
        draw_shape_circle(shape, rgb, cam)
    elif shape.type == 'point':
        draw_shape_point(shape, rgb, cam)

def draw_shape_polygon(polygon, rgb, cam):
    points = polygon.get_points()
    if cam:
        points = map(camera_align, points)
    points = [p.tuple() for p in points]
    pygame.draw.polygon(screen, rgb, points, 1)

def draw_shape_circle(circle, rgb, cam):
    pnt = circle.centre
    if cam:
        pnt = camera_align(pnt)
    pygame.draw.circle(screen, rgb, pnt.tuple(), circle.radius, 1)

def draw_shape_point(point, rgb, cam):
    centre = point.centre
    if cam:
          centre  = camera_align(centre)
    screen.fill(rgb, (centre.x, centre.y, 1, 1))

def draw_rect(rect, rgb, cam=True, width = 1):
    p, w, h = rect.tuple()
    if cam:
        p = camera_align(p)
    pygame.draw.rect(screen, rgb, (p.x, p.y, w, h), width) 

def draw_shape_bound(shape, r, g, b, cam=True):
    p, w, h = shape.bounding_box().tuple()
    if cam:
        p = camera_align(p)
    pygame.draw.rect(screen, (r,g,b), (p.x,p.y,w,h), 1)
    
def draw_point(pos, r, g, b):
    pygame.draw.line(screen, (r,g,b), pos, pos, 1)
        
def draw_line(pos1, pos2, r, g, b, width=1):
    pygame.draw.line(screen, (r,g,b), pos1, pos2, width)

def draw_circle(pos, rad, r, g, b):
    pygame.draw.circle(screen, (r,g,b), pos, rad)

def draw_arc(pos, rad, ang1, ang2, r, g, b, width=1):
    rect = (pos[0]-rad, pos[1]-rad, rad*2, rad*2)
    pygame.draw.arc(screen, (r,g,b), rect, ang1, ang2, width)

def draw_poly(poly, r, g, b, width=0):
    pygame.draw.polygon(screen, (r,g,b), poly, width)
    #poly.append(poly[0])
    #for i in range(len(poly)-1):
    #    draw_line(poly[i], poly[i+1], r,g,b)

def draw_text(text, pos, r,g,b):
    text = font.render(text, True, (r,g,b))
    screen.blit(text, pos)

def flip(col = (0,0,0)):
    pygame.display.flip()
    screen.fill(col)
