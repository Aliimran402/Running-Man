from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
import time

GAME_RUNNING = 0
GAME_OVER = 1
GAME_PAUSED = 2
game_state = GAME_RUNNING

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
POWERUP_PROBABILITY = 0.1
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

    global game_state, player_pos, player_lane, player_jumping
    global jump_height, jump_velocity, path_segments, obstacles, coins, powerups
    global score, coins_collected, game_speed, game_start_time, total_distance
    global current_direction, active_powerups
    
    game_state = GAME_RUNNING
    player_pos = (0, 0, 0)
    player_lane = 1
    player_jumping = False
    jump_height = 0
    jump_velocity = 0
    
    path_segments = []
    obstacles = []
    coins = []
    powerups = []
    
    active_powerups = {
        'magnet': {'active': False, 'end_time': 0},
        'shield': {'active': False, 'end_time': 0}
    }
    
    for i in range(MAX_VISIBLE_SEGMENTS):
        generate_path_segment()
    
    score = 0
    coins_collected = 0
    game_speed = 2.0
    game_start_time = time.time()
    total_distance = 0
    current_direction = 0
    
def generate_path_segment():
    global path_segments, current_direction
    
    if len(path_segments) == 0:
        segment_z = -PATH_SEGMENT_LENGTH / 2
        segment_x = 0
        segment_angle = 0
    else:
        prev_segment = path_segments[-1]
        segment_z = prev_segment['z'] - PATH_SEGMENT_LENGTH
        segment_x = 0
        segment_angle = 0
    
    segment = {
        'x': segment_x,
        'z': segment_z,
        'angle': segment_angle
    }
    path_segments.append(segment)
    
    current_obstacle_prob = min(OBSTACLE_PROBABILITY + total_distance * OBSTACLE_DENSITY_FACTOR, 0.5)
    
    if random.random() < current_obstacle_prob and len(path_segments) > 3:
        obstacle_lane = random.randint(0, 2)
        obstacle_z_offset = random.uniform(-PATH_SEGMENT_LENGTH/2, PATH_SEGMENT_LENGTH/2)
        obstacle_type = random.choice(['rock', 'tree'])
        obstacle_x = (obstacle_lane - 1) * LANE_WIDTH
        obstacle_z = segment_z + obstacle_z_offset
        
        obstacles.append({
            'x': obstacle_x,
            'z': obstacle_z,
            'lane': obstacle_lane,
            'type': obstacle_type,
            'angle': segment_angle
        })
    
    if random.random() < COIN_PROBABILITY and len(path_segments) > 3:
        coin_lane = random.randint(0, 2)
        coin_z_offset = random.uniform(-PATH_SEGMENT_LENGTH/2, PATH_SEGMENT_LENGTH/2)
        coin_x = (coin_lane - 1) * LANE_WIDTH
        coin_z = segment_z + coin_z_offset
        
        coins.append({
            'x': coin_x,
            'z': coin_z,
            'lane': coin_lane,
            'collected': False,
            'angle': segment_angle
        })
    
    if random.random() < POWERUP_PROBABILITY and len(path_segments) > 3:
        powerup_lane = random.randint(0, 2)
        powerup_z_offset = random.uniform(-PATH_SEGMENT_LENGTH/2, PATH_SEGMENT_LENGTH/2)
        powerup_type = random.choice(POWERUP_TYPES)
        powerup_x = (powerup_lane - 1) * LANE_WIDTH
        powerup_z = segment_z + powerup_z_offset
        
        powerups.append({
            'x': powerup_x,
            'z': powerup_z,
            'lane': powerup_lane,
            'type': powerup_type,
            'collected': False,
            'angle': segment_angle
        })
   
    
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(*COLORS['text'])
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
       

