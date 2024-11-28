from turtle import *
import random
import time
import numpy as np

def x_dist(turt1,turt2):
    return abs(turt1.xcor() - turt2.xcor())
def y_dist(turt1,turt2):
    return abs(turt1.ycor() - turt2.ycor())


class Block(Turtle):
    def __init__(self,pos):
        super().__init__()
        self.make_block(pos)

    def make_block(self,pos):
        self.penup()
        self.goto(pos)
        self.shape('square')
        self.width = 21
        self.height = 75
        self.shapesize(6,.7,1)
        if self.xcor() > 0:
            self.color('red')
        elif self.xcor() < 0:
            self.color('blue')
        else:
            self.color('white')
    def go_up(self):
        if self.ycor() < 320:
            y = self.ycor() + 40
            self.goto((self.xcor(),y))
    def go_down(self):
        if self.ycor() > -320:
            y = self.ycor() - 40
            self.goto((self.xcor(),y))





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
    def bounce(self,x_flag,y_flag):
        if x_flag == 1:
            self.x_vel = -self.x_vel
        if y_flag == 1:
            self.y_vel = -self.y_vel




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
            self.left.goto(-200,100)
            self.left.write(f'Blue Wins!',font=('Comic Sans', 80))
            self.left.goto(-220, 10)
            time.sleep(1)
            self.left.write(f'Score is {self.score1}:{self.score2}', font=('Comic Sans', 80))
        else:
            self.right.goto(-200,100)
            self.right.write(f'Red Wins!',font=('Comic Sans', 80))
            self.right.goto(-220,10)
            time.sleep(1)
            self.right.write(f'Score is {self.score1}:{self.score2}',font=('Comic Sans', 80))




