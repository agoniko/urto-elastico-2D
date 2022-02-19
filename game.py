from table import Table
import numpy as np
from ball import Ball
import pygame
from time import sleep


class Game:
    def __init__(self):
        self.table = Table(500,300)
        self.b1 = Ball(x = 30, y = 30, vx=35, vy=-100, radius=20, mass=10)
        self.b2 = Ball(x = 200, y = 200, vx=-500, vy=200, radius=20, mass=10)
        self.step = 0.01


    def urto(self,b1,b2):
        i = [(b2.pos[0]-b1.pos[0])/(b1.radius+b2.radius),(b2.pos[1]-b1.pos[1])/(b1.radius+b2.radius)]
        j = [i[1],-i[0]]

        c = b1.v #copio b1.v per calcolo velocità v2
        b1.v = np.add(np.inner(np.dot(b1.v,j),j),np.inner(np.dot(b2.v,i),i))
        b2.v = np.add(np.inner(np.dot(b2.v,j),j),np.inner(np.dot(c,i),i))
        while self.check_distance(b1,b2):
            b1.pos = np.add(b1.pos,np.inner(b1.v,self.step))
            b2.pos = np.add(b2.pos,np.inner(b2.v,self.step))
            print("b1: ",b1.pos, " b2:",b2.pos)
            if self.check_urto_bordi(b1,self.table):
                break
            if self.check_urto_bordi(b2,self.table):
                break

    def check_urto_bordi(self,ball,table):
        if ball.pos[0]-ball.radius<0 or ball.pos[0]+ball.radius>table.width:
            ball.v[0] = -ball.v[0]
        if ball.pos[1]-ball.radius<0 or ball.pos[1]+ball.radius>table.height:
            ball.v[1] = -ball.v[1]

    def check_distance(self,b1,b2):
        x1 = b1.pos[0]
        y1 = b1.pos[1]
        x2 = b2.pos[0]
        y2 = b2.pos[1]
        r1 = b1.radius
        r2 = b2.radius
        if (x1 - x2) ** 2 + (y1 - y2) ** 2 <= (r1 + r2) ** 2:
            return True
        else:
            return False


    def move(self,dt):
        self.check_urto_bordi(self.b1,self.table)
        self.check_urto_bordi(self.b2,self.table)

        if self.check_distance(self.b1,self.b2):
            #Urto tra palline
            self.urto(self.b1,self.b2)
        else:
            self.b1.pos = np.add(self.b1.pos,np.inner(self.b1.v,dt))
            self.b2.pos = np.add(self.b2.pos,np.inner(self.b2.v,dt))
            print("b1: ",self.b1.pos, " b2:",self.b2.pos)


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([self.table.width, self.table.height])
        running = True
        t = 0
        while t in range(0, 1000) and running:
            screen.fill("white")
            pygame.draw.circle(screen, "black", (self.b1.pos[0], self.table.height - self.b1.pos[1]), self.b1.radius)
            pygame.draw.circle(screen, "red", (self.b2.pos[0], self.table.height - self.b2.pos[1]), self.b2.radius)
            sleep(self.step)
            # Flip the display
            pygame.display.flip()
            self.move(self.step)

        pygame.quit()
