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







def draw_player(): #generates the player on the screen


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

    
