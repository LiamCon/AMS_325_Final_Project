from Pong_Methods import *
import time
import random
import math

game_is_on = True
speed_mode_dict = {'s':3, 'm':6, 'f':8, 'h':12}
powers_dict = {'n':0,'l':3,'m':10,'h':16,'i':99999}
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
    powers_flag = input('Enter "n" for no powerups, "l" for low powerups (3), "m" for medium powerups (10), "h" for high powerups (16), and "i" for infinite: ')
    if powers_flag not in powers_dict.keys():
        powers_flag = 'n'
else:
    points_to_win = 5
    speed_mode = 'm'
    game_mode = 's'
    powers_flag = 'l'
num_powers = powers_dict[powers_flag]

screen = Screen()
screen.bgcolor('black')                        #Creating a black screen with title of "Pong"
screen.title('Pong')
scoreboard = Scoreboard()

for i in range(6):
    decor = Block((0,-345 + 140*i))
    decor.shapesize(4,1,1)
delay = .5                     #Time delay for ball to be launched

time_step = .01
num_delays = 5                #Used to prevent double collisions with blocks. Number of iterations before ball can be hit by block again
current_delays = 0              #Starts counter for num_delays
move_lockout_time = 5
pow_lockout_time = 70
pow2_duration = 250
max_disable_duration = 80

#Create blocks, ball, and scoreboard
ball = Ball((0,0))
block1 = Block((-450,0),ball,num_powers,num_powers,num_powers)
block2 = Block((450,0),ball,num_powers,num_powers,num_powers)
block1.set_other(block2)
block2.set_other(block1)
scoreboard = Scoreboard()


