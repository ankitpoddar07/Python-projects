import pygame
import random
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ocean Ball Simulation with Splash Effects")

# Colors
BLUE = (50, 100, 255)
OCEAN_BLUE = (0, 105, 148)
LIGHT_BLUE = (173, 216, 230)
SAND = (194, 178, 128)
WHITE = (255, 255, 255)
FISH_COLORS = [(255, 100, 100), (255, 215, 0), (100, 255, 100), (255, 165, 0)]

# Water physics
WATER_LEVEL = HEIGHT - 150
WATER_DENSITY = 0.02
WATER_DRAG = 0.98
BUOYANCY = 0.3

# Ball settings
ball_radius = 30
ball_color = BLUE
x = random.randint(ball_radius, WIDTH - ball_radius)
y = ball_radius
vx = random.uniform(-3, 3)
vy = 0

# Physics constants
gravity = 0.5
bounce_factor = -0.7
friction = 0.95

# Track water entry for splash effect
last_water_state = False
splash_particles = []

# Fish class with jumping ability
class Fish:
    def __init__(self):
        self.size = random.randint(20, 50)
        self.reset_position()
        self.speed = random.uniform(0.5, 2.5)
        self.direction = random.choice([-1, 1])
        self.color = random.choice(FISH_COLORS)
        self.wobble = 0
        self.wobble_speed = random.uniform(0.05, 0.1)
        self.wobble_size = random.uniform(2, 5)
        self.is_jumping = False
        self.jump_vy = 0
        self.max_jumps = random.randint(1, 3)
        self.jump_count = 0
        
    def reset_position(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(WATER_LEVEL + 50, HEIGHT - 50)
        self.is_jumping = False
        self.jump_vy = 0
        
    def move(self):
        if self.is_jumping:
            # Apply gravity to jumping fish
            self.jump_vy += gravity * 0.5
            self.y += self.jump_vy
            
            # Fish can move while jumping
            self.x += self.speed * self.direction * 0.5
            
            # If fish falls back into water
            if self.y > WATER_LEVEL - self.size//4:
                self.y = WATER_LEVEL - self.size//4
                self.jump_count += 1
                
                # Decide whether to jump again or swim normally
                if self.jump_count < self.max_jumps and random.random() < 0.7:
                    self.jump_vy = random.uniform(-15, -8)
                else:
                    self.is_jumping = False
                    self.jump_count = 0
        else:
            # Normal swimming behavior
            self.x += self.speed * self.direction
            self.wobble += self.wobble_speed
            self.y += math.sin(self.wobble) * self.wobble_size
            
            # Change direction at edges
            if self.x < -50 and self.direction == -1:
                self.direction = 1
            elif self.x > WIDTH + 50 and self.direction == 1:
                self.direction = -1
                
    def jump(self):
        if not self.is_jumping and random.random() < 0.7:  # 70% chance to jump
            self.is_jumping = True
            self.jump_vy = random.uniform(-15, -8)
            self.max_jumps = random.randint(1, 3)
            
    def draw(self):
        # Draw fish body
        pygame.draw.ellipse(screen, self.color, 
                          (self.x - self.size//2, self.y - self.size//4, 
                           self.size, self.size//2))
        # Draw tail
        tail_points = [
            (self.x + self.size//2 * self.direction, self.y),
            (self.x + self.size//1.5 * self.direction, self.y - self.size//4),
            (self.x + self.size//1.5 * self.direction, self.y + self.size//4)
        ]
        pygame.draw.polygon(screen, self.color, tail_points)
        # Draw eye
        eye_x = self.x - self.size//4 * self.direction
        pygame.draw.circle(screen, WHITE, (int(eye_x), int(self.y - 2)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(self.y - 2)), 1)

# Create fish
fishes = [Fish() for _ in range(10)]

# Bubbles and splash particles
bubbles = []
splash_particles = []
bubble_timer = 0

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000.0  # Delta time in seconds
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                # Add random force to ball
                vx = random.uniform(-10, 10)
                vy = random.uniform(-15, -5)
    
    # Check if ball just entered water
    current_water_state = (y + ball_radius > WATER_LEVEL)
    if current_water_state and not last_water_state:
        # Create splash effect
        for _ in range(20):
            angle = random.uniform(0, math.pi)
            speed = random.uniform(3, 8)
            splash_particles.append({
                'x': x,
                'y': WATER_LEVEL,
                'vx': math.cos(angle) * speed,
                'vy': -abs(math.sin(angle) * speed * 1.5),
                'size': random.uniform(2, 5),
                'life': random.uniform(0.5, 1.5)
            })
        
        # Make fish jump
        for fish in fishes:
            if random.random() < 0.6:  # 60% chance for each fish to react
                distance = math.hypot(fish.x - x, fish.y - y)
                if distance < 200:  # Only fish near the splash jump
                    fish.jump()
    
    last_water_state = current_water_state
    
    # Apply physics
    vy += gravity
    
    # Water physics when ball is submerged
    if y + ball_radius > WATER_LEVEL:
        # Buoyancy force (reduced gravity)
        vy -= BUOYANCY
        
        # Water drag
        vx *= WATER_DRAG
        vy *= WATER_DRAG
        
        # Add some horizontal movement from water currents
        vx += math.sin(y * 0.05) * 0.1
        
        # Occasionally give the ball a small upward boost to simulate waves
        if random.random() < 0.02:
            vy -= random.uniform(0.5, 1.5)
    
    # Update ball position
    x += vx
    y += vy
    
    # Bounce off the floor (sand)
    if y + ball_radius > HEIGHT - 20:
        y = HEIGHT - 20 - ball_radius
        vy *= bounce_factor
        vx *= friction
        
        # Create sand particles on impact
        for _ in range(15):
            angle = random.uniform(0, math.pi)
            speed = random.uniform(1, 5)
            splash_particles.append({
                'x': x,
                'y': HEIGHT - 20,
                'vx': math.cos(angle) * speed,
                'vy': -abs(math.sin(angle) * speed),
                'size': random.uniform(2, 4),
                'life': random.uniform(0.3, 0.8),
                'color': SAND
            })
    
    # Bounce off the ceiling
    if y - ball_radius < 0:
        y = ball_radius
        vy *= bounce_factor
    
    # Bounce off the walls
    if x + ball_radius > WIDTH or x - ball_radius < 0:
        vx *= -0.9  # Some energy loss on wall bounce
    
    # Move fishes
    for fish in fishes:
        fish.move()
        # Keep fish from going too far underwater
        if fish.y > HEIGHT - 50 and not fish.is_jumping:
            fish.y = HEIGHT - 50
    
    # Generate bubbles
    bubble_timer += dt
    if bubble_timer > 0.1 and y + ball_radius > WATER_LEVEL:
        bubble_timer = 0
        bubbles.append({
            'x': x + random.uniform(-ball_radius, ball_radius),
            'y': y + ball_radius,
            'size': random.uniform(2, 8),
            'speed': random.uniform(0.5, 2)
        })
    
    # Update bubbles
    for bubble in bubbles[:]:
        bubble['y'] -= bubble['speed']
        bubble['x'] += math.sin(bubble['y'] * 0.1) * 0.3  # Sway side to side
        if bubble['y'] < 0:
            bubbles.remove(bubble)
    
    # Update splash particles
    for particle in splash_particles[:]:
        particle['x'] += particle['vx']
        particle['y'] += particle['vy']
        particle['vy'] += gravity * 0.3  # Gravity affects particles
        particle['life'] -= dt
        
        if particle['life'] <= 0:
            splash_particles.remove(particle)
    
    # Drawing
    # Draw sky
    screen.fill(LIGHT_BLUE)
    
    # Draw ocean
    pygame.draw.rect(screen, OCEAN_BLUE, (0, WATER_LEVEL, WIDTH, HEIGHT - WATER_LEVEL))
    
    # Draw sand bottom
    pygame.draw.rect(screen, SAND, (0, HEIGHT - 20, WIDTH, 20))
    
    # Draw waves
    for i in range(0, WIDTH, 20):
        wave_height = math.sin(pygame.time.get_ticks() * 0.001 + i * 0.1) * 5
        pygame.draw.line(screen, WHITE, (i, WATER_LEVEL + wave_height), 
                         (i + 10, WATER_LEVEL - wave_height), 2)
    
    # Draw splash particles
    for particle in splash_particles:
        color = particle.get('color', WHITE)
        alpha = min(255, int(particle['life'] * 255))
        s = pygame.Surface((particle['size']*2, particle['size']*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*color[:3], alpha), 
                          (int(particle['size']), int(particle['size'])), 
                          int(particle['size']))
        screen.blit(s, (int(particle['x'] - particle['size']), 
                      int(particle['y'] - particle['size'])))
    
    # Draw bubbles
    for bubble in bubbles:
        pygame.draw.circle(screen, WHITE, (int(bubble['x']), int(bubble['y'])), int(bubble['size']))
        pygame.draw.circle(screen, OCEAN_BLUE, (int(bubble['x']), int(bubble['y'])), 
                          int(bubble['size'] * 0.7))
    
    # Draw fishes
    for fish in fishes:
        fish.draw()
    
    # Draw ball with highlight for water effect
    pygame.draw.circle(screen, ball_color, (int(x), int(y)), ball_radius)
    if y + ball_radius > WATER_LEVEL:
        # Water distortion effect
        for i in range(1, 4):
            alpha = 100 - i * 25
            radius = ball_radius - i * 2
            if radius > 0:
                s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*ball_color[:3], alpha), (radius, radius), radius)
                screen.blit(s, (x - radius, y - radius))
        
        # Water line
        water_line_y = max(y - ball_radius, WATER_LEVEL)
        if water_line_y < y + ball_radius:
            pygame.draw.circle(screen, WHITE, (int(x), int(water_line_y)), 
                              int(math.sqrt(ball_radius**2 - (water_line_y - y)**2)), 1)
    
    pygame.display.flip()

pygame.quit()