from Pong_Methods import *
import time
import random
import math

                            #It is recommended to read the Pong_Methods comments before this section




game_is_on = True
speed_mode_dict = {'s':4, 'm':5, 'f':6, 'h':7}                   #Dictionaries to convert modes into ball speeds/number of powers
powers_dict = {'n':0,'l':3,'m':10,'h':16,'i':999999}
play_defaults = input('Enter "y" to play with default settings, any other entry will have you set them manually: ')
if play_defaults != "y":
    points_to_win = input('Enter how many points to win: ')
    try:
        points_to_win = int(points_to_win)
    except ValueError:
        points_to_win = 1
    speed_mode = input('Enter speed mode. "s" for slow, "m" for medium, "f" for fast, "h" for hyperspeed: ')
    if speed_mode not in speed_mode_dict.keys():              #Sets any non-valid inputs to medium speed
        speed_mode = 'm'
    game_mode = input('Enter game mode. "s" for standard, "a" for accelerate-pong, "p" for portal-pong, "r" for random: ')
    if game_mode not in ['s','a','p','r']:                #Sets any non-valid inputs to standard mode
        game_mode = 's'
    elif game_mode == 'r':
        game_mode = random.choice(['s','a','p'])
    powers_flag = input('Enter "n" for no powerups, "l" for low powerups (3), "m" for medium powerups (10), "h" for high powerups (16), and "i" for infinite: ')
    if powers_flag not in powers_dict.keys():
        powers_flag = 'n'
else:
    points_to_win = 5                 #Default is 5 points to win, medium speed, standard mode, no powerups
    speed_mode = 'm'
    game_mode = 's'
    powers_flag = 'n'
num_powers = powers_dict[powers_flag]

screen = Screen()
screen.bgcolor('black')                        #Creating a black screen with title of "Pong"
screen.title('Pong')
scoreboard = Scoreboard()

for i in range(6):                             #Creates decoration blocks in the middle
    decor = Block((0,-345 + 140*i))
    decor.shapesize(4,1,1)
delay = .5                     #Time delay for ball to be launched

time_step = .01
num_delays = 5                #Used to prevent double collisions with blocks. Number of iterations before ball can be hit by block again
current_delays = 0              #Starts counter for num_delays
move_lockout_time = 5           #Prevents spamming of movement to make game run better, can be lowered to allow faster movement at the expense of framerate
pow_lockout_time = 50         #Time (in frames) before you can use a powerup after using it beforehand
pow2_duration = 250             #Time (in frames) the "golden defense" powerup lasts
max_disable_duration = 80       #Movement lockout time (in frames) if hit by disable beam




                                        #For powerups, pow1=psychic_bounce, pow2=golden_defense, pow3=disable_beam. These terms will be used interchangebly.



                                                                  #Writes out the display for how many of each powerup each player has
power_writer = Turtle()
power_writer.penup()
power_writer.hideturtle()
power_writer.pencolor('blue')
power_writer.goto(-350,-350)
power_writer.write('Pow1:',font=('Comic Sans', 15))
power_writer.goto(-350,-370)
power_writer.write('Pow2:',font=('Comic Sans', 15))
power_writer.goto(-350,-390)
power_writer.write('Pow3:',font=('Comic Sans', 15))
power_writer.pencolor('red')
power_writer.goto(270,-350)
power_writer.write('Pow1:',font=('Comic Sans', 15))
power_writer.goto(270,-370)
power_writer.write('Pow2:',font=('Comic Sans', 15))
power_writer.goto(270,-390)
power_writer.write('Pow3:',font=('Comic Sans', 15))

left_1 = Turtle()                                                           #Display the number of powerup uses for blue/red (pow1, pow2, pow3)
left_2 = Turtle()
left_3 = Turtle()

for turt in [left_1,left_2,left_3]:
    turt.penup()
    turt.hideturtle()
    turt.pencolor('blue')

