#########################################
#   PONG PARA DOIS (PONG FOR TWO) 2024  #
#   RENAN DA ROSA                       #
#   RENAN EUZEBIO                       #
#########################################

# import das bibliotecas utilizadas
from OpenGL.GL import *
from OpenGL.GLUT import *
import time

# declaração de variaveis globais
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 15
PLAYER_HEIGHT = 150
BALL_SIZE = 15
BALL_ORIGINAL_SPEED = 1  # Atualiza a velocidade da bola para 1 quando um gol ocorrer.
PLAYER_SPEED = 30
BALL_SPEED_X = 1
BALL_SPEED_Y = 1
LEFT_PLAYER_POSITION = [0, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
RIGHT_PLAYER_POSITION = [SCREEN_WIDTH - 0 - PLAYER_WIDTH, SCREEN_HEIGHT // 2 - PLAYER_HEIGHT // 2]
BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
BALL_DIRECTION = [1, 1]
WAS_GOAL, WAS_HIT, GOAL_PLAYER_1, GOAL_PLAYER_2 = 0, 0, 0, 0
SCORE = "0 : 0"


# Função utilitaria para desenhar um quadrado
def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


# Renderizar o a string do placar
def write_score(txt):
    glRasterPos2f(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.1)  # posição do texto
    for i in range(len(txt)):
        char = ord(txt[i])  # ascii value
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, char)  # (charset utilizado, char)


# desenha as bordas para sinalizar o campo
def draw_field():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(5.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-10, 1)
    glVertex2f(SCREEN_WIDTH + 10, 1)
    glVertex2f(SCREEN_WIDTH + 10, SCREEN_HEIGHT)
    glVertex2f(-10, SCREEN_HEIGHT)
    glEnd()


# Desenha os jogadores
def draw_players():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(LEFT_PLAYER_POSITION[0], LEFT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)
    draw_rectangle(RIGHT_PLAYER_POSITION[0], RIGHT_PLAYER_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT)


# Desenha a bola
def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    draw_rectangle(BALL_POSITION[0] - BALL_SIZE / 2, BALL_POSITION[1] - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE)


# Atualiza a localização da bola na tela
def update_ball():
    global BALL_POSITION, BALL_DIRECTION
    BALL_POSITION[0] += BALL_DIRECTION[0] * BALL_SPEED_X
    BALL_POSITION[1] += BALL_DIRECTION[1] * BALL_SPEED_Y


# Detecta colisão
def detect_collision():
    detect_border_collision()
    detect_player_collision()


# Detectar colisao com os jogadores
def detect_player_collision():
    global WAS_HIT

    if (BALL_POSITION[0] - BALL_SIZE / 2 <= LEFT_PLAYER_POSITION[0] + PLAYER_WIDTH and
            LEFT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= LEFT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1
        WAS_HIT = 1

    if (BALL_POSITION[0] + BALL_SIZE / 2 >= RIGHT_PLAYER_POSITION[0] and
            RIGHT_PLAYER_POSITION[1] <= BALL_POSITION[1] <= RIGHT_PLAYER_POSITION[1] + PLAYER_HEIGHT):
        BALL_DIRECTION[0] *= -1
        WAS_HIT = 1


# Detectar colisão com as bordas de cima e baixo
def detect_border_collision():
    if BALL_POSITION[1] <= 0 or BALL_POSITION[1] >= SCREEN_HEIGHT:
        BALL_DIRECTION[1] *= -1


# Detecta se ocorreu um gol
def detect_score():
    if BALL_POSITION[0] < 0:
        update_score_variables(False)
    elif BALL_POSITION[0] > SCREEN_WIDTH:
        update_score_variables(True)


# Atualiza as variaveis referentes ao gol
def update_score_variables(has_player_one_scored):
    global BALL_POSITION, WAS_GOAL, BALL_SPEED_X, BALL_SPEED_Y, GOAL_PLAYER_2, GOAL_PLAYER_1, SCORE
    if has_player_one_scored:
        GOAL_PLAYER_1 += 1
    else:
        GOAL_PLAYER_2 += 1

    SCORE = f"{GOAL_PLAYER_1} : {GOAL_PLAYER_2}"  # Atualização do placar
    BALL_POSITION = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    WAS_GOAL = 2
    BALL_SPEED_X = BALL_ORIGINAL_SPEED
    BALL_SPEED_Y = BALL_ORIGINAL_SPEED


# Input dos jogadores
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


# Para a execução da aplicação por um segundo, para ajudar os jogadores a perceber que ocorreu um gol
def wait_ball():
    global WAS_GOAL, WAS_HIT
    if WAS_GOAL > 0:
        if WAS_GOAL == 1:
            WAS_GOAL = 0
            WAS_HIT = 0
            time.sleep(0.5)
        else:
            WAS_GOAL = 1


# Metodo para aumentar a dificuldade do jogo, caso um gol nao seja feito
def increase_difficulty():
    global WAS_HIT, BALL_SIZE, BALL_SPEED_X, BALL_SPEED_Y
    if WAS_HIT == 1:
        WAS_HIT = 0
        BALL_SPEED_X += 0.2
        BALL_SPEED_Y += 0.2


# Funçao callback de display
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


# inicio do opengl
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(SCREEN_WIDTH, SCREEN_HEIGHT)
glutCreateWindow(b"T1-GC Renan Rosa e Renan Euzebio")
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(keyboard)
glClearColor(0.09, 0.60, 0.43, 1.0)  # background for the field, this RGB code produces is a light green
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT, -1, 1)
glMatrixMode(GL_MODELVIEW)
glutMainLoop()
