from turtle import *
import random
import time


def x_dist(turt1,turt2):
    """
        Calculate the absolute distance between the x-coordinates of two turtles.

        Args:
            turt1 (Turtle): First turtle object.
            turt2 (Turtle): Second turtle object.

        Returns:
            float: The absolute difference between the x-coordinates of the two turtles.
    """

    return abs(turt1.xcor() - turt2.xcor())
def y_dist(turt1,turt2):
    """
        Calculate the absolute distance between the y-coordinates of two turtles.

        Args:
            turt1 (Turtle): First turtle object.
            turt2 (Turtle): Second turtle object.

        Returns:
            float: The absolute difference between the y-coordinates of the two turtles.
    """

    return abs(turt1.ycor() - turt2.ycor())


class Block(Turtle):

    """
       Represents a game block. Player blocks can interact with a ball, use
       power-ups, and move up and down.

       Attributes:
           disp1, disp2, disp3 (Turtle): Turtles that display the number of uses for power-ups.
           ball (Ball): The ball object in the game.
           pow1, pow2, pow3 (int): The number of uses remaining for each power-up.
           move_lockout, pow1_lockout, pow2_lockout, pow3_lockout (bool): Lockout flags for movement and power-ups.
           pow2_is_active (bool): Flag to indicate if Power 2 is active.
           beam (Turtle): A turtle used to represent the beam in Power 3.
           disabled (bool): Indicates if the block is disabled by an enemy's power-up.
    """

    def __init__(self,pos,disp1=None,disp2=None,disp3=None,ball=None,pow1=0,pow2=0,pow3=0):

        """
               Initializes the block at a specified position with optional display and power-up settings.

               Args:
                   pos (tuple): Position of the block (x, y).
                   disp1 (Turtle, optional): Display turtle for Power 1 use count.
                   disp2 (Turtle, optional): Display turtle for Power 2 use count.
                   disp3 (Turtle, optional): Display turtle for Power 3 use count.
                   ball (Ball, optional): The ball object.
                   pow1 (int, optional): Number of uses for Power 1.
                   pow2 (int, optional): Number of uses for Power 2.
                   pow3 (int, optional): Number of uses for Power 3.
        """



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

        """
            Draws the block at the specified position.

            Args:
                pos (tuple): Position where the block will be drawn.
        """

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

        """
            Sets the opponent's block as the other block for power-up interactions.

            Args:
                block (Block): The opponent's block.
        """

        self.other = block                               #Will be used to designate opponent's block as "other" in order to access it easily for powerups
    def go_up(self):

        """
            Moves the block upwards by a set distance, if allowed by the screen boundaries.
        """

        if not self.move_lockout and self.ycor() < 320:             #Move up if the block is not too high and starts move lockout
            y = self.ycor() + self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True
    def go_down(self):

        """
            Moves the block downwards by a set distance, if allowed by the screen boundaries.
        """

        if not self.move_lockout and self.ycor() > -320:
            y = self.ycor() - self.move_dist
            self.goto((self.xcor(),y))
        self.move_lockout = True

    def psychic_bounce(self):

        """
            Power 1: Freezes the ball and causes it to shake before reversing its x-momentum.
        """

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

        """
            Power 2: Doubles the size and move distance of the block temporarily.
        """

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
        """
            Power 3: Fires a beam that temporarily disables the opponent's block if it collides with it.
        """

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
    """
        Represents the ball in the game that bounces off surfaces and interacts with power-ups.

        Attributes:
            accel_mode (str): Mode for ball acceleration ('a' for accelerate mode).
            bounce_counter (int): Counts the number of bounces the ball has made.
            x_vel (float): Ball's horizontal velocity.
            y_vel (float): Ball's vertical velocity.
            collision (bool): Whether the ball is currently in a collision state.
    """

    def __init__(self,pos,accel_mode,bounce_counter=0):

        """
            Initializes the ball at the given position and sets the acceleration mode.


            Args:
                pos (tuple): Position of the ball (x, y).
                accel_mode (str): Acceleration mode for the ball.
                bounce_counter (int, optional): Initial bounce count.
        """

        super().__init__()
        self.accel_mode = accel_mode                                          #Accel mode used to determine if bounce should increase ball speed
        self.make_ball(pos)
        self.bounce_counter = 0
        self.x_vel = 0                                            #Initially ball has no velocity and has collision active
        self.y_vel = 0
        self.collision = True
    def make_ball(self,pos):

        """
            Draws the ball at the specified position.

            Args:
                pos (tuple): Position where the ball will be drawn.
        """

        self.penup()
        self.goto(pos)
        self.shape('circle')
        self.shapesize(1,1,1)
        self.color('gray')
    def initial_takeoff(self,speed,number_flag):

        """
            Initializes the ball's movement at the start of the game, with a random direction.

            Args:
                speed (int): The speed of the ball.
                number_flag (int): Flag to determine if this is the first round.
        """

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

        """
            Moves the ball based on its velocity.
        """
        x = self.xcor() + self.x_vel
        y = self.ycor() + self.y_vel
        self.goto((x,y))
    def bounce(self,x_flag,y_flag):

        """
            Reverses the ball's velocity when it hits a surface.

            Args:
                x_flag (int): Flag to indicate horizontal collision (1 for collision).
                y_flag (int): Flag to indicate vertical collision (1 for collision).
        """

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

    def reset_position(self):
        self.goto(0, 0)
        self.x_vel = 0
        self.y_vel = 0




