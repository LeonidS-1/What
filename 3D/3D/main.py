import pygame as pg
import math
W = 1000
H = 1000
W_3D = 1600
H_3D = 900
pg.init()

win = pg.display.set_mode((W_3D, H_3D), pg.NOFRAME)
fps_clock = pg.time.Clock()
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
hero_list = []
wall_list = []
FOV = 90
minicard = 5
toscrange = 1125


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
                    hero_list.append(Hero([W//len(self.map_matrix[0])*x, H//len(self.map_matrix)*y], 270, [len(self.map_matrix[0]), len(self.map_matrix)], self.map_matrix))
        
                if self.map_matrix[y][x] == 1:
                    wall_list.append(Wall([W//len(self.map_matrix[0])*x, H//len(self.map_matrix)*y, W//len(self.map_matrix[0]), H//len(self.map_matrix)], [len(self.map_matrix[0]), len(self.map_matrix)]))

        #отрисовываю карту в консоли           
        for print_map_1 in self.map_matrix: 
            for print_map_2 in print_map_1:
                print(print_map_2, end=' ')
            print()
            
    def blit_2D(self):
        #отрисовываю карту на экране
        pg.draw.rect(win, WHITE, ((W_3D-H_3D/minicard), 0, int(H_3D/minicard), int(H_3D/minicard)))
        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[0])):
                if self.map_matrix[y][x] == 1:
                    pg.draw.rect(win, BLACK, (H_3D/minicard//len(self.map_matrix[0])*x+(W_3D-H_3D/minicard), H_3D/minicard//len(self.map_matrix)*y, H_3D/minicard//len(self.map_matrix[0]), H_3D/minicard//len(self.map_matrix)))
        

    def blit_3D(self, vision_list):
        win.fill(WHITE) 
        self.vision_list = vision_list 

        # self.vision_list.sort(key=lambda x: x[3])
        # self.vision_list.reverse()    
        #print(self.vision_list)
        for i in range(len(self.vision_list)) :
            self.vision_list[i][3] = self.vision_list[i][3]//2*2
        pg.draw.rect(win, (135, 206, 235), [0, 0, W_3D, H_3D//2])
        pg.draw.rect(win, (128, 128, 128), [0, H_3D//2, W_3D, H_3D//2])
        for i in range(len(self.vision_list)-1):
            screen_blit = (toscrange*H_3D)/(toscrange+100*self.vision_list[i][3])
            screen_blit_scnd = (toscrange*H_3D)/(toscrange+100*self.vision_list[i+1][3])
            pg.draw.polygon(win, BLACK,[ [self.vision_list[i][2]+W_3D//2, (H_3D - screen_blit)//2], [self.vision_list[i][2]+W_3D//2, (H_3D + screen_blit)//2],
                                        [self.vision_list[i+1][2]+W_3D//2, (H_3D + screen_blit_scnd)//2], [self.vision_list[i+1][2]+W_3D//2, (H_3D - screen_blit_scnd)//2]],  )
            pg.draw.aalines(win, BLUE, 1, [ [self.vision_list[i][2]+W_3D//2, (H_3D - screen_blit)//2], [self.vision_list[i][2]+W_3D//2, (H_3D + screen_blit)//2],
                                        [self.vision_list[i+1][2]+W_3D//2, (H_3D + screen_blit_scnd)//2], [self.vision_list[i+1][2]+W_3D//2, (H_3D - screen_blit_scnd)//2]],  3)
            #pg.draw.line(win, BLUE, [self.vision_list[i][2]+W_3D//2, (H_3D - screen_blit)//2], [self.vision_list[i][2]+W_3D//2, (H_3D + screen_blit)//2])
            i+=1

class Hero():    
    def __init__(self, spawn_position, spawn_eye_angle, xy_matrix, map_matrix):
        #создаю героя
        self.hero_crd = spawn_position
        self.eye_angle = spawn_eye_angle
        self.xy_matrix = xy_matrix
        self.vision_bullet = [self.hero_crd[0], self.hero_crd[1]]
        self.vision_list = []
        self.map_matrix = map_matrix
        
    def vision(self):      
        #определяю центральное направление взгляда
        for angle_change in range(-W_3D//2, W_3D//2):
            stop_while = False
            S_count = 0
            
            while stop_while == False:               
                if  self.map_matrix[int((self.vision_bullet[1]*len(self.map_matrix))//H)][int((self.vision_bullet[0]*len(self.map_matrix))//W)] :
                    check_wall = [self.vision_bullet[1]//len(self.map_matrix), self.vision_bullet[0]//len(self.map_matrix)]
                    if len(self.vision_list)>=2:
                        if  (check_wall[0] == self.vision_list[-1][1][0] and check_wall[0] == self.vision_list[-2][1][0]) or \
                            (check_wall[1] == self.vision_list[-1][1][1] and check_wall[1] == self.vision_list[-2][1][1]):
                            self.vision_list.pop(-1)

                    
                    self.vision_list.append([self.vision_bullet, check_wall, angle_change, S_count])
                    
                    self.vision_bullet = [self.hero_crd[0], self.hero_crd[1]]
                    stop_while = True
                self.vision_bullet[0] += 10* math.cos(math.radians(self.eye_angle + angle_change * (FOV//2) / (W_3D//2)))
                self.vision_bullet[1] += 10* math.sin(math.radians(self.eye_angle + angle_change * (FOV//2) / (W_3D//2)))
                S_count += 1
        #print(self.vision_list)    

    def blit_2D(self):
        #отрисовываю героя
        pg.draw.circle(win, BLUE, [self.hero_crd[0]/minicard-H_3D/minicard//len(self.map_matrix[0])+(W_3D-H_3D/minicard), self.hero_crd[1]/minicard-H_3D/minicard//len(self.map_matrix[0])], H_3D/minicard//self.xy_matrix[0]//4)
        if len(self.vision_list) != 0:
            for vision_point in range(len(self.vision_list)):
                if vision_point == 0 or vision_point == len(self.vision_list)-1:
                    pg.draw.line(win, BLUE, [self.hero_crd[0]/minicard+(W_3D-H_3D/minicard)-H_3D/minicard//len(self.map_matrix[0]), self.hero_crd[1]/minicard-H_3D/minicard//len(self.map_matrix[0])], [self.vision_list[vision_point][0][0]/minicard-H_3D/minicard//len(self.map_matrix[0])+(W_3D-H_3D/minicard), 
                    self.vision_list[vision_point][0][1]/minicard-H_3D/minicard//len(self.map_matrix[0])])
        

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
                return False
        #для точки
        elif len(outer_crd) ==  2:
            if point_check(outer_crd[0], outer_crd[1]) == True:
                return False
        return True


map1 = Map('lvl_1_map.txt')

for blit_hero in hero_list:   
    blit_hero.vision()
    map1.blit_3D(blit_hero.vision_list)
map1.blit_2D()
for blit_hero in hero_list: 
    blit_hero.blit_2D()
pg.display.update()

while 1:        
    for event in pg.event.get():
        if event.type == pg.QUIT:                
            pg.quit()
            exit()
    
    key = pg.key.get_pressed()
    change_k = H//333
    for blit_hero in hero_list:
        if key[pg.K_LEFT]:        
            blit_hero.eye_angle-=1
        elif key[pg.K_RIGHT]:        
            blit_hero.eye_angle+=1
        if key[pg.K_ESCAPE]: 
            pg.quit()
            exit()
        if key[pg.K_w]:
            true_move = [blit_hero.hero_crd[0]+change_k*math.cos(math.radians(blit_hero.eye_angle)), blit_hero.hero_crd[1]+change_k*math.sin(math.radians(blit_hero.eye_angle))]                    
        elif key[pg.K_s]:
            true_move = [blit_hero.hero_crd[0]-change_k*math.cos(math.radians(blit_hero.eye_angle)), blit_hero.hero_crd[1]-change_k*math.sin(math.radians(blit_hero.eye_angle))]
        elif key[pg.K_d]:
            true_move = [blit_hero.hero_crd[0]-change_k*math.sin(math.radians(blit_hero.eye_angle)), blit_hero.hero_crd[1]+change_k*math.cos(math.radians(blit_hero.eye_angle))]
        elif key[pg.K_a]:
            true_move = [blit_hero.hero_crd[0]+change_k*math.sin(math.radians(blit_hero.eye_angle)), blit_hero.hero_crd[1]-change_k*math.cos(math.radians(blit_hero.eye_angle))]
        #print(wall_check.check_collision(true_move))
        if key[pg.K_w] or key[pg.K_s] or key[pg.K_a] or key[pg.K_d]:
            for wall_check in wall_list:
                if not wall_check.check_collision(true_move[0], true_move[1]):   
                    break
            else:
                blit_hero.hero_crd = true_move   
                                           
    map1.blit_3D(blit_hero.vision_list)  
    map1.blit_2D()
    blit_hero.blit_2D()
    
    blit_hero.vision_list = []
    blit_hero.vision()
    pg.display.flip()
        
    fps_clock.tick(10)