left_1.goto(-290,-350)
left_2.goto(-290,-370)
left_3.goto(-290,-390)

right_1 = Turtle()
right_2 = Turtle()
right_3 = Turtle()

for turt in [right_1,right_2,right_3]:
    turt.penup()
    turt.hideturtle()
    turt.pencolor('red')

right_1.goto(330,-350)
right_2.goto(330,-370)
right_3.goto(330,-390)


#Create blocks, ball, and scoreboard
ball = Ball((0,0),game_mode)
block1 = Block((-450,0),left_1,left_2,left_3,ball,num_powers,num_powers,num_powers)
block2 = Block((450,0),right_1,right_2,right_3,ball,num_powers,num_powers,num_powers)
block1.set_other(block2)
block2.set_other(block1)                     #Makes it easier to access other block for powerups
scoreboard = Scoreboard()

for round in range(2*points_to_win-1):
    if game_mode == 's' or game_mode == 'a':                                    #Only difference between standard mode and accelerate mode is the accelerate flag, the game loop is the same
        #Each time a round resets the block positions and resets the ball
        if scoreboard.score1 < points_to_win and scoreboard.score2 < points_to_win:
            time_1 = 0
            block1.color('blue')
            block2.color('red')
            block1.shapesize(6,.7,1)
            block1.width = 21                                                   #When a round starts, reset block positions/states, as well as all counters/lockout flags
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
                time_step = time_step/5
                ball.initial_takeoff(speed_mode_dict[speed_mode], flag)                       #Speed/framerate is adjusted for accelerate mode for performance, a ball moving quickly would often phase through the blocks

            game_is_on = True
        while game_is_on:        #Game flag to keep game running until point is scored
            if time_1 == 0:                  #If the round is just starting the delays reset before pausing the screen and launching the ball
                current_delays = 0                                  #Exists to count time before ball can bounce again
                block_1_move_lockout = 0
                block_2_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0                             #All the different counters exist to control the rate at which each of the four options (move, pow1, pow2, and pow3) can be used
                block_1_pow3_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block1.disabled = False
                block2.disabled = False
                golden_timer_1 = 0                                  #Golden_timer is used to count time after pow2 is used
                golden_timer_2 = 0
                disable_timer_1 = 0                                 #Disable_timer is used to count time after a block has been disabled by the disable beam power
                disable_timer_2 = 0
                screen.update()
                time.sleep(delay)
                ball.move()

                ball.collision = True                          #Reset ball collision to make sure it can collide with blocks

            #Checks if users input their movement keys and assign them to move_up and move_down functions
            screen.listen()
            screen.onkey(block1.go_up, "w")
            screen.onkey(block1.go_down, "s")
            screen.onkey(block2.go_up, "Up")
            screen.onkey(block2.go_down, "Down")                             #Assigns controls to keys for both players
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
            time_1 += 1                                #Measures game time and is used to reset rounds
            current_delays += 1
            color_map = {0:'gray', 5:'burlywood', 10:'DarkOrange',15:'tan4',20:'salmon4',25:'red4',30:'gold'}              #Changes ball color in accelerate mode as it bounces more
            if game_mode == 'a':
                if ball.bounce_counter > 30:
                    ball.bounce_counter = 30
                ball.color(color_map[5*math.floor(ball.bounce_counter/5)])
            if block1.pow2_is_active:                      #If someone is using pow2, the lockout timer should be reset and only start after the power has expired
                golden_timer_1 += 1
                block_1_pow2_lockout = 0
            if block2.pow2_is_active:
                golden_timer_2 += 1
                block_2_pow2_lockout = 0
            if golden_timer_1 >= pow2_duration:                 #Once pow2 has expired, reset the block stats and counters
                golden_timer_1 = 0
                block1.pow2_is_active = False
                block_1_pow2_lockout = 0
                block1.shapesize(6, .7, 1)
                block1.width = 21
                block1.height = 75
                block1.move_dist = 40
                if block1.disabled:  # If block is still disabled it should remain gray after changing back
                    block1.color('gray')
                else:
                    block1.color(block1.block_color)
            if golden_timer_2 >= pow2_duration:
                golden_timer_2 = 0
                block2.pow2_is_active = False
                block_2_pow2_lockout = 0
                block2.color(block2.block_color)
                block2.shapesize(6,.7,1)
                block2.width = 21
                block2.height = 75
                block2.move_dist = 40


            block_1_pow1_lockout += 1                           #All counters are updated each frame
            block_1_pow2_lockout += 1
            block_1_pow3_lockout += 1
            block_2_pow1_lockout += 1
            block_2_pow2_lockout += 1
            block_2_pow3_lockout += 1
            if block1.disabled:
                disable_timer_1 += 1
                block_1_pow1_lockout -= 1                  #A block hit by pow3 has its lockout timers frozen (-1 to compensate the +1 per frame) to prevent them from using powers while disabled
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
                if block1.move_lockout:
                    block_1_move_lockout += 1
                if block_1_move_lockout >= move_lockout_time:                     #Resets block movement if enough time has passed since the last movement press and the block is not disabled
                    block_1_move_lockout = 0
                    block1.move_lockout = False
            elif disable_timer_1 >= max_disable_duration:
                block_1_move_lockout = 0                                        #After the disable timer has run out, the block has all its timers/lockouts reset
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
                if block2.move_lockout:
                    block_2_move_lockout += 1
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
            if block_1_pow1_lockout >= pow_lockout_time:                                             #Basic lockout counters for each blocks powerups
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

            if ball.ycor() > 390:            #Bounce off of top boundary (reverse y-momentum). Gamemode flag included to increase velocity if ball bounces in accelerate mode
                ball.bounce(0,1)
            elif ball.ycor() < -390:                #Bounce off of bottom boundary (reverse y-momentum)
                ball.bounce(0, 1)

                #Checks if ball is colliding with the left/right block by checking if it is near enough in x and y direction
            elif ball.collision and x_dist(ball,block1) < block1.width and y_dist(ball,block1) < block1.height:
                ball.bounce(1, 0)
                ball.collision = False            #Turns of block collision for and resets delays to prevent double collisions
                current_delays = 0
            elif ball.collision and x_dist(ball,block2) < block2.width and y_dist(ball,block2) < block2.height:
                ball.bounce(1, 0)
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
            block1.width = 21                            #When a round starts, reset block positions/states, as well as all counters/lockout flags
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
            portal = Portal((0, 200), (0, -200))                       #Creates two portal positions


        while game_is_on:        #Game flag to keep game running until point is scored
            if time_1 == 0:                  #If the round is just starting the delays reset before pausing the screen and launching the ball
                current_delays = 0                                  #Exists to count time before ball can bounce again
                block_1_move_lockout = 0
                block_2_move_lockout = 0
                block_1_pow1_lockout = 0
                block_1_pow2_lockout = 0                             #All the different counters exist to control the rate at which each of the four options (move, pow1, pow2, and pow3) can be used
                block_1_pow3_lockout = 0
                block_2_pow1_lockout = 0
                block_2_pow2_lockout = 0
                block_2_pow3_lockout = 0
                block1.disabled = False
                block2.disabled = False
                golden_timer_1 = 0                                  #Golden_timer is used to count time after pow2 is used
                golden_timer_2 = 0
                disable_timer_1 = 0                                 #Disable_timer is used to count time after a block has been disabled by the disable beam power
                disable_timer_2 = 0
                screen.update()
                time.sleep(delay)
                ball.move()

                ball.collision = True                          #Reset ball collision to make sure it can collide with blocks

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



            #Portal.teleported flag set to true when portal teleports ball in order to prevent double teleports. Uses same delays counter as the ball
            if not portal.teleported and math.sqrt(x_dist(ball, portal.port1) ** 2 + y_dist(ball, portal.port1) ** 2) < 40:
                portal.teleport(portal.port1, ball)
                current_delays = 0
            elif not portal.teleported and math.sqrt(x_dist(ball, portal.port2) ** 2 + y_dist(ball, portal.port2) ** 2) < 40:       #If ball collides with either portal it teleports to the other
                portal.teleport(portal.port2, ball)
                current_delays = 0

            # Updates screen for one frame, increments time/current_delays
            screen.update()
            ball.move()
            time.sleep(time_step)
            time_1 += 1                                #Used to measure game time and resets to reset round
            current_delays += 1

            if block1.pow2_is_active:                      #If someone is using pow2, the lockout timer should be reset and only start after the power has expired
                golden_timer_1 += 1
                block_1_pow2_lockout = 0
            if block2.pow2_is_active:
                golden_timer_2 += 1
                block_2_pow2_lockout = 0
            if golden_timer_1 >= pow2_duration:                 #Once pow2 has expired, reset the block stats and counters
                golden_timer_1 = 0
                block1.pow2_is_active = False
                block_1_pow2_lockout = 0
                block1.shapesize(6, .7, 1)
                block1.width = 21
                block1.height = 75
                block1.move_dist = 40
                if block1.disabled:                            #If block is still disabled it should remain gray after changing back
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

            block_1_pow1_lockout += 1                           #All counters are updated each frame
            block_1_pow2_lockout += 1
            block_1_pow3_lockout += 1
            block_2_pow1_lockout += 1
            block_2_pow2_lockout += 1
            block_2_pow3_lockout += 1
            if block1.disabled:
                disable_timer_1 += 1
                block_1_pow1_lockout -= 1                  #A block hit by pow3 has its lockout timers frozen (-1 to compensate the +1 per frame) to prevent them from using powers while disabled
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
                if block1.move_lockout:
                    block_1_move_lockout += 1
                if block_1_move_lockout >= move_lockout_time:  # Resets block movement if enough time has passed since the last movement press and the block is not disabled
                    block_1_move_lockout = 0
                    block1.move_lockout = False
            elif disable_timer_1 >= max_disable_duration:
                block_1_move_lockout = 0  # After the disable timer has run out, the block has all its timers/lockouts reset
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
                if block2.move_lockout:
                    block_2_move_lockout += 1
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
            if block_1_pow1_lockout >= pow_lockout_time:  # Basic lockout counters for each blocks powerups
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

            if current_delays > num_delays:   #Resets delays and allows ball to collide again/portal to teleport again (only matters if ball has collided with a paddle)
                current_delays = 0
                ball.collision = True
                portal.teleported = False

            if ball.ycor() > 390:  # Bounce off of top boundary (reverse y-momentum)
                ball.bounce(0, 1)
            elif ball.ycor() < -390:  # Bounce off of bottom boundary (reverse y-momentum)
                ball.bounce(0, 1)

                # Checks if ball is colliding with the left/right block by checking if it is near enough in x and y direction
            elif ball.collision and x_dist(ball, block1) < block1.width and y_dist(ball, block1) < block1.height:
                ball.bounce(1, 0)
                ball.collision = False  # Turns of block collision for and resets delays to prevent double collisions
                current_delays = 0
            elif ball.collision and x_dist(ball, block2) < block2.width and y_dist(ball, block2) < block2.height:
                ball.bounce(1, 0)
                ball.collision = False
                current_delays = 0
            elif ball.xcor() > 480:  # If ball escapes either left or right boundary the other player scores and game flag resets, exiting while loop
                scoreboard.display(scoreboard.left)
                game_is_on = False
            elif ball.xcor() < -480:
                scoreboard.display(scoreboard.right)
                game_is_on = False

scoreboard.victory()            #After game is over this will display the winner


screen.exitonclick()           #After game is over you click to exit