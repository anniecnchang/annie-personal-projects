"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.graphics.gobjects import GOval, GRect, GLabel, GLine

FRAME_RATE = 10         # 100 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()
    while True:
        lives = NUM_LIVES
        while lives > 0 and graphics.remaining_bricks > 0:
            pause(FRAME_RATE)
            graphics.ball.move(graphics.get_dx(), graphics.get_dy())
            graphics.check_collision()  # checks whether ball hits bricks or paddle

            # if ball touches window bottom, lose 1 live and reset the ball
            if graphics.ball.y + graphics.ball.height >= graphics.window.height:
                lives -= 1
                graphics.reposition_ball()

            # if ball touches window top, it will bounce
            if graphics.ball.y <= 0:
                graphics.set_dy(-graphics.get_dy())

            # if ball touches either window left or right edge, it will bounce
            if graphics.ball.x <= 0 or graphics.ball.x + graphics.ball.width >= graphics.window.width:
                graphics.set_dx(-graphics.get_dx())

        # when there are no more lives, game will reset
        if lives == 0:
            graphics.game_over_label = GLabel("No more lives left :( Click to restart!")
            graphics.game_over_label.font = '-16'
            graphics.game_over_label.color = 'crimson'
            graphics.window.add(graphics.game_over_label, x=graphics.window_width/2-graphics.game_over_label.width/2, y=graphics.window_height)
        graphics.reset()


if __name__ == '__main__':
    main()
