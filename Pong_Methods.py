from turtle import *
import random
import time


def x_dist(turt1,turt2):                       #Gives x/y distances between two objects for block collisions
    return abs(turt1.xcor() - turt2.xcor())
def y_dist(turt1,turt2):
    return abs(turt1.ycor() - turt2.ycor())


class Block(Turtle):

    #Create a block at a given position with access to the ball and 3 power counters

    def __init__(self,pos,disp1=None,disp2=None,disp3=None,ball=None,pow1=0,pow2=0,pow3=0):
        super().__init__()
        self.disp1 = disp1                            #Disp1/2/3 are used to display the number of uses of each powerup for each plater
        self.disp2 = disp2
        self.disp3 = disp3
        self.ball = ball
        self.pow1 = pow1                              #Number of each powerup
        self.pow2 = pow2
        self.pow3 = pow3
        self.make_block(pos)
        self.move_lockout = False
        self.pow1_lockout = False                    #Creates blocks with all lockout flags set to false, with no status effects or beam active
        self.pow2_lockout = False
        self.pow3_lockout = False
        self.pow2_is_active = False
        self.beam = None
        self.disabled = False
        if self.disp1 is not None:
            self.disp1.write(f'{self.pow1}', font=('Comic Sans', 15))
        if self.disp2 is not None:
            self.disp2.write(f'{self.pow2}', font=('Comic Sans', 15))
        if self.disp3 is not None:
            self.disp3.write(f'{self.pow3}', font=('Comic Sans', 15))
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
        self.other = block                               #Will be used to designate opponent's block as "other" in order to access it easily for powerups
    def go_up(self):
        if not self.move_lockout and self.ycor() < 320:             #Move up if the block is not too high and starts move lockout
            y = self.ycor() + self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True
    def go_down(self):
        if not self.move_lockout and self.ycor() > -320:
            y = self.ycor() - self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True

    def psychic_bounce(self):

        #Power 1, freezes ball and causes it to shake before reversing its x momentum

        if not self.pow1_lockout and self.pow1 > 0 and abs(self.ball.ycor()) < 340:              #Checks that the pow1 lockout is not active and that the block has 1 or more uses left. Also makes sure the ball is not too high/low
            self.pow1 -= 1                                                                   #Decrements uses
            self.pow1_lockout = True
            self.disp1.clear()                                                            #Erases previous display and writes new score
            self.disp1.write(f'{self.pow1}', font=('Comic Sans', 15))
            color = self.ball.pencolor()                                               #Save ball color to restore it after using
            block_color = self.pencolor()
            x, y = self.ball.xcor(), self.ball.ycor()
            self.color('DarkOrchid')
            self.ball.color('DarkOrchid')
            time.sleep(.1)                                                                     #Pauses screen briefly, then does a series of short teleports in random directions before returning ball to original spot to give shaking animation
            for i in range(10):
                self.ball.goto(x+random.choice([-1,0,1])*3,y+random.choice([-1,0,1])*3)
                time.sleep(.01)
            self.ball.goto(x,y)
            self.ball.bounce(1,0)                                                          #Bounces ball in x direction (this will cause acceleration in acceleration mode)
            self.ball.color(color)
            self.color(block_color)


    def golden_defense(self):

        #Power 2, doubles the size of the block and doubles it move distance temporarily

        if not self.pow2_lockout and self.pow2 > 0 and abs(self.ycor()) < 260:                #Checks that pow2 lockout is not active and that the user has uses of pow2 left. Checks to see if block is too high as well
            self.pow2 -= 1                                                               #Decrements uses
            self.pow2_lockout = True
            self.pow2_is_active = True
            self.disp2.clear()                                                        #Erases previous display and writes new score
            self.disp2.write(f'{self.pow2}', font=('Comic Sans', 15))
            for i in range(3):
                self.shapesize(8+2*i,.7+.25*i,1)                                  #Creates the growing three times animation while darkening the block
                col = f'DarkGoldenrod{i+1}'
                self.color(col)
                time.sleep(.25)
            self.width *= 1.3
            self.height *= 2                                                 #Enlarges hitbox and move distance
            self.move_dist *= 2


    def disable_beam(self):

        #Power 3, fires beam from the center of the block, if it collides with the other block your opponent will be temporarily unable to move or use powerups

        if not self.pow3_lockout and self.pow3 > 0:                             #Checks that the power is not locked out and that you have at least one use of the ability left
            self.pow3_lockout = True
            self.pow3 -= 1                                              #Decrements uses
            self.disp3.clear()                                                   #Erases previous display and writes new score
            self.disp3.write(f'{self.pow3}', font=('Comic Sans', 15))

            #Creates beam and draws it across the screen (just an animation)
            self.beam = Turtle()
            self.beam.penup()
            self.beam.hideturtle()
            self.beam.speed(6)
            self.beam.color(self.pencolor())
            self.beam.goto(self.xcor(),self.ycor())
            self.beam.pendown()
            self.beam.goto(-self.xcor(),self.ycor())


            if y_dist(self.beam,self.other) < self.other.height:               #Checks that the beam collides with the other

                self.other.move_lockout = True                           #Locks opponent out of all options and gives disabled status effect
                self.other.disabled = True
                self.other.pow1_lockout = True
                self.other.pow2_lockout = True
                self.other.pow3_lockout = True
                self.other.color('gray')
            self.beam.clear()
            self.beam = None







