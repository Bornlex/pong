#coding: utf-8

import turtle
import random


log_file = open('error.log', 'w+')


class Environment(object):
    def __init__(self):
        # Variables
        self.done = False
        self.hit = 0
        self.miss = 0
        self.reward = 0

        # Window setup
        self.window = turtle.Screen()
        self.window.title('Environment')
        self.window.bgcolor('black')
        self.window.tracer(0)
        self.window.setup(width=600, height=600)

        # Paddle
        self.paddle = turtle.Turtle()
        self.paddle.shape('square')
        self.paddle.speed(0)
        self.paddle.shapesize(stretch_wid=1, stretch_len=5)
        self.paddle.penup()
        self.paddle.color('white')
        self.paddle.goto(0, -275)

        # Ball
        self.ball = turtle.Turtle()
        self.ball.shape('circle')
        self.ball.speed(0)
        self.ball.color('red')
        self.ball.penup()
        self.ball.goto(0, 100)
        self.ball.dx = 3
        self.ball.dy = -3

        # Score
        self.score = turtle.Turtle()
        self.score.speed(0)
        self.score.color('white')
        self.score.hideturtle()
        self.score.goto(0, 250)
        self.score.penup()
        self.write_score()

        self.window.listen()
        self.window.onkey(self.paddle_right, 'Right')
        self.window.onkey(self.paddle_left, 'Left')


    def paddle_right(self):
        x = self.paddle.xcor()
        if x < 255:
            self.paddle.setx(x + 20)

    def paddle_left(self):
        x = self.paddle.xcor()
        if x > -225:
            self.paddle.setx(x - 20)
    
    def write_score(self):
        self.score.write(f"Hit: {self.hit}   Missed: {self.miss}", align='center', font=('Courier', 24, 'normal'))
    
    def reset(self):
        self.done = False
        self.reward = 0
        self.paddle.goto(0, -275)
        self.ball.goto(0, 100)
        return [
            self.paddle.xcor(),# * 0.01,
            self.ball.xcor(),# * 0.01,
            self.ball.ycor(),# * 0.01,
            self.ball.dx,
            self.ball.dy
        ]
    
    def step(self, action):
        """
        Performs an action:
        - moving left  : 0
        - moving right : 1
        - not moving   : 2

        We penalize the agent when moving so it does not move unecessarily.
        """
        if action == 0:
            self.paddle_left()
            self.reward -= 0.005
        if action == 1:
            self.paddle_right()
            self.reward -= 0.005
        self.frame()
        state = [
            self.paddle.xcor(),
            self.ball.xcor(),
            self.ball.ycor(),
            self.ball.dx,
            self.ball.dy
        ]
        return self.reward, state, self.done

    def frame(self):
        self.window.update()
        self.ball.setx(self.ball.xcor() + self.ball.dx)
        self.ball.sety(self.ball.ycor() + self.ball.dy)
        if self.ball.xcor() > 290:
            self.ball.setx(290)
            self.ball.dx *= -1
        if self.ball.xcor() < -290:
            self.ball.setx(-290)
            self.ball.dx *= -1
        if self.ball.ycor() > 290:
            self.ball.sety(290)
            self.ball.dy *= -1

        if self.ball.ycor() < -255:
            if self.ball.xcor() > self.paddle.xcor() - 60 and self.ball.xcor() < self.paddle.xcor() + 60:
                ###
                # Hit the ball
                ###
                self.ball.dy *= -1
                self.hit += 1
                self.score.clear()
                self.write_score()
                self.reward += 3
            else:
                ###
                # Missed the ball
                ###
                self.ball.goto(0, 100)
                self.ball.dx = random.choice([-4.5, -3, 3, 4.5])
                self.ball.dy = random.choice([-4.5, -3, 3, 4.5])
                self.miss += 1
                self.score.clear()
                self.write_score()
                self.reward -= 5
                self.done = True