def draw_player():
    global player_lane, jump_height

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

    glPushMatrix()
    glColor3f(0.7, 0.5, 0.3)
    glTranslatef(0, human_height * 0.5, 0)
    glScalef(1.0, 1.5, 0.7)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.8, 0.6, 0.4)
    glTranslatef(0, human_height * 0.85, 0)
    glPushMatrix()
    glTranslatef(0, -5, 0)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 12, 4)
    glPopMatrix()
    glutSolidSphere(7, 16, 16)
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
    glPopMatrix()

    arm_cycle_speed = 10
    arm_swing_amplitude = 40
    swing_angle = arm_swing_amplitude * math.sin(time.time() * arm_cycle_speed)

    glPushMatrix()
    glColor3f(0.7, 0.5, 0.3)
    glTranslatef(-7, human_height * 0.7, 0)
    glutSolidSphere(3, 12, 12)
    glPushMatrix()
    glRotatef(-swing_angle, 1, 0, 0)
    glRotatef(180, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glutSolidSphere(2, 12, 12)
    elbow_bend = -30 - 15 * math.sin(time.time() * arm_cycle_speed)
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
    gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
    glTranslatef(0, 0, 15)
    glutSolidSphere(2, 12, 12)
    elbow_bend = 20 - 10 * math.sin(time.time() * arm_cycle_speed)
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
        glRotatef(leg_angle, 1, 0, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 3, 2.5, 15, 12, 4)
        glTranslatef(0, 0, 15)
        glutSolidSphere(2.5, 12, 12)
        knee_bend = 20 + 30 * max(0, -math.sin(time.time() * leg_cycle_speed * side))
        glRotatef(knee_bend, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 2.5, 2, 15, 12, 4)
        glTranslatef(0, 0, 15)
        glutSolidSphere(2, 10, 10)
        glColor3f(0.2, 0.1, 0.1)
        foot_angle = 15 * math.sin(time.time() * leg_cycle_speed * side)
        glRotatef(-foot_angle, 1, 0, 0)
        glTranslatef(0, -2, 2)
        glScalef(1.0, 1.0, 2.5)
        glutSolidCube(2.5)
        glPopMatrix()
        glPopMatrix()

    glPushMatrix()
    glColor3f(0.1, 0.6, 0.1)
    glTranslatef(0, human_height * 0.6, 0)
    glScalef(1.1, 1.5, 0.8)
    glutSolidCube(10)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0.2, 0.2, 0.7)
    glTranslatef(0, human_height * 0.35, 0)
    glScalef(1.2, 0.8, 0.9)
    glutSolidCube(10)
    glPopMatrix()

    glPopMatrix()



def draw_path():
    global path_segments, total_distance
    
    for segment in path_segments:
        glPushMatrix()
        glTranslatef(segment['x'], 0, segment['z'])
        glRotatef(segment['angle'], 0, 1, 0)
        
        glBegin(GL_QUADS)
        glColor3f(*COLORS['path'])
        
        path_width = LANE_WIDTH * 3
        
        glVertex3f(-path_width/2, -5, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, -5, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, -5, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, -5, -PATH_SEGMENT_LENGTH/2)
        
        wall_height = 30
        
        glColor3f(*COLORS['temple_stone'])
        glVertex3f(-path_width/2, -5, PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, -5, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, wall_height, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, wall_height, PATH_SEGMENT_LENGTH/2)
        
        glVertex3f(path_width/2, -5, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, wall_height, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, wall_height, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, -5, -PATH_SEGMENT_LENGTH/2)
        
        glVertex3f(-path_width/2-10, wall_height, PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, wall_height, PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2, wall_height, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(-path_width/2-10, wall_height, -PATH_SEGMENT_LENGTH/2)
        
        glVertex3f(path_width/2, wall_height, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2+10, wall_height, PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2+10, wall_height, -PATH_SEGMENT_LENGTH/2)
        glVertex3f(path_width/2, wall_height, -PATH_SEGMENT_LENGTH/2)
        
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(0.8, 0.8, 0.8)
        
        glVertex3f(-LANE_WIDTH, -4.99, PATH_SEGMENT_LENGTH/2)
        glVertex3f(-LANE_WIDTH, -4.99, -PATH_SEGMENT_LENGTH/2)
        
        glVertex3f(LANE_WIDTH, -4.99, PATH_SEGMENT_LENGTH/2)
        glVertex3f(LANE_WIDTH, -4.99, -PATH_SEGMENT_LENGTH/2)
        
        glEnd()
        
        glPopMatrix()

    
def draw_obstacles():    
    global obstacles
    
    for obstacle in obstacles:
        glPushMatrix()
        
        glTranslatef(obstacle['x'], 0, obstacle['z'])
        glRotatef(obstacle['angle'], 0, 1, 0)
        
        glColor3f(*COLORS['obstacle'])
        
        if obstacle['type'] == 'rock':
            glTranslatef(0, 0, 0)
            glutSolidSphere(12, 8, 8)
        elif obstacle['type'] == 'tree':
            glColor3f(0.55, 0.27, 0.07)
            glTranslatef(0, 23, 0)
            glRotatef(90, 1, 0, 0)
            gluCylinder(gluNewQuadric(), 12, 12, 58, 8, 2)
            
            glColor3f(0.0, 0.5, 0.0)
            glTranslatef(0, 0, -69)
            glutSolidCone(46, 92, 8, 8)
        
        glPopMatrix()



def draw_coins():
    global coins
    
    for coin in coins:
        if not coin['collected']:
            glPushMatrix()
            
            glTranslatef(coin['x'], 10, coin['z'])
            glRotatef(coin['angle'], 0, 1, 0)
            
            glRotatef(90, 1, 0, 0)
            
            current_time = time.time() % 360
            glRotatef(current_time * 50, 0, 0, 1)
            
            glColor3f(*COLORS['coin'])
            
            gluDisk(gluNewQuadric(), 0, 10, 15, 1)
            
            glPopMatrix()
    
def draw_powerups():
    global powerups
    
    for powerup in powerups:
        if not powerup['collected']:
            glPushMatrix()
            
            glTranslatef(powerup['x'], 15, powerup['z'])
            glRotatef(powerup['angle'], 0, 1, 0)
            
            current_time = time.time()
            float_height = 5 * math.sin(current_time * 3)
            glTranslatef(0, float_height, 0)
            glRotatef(current_time * 100, 0, 1, 0)
            
            if powerup['type'] == 'magnet':
                glColor3f(*COLORS['magnet'])
                glutSolidCube(15)
            else:
                glColor3f(*COLORS['shield'])
                glutSolidSphere(10, 16, 16)
            
            glPopMatrix()

def draw_skybox():
    glPushMatrix()
    
    glDisable(GL_DEPTH_TEST)
    
    radius = 1000
    
    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0.53, 0.81, 0.92)
    glVertex3f(0, radius, 0)
    
    slices = 20
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
    draw_text(400, 400, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 350, f"Coins Collected: {coins_collected}", GLUT_BITMAP_HELVETICA_18)
    draw_text(350, 290, "Press 'R' to restart", GLUT_BITMAP_HELVETICA_18)   
            
    
