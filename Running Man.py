#cse423_project
#runnning_man

from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import time
import math


camera_position= (0,50,200)
camera_tracking=(0,0,0)

GAME_RUNNING=0
GAME_OVER=1
GAME_PAUSED=2
game_status=GAME_RUNNING

player_position=(0,0,0)
player_lane=1
player_jumping=False
player_sliding=False
slide_timer=0
slide_duration=1.5
jump_height=0.0
jump_velocity=0.0
JUMP_INITIAL_VELOCITY=12
GRAVITY=0.5
JUMP_WINDOW=40
LANE_WIDTH=60

PATH_SEGMENT_LENGTH=10
path_segments=[]
MAX_VISIBLE_SEGMENTS=10
total_distance=0.0

score=0
coins_collected=0
game_speed=0.3
MAX_SPEED=5.0
SPEED_INCREMENT=0.05
game_start_time=time.time()







def draw_player():
    global player_lane, jump_height, player_sliding

    x = (player_lane - 1) * LANE_WIDTH
    y = jump_height
    z = 0

    glPushMatrix()
    glTranslatef(x, y, z)
    human_height = 70.0
    glScalef(0.8, 0.8, 0.8)

    if not player_jumping:
        bounce_height = 3.0 * abs(math.sin(time.time() * 10))
        glTranslatef(0, bounce_height, 0)

    if player_sliding:
        glTranslatef(0, -human_height * 0.3, 0)

    glPushMatrix()
    glColor3f(0.7, 0.5, 0.3)
    if player_sliding:
        glTranslatef(0, human_height * 0.45, 0)
        glRotatef(30, 1, 0, 0)
    else:
        glTranslatef(0, human_height * 0.5, 0)
    glScalef(1.0, 1.5, 0.7)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.8, 0.6, 0.4)
    if player_sliding:
        glTranslatef(0, human_height * 0.75, 5)
        glRotatef(30, 1, 0, 0)
    else:
        glTranslatef(0, human_height * 0.85, 0)
    glPushMatrix()
    glTranslatef(0, -5, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 12, 4)
    glPopMatrix()
    glutSolidSphere(7, 16, 16)
    glColor3f(1.0, 1.0, 1.0)
    pass
    glColor3f(0.2, 0.1, 0.0)
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(1.1, 0.7, 1.1)
    glutSolidSphere(7, 16, 16)
    glPopMatrix()
    glColor3f(0.2, 0.1, 0.0)
    for angle in range(0, 360, 45):
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0, 2, 5)
        glScalef(0.3, 0.3, 1.0)
        glutSolidSphere(3, 8, 8)
        glPopMatrix()
    glColor3f(0.2, 0.1, 0.0)
    glPushMatrix()
    glTranslatef(0, 2, 0)
    glScalef(1.1, 0.7, 1.1)
    glutSolidSphere(7, 16, 16)
    glPopMatrix()
    glPopMatrix()

    arm_cycle_speed = 10
    arm_swing_amplitude = 40
    if player_sliding:
        arm_swing_amplitude = 20
        arm_forward_offset = 30
    else:
        arm_forward_offset = 0
    swing_angle = arm_swing_amplitude * math.sin(time.time() * arm_cycle_speed)

    glPushMatrix()
    glColor3f(0.7, 0.5, 0.3)
    glTranslatef(-7, human_height * 0.7, 0)
    glutSolidSphere(3, 12, 12)
    glPushMatrix()
    glRotatef(-swing_angle, 1, 0, 0)
    glRotatef(arm_forward_offset, 1, 0, 0)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glutSolidSphere(2, 12, 12)
    elbow_bend = -30 - 15 * math.sin(time.time() * arm_cycle_speed)
    if player_sliding:
        elbow_bend -= 30
    glRotatef(elbow_bend, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 2, 1.5, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glutSolidSphere(2, 12, 12)
    elbow_bend = 30 + 15 * math.sin(time.time() * arm_cycle_speed)
    if player_sliding:
        elbow_bend += 30
    glRotatef(elbow_bend, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 2, 1.5, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glColor3f(0.75, 0.55, 0.35)
    glutSolidSphere(2.5, 10, 10)
    glColor3f(0.75, 0.55, 0.35)
    glutSolidSphere(2.5, 10, 10)
    glPopMatrix()
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.7, 0.5, 0.3)
    glTranslatef(7, human_height * 0.7, 0)
    glutSolidSphere(3, 12, 12)
    glPushMatrix()
    glRotatef(swing_angle, 1, 0, 0)
    glRotatef(arm_forward_offset, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glutSolidSphere(2, 12, 12)
    elbow_bend = 20 - 10 * math.sin(time.time() * arm_cycle_speed)
    if player_sliding:
        elbow_bend += 40
    glRotatef(elbow_bend, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 2, 1.5, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glColor3f(0.75, 0.55, 0.35)
    glutSolidSphere(2.5, 10, 10)
    glPopMatrix()
    glPopMatrix()

    leg_cycle_speed = 10
    leg_swing_amplitude = 45
    leg_swing_angle = leg_swing_amplitude * math.sin(time.time() * leg_cycle_speed)

    for side, dx in [(1, -3.5), (-1, 3.5)]:
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.7)
        glTranslatef(dx, human_height * 0.4, 0)
        glutSolidSphere(3, 12, 12)
        glPushMatrix()
        leg_angle = -side * leg_swing_angle
        if player_sliding:
            glRotatef(-30 + (leg_angle * 0.3), 1, 0, 0)
            glRotatef(60, 1, 0, 0)
        else:
            glRotatef(leg_angle, 1, 0, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 3, 2.5, 15, 12, 4)
        glTranslatef(0, 0, 15)
        glutSolidSphere(2.5, 12, 12)
        if player_sliding:
            knee_bend = 60
        else:
            knee_bend = 20 + 30 * max(0, -math.sin(time.time() * leg_cycle_speed * side))
        glRotatef(knee_bend, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
        glTranslatef(0, 0, 15)
        glutSolidSphere(2, 10, 10)
        glColor3f(0.2, 0.1, 0.1)
        foot_angle = 15 * math.sin(time.time() * leg_cycle_speed * side)
        if player_sliding:
            foot_angle = 0
        glRotatef(-foot_angle, 1, 0, 0)
        glTranslatef(0, -2, 2)
        glScalef(1.0, 1.0, 2.5)
        glutSolidCube(2.5)
        glPopMatrix()
        glPopMatrix()

    glPushMatrix()
    glColor3f(0.1, 0.6, 0.1)
    if player_sliding:
        glTranslatef(0, human_height * 0.55, 0)
        glRotatef(30, 1, 0, 0)
    else:
        glTranslatef(0, human_height * 0.6, 0)
    glScalef(1.1, 1.5, 0.8)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.7)
    if player_sliding:
        glTranslatef(0, human_height * 0.3, 0)
    else:
        glTranslatef(0, human_height * 0.35, 0)
    glScalef(1.2, 0.8, 0.9)
    glutSolidCube(10)
    glPopMatrix()

    glPopMatrix()


def draw_text(): #displays text on the screen


def draw_shapes():



def keyboard_listener(): #keyborad inputs
   


def special_key_listener(): #special key inputs



def  setup_camera(): #viewing camera 3rd person view


def update_game():
    

def idle(): #functions keeps running in backgound
    update_game()
    glutPostRedisplay()


def show_screen(): #displays the screen
    



def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(show_screen)  # Register display function
    glutKeyboardFunc(keyboard_listener)  # Register keyboard listener
    glutSpecialFunc(special_key_listener)
    #glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()

    
