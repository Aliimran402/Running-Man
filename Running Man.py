#cse423_project
#runnning_man

from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import random
import time
import math


GAME_RUNNING=0
GAME_OVER=1
GAME_PAUSED=2
game_status=GAME_RUNNING

player_lane = 1  
player_jumping = False
jump_height = 0.5
jump_velocity = 0.9 
JUMP_INITIAL_VELOCITY = 8  
GRAVITY = 0.21 
JUMP_WINDOW = 30  
LANE_WIDTH = 60


PATH_SEGMENT_LENGTH = 500 
path_segments = []  
MAX_VISIBLE_SEGMENTS = 10  
total_distance = 0  
current_direction = 0 

obstacles = []  
coins = []  
OBSTACLE_PROBABILITY = 5.0  
COIN_PROBABILITY = 0.8  
OBSTACLE_DENSITY_FACTOR = 0.005  

score = 0  
coins_collected = 0
game_speed = 2.0 
stored_game_speed = 2.0  
MAX_SPEED = 10.0
SPEED_INCREMENT = 0.15 
game_start_time = time.time()


POWERUP_TYPES = ['magnet', 'shield']
POWERUP_PROBABILITY = 0.05  
POWERUP_DURATION = 10  
active_powerups = {
    'magnet': {'active': False, 'end_time': 0},
    'shield': {'active': False, 'end_time': 0}
}
powerups = []  
MAGNET_RANGE = 150  


COLORS = {
    'temple_stone': (0.7, 0.65, 0.5),
    'path': (0.6, 0.5, 0.4),
    'obstacle': (0.8, 0.2, 0.2),
    'coin': (1.0, 0.84, 0.0),
    'sky': (0.5, 0.7, 1.0),
    'text': (1.0, 1.0, 1.0),
    'magnet': (0.0, 0.7, 1.0), 
    'shield': (0.0, 1.0, 0.7)   
}


def reset_game():
    
    
def generate_path_segment():
    
    
def draw_text(): 
    
       

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



def draw_path():
    
    
def draw_obstacles():    


def draw_coins():
    
def draw_powerups():
    

def draw_background():
    glPushMatrix()
    glDisable(GL_DEPTH_TEST)
    radius = 1000
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.53, 0.81, 0.92)
    glVertex3f(0, radius, 0)
    slices = 20
    stacks = 10
    for i in range(slices + 1):
        angle = 2.0 * math.pi * i / slices
        x = math.cos(angle)
        z = math.sin(angle)
        glColor3f(0.4, 0.7, 0.9)
        glVertex3f(radius * x, 0, radius * z)
    glEnd()
    glBegin(GL_QUADS)
    path_width = LANE_WIDTH * 3
    ocean_width = 800
    ocean_length = 2000
    glColor3f(0.0, 0.6, 0.8)
    glVertex3f(-path_width/2 - ocean_width, -15, -ocean_length)
    glVertex3f(-path_width/2, -15, -ocean_length)
    glColor3f(0.0, 0.4, 0.8)
    glVertex3f(-path_width/2, -15, ocean_length)
    glVertex3f(-path_width/2 - ocean_width, -15, ocean_length)
    glColor3f(0.0, 0.6, 0.8)
    glVertex3f(path_width/2, -15, -ocean_length)
    glVertex3f(path_width/2 + ocean_width, -15, -ocean_length)
    glColor3f(0.0, 0.4, 0.8)
    glVertex3f(path_width/2 + ocean_width, -15, ocean_length)
    glVertex3f(path_width/2, -15, ocean_length)
    glEnd()
    num_waves = 20
    wave_width = ocean_width / num_waves
    glBegin(GL_LINES)
    glColor3f(0.3, 0.7, 0.9)
    for i in range(num_waves):
        for z in range(-ocean_length, ocean_length, 100):
            wave_offset = math.sin(time.time() * 2 + i * 0.5) * 5
            x1 = -path_width/2 - (i * wave_width)
            x2 = -path_width/2 - ((i+1) * wave_width)
            glVertex3f(x1, -15 + wave_offset, z)
            glVertex3f(x2, -15 + wave_offset, z)
    for i in range(num_waves):
        for z in range(-ocean_length, ocean_length, 100):
            wave_offset = math.sin(time.time() * 2 + i * 0.5) * 5
            x1 = path_width/2 + (i * wave_width)
            x2 = path_width/2 + ((i+1) * wave_width)
            glVertex3f(x1, -15 + wave_offset, z)
            glVertex3f(x2, -15 + wave_offset, z)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()

    

def draw_game_over_screen():
    
            
    
def update_game():
    

def handle_movement():                    



def keyboard_listener(): #keyborad inputs
   


def specialkey_listener(): #special key inputs



def  setup_camera(): #viewing camera 3rd person view


    

def idle(): #functions keeps running in backgound
    update_game()
    glutPostRedisplay()


def show_screen(): #displays the screen
    



def main():
    """Main function to set up OpenGL window and loop"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Running Man OpenGL")
    
    glEnable(GL_DEPTH_TEST)
    
    glClearColor(0.2, 0.2, 0.2, 1.0)
    
    glEnable(GL_COLOR_MATERIAL)
    
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(specialkey_listener)
    glutIdleFunc(idle)
      
    reset_game()
    
    glutMainLoop()

if __name__ == "__main__":
    main()

    
