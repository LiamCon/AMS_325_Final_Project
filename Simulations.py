from turtle import *
from Pong_Methods import *
import random
import time
import numpy as np
import matplotlib.pyplot as plt

# PongGame Class
class PongGame:
    """
    A class to represent a Pong game simulation.

    Args:
        left_paddle (Block): The paddle on the left side of the game area.
        right_paddle (Block) The paddle on the right side of the game area.
        ball (Ball): The ball that moves across the game area.
        scoreboard (Scoreboard): Keeps track of the game scores for both players.
        game_is_on (bool): A flag to indicate whether the game is running.
    """
    def __init__(self):
        """
        Initializes the Pong game with paddles, a ball, and a scoreboard.
        """
        self.left_paddle = Block((-450, 0))
        self.right_paddle = Block((450, 0))
        self.ball = Ball((0, 0))
        self.scoreboard = Scoreboard()
        self.game_is_on = True

    def simulate_keypress(self, paddle, direction):
        """
        Simulate paddle movement based on keypress input.

        Parameters:
            paddle (str): Specifies which paddle to move ('left' or 'right').
            direction (str): Specifies the direction to move ('up' or 'down').
        """
        if paddle == "left":
            if direction == "up":
                self.left_paddle.go_up()
            elif direction == "down":
                self.left_paddle.go_down()
        elif paddle == "right":
            if direction == "up":
                self.right_paddle.go_up()
            elif direction == "down":
                self.right_paddle.go_down()

    def run_simulation_step(self):
        """
        Executes a single step of the simulation by moving the ball, handling collisions, and updating scores.
        """
        self.ball.move()
        self.handle_collisions()
        self.update_scores()

    def handle_collisions(self):
        """
        Handle collisions of the ball with walls and paddles.
        """
        # Ball collision with top or bottom wall
        if self.ball.ycor() > 300 or self.ball.ycor() < -300:
            self.ball.bounce(0,1,'s')

        # Ball collision with paddles
        if self.ball.collision and x_dist(self.ball,self.left_paddle) < self.left_paddle.width and y_dist(self.ball,self.left_paddle) < self.left_paddle.height:
                self.ball.bounce(1, 0,'s')            #Turns of block collision for and resets delays to prevent double collisions
        elif self.ball.collision and x_dist(self.ball,self.right_paddle) < self.right_paddle.width and y_dist(self.ball,self.right_paddle) < self.right_paddle.height:
                self.ball.bounce(1, 0,'s')

    def update_scores(self):
        """
        Update the scores if the ball goes out of bounds.
        Resets the ball position and launches it again.
        """
        # Ball out of bounds
        if self.ball.xcor() > 480:
            self.scoreboard.display(self.scoreboard.left)
            self.ball.reset_position()
            self.ball.initial_takeoff(10, 1)
        elif self.ball.xcor() < -480:
            self.scoreboard.display(self.scoreboard.right)
            self.ball.reset_position()
            self.ball.initial_takeoff(10, 1)

# Simulation and Graphing
ball_positions = []

def run_simulation(game, steps=1000, max_score=10):
    """
    Run the Pong game simulation for a specified number of steps or until a player reaches the maximum score.

    Parameters:
        game (PongGame): An instance of the PongGame class representing the simulation.
        steps (int): The maximum number of simulation steps to execute (default is 1000).
        max_score (int): The score threshold at which the game ends (default is 10).
    """
    game.ball.initial_takeoff(10, 0)  # Launch the ball
    for step in range(steps):
        # Simulate random paddle movements
        left_move = random.choice(["up", "down", None])
        right_move = random.choice(["up", "down", None])
        if left_move:
            game.simulate_keypress("left", left_move)
        if right_move:
            game.simulate_keypress("right", right_move)

        # Run one simulation step
        game.run_simulation_step()
        ball_positions.append((game.ball.xcor(), game.ball.ycor()))

        # Stop if a player reaches the maximum score
        if game.scoreboard.score1 >= max_score or game.scoreboard.score2 >= max_score:
            print("Game Over!")
            print(f"Final Score: Left - {game.scoreboard.score1}, Right - {game.scoreboard.score2}")
            break

    else:
        print("Simulation completed: Max steps reached!")

# Initialize Game and Run Simulation
pong_game = PongGame()
run_simulation(pong_game, steps=1000, max_score=10)

# Graphs Ball Trajectory
if ball_positions:
    x, y = zip(*ball_positions)
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, label="Ball Trajectory")
    plt.axhline(300, color="red", linestyle="--", label="Top Wall")
    plt.axhline(-300, color="blue", linestyle="--", label="Bottom Wall")
    plt.axvline(340, color="green", linestyle="--", label="Right Paddle Area")
    plt.axvline(-340, color="purple", linestyle="--", label="Left Paddle Area")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Ball Trajectory During Simulation")
    plt.legend()
    plt.show()
else:
    print("No ball positions recorded.")
