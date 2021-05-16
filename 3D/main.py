import pygame as pg
import math
W = 1000
H = 1000
pg.init()
win = pg.display.set_mode((W, H))
win.fill((255, 255, 255))
pg.display.flip()
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
hero_list = []
wall_list = []


class Map():
    def __init__(self, map_file):        
        #добавляю матрицу
        with open(map_file, 'r') as map_open: 
            self.map_matrix = list(filter(lambda x: x != '', map_open.read().split('\n')))

        #превращаю матрицу в листы
        for y in range(len(self.map_matrix)):
            for x in self.map_matrix[y]:
                self.map_matrix[y] = list(map(int, self.map_matrix[y]))

        #записываю координаты всех стен и определяю положение героя
        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[y])):
                if self.map_matrix[y][x] == 2:
                    self.map_matrix[y][x] = 0
                    hero_list.append(Hero([W//len(self.map_matrix[0])*x, H//len(self.map_matrix)*y], 270, [len(self.map_matrix[0]), len(self.map_matrix)]))
        
                if self.map_matrix[y][x] == 1:
                    wall_list.append(Wall([W//len(self.map_matrix[0])*x, H//len(self.map_matrix)*y, W//len(self.map_matrix[0]), H//len(self.map_matrix)], \
                     [len(self.map_matrix[0]), len(self.map_matrix)]))

        #отрисовываю карту в консоли           
        for print_map_1 in self.map_matrix: 
            for print_map_2 in print_map_1:
                print(print_map_2, end=' ')
            print()
            
    def blit_2D(self):
        #отрисовываю карту на экране
        win.fill((255, 255, 255))
        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[0])):
                if self.map_matrix[y][x] == 1:
                    pg.draw.rect(win, BLACK, (W//len(self.map_matrix[0])*x, H//len(self.map_matrix)*y, W//len(self.map_matrix[0]), H//len(self.map_matrix)))
        pg.display.flip()


class Hero():    
    def __init__(self, spawn_position, spawn_eye_angle, xy_matrix):
        #создаю героя
        self.hero_crd = spawn_position
        self.eye_angle = spawn_eye_angle
        self.xy_matrix = xy_matrix
        self.vision_bullet = [self.hero_crd[0], self.hero_crd[1]]
        self.vision_list = []
        
    def vision(self):      
        #определяю центральное направление взгляда
        #cn = 0
        stop_while = False
        while stop_while == False:  
            for check_wall in wall_list:
                if check_wall.check_collision(self.vision_bullet[0], self.vision_bullet[1]) == True:
                    self.vision_list.append([self.vision_bullet, check_wall])
                    
                    self.vision_bullet = [self.hero_crd[0], self.hero_crd[1]]
                    stop_while = True
            self.vision_bullet[0] += math.cos(math.radians(self.eye_angle))
            self.vision_bullet[1] += math.sin(math.radians(self.eye_angle))
            #cn+=1
        #print(cn)

    def blit_2D(self):
        #отрисовываю героя
        pg.draw.circle(win, BLUE, self.hero_crd, 15)
        if len(self.vision_list) != 0:
            for vision_point in self.vision_list:
                pg.draw.line(win, BLUE, self.hero_crd, vision_point[0])
        pg.display.flip()




class Wall():    
    def __init__(self, wall_crd, xy_matrix):
        #создаю блок стены
        self.wall_crd = wall_crd
        self.xy_matrix = xy_matrix

    def check_collision(self, *outer_crd):
        #проверяю соприкосновение объектов
        def point_check(x_point, y_point):            
                if x_point <= self.wall_crd[0] + self.wall_crd[2] and x_point >= self.wall_crd[0] and y_point >= self.wall_crd[1] and y_point <= self.wall_crd[1] + self.wall_crd[3]:
                    return True
        #для объекта
        if len(outer_crd) ==  4:
            if point_check(outer_crd[0], outer_crd[1]) \
               or point_check(outer_crd[0]+ outer_crd[2], outer_crd[1]) \
               or point_check(outer_crd[0]+ outer_crd[2], outer_crd[1]+ outer_crd[3]) \
               or point_check(outer_crd[0], outer_crd[1]+ outer_crd[3]) == True:
                return True
        #для точки
        elif len(outer_crd) ==  2:
            if point_check(outer_crd[0], outer_crd[1]) == True:
                return True
        return False








map1= Map('map.txt')
for blit_hero in hero_list:
    blit_hero.vision()
    blit_hero.vision()
    print(blit_hero.vision_list)
while 1:        
    for event in pg.event.get():
        if event.type == pg.QUIT:                
            pg.quit()
            exit()

    key = pg.key.get_pressed()
    if key[pg.K_LEFT]:
        for blit_hero in hero_list:
            blit_hero.eye_angle-=1
    elif key[pg.K_RIGHT]:
        for blit_hero in hero_list:
            blit_hero.eye_angle+=1


            
    map1.blit_2D()
    for blit_hero in hero_list:
        
        blit_hero.blit_2D()
        blit_hero.vision_list = []
        blit_hero.vision()
    































