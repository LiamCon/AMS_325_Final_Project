from Pong_Methods import *
import time
import random

game_is_on = True
speed_mode_dict = {'s':3, 'm':6, 'f':10, 'h':20}
play_defaults = input('Enter "y" to play with default settings, any other entry will have you set them manually: ')
if play_defaults != "y":
    points_to_win = input('Enter how many points to win: ')
    try:
        points_to_win = int(points_to_win)
    except ValueError:
        points_to_win = 1
    speed_mode = input('Enter speed mode. "s" for slow, "m" for medium, "f" for fast, "h" for hyperspeed: ')
    if speed_mode not in speed_mode_dict.keys():
        speed_mode = 'm'
    game_mode = input('Enter game mode. "s" for standard, "a" for accelerate-pong, "p" for portal-pong, "o" for obstacle-pong, "r" for random: ')
    if game_mode not in ['s','a','p','o','r']:
        game_mode = 's'
else:
    points_to_win = 5
    speed_mode = 'm'
    game_mode = 's'

screen = Screen()
screen.bgcolor('black')                        #Creating a black screen with title of "Pong"
screen.title('Pong')
scoreboard = Scoreboard()

for i in range(6):
    decor = Block((0,-345 + 140*i))
    decor.shapesize(4,1,1)
delay = .5                     #Time delay for ball to be launched

time_step = .01
num_delays = 20                #Used to prevent double collisions with blocks. Number of iterations before ball can be hit by block again
current_delays = 0              #Starts counter for num_delays


#Create blocks, ball, and scoreboard

block1 = Block((-450,0))
block2 = Block((450,0))
ball = Ball((0,0))
scoreboard = Scoreboard()


for round in range(2*points_to_win-1):
    if game_mode == 's' or game_mode == 'a':
        #Each time a round resets the block positions and resets the ball
        if scoreboard.score1 < points_to_win and scoreboard.score2 < points_to_win:
            time_1 = 0
            block1.goto((-450,0))
            block2.goto((450, 0))

            #This exists solely to unbind keys before ball has launched to prevent moving paddle between rounds
            screen.listen()
            screen.onkey(None, "w")
            screen.onkey(None, "s")
            screen.onkey(None, "Up")
            screen.onkey(None, "Down")

            flag = round    #This flag exists to be 0 the first round so that the ball is not visible traveling back to the start in later rounds
            if game_mode == "s":
                ball.initial_takeoff(speed_mode_dict[speed_mode],flag)     #Starts the ball moving
            else:
                time_step = time_step/5
                ball.initial_takeoff(speed_mode_dict[speed_mode]/2, flag)

            game_is_on = True
        while game_is_on:        #Game flag to keep game running until point is scored
            if time_1 == 0:
                current_delays = 0    #If the round is just starting the delays reset before pausing the screen and launching the ball
                screen.update()
                time.sleep(delay)
                ball.move()
                ball.collision = True   #Reset ball collision to make sure it can collide with blocks

            #Checks if users input their movement keys and assign them to move_up and move_down functions
            screen.listen()
            screen.onkey(block1.go_up, "w")
            screen.onkey(block1.go_down, "s")
            screen.onkey(block2.go_up, "Up")
            screen.onkey(block2.go_down, "Down")

            #Updates screen for one frame, increments time/current_delays
            screen.update()
            ball.move()
            time.sleep(time_step)
            time_1 += 1
            current_delays += 1
            if current_delays > num_delays:   #Resets delays and allows ball to collide again (only matters if ball has collided with a paddle)
                current_delays = 0
                ball.collision = True
            if ball.ycor() > 390:            #Bounce off of top boundary (reverse y-momentum)
                ball.bounce(0,1,game_mode)
            elif ball.ycor() < -390:                #Bounce off of bottom boundary (reverse y-momentum)
                ball.bounce(0, 1,game_mode)

                #Checks if ball is colliding with the left/right block by checking if it is near enough in x and y direction
            elif ball.collision and x_dist(ball,block1) < block1.width and y_dist(ball,block1) < block1.height:
                ball.bounce(1, 0,game_mode)
                ball.collision = False            #Turns of block collision for and resets delays to prevent double collisions
                current_delays = 0
            elif ball.collision and x_dist(ball,block2) < block2.width and y_dist(ball,block2) < block2.height:
                ball.bounce(1, 0,game_mode)
                ball.collision = False
                current_delays = 0
            elif ball.xcor() > 480:                       #If ball escapes either left or right boundary the other player scores and game flag resets, exiting while loop
                scoreboard.display(scoreboard.left)
                game_is_on = False
            elif ball.xcor() < -480:
                scoreboard.display(scoreboard.right)
                game_is_on = False
    #

scoreboard.victory()            #After game is over this will display the winner


screen.exitonclick()