class Scoreboard(Turtle):
    """
       Displays the scores for both players and handles victory conditions.

       Attributes:
           score1 (int): Score for player 1 (blue).
           score2 (int): Score for player 2 (red).
           left (Turtle): Display turtle for player 1.
           right (Turtle): Display turtle for player 2.
           pos1 (tuple): Position for player 1's score display.
           pos2 (tuple): Position for player 2's score display.
    """

    def __init__(self):

        """
            Sets up the scoreboard by positioning the score display turtles.
        """

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

        """
            Sets up the scoreboard by positioning the score display turtles.
        """
        self.left.penup()
        self.right.penup()
        self.left.hideturtle()
        self.right.hideturtle()

    def display(self, turt):

        """
            Updates the score display when a player scores a point.

            Args:
                turt (Turtle): The turtle representing the player who scored.
        """
        if turt == self.left:
            self.score1 += 1  # Increment left score
            self.left.goto(self.pos1[0] + self.score1*15,self.pos1[1])
            self.left.write('|', font=('Comic Sans', 40))

        elif turt == self.right:

            self.score2 += 1  # Increment right score
            self.right.goto(self.pos2[0] + self.score2 * 15, self.pos2[1])
            self.right.write('|', font=('Comic Sans', 40))

    def victory(self):

        """
            Displays the victory screen and final scores when a player wins.
        """

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
    """
        Creates two portals that teleport the ball between them upon collision.

        Attributes:
            port1 (Turtle): The first portal.
            port2 (Turtle): The second portal.
            teleported (bool): Flag to prevent double teleportation.
            radius (int): Radius of the portals.
        """
    def __init__(self, pos_1, pos_2):

        """
            Initializes two portals at specified positions.

            Args:
                pos_1 (tuple): Position of the first portal.
                pos_2 (tuple): Position of the second portal.
        """

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

        """
            Teleports the ball to the other portal when it collides with one.

            Args:
                portal (Turtle): The portal the ball is currently touching.
                ball (Ball): The ball being teleported.
        """
        if portal == self.port1:
            ball.hideturtle()
            ball.goto(self.port2.pos())
            ball.showturtle()

        else:
            ball.hideturtle()
            ball.goto(self.port1.pos())
            ball.showturtle()
        self.teleported = True

