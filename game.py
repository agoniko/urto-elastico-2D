import random
import numpy as np
from ball import Ball
import pygame
from time import sleep
import math


class Game:
    def __init__(self,width,height, rand):
        self.width = width
        self.height = height
        if rand:
            r1 = random.randrange(20,50)
            r2 = random.randrange(20,50)
            self.b1 = Ball(
                x = random.randrange(r1,width-r1),
                y = random.randrange(r1,height-r2),
                vx=random.randrange(-1000,1000),
                vy=random.randrange(-1000,1000),
                radius=r1
            )
            self.b2 = Ball(
                x = random.randrange(r2,width-r1),
                y = random.randrange(r2,height-r2),
                vx=random.randrange(-1000,1000),
                vy=random.randrange(-1000,1000),
                radius=r2
            )
        else:
            radius = 20 * height / 500
            self.b1 = Ball(
                x = radius,
                y = height - radius ,
                vx= height / 2, #px/s
                vy= -height / 4, #px/s
                radius=radius
            )
            self.b2 = Ball(
                x = radius + 5,
                y = radius,
                vx= height / 2, #px/s
                vy= height / 2, #px/s
                radius=radius
            )
        self.step = 0.01


    def urto(self,b1,b2):
        #i = [(b2.pos[0]-b1.pos[0])/(b1.radius+b2.radius),(b2.pos[1]-b1.pos[1])/(b1.radius+b2.radius)]
        i = [(b2.pos[0]-b1.pos[0]),(b2.pos[1]-b1.pos[1])]
        i = i/np.linalg.norm(i) #Normalizzo il versore a causa del problema di sovrapposizione si cerchi a causa di dt
        j = [i[1],-i[0]]
        print("i: ",i," j: ",j, "norm")

        c = b1.v #copio b1.v per calcolo velocità v2
        b1.v = np.add(np.inner(np.inner(b1.v,j),j),np.inner(np.inner(b2.v,i),i))
        b2.v = np.add(np.inner(np.inner(b2.v,j),j),np.inner(np.inner(c,i),i))

        while self.check_distance(b1,b2):
            b1.pos = np.add(b1.pos,np.inner(b1.v,self.step))
            b2.pos = np.add(b2.pos,np.inner(b2.v,self.step))
            print("b1: ",b1.pos, " b2:",b2.pos)
            if self.check_urto_bordi(b1,self.width, self.height):
                break
            if self.check_urto_bordi(b2,self.width, self.height):
                break

    def check_urto_bordi(self,ball,width,height):
        if ball.pos[0]-ball.radius<0 or ball.pos[0]+ball.radius>width:
            ball.v[0] = -ball.v[0]
        if ball.pos[1]-ball.radius<0 or ball.pos[1]+ball.radius>height:
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

    def attrito(self,b1,b2):
        c = 0.05
        g = 9.81 * 6250 * (self.step) #1m = 6250 px e devo rapportare a dt
        #g = g*4 #se lo schermo è in 4k
        at = -(c * g) * (self.step)
        v1 = math.sqrt(b1.v[0]**2+b1.v[1]**2)
        if v1 > 0:
            i = [b1.v[0] / v1, b1.v[1] / v1] # versore velocità
            b1.v = np.add(b1.v,np.inner(at,i)) #sommo V0 con at scomponendo tra asse x ed y con il versore i
            v2 = math.sqrt(b1.v[0] ** 2 + b1.v[1] ** 2)
            if v2 > v1:
                b1.v = [0,0]

        v2 = math.sqrt(b2.v[0]**2+b2.v[1]**2)
        if v2 > 0:
            i = [b2.v[0] / v2,b2.v[1] / v2] #versore velocità
            b2.v = np.add(b2.v, np.inner(at,i)) #sommo V0 con at scomponendo tra asse x ed y con il versore i
            v3 = math.sqrt(b2.v[0] ** 2 + b2.v[1] ** 2)
            if v3 > v2:
                b2.v = [0,0]




    def move(self,dt):
        self.check_urto_bordi(self.b1,self.width,self.height)
        self.check_urto_bordi(self.b2,self.width,self.height)
        if self.check_distance(self.b1,self.b2):
            #Urto tra palline
            self.urto(self.b1,self.b2)
        else:
            a = self.attrito(self.b1, self.b2)
            self.b1.pos = np.add(self.b1.pos,np.inner(self.b1.v,dt))
            self.b2.pos = np.add(self.b2.pos,np.inner(self.b2.v,dt))
            print("b1: ",self.b1.v, " b2:",self.b2.v)

        print(np.linalg.norm([np.linalg.norm(self.b1.v), np.linalg.norm(self.b2.v)]))


    def run(self):
        pygame.init()
        screen = pygame.display.set_mode([self.width, self.height])
        running = True
        t = 0
        while t in range(0, 1000) and running:
            screen.fill("white")
            pygame.draw.circle(screen, "black", (self.b1.pos[0], self.height - self.b1.pos[1]), self.b1.radius)
            pygame.draw.circle(screen, "red", (self.b2.pos[0], self.height - self.b2.pos[1]), self.b2.radius)
            sleep(self.step)
            # Flip the display
            pygame.display.flip()
            self.move(self.step)
        pygame.quit()