class Ball(Turtle):

    #The ball that bounces across the screen

    def __init__(self,pos,accel_mode,bounce_counter=0):
        super().__init__()
        self.accel_mode = accel_mode                                          #Accel mode used to determine if bounce should increase ball speed
        self.make_ball(pos)
        self.bounce_counter = 0
        self.x_vel = 0                                            #Initially ball has no velocity and has collision active
        self.y_vel = 0
        self.collision = True
    def make_ball(self,pos):                                            #Draws the ball
        self.penup()
        self.goto(pos)
        self.shape('circle')
        self.shapesize(1,1,1)
        self.color('gray')
    def initial_takeoff(self,speed,number_flag):

        #Initializes ball to move in a random direction at the start of a round

        self.bounce_counter = 0
        if number_flag != 0:                      #On all rounds but the first the ball must be hidden before traveling back to (0,0)
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

        #Function that reverses ball momentum if it hits a surface. x_flag/y_flag used to signify vertical/horizontal collision

        if self.accel_mode != 'a':                 #In all modes but accelerate mode the ball should bounce at the same speed
            if x_flag == 1:
                self.x_vel = -self.x_vel
            if y_flag == 1:
                self.y_vel = -self.y_vel
        else:
            if x_flag == 1:                            #Accel mode speeds up ball by 3% per bounce
                self.x_vel = -1.03*self.x_vel
                self.y_vel = 1.03*self.y_vel
            if y_flag == 1:
                self.x_vel = 1.03 * self.x_vel
                self.y_vel = -1.03 * self.y_vel
        self.bounce_counter += 1





class Scoreboard(Turtle):

    #Displays scores and victory screens

    def __init__(self):

        #Hides two turtles that will write the blue/red player scores

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

        #Hides the "left" and "right" turtles before __init__ sends them to the correct location
        self.left.penup()
        self.right.penup()
        self.left.hideturtle()
        self.right.hideturtle()

    def display(self, turt):

        #When someone scores a point, the left/right turtle will create another tally mark for that player to the right of the most recently created tally
        if turt == self.left:
            self.score1 += 1  # Increment left score
            self.left.goto(self.pos1[0] + self.score1*15,self.pos1[1])
            self.left.write('|', font=('Comic Sans', 40))

        elif turt == self.right:

            self.score2 += 1  # Increment right score
            self.right.goto(self.pos2[0] + self.score2 * 15, self.pos2[1])
            self.right.write('|', font=('Comic Sans', 40))

    def victory(self):

        # Called when someone wins to display final score

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

    #Used in portal pong, creates two circular portals that cause a ball that comes in contact with one to teleport to the other
    def __init__(self, pos_1, pos_2):
        super().__init__()
        self.port1 = Turtle()                            #Creates the two portals
        self.port2 = Turtle()
        self.teleported = False                           #Flag is used to prevent double teleports, temporarily set to True when the ball teleports
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

        #Takes ball and moves it to the center of the portal it is not touching
        if portal == self.port1:
            ball.hideturtle()
            ball.goto(self.port2.pos())
            ball.showturtle()

        else:
            ball.hideturtle()
            ball.goto(self.port1.pos())
            ball.showturtle()
        self.teleported = True