def update_game():
    global total_distance, path_segments, obstacles, coins, powerups
    global player_jumping, jump_height, jump_velocity
    global score, game_speed, game_state, coins_collected
    global active_powerups
    
    if game_state == GAME_OVER:
        return
    
    total_distance += game_speed
    
    if player_jumping:
        jump_height += jump_velocity
        jump_velocity -= GRAVITY
        
        if jump_height <= 0:
            jump_height = 0
            jump_velocity = 0
            player_jumping = False
    
    for i in range(len(path_segments)):
        path_segments[i]['z'] += game_speed
    
    if path_segments[0]['z'] > PATH_SEGMENT_LENGTH:
        path_segments.pop(0)
        generate_path_segment()
    
    for i in range(len(obstacles)):
        obstacles[i]['z'] += game_speed
    
    obstacles = [obs for obs in obstacles if obs['z'] < PATH_SEGMENT_LENGTH]
    
    for i in range(len(coins)):
        coins[i]['z'] += game_speed
    
    coins = [coin for coin in coins if coin['z'] < PATH_SEGMENT_LENGTH]
    
    for i in range(len(powerups)):
        powerups[i]['z'] += game_speed
    
    powerups = [p for p in powerups if p['z'] < PATH_SEGMENT_LENGTH]
    
    player_x = (player_lane - 1) * LANE_WIDTH
    for powerup in powerups:
        if not powerup['collected']:
            dx = abs(player_x - powerup['x'])
            dz = abs(powerup['z'])
            
            if dx < 30 and dz < 30:
                powerup['collected'] = True
                active_powerups[powerup['type']]['active'] = True
                active_powerups[powerup['type']]['end_time'] = time.time() + POWERUP_DURATION
    
    current_time = time.time()
    for powerup_type in active_powerups:
        if active_powerups[powerup_type]['active'] and current_time > active_powerups[powerup_type]['end_time']:
            active_powerups[powerup_type]['active'] = False
    
    if active_powerups['magnet']['active']:
        for coin in coins:
            if not coin['collected']:
                dx = player_x - coin['x']
                dz = -coin['z']
                distance = math.sqrt(dx*dx + dz*dz)
                
                if distance < MAGNET_RANGE:
                    move_speed = 5.0
                    if distance > 0:
                        coin['x'] += (dx/distance) * move_speed
                        coin['z'] += (dz/distance) * move_speed
    
    if not active_powerups['shield']['active']:
        for obstacle in obstacles:
            dx = abs(player_x - obstacle['x'])
            dz = abs(obstacle['z'])
            
            if dx < 30 and dz < JUMP_WINDOW:
                if obstacle['type'] == 'rock' and jump_height > 10:
                    continue
                elif obstacle['type'] == 'tree' and jump_height > 20:
                    continue
               
                
                game_state = GAME_OVER
    
    for coin in coins:
        if not coin['collected']:
            dx = abs(player_x - coin['x'])
            dz = abs(coin['z'])
            
            if dx < 30 and dz < 30:
                coin['collected'] = True
                coins_collected += 1
                score = coins_collected
                if game_speed < MAX_SPEED:
                    game_speed += SPEED_INCREMENT
                      
    

