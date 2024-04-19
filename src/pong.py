from OpenGL.GL import *
from OpenGL.GLUT import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 100
BALL_SIZE = 15
PLAYER_SPEED = 25
BALL_SPEED_X = 3
BALL_SPEED_Y = 3
LEFT_PLAYER_POSITION = [10, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
RIGHT_PLAYER_POSITION = [SCREEN_WIDTH - 10 - PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
BALL_DIRECTION = [1, 1]


def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def draw_players():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(LEFT_PLAYER_POSITION[0], LEFT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)
    draw_rectangle(RIGHT_PLAYER_POSITION[0], RIGHT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)


def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(BALL_POSITION[0] - BALL_SIZE / 2, BALL_POSITION[1] - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)


def update_ball():
    global BALL_POSITION, BALL_DIRECTION
    BALL_POSITION[0] += BALL_DIRECTION[0] * BALL_SPEED_X
    BALL_POSITION[1] += BALL_DIRECTION[1] * BALL_SPEED_Y


def detect_collision():
    # collision with borders
    if BALL_POSITION[1] <= 0 or BALL_POSITION[1] >= SCREEN_HEIGHT:
        BALL_DIRECTION[1] *= -1

    # collision with the players
    if (BALL_POSITION[0] - BALL_SIZE / 2 <= LEFT_PLAYER_POSITION[0] + PLAYER_WIDTH and
            LEFT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= LEFT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1

    if (BALL_POSITION[0] + BALL_SIZE / 2 >= RIGHT_PLAYER_POSITION[0] and
            RIGHT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= RIGHT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1


def detect_score():
    global BALL_POSITION
    if BALL_POSITION[0] <= 0 or BALL_POSITION[0] >= SCREEN_WIDTH:
        BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]


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


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    draw_players()
    draw_ball()
    update_ball()
    detect_collision()
    detect_score()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"Pong For Two - Renan&Renan")

glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboard)

glClearColor(0.09, 0.60, 0.43, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)

glutMainLoop()
