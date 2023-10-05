import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Constants
SUN_RADIUS = 2.0
PLANET_RADIUS = [0.4, 0.9, 1.0, 1.05, 1.9, 1.3, 1.2]  # Adjusted radii of the planets
PLANET_DISTANCE = [4, 7, 10, 15, 22, 28, 34]  # Adjusted distances of the planets from the sun
PLANET_PERIOD = [0.24, 0.62, 1.0, 1.88, 11.86, 29.46, 84.07]  # Orbital periods of the planets (in Earth years)
PLANET_COLORS = [
    (0.8, 0.6, 0.2),  # Mercury
    (0.6, 0.6, 0.6),  # Venus
    (0.0, 0.4, 0.8),  # Earth
    (0.9, 0.4, 0.1),  # Mars
    (0.9, 0.8, 0.6),  # Jupiter
    (0.6, 0.6, 0.6),  # Saturn
    (0.4, 0.6, 0.8)   # Uranus
]

# Initialize Pygame and set up the display
pygame.init()
width, height = 800, 600
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("3D Solar System")

# Set up perspective projection
gluPerspective(45, (width / height), 1, 100.0)

# Set up initial camera position
camera_distance = 40.0
glTranslatef(0.0, 0.0, -camera_distance)

# Initial velocities and periods of planets
planet_velocities = [0.0] * len(PLANET_PERIOD)
planet_periods = list(PLANET_PERIOD)

# Function to draw the orbit of a planet
def draw_orbit(distance):
    glBegin(GL_LINE_LOOP)
    for i in range(360):
        angle = math.radians(i)
        x = distance * math.cos(angle)
        y = distance * math.sin(angle)
        glVertex3f(x, y, 0.0)
    glEnd()

# Main loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # Scroll Up
            camera_distance += 1.0
            glTranslatef(0.0, 0.0, 1.0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # Scroll Down
            camera_distance -= 1.0
            glTranslatef(0.0, 0.0, -1.0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                planet_velocities = [v + 1.0 for v in planet_velocities]
            elif event.key == pygame.K_DOWN:
                planet_velocities = [v - 1.0 for v in planet_velocities]
            elif event.key == pygame.K_1:  # Increase period
                planet_periods = [p + 0.1 for p in planet_periods]
            elif event.key == pygame.K_2:  # Decrease period
                planet_periods = [p - 0.1 for p in planet_periods]

    # Handle mouse movement
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_rel()
        glRotatef(x, 0, 1, 0)
        glRotatef(y, 1, 0, 0)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the sun
    glColor3fv((1, 1, 0))
    gluSphere(gluNewQuadric(), SUN_RADIUS, 100, 100)

    # Draw orbits and planets
    for i, (radius, distance, period, color, velocity) in enumerate(zip(PLANET_RADIUS, PLANET_DISTANCE, planet_periods, PLANET_COLORS, planet_velocities)):
        glColor3fv(color)
        
        # Draw orbit
        draw_orbit(distance)
        
        # Calculate the angle based on the period and velocity
        angle = 360.0 * pygame.time.get_ticks() / (period * 1000)  # Convert to seconds
        angle += velocity
        
        # Calculate planet position
        x = distance * math.cos(math.radians(angle))
        y = distance * math.sin(math.radians(angle))
        
        # Draw planet
        glPushMatrix()
        glTranslatef(x, y, 0)
        gluSphere(gluNewQuadric(), radius, 100, 100)
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
    clock.tick(60)