def handle_movement(direction):   
    global player_lane
    if direction == 'left' and player_lane > 0:
        player_lane -= 1
    elif direction == 'right' and player_lane < 2:
        player_lane += 1



def keyboardListener(key,x,y):
    global player_lane, player_jumping, jump_velocity, game_state, game_speed, stored_game_speed
    
    if game_state == GAME_OVER:
        if key == b'r':
            reset_game()
        return
    
    if key == b'p':
        if game_state == GAME_RUNNING:
            game_state = GAME_PAUSED
            stored_game_speed = game_speed
            game_speed = 0
        else:
            game_state = GAME_RUNNING
            game_speed = stored_game_speed
        return
    
    if game_state != GAME_RUNNING:
        return
    
    if key == b'a':
        handle_movement('left')
    elif key == b'd':
        handle_movement('right')
    
    if (key == b'w' or key == b' ') and not player_jumping:
        player_jumping = True
        jump_velocity = JUMP_INITIAL_VELOCITY
    
    if key == b'r':
        reset_game()

def specialKeyListener(key,x,y):
    global player_lane, player_jumping, jump_velocity, game_state
    
    if game_state == GAME_OVER:
        return
    
    if game_state != GAME_RUNNING:
        return
    
    if key == GLUT_KEY_LEFT:
        handle_movement('left')
    elif key == GLUT_KEY_RIGHT:
        handle_movement('right')
    
    if key == GLUT_KEY_UP and not player_jumping:
        player_jumping = True
        jump_velocity = JUMP_INITIAL_VELOCITY


def  setup_camera(): 
    global  player_lane, jump_height
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.25, 0.1, 2000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    player_x = (player_lane - 1) * LANE_WIDTH
    camera_target = (player_x, jump_height + 15, 0)
    
    camera_x = player_x
    camera_y = jump_height + 65
    camera_z = 150
    
    gluLookAt(camera_x, camera_y, camera_z,
              camera_target[0], camera_target[1], camera_target[2],
              0, 1, 0)


    

def idle(): 
    update_game()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    
    setup_camera()
    
    draw_skybox()
    
    draw_path()
    draw_obstacles()
    draw_coins()
    draw_player()
    draw_powerups()
    
    if game_state == GAME_RUNNING:
        draw_text(10, 730, f"Score: {score}")
        draw_text(10, 700, f"Coins: {coins_collected}")
        draw_text(10, 670, f"Speed: {game_speed:.1f}")
        
        y_offset = 640
        current_time = time.time()
        for powerup_type in POWERUP_TYPES:
            if active_powerups[powerup_type]['active']:
                remaining_time = max(0, int(active_powerups[powerup_type]['end_time'] - current_time))
                draw_text(10, y_offset, f"{powerup_type.capitalize()} Power-Up: {remaining_time}s")
                y_offset -= 30
    elif game_state == GAME_PAUSED:
        draw_text(400, 400, "GAME PAUSED", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(350, 350, "Press 'P' to resume", GLUT_BITMAP_HELVETICA_18)    
    else:
        draw_game_over_screen()
    
    draw_text(800, 730, "A/D: Move")
    draw_text(800, 710, "W: Jump")
    draw_text(800, 690, "R: Restart")
    draw_text(800, 670, "P: Pause/Resume")
    
    glutSwapBuffers()
    

    



def main():
    """Main function to set up OpenGL window and loop"""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    winddow = glutCreateWindow(b"Running Man OpenGL")
    
    glEnable(GL_DEPTH_TEST)
    
    glClearColor(0.2, 0.2, 0.2, 1.0)
    
    glEnable(GL_COLOR_MATERIAL)
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutIdleFunc(idle)
    
    reset_game()
    
    glutMainLoop()

if __name__ == "__main__":
    main()
    