for round in range(2*points_to_win-1):
    if game_mode == 's' or game_mode == 'a':
        #Each time a round resets the block positions and resets the ball
        if scoreboard.score1 < points_to_win and scoreboard.score2 < points_to_win:
            time_1 = 0
            block1.color('blue')
            block2.color('red')
            block1.shapesize(6,.7,1)
            block1.width = 21
            block1.height = 75
            block1.move_dist = 40
            block2.shapesize(6, .7, 1)
            block2.width = 21
            block2.height = 75
            block2.move_dist = 40
            block1.goto((-450,0))
            block1.move_lockout = False
            block2.goto((450, 0))
            block2.move_lockout = False
            block_1_pow2_lockout = 0
            block_2_pow2_lockout = 0
            block1.pow2_lockout = False
            block2.pow2_lockout = False

            #This exists solely to unbind keys before ball has launched to prevent moving paddle between rounds
            screen.listen()
            screen.onkey(None, "w")
            screen.onkey(None, "s")
            screen.onkey(None, "Up")
            screen.onkey(None, "Down")
            screen.onkey(None, '1')
            screen.onkey(None, '2')
            screen.onkey(None, '3')
            screen.onkey(None, '8')
            screen.onkey(None, '9')
            screen.onkey(None, '0')

            flag = round    #This flag exists to be 0 the first round so that the ball is not visible traveling back to the start in later rounds
            if game_mode == "s":
                ball.initial_takeoff(speed_mode_dict[speed_mode],flag)     #Starts the ball moving
            else:
                time_step = time_step/2
                ball.initial_takeoff(speed_mode_dict[speed_mode]/1.4, flag)

            game_is_on = True
        while game_is_on:        #Game flag to keep game running until point is scored
            if time_1 == 0:
                current_delays = 0    #If the round is just starting the delays reset before pausing the screen and launching the ball
                block_1_move_lockout = 0
                block_2_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0
                block_1_pow3_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block1.disabled = False
                block2.disabled = False
                golden_timer_1 = 0
                golden_timer_2 = 0
                disable_timer_1 = 0
                disable_timer_2 = 0
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
            screen.onkey(block1.psychic_bounce,'1')
            screen.onkey(block1.golden_defense, '2')
            screen.onkey(block1.disable_beam, '3')
            screen.onkey(block2.psychic_bounce, '8')
            screen.onkey(block2.golden_defense, '9')
            screen.onkey(block2.disable_beam, '0')

            #Updates screen for one frame, increments time/current_delays
            screen.update()
            ball.move()
            time.sleep(time_step)
            time_1 += 1
            current_delays += 1
            if block1.pow2_is_active:
                golden_timer_1 += 1
                block_1_pow2_lockout = 0
            if block2.pow2_is_active:
                golden_timer_2 += 1
                block_2_pow2_lockout = 0
            if golden_timer_1 >= pow2_duration:
                golden_timer_1 = 0
                block1.pow2_is_active = False
                block_1_pow2_lockout = 0
                block1.color(block1.block_color)
                block1.shapesize(6,.7,1)
                block1.width = 21
                block1.height = 75
                block1.move_dist = 40
            if golden_timer_2 >= pow2_duration:
                golden_timer_2 = 0
                block2.pow2_is_active = False
                block_2_pow2_lockout = 0
                block2.color(block2.block_color)
                block2.shapesize(6,.7,1)
                block2.width = 21
                block2.height = 75
                block2.move_dist = 40


            block_1_move_lockout += 1
            block_2_move_lockout += 1
            block_1_pow1_lockout += 1
            block_1_pow2_lockout += 1
            block_1_pow3_lockout += 1
            block_2_pow1_lockout += 1
            block_2_pow2_lockout += 1
            block_2_pow3_lockout += 1
            if block1.disabled:
                disable_timer_1 += 1
                block_1_pow1_lockout -= 1
                block_1_pow2_lockout -= 1
                block_1_pow3_lockout -= 1
            if block2.disabled:
                disable_timer_2 += 1
                block_2_pow1_lockout -= 1
                block_2_pow2_lockout -= 1
                block_2_pow3_lockout -= 1
            if current_delays > num_delays:   #Resets delays and allows ball to collide again (only matters if ball has collided with a paddle)
                current_delays = 0
                ball.collision = True
            if not block1.disabled:
                if block_1_move_lockout >= move_lockout_time:
                    block_1_move_lockout = 0
                    block1.move_lockout = False
            elif disable_timer_1 >= max_disable_duration:
                block_1_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0
                block_1_pow3_lockout = 0
                block1.move_lockout = False
                block1.pow1_lockout = False
                block1.pow2_lockout = False
                block1.pow3_lockout = False
                disable_timer_1 = 0
                block1.disabled = False
                block1.color('blue')
            if not block2.disabled:
                if block_2_move_lockout >= move_lockout_time:
                    block_2_move_lockout = 0
                    block2.move_lockout = False
            elif disable_timer_2 >= max_disable_duration:
                block_2_move_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block2.move_lockout = False
                block2.pow1_lockout = False
                block2.pow2_lockout = False
                block2.pow3_lockout = False
                disable_timer_2 = 0
                block2.disabled = False
                block2.color('red')
            if block_1_pow1_lockout >= pow_lockout_time:
                block_1_pow1_lockout = 0
                block1.pow1_lockout = False
            if block_2_pow1_lockout >= pow_lockout_time:
                block_2_pow1_lockout = 0
                block2.pow1_lockout = False
            if block_1_pow2_lockout >= pow_lockout_time:
                block_1_pow2_lockout = 0
                block1.pow2_lockout = False
            if block_2_pow2_lockout >= pow_lockout_time:
                block_2_pow2_lockout = 0
                block2.pow2_lockout = False
            if block_1_pow3_lockout >= pow_lockout_time:
                block_1_pow3_lockout = 0
                block1.pow3_lockout = False
            if block_2_pow3_lockout >= pow_lockout_time:
                block_2_pow3_lockout = 0
                block2.pow3_lockout = False

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








    elif game_mode == "p":
        # Each time a round resets the block positions and resets the ball
        if scoreboard.score1 < points_to_win and scoreboard.score2 < points_to_win:
            time_1 = 0
            block1.color('blue')
            block2.color('red')
            block1.shapesize(6, .7, 1)
            block1.width = 21
            block1.height = 75
            block1.move_dist = 40
            block2.shapesize(6, .7, 1)
            block2.width = 21
            block2.height = 75
            block2.move_dist = 40
            block1.goto((-450, 0))
            block1.move_lockout = False
            block2.goto((450, 0))
            block2.move_lockout = False
            block_1_pow2_lockout = 0
            block_2_pow2_lockout = 0
            block1.pow2_lockout = False
            block2.pow2_lockout = False

            # This exists solely to unbind keys before ball has launched to prevent moving paddle between rounds
            screen.listen()
            screen.onkey(None, "w")
            screen.onkey(None, "s")
            screen.onkey(None, "Up")
            screen.onkey(None, "Down")
            screen.onkey(None, '1')
            screen.onkey(None, '2')
            screen.onkey(None, '3')
            screen.onkey(None, '8')
            screen.onkey(None, '9')
            screen.onkey(None, '0')

            flag = round  # This flag exists to be 0 the first round so that the ball is not visible traveling back to the start in later rounds
            ball.initial_takeoff(speed_mode_dict[speed_mode], flag)  # Starts the ball moving
            game_is_on = True
            portal = Portal((0, 200), (0, -200))





        while game_is_on:  # Game flag to keep game running until point is scored
            if time_1 == 0:
                current_delays = 0    #If the round is just starting the delays reset before pausing the screen and launching the ball
                block_1_move_lockout = 0
                block_2_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0
                block_1_pow3_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block1.disabled = False
                block2.disabled = False
                golden_timer_1 = 0
                golden_timer_2 = 0
                disable_timer_1 = 0
                disable_timer_2 = 0
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
            screen.onkey(block1.psychic_bounce,'1')
            screen.onkey(block1.golden_defense, '2')
            screen.onkey(block1.disable_beam, '3')
            screen.onkey(block2.psychic_bounce, '8')
            screen.onkey(block2.golden_defense, '9')
            screen.onkey(block2.disable_beam, '0')




            if not portal.teleported and math.sqrt(x_dist(ball, portal.port1) ** 2 + y_dist(ball, portal.port1) ** 2) < 38:
                portal.teleport(portal.port1, ball)
                current_delays = 0
            elif not portal.teleported and math.sqrt(x_dist(ball, portal.port2) ** 2 + y_dist(ball, portal.port2) ** 2) < 38:
                portal.teleport(portal.port2, ball)
                current_delays = 0

            screen.update()
            ball.move()
            time.sleep(time_step)
            time_1 += 1
            current_delays += 1
            if block1.pow2_is_active:
                golden_timer_1 += 1
                block_1_pow2_lockout = 0
            if block2.pow2_is_active:
                golden_timer_2 += 1
                block_2_pow2_lockout = 0
            if golden_timer_1 >= pow2_duration:
                golden_timer_1 = 0
                block1.pow2_is_active = False
                block_1_pow2_lockout = 0
                block1.shapesize(6, .7, 1)
                block1.width = 21
                block1.height = 75
                block1.move_dist = 40
                if block1.disabled:
                    block1.color('gray')
                else:
                    block1.color(block1.block_color)


            if golden_timer_2 >= pow2_duration:
                golden_timer_2 = 0
                block2.pow2_is_active = False
                block_2_pow2_lockout = 0
                block2.shapesize(6, .7, 1)
                block2.width = 21
                block2.height = 75
                block2.move_dist = 40
                if block2.disabled:
                    block2.color('gray')
                else:
                    block2.color(block2.block_color)


            block_1_move_lockout += 1
            block_2_move_lockout += 1
            block_1_pow1_lockout += 1
            block_1_pow2_lockout += 1
            block_1_pow3_lockout += 1
            block_2_pow1_lockout += 1
            block_2_pow2_lockout += 1
            block_2_pow3_lockout += 1
            if block1.disabled:
                disable_timer_1 += 1
                block_1_pow1_lockout -= 1
                block_1_pow2_lockout -= 1
                block_1_pow3_lockout -= 1
            if block2.disabled:
                disable_timer_2 += 1
                block_2_pow1_lockout -= 1
                block_2_pow2_lockout -= 1
                block_2_pow3_lockout -= 1
            if current_delays > num_delays:  # Resets delays and allows ball to collide again (only matters if ball has collided with a paddle)
                current_delays = 0
                ball.collision = True
            if not block1.disabled:
                if block_1_move_lockout >= move_lockout_time:
                    block_1_move_lockout = 0
                    block1.move_lockout = False
            elif disable_timer_1 >= max_disable_duration:
                block_1_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0
                block_1_pow3_lockout = 0
                block1.move_lockout = False
                block1.pow1_lockout = False
                block1.pow2_lockout = False
                block1.pow3_lockout = False
                disable_timer_1 = 0
                block1.disabled = False
                block1.color('blue')
            if not block2.disabled:
                if block_2_move_lockout >= move_lockout_time:
                    block_2_move_lockout = 0
                    block2.move_lockout = False
            elif disable_timer_2 >= max_disable_duration:
                block_2_move_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block2.move_lockout = False
                block2.pow1_lockout = False
                block2.pow2_lockout = False
                block2.pow3_lockout = False
                disable_timer_2 = 0
                block2.disabled = False
                block2.color('red')
            if block_1_pow1_lockout >= pow_lockout_time:
                block_1_pow1_lockout = 0
                block1.pow1_lockout = False
            if block_2_pow1_lockout >= pow_lockout_time:
                block_2_pow1_lockout = 0
                block2.pow1_lockout = False
            if block_1_pow2_lockout >= pow_lockout_time:
                block_1_pow2_lockout = 0
                block1.pow2_lockout = False
            if block_2_pow2_lockout >= pow_lockout_time:
                block_2_pow2_lockout = 0
                block2.pow2_lockout = False
            if block_1_pow3_lockout >= pow_lockout_time:
                block_1_pow3_lockout = 0
                block1.pow3_lockout = False
            if block_2_pow3_lockout >= pow_lockout_time:
                block_2_pow3_lockout = 0
                block2.pow3_lockout = False


            if current_delays > num_delays:   #Resets delays and allows ball to collide again (only matters if ball has collided with a paddle)
                current_delays = 0
                ball.collision = True
                portal.teleported = False

            if ball.ycor() > 390:  # Bounce off of top boundary (reverse y-momentum)
                ball.bounce(0, 1, game_mode)
            elif ball.ycor() < -390:  # Bounce off of bottom boundary (reverse y-momentum)
                ball.bounce(0, 1, game_mode)

                # Checks if ball is colliding with the left/right block by checking if it is near enough in x and y direction
            elif ball.collision and x_dist(ball, block1) < block1.width and y_dist(ball, block1) < block1.height:
                ball.bounce(1, 0, game_mode)
                ball.collision = False  # Turns of block collision for and resets delays to prevent double collisions
                current_delays = 0
            elif ball.collision and x_dist(ball, block2) < block2.width and y_dist(ball, block2) < block2.height:
                ball.bounce(1, 0, game_mode)
                ball.collision = False
                current_delays = 0
            elif ball.xcor() > 480:  # If ball escapes either left or right boundary the other player scores and game flag resets, exiting while loop
                scoreboard.display(scoreboard.left)
                game_is_on = False
            elif ball.xcor() < -480:
                scoreboard.display(scoreboard.right)
                game_is_on = False

scoreboard.victory()            #After game is over this will display the winner


screen.exitonclick()