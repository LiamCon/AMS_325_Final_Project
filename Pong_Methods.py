from turtle import *
import random
import time
import numpy as np

def x_dist(turt1,turt2):                       #Gives x/y distances between two objects for block collisions
    return abs(turt1.xcor() - turt2.xcor())
def y_dist(turt1,turt2):
    return abs(turt1.ycor() - turt2.ycor())


class Block(Turtle):
    def __init__(self,pos,ball=None,pow1=0,pow2=0,pow3=0):
        super().__init__()
        self.ball = ball
        self.pow1 = pow1
        self.pow2 = pow2
        self.pow3 = pow3
        self.make_block(pos)
        self.move_lockout = False
        self.pow1_lockout = False
        self.pow2_lockout = False
        self.pow3_lockout = False
        self.pow2_is_active = False
        self.beam = None
        self.disabled = False
    def make_block(self,pos):
        self.penup()
        self.goto(pos)                     #Puts penup to avoid drawing line and creates block with specific width/height at given coords
        self.shape('square')
        self.width = 21
        self.height = 75
        self.shapesize(6,.7,1)
        self.move_dist = 40
        if self.xcor() > 0:              #Right block is red, left block is blue. Decorations in middle are white
            self.color('red')
        elif self.xcor() < 0:
            self.color('blue')
        else:
            self.color('white')
        self.block_color = self.pencolor()
    def set_other(self,block):
        self.other = block
    def go_up(self):
        if not self.move_lockout and self.ycor() < 320:
            y = self.ycor() + self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True
    def go_down(self):
        if not self.move_lockout and self.ycor() > -320:
            y = self.ycor() - self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True

    def psychic_bounce(self):
        if not self.pow1_lockout and self.pow1 > 0 and abs(self.ball.ycor()) < 320:
            color = self.ball.pencolor()
            x, y = self.ball.xcor(), self.ball.ycor()
            self.ball.color('DarkOrchid')
            time.sleep(.2)
            for i in range(10):
                self.ball.goto(x+random.choice([-1,0,1])*3,y+random.choice([-1,0,1])*3)
                time.sleep(.01)
            self.ball.goto(x,y)
            self.ball.x_vel = -1*self.ball.x_vel
            self.ball.color(color)
            self.pow1 -= 1
            self.pow1_lockout = True

    def golden_defense(self):
        if not self.pow2_lockout and self.pow2 > 0 and abs(self.ycor()) < 260:
            for i in range(3):
                self.shapesize(8+2*i,.7+.25*i,1)
                col = f'DarkGoldenrod{i+1}'
                self.color(col)
                time.sleep(.25)
            self.width *= 1.3
            self.height *= 2

            self.move_dist *= 2
            self.pow2 -= 1
            self.pow2_lockout = True
            self.pow2_is_active = True

    def disable_beam(self):
        if not self.pow3_lockout and self.pow3 > 0:
            self.pow3_lockout = True
            self.pow3 -= 1
            self.beam = Turtle()
            self.beam.penup()
            self.beam.hideturtle()
            self.beam.speed(6)
            self.beam.color(self.pencolor())
            self.beam.goto(self.xcor(),self.ycor())
            self.beam.pendown()
            self.beam.goto(-self.xcor(),self.ycor())
            if y_dist(self.beam,self.other) < self.other.height:
                self.other.move_lockout = True
                self.other.disabled = True
                self.other.color('gray')
            self.beam.clear()
            self.beam = None







class Ball(Turtle):
    def __init__(self,pos):
        super().__init__()
        self.make_ball(pos)
        self.x_vel = 0
        self.y_vel = 0
        self.collision = True
    def make_ball(self,pos):
        self.penup()
        self.goto(pos)
        self.shape('circle')
        self.shapesize(1,1,1)
        self.color('gray')
    def initial_takeoff(self,speed,number_flag):
        if number_flag != 0:
            self.hideturtle()
            self.goto(0,0)
            self.showturtle()
        else:
            self.goto(0, 0)
        self.color('gray')
        self.x_vel = speed * random.choice([-1,1])
        self.y_vel = speed * random.choice([-1, 1])

    def move(self):
        x = self.xcor() + self.x_vel
        y = self.ycor() + self.y_vel
        self.goto((x,y))
    def bounce(self,x_flag,y_flag,accel_mode):
        if accel_mode != 'a':
            if x_flag == 1:
                self.x_vel = -self.x_vel
            if y_flag == 1:
                self.y_vel = -self.y_vel
        else:
            if x_flag == 1:
                self.x_vel = -1.1*self.x_vel
            if y_flag == 1:
                self.y_vel = -1.05*self.y_vel





class Scoreboard(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.score1 = 0
        self.score2 = 0
        self.left = Turtle()
        self.right = Turtle()
        self.make_scoreboard()
        self.pos1 = (-240,300)
        self.pos2 = (160, 300)
        self.left.goto(self.pos1)
        self.right.goto(self.pos2)
        self.left.color('blue')
        self.right.color('red')


    def make_scoreboard(self):
        self.left.penup()
        self.right.penup()
        self.left.hideturtle()
        self.right.hideturtle()

    def display(self, turt):
        if turt == self.left:
            self.score1 += 1  # Increment left score
            self.left.goto(self.pos1[0] + self.score1*15,self.pos1[1])
            self.left.write('|', font=('Comic Sans', 40))

        elif turt == self.right:

            self.score2 += 1  # Increment right score
            self.right.goto(self.pos2[0] + self.score2 * 15, self.pos2[1])
            self.right.write('|', font=('Comic Sans', 40))

    def victory(self):
        if self.score1 > self.score2:
            self.left.goto(-240,100)
            self.left.write(f'Blue Wins!',font=('Comic Sans', 80))
            self.left.goto(-260, 10)
            time.sleep(1)
            self.left.write(f'Score is', font=('Comic Sans', 80))
            self.left.goto(170,10)
            self.left.write(f'{self.score1}', font=('Comic Sans', 80))
            self.left.goto(230, 10)
            self.left.write(':', font=('Comic Sans', 80))
            self.right.goto(255,10)
            self.right.write(f'{self.score2}',font=('Comic Sans', 80))
        else:
            self.right.goto(-240,100)
            self.right.write(f'Red Wins!',font=('Comic Sans', 80))
            self.right.goto(-260,10)
            time.sleep(1)
            self.right.write(f'Score is', font=('Comic Sans', 80))
            self.left.goto(170, 10)
            self.left.write(f'{self.score1}', font=('Comic Sans', 80))
            self.right.goto(230, 10)
            self.right.write(':', font=('Comic Sans', 80))
            self.right.goto(255, 10)
            self.right.write(f'{self.score2}', font=('Comic Sans', 80))


class Portal(Turtle):
    def __init__(self, pos_1, pos_2):
        super().__init__()
        self.port1 = Turtle()
        self.port2 = Turtle()
        self.teleported = False
        self.radius = 3
        self.hideturtle()
        self.port1.penup()
        self.port2.penup()
        self.port1.goto(pos_1)
        self.port2.goto(pos_2)
        self.port1.color('purple')
        self.port2.color('dark violet')
        self.port1.shape('circle')
        self.port2.shape('circle')
        self.port1.shapesize(self.radius,self.radius,0)
        self.port2.shapesize(self.radius,self.radius, 0)

    def teleport(self,portal,ball):
        if portal == self.port1:
            ball.hideturtle()
            ball.goto(self.port2.pos())
            ball.showturtle()

        else:
            ball.hideturtle()
            ball.goto(self.port1.pos())
            ball.showturtle()
        self.teleported = True

