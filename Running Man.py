#cse423_project
#runnning_man

from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import time
import math

#initializing_player window


def draw_player(): #generates the player on the screen


def draw_text(): #displays text on the screen


def draw_shapes():



def keyboard_listener(): #keyborad inputs
   


def special_key_listener(): #special key inputs



def  setup_camera(): #viewing camera 3rd person view



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
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()

    
