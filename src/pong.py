#########################################
#   PONG PARA DOIS (PONG FOR TWO) 2024  #
#   RENAN DA ROSA                       #
#   RENAN EUZEBIO                       #
#########################################
from OpenGL.GL import *
from OpenGL.GLUT import *
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 150
BALL_SIZE = 15
BALL_ORIGINAL_SPEED = 1  # update the ball speed to the original value after a goal
PLAYER_SPEED = 30
BALL_SPEED_X = 1
BALL_SPEED_Y = 1
LEFT_PLAYER_POSITION = [0, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
RIGHT_PLAYER_POSITION = [SCREEN_WIDTH - 0 - PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
BALL_DIRECTION = [1, 1]
WAS_GOAL = 0
WAS_HIT = 0

# TODO use this variables to update the player score maybe increase them inside the detect_score() method
GOAL_RIGHT_PLAYER = 0
GOAL_LEFT_PLAYER = 0
SCORE = "0 : 0"


# Utilitarian function to drawn a rectangle
def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


# Render the score
# TODO: update the score
def write_score(txt):
    glRasterPos2f(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1)  # text position
    for i in range(len(txt)):
        char = ord(txt[i])  # ascii value
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, char)  # font being used, and the char to display


# Draw border on the screen limit
# TODO: make to upper half of the border fit inside the game screen
def draw_field():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(5.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(0, 0)
    glVertex2f(SCREEN_WIDTH, 0)
    glVertex2f(SCREEN_WIDTH, SCREEN_HEIGHT)
    glVertex2f(0, SCREEN_HEIGHT)
    glEnd()


# Draw the player paddles
def draw_players():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(LEFT_PLAYER_POSITION[0], LEFT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)
    draw_rectangle(RIGHT_PLAYER_POSITION[0], RIGHT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)


# drawn the ball
def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(BALL_POSITION[0] - BALL_SIZE / 2, BALL_POSITION[1] - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)


# Update the ball location on the screen
def update_ball():
    global BALL_POSITION, BALL_DIRECTION
    BALL_POSITION[0] += BALL_DIRECTION[0] * BALL_SPEED_X
    BALL_POSITION[1] += BALL_DIRECTION[1] * BALL_SPEED_Y


# Detect collision
def detect_collision():
    global WAS_HIT
    # collision with borders
    if BALL_POSITION[1] <= 0 or BALL_POSITION[1] >= SCREEN_HEIGHT:
        BALL_DIRECTION[1] *= -1

    # collision with the players
    if (BALL_POSITION[0] - BALL_SIZE / 2 <= LEFT_PLAYER_POSITION[0] + PLAYER_WIDTH and
            LEFT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= LEFT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1
        WAS_HIT = 1

    if (BALL_POSITION[0] + BALL_SIZE / 2 >= RIGHT_PLAYER_POSITION[0] and
            RIGHT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= RIGHT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1
        WAS_HIT = 1


# Detect if a goal was made, and reset the variables
def detect_score():
    global BALL_POSITION, WAS_GOAL, BALL_SPEED_X, BALL_SPEED_Y
    if BALL_POSITION[0] < 0 or BALL_POSITION[0] > SCREEN_WIDTH:
        BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        WAS_GOAL = 2
        BALL_SPEED_X = BALL_ORIGINAL_SPEED
        BALL_SPEED_Y = BALL_ORIGINAL_SPEED


# Player input
def keyboard(key, x, y):
    global LEFT_PLAYER_POSITION, RIGHT_PLAYER_POSITION
    if (key == b'w' or key == b'W') and (LEFT_PLAYER_POSITION[1] < SCREEN_HEIGHT - PLAYER_HEIGHT):
        LEFT_PLAYER_POSITION[1] += PLAYER_SPEED
    elif (key == b's' or key == b'S') and (LEFT_PLAYER_POSITION[1] > 0):
        LEFT_PLAYER_POSITION[1] -= PLAYER_SPEED
    elif (key == b'o' or key == b'O') and (RIGHT_PLAYER_POSITION[1] < SCREEN_HEIGHT - PLAYER_HEIGHT):
        RIGHT_PLAYER_POSITION[1] += PLAYER_SPEED
    elif (key == b'l' or key == b'L') and (RIGHT_PLAYER_POSITION[1] > 0):
        RIGHT_PLAYER_POSITION[1] -= PLAYER_SPEED


# Halt the execution for one second to help the players to see that the goal was made
def wait_ball():
    global WAS_GOAL, WAS_HIT, SCORE
    if WAS_GOAL > 0:
        if WAS_GOAL == 1:
            WAS_GOAL = 0
            WAS_HIT = 0
            time.sleep(0.5)
        else:
            WAS_GOAL = 1


# Method to increase difficulty for each player hit on the ball
def increase_difficulty():
    global WAS_HIT, BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y
    if WAS_HIT == 1:
        WAS_HIT = 0
        BALL_SPEED_X += 0.2
        BALL_SPEED_Y += 0.2


# display callback function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_field()
    draw_players()
    draw_ball()
    update_ball()
    detect_collision()
    detect_score()
    write_score(SCORE)
    increase_difficulty()
    glutSwapBuffers()
    wait_ball()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Pong For Two - Renan&Renan")
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboard)
glClearColor(0.09, 0.60, 0.43, 1.0)  # background for the field, this RGB code produces is a light green
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()
