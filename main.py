from Pong_Methods import *
import time
import random

game_is_on = True


screen = Screen()
screen.bgcolor('black')
screen.title('Pong')
scoreboard = Scoreboard()

decorations = []
delay = .02
win = 5
time_step = .01
num_delays = 20
current_delays = 0
block1 = Block((-450,0))
block2 = Block((450,0))
ball = Ball((0,0))
scoreboard = Scoreboard()


for round in range(2*win-1):
    if scoreboard.score1 < win and scoreboard.score2 < win:
        time_1 = 0
        block1.goto((-450,0))
        block2.goto((450, 0))
        flag = scoreboard.score1 + scoreboard.score2
        ball.initial_takeoff(8,flag)

        game_is_on = True
    while game_is_on:
        if time_1 == 0:
            current_delays = 0
            screen.update()
            time.sleep(delay)
            ball.move()
            ball.collision = True
        screen.listen()
        screen.onkey(block1.go_up, "w")
        screen.onkey(block1.go_down, "s")
        screen.onkey(block2.go_up, "Up")
        screen.onkey(block2.go_down, "Down")
        screen.update()
        ball.move()
        time.sleep(time_step)
        time_1 += 1
        current_delays += 1
        if current_delays > num_delays:
            current_delays = 0
            ball.collision = True
        if ball.ycor() > 390:
            ball.bounce(0,1)
        elif ball.ycor() < -390:
            ball.bounce(0, 1)
        elif ball.collision and x_dist(ball,block1) < block1.width and y_dist(ball,block1) < block1.height:
            ball.bounce(1, 0)
            ball.collision = False
        elif ball.collision and x_dist(ball,block2) < block2.width and y_dist(ball,block2) < block2.height:
            ball.bounce(1, 0)
            ball.collision = False
        elif ball.xcor() > 480:
            scoreboard.display(scoreboard.left)
            game_is_on = False
        elif ball.xcor() < -480:
            scoreboard.display(scoreboard.right)
            game_is_on = False

scoreboard.victory()


screen.exitonclick()