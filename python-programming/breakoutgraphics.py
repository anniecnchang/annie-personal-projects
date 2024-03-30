"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

In this project, players are tasked with breaking a wall of bricks using a paddle and
a bouncing ball. The objective is to clear all the bricks from the screen while preventing
the ball from falling off the bottom of the window. The BreakoutGraphics class serves as
the backbone of the game's graphical interface and interactive elements, managing player inputs,
ball physics, paddle movement, and collision detection with precision and responsiveness.
"""

from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Width of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window.width - self.paddle.width)/2, y=self.window.height - PADDLE_OFFSET)

        # Center a filled ball in the graphical window
        self.ball = GOval(BALL_RADIUS*2, BALL_RADIUS*2)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width - self.ball.width)/2, y=(self.window.height - self.ball.height)/2)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0

        # Initialize whether the game is currently progress, if so, mouse clicks shouldn't affect the ball
        self.is_running = False

        # Initialize our mouse listeners
        onmouseclicked(self.start)
        onmousemoved(self.move)

        # Initialize game over and success labels
        self.game_over_label = None
        self.success_label = None

        # Initialize remaining bricks to keep count of how close the player is to complete the game
        self.remaining_bricks = BRICK_ROWS * BRICK_COLS

        # Draw bricks
        self.draw_bricks()

    # Mouse click within the window will start the game
    def start(self, mouse):
        if self.is_running:
            return
        self.is_running = True
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx
        if self.game_over_label:
            self.window.remove(self.game_over_label)
        if self.success_label:
            self.window.remove(self.success_label)

    # When user did not pass the game, reset the game
    def reset(self):
        self.reposition_ball()
        self.draw_bricks()
        self.is_running = False
        self.remaining_bricks = BRICK_ROWS * BRICK_COLS

    # When there are lives remaining, ball will reposition when touches the window bottom
    def reposition_ball(self):
        self.window.remove(self.ball)
        self.ball = GOval(BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.ball.filled = True
        self.window.add(self.ball, x=(self.window.width - self.ball.width)/2, y=(self.window.height - self.ball.height)/2)
        self.__dx = 0
        self.__dy = 0
        self.is_running = False

    # Paddle will move with the mouse
    def move(self, mouse):
        self.paddle.x = mouse.x-PADDLE_WIDTH/2
        if self.paddle.x + self.paddle.width > self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        if self.paddle.x < 0:
            self.paddle.x = 0

    # Draw bricks
    def draw_bricks(self):
        color = ['red', 'orange', 'yellow', 'green', 'blue']
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_SPACING)
                if row == 0:
                    y = BRICK_OFFSET
                else:
                    y = row * (BRICK_HEIGHT + BRICK_SPACING) + BRICK_OFFSET
                self.brick = GRect(BRICK_WIDTH, BRICK_HEIGHT)
                self.brick.filled = True
                self.brick.fill_color = color[row // 2]
                self.brick.color = color[row // 2]
                self.window.add(self.brick, x=x, y=y)
        return self.draw_bricks

    # Checks whether ball collides with bricks or paddle
    def check_collision(self):
        ball_top_left = (self.ball.x, self.ball.y)
        ball_top_right = (self.ball.x + 2*BALL_RADIUS, self.ball.y)
        ball_bottom_left = (self.ball.x, self.ball.y + 2*BALL_RADIUS)
        ball_bottom_right = (self.ball.x + 2*BALL_RADIUS, self.ball.y + 2*BALL_RADIUS)

        for corner_x, corner_y in [ball_top_left, ball_top_right, ball_bottom_left, ball_bottom_right]:
            self.maybe_obj = self.window.get_object_at(corner_x, corner_y)
            if self.maybe_obj:
                if self.maybe_obj != self.paddle:
                    self.window.remove(self.maybe_obj)
                    self.bounce()
                    self.remaining_bricks -= 1
                    if self.remaining_bricks == 0:  # Check if all bricks have been destroyed
                        self.success_label = GLabel("You won! Click to restart!")
                        self.success_label.font = '-16'
                        self.success_label.color = 'green'
                        self.window.add(self.success_label, x=self.window_width/2-self.success_label.width/2, y=self.window_height)
                    break
                else:
                    self.bounce_paddle()

    # Ball will bounce once it collides with bricks
    def bounce(self):
        if self.ball.y + self.ball.height >= self.maybe_obj.y or self.ball.y <= self.maybe_obj.y + self.maybe_obj.height:
            self.__dy = -self.__dy

    # Ball will bounce up once collides with paddle
    def bounce_paddle(self):
        if self.get_dy() > 0 and self.ball.y + 2 * BALL_RADIUS >= self.paddle.y:
            self.__dy = -self.__dy

    def get_dx(self):
        return self.__dx

    def get_dy(self):
        return self.__dy

    def set_dx(self, dx):
        self.__dx = dx

    def set_dy(self, dy):
        self.__dy = dy


