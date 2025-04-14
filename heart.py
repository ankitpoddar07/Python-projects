import turtle
import math
import random
import time

# Setup screen
screen = turtle.Screen()
screen.bgcolor("lightblue")
screen.title("Realistic Heart with Animation")
screen.tracer(0)  # Turn off automatic screen updates for smoother animation

# Create heart drawer
heart = turtle.Turtle()
heart.color("red")
heart.pensize(3)
heart.speed(0)  # Fastest speed
heart.hideturtle()

# Improved realistic heart drawing with beating animation
def draw_heart(scale=1.0):
    heart.clear()
    heart.begin_fill()
    heart.penup()
    heart.goto(0, -100 * scale)
    heart.pendown()
    heart.left(140 * scale)
    heart.forward(180 * scale)
    
    # Draw the curves with more segments for smoother shape
    for _ in range(20):
        heart.right(200/20 * 0.1)
        heart.forward(2 * scale)
    
    for _ in range(20):
        heart.right(200/20 * 0.9)
        heart.forward(2 * scale)
    
    heart.left(120 * scale)
    
    for _ in range(20):
        heart.right(200/20 * 0.9)
        heart.forward(2 * scale)
    
    for _ in range(20):
        heart.right(200/20 * 0.1)
        heart.forward(2 * scale)
    
    heart.forward(180 * scale)
    heart.end_fill()

# Create message writer
message = turtle.Turtle()
message.hideturtle()
message.penup()
message.speed(0)

def write_message():
    message.clear()
    message.goto(0, -20)
    message.color("darkred")
    message.write("I Love You", align="center", font=("Arial", 28, "bold"))

# Create butterfly class with more realistic movement
class Butterfly(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color(random.choice(['purple', 'orange', 'blue', 'green', 'pink']))
        self.penup()
        self.speed(0)
        self.shapesize(0.8, 1.2)
        self.setheading(random.randint(0, 360))
        self.wing_angle = 0
        self.flap_speed = random.uniform(0.1, 0.3)
        self.x_off = random.uniform(0, 2*math.pi)
        self.y_off = random.uniform(0, 2*math.pi)
        self.speed_x = random.uniform(0.02, 0.05)
        self.speed_y = random.uniform(0.02, 0.05)
        self.radius_x = random.randint(100, 200)
        self.radius_y = random.randint(50, 150)
        self.center_x = random.randint(-100, 100)
        self.center_y = random.randint(-50, 100)
        
    def update(self, frame):
        # Wing flapping animation
        self.wing_angle += self.flap_speed
        wing_scale = math.sin(self.wing_angle) * 0.2 + 0.8
        self.shapesize(wing_scale, 1.5 - wing_scale*0.5)
        
        # Circular motion with slight irregularities
        angle = frame * self.speed_x + self.x_off
        x = self.center_x + math.cos(angle) * self.radius_x
        y = self.center_y + math.sin(frame * self.speed_y + self.y_off) * self.radius_y
        
        # Smooth movement towards target position
        current_x, current_y = self.pos()
        dx = (x - current_x) * 0.1
        dy = (y - current_y) * 0.1
        self.goto(current_x + dx, current_y + dy)
        
        # Face direction of movement
        if abs(dx) > 0.1 or abs(dy) > 0.1:
            target_heading = math.degrees(math.atan2(dy, dx))
            current_heading = self.heading()
            angle_diff = (target_heading - current_heading + 180) % 360 - 180
            self.setheading(current_heading + angle_diff * 0.1)

# Initialize butterflies
butterflies = [Butterfly() for _ in range(8)]

# Place butterflies randomly around the heart
for b in butterflies:
    b.goto(random.randint(-200, 200), random.randint(-100, 200))

# Heart beat animation variables
heart_scale = 1.0
heart_growing = True
last_beat_time = time.time()

# Main animation loop
frame = 0
while True:
    # Heart beat animation
    current_time = time.time()
    if current_time - last_beat_time > 0.7:  # Beat every 0.7 seconds
        heart_growing = not heart_growing
        last_beat_time = current_time
    
    if heart_growing:
        heart_scale = min(heart_scale + 0.02, 1.1)
    else:
        heart_scale = max(heart_scale - 0.02, 0.95)
    
    draw_heart(heart_scale)
    
    # Update butterflies
    for butterfly in butterflies:
        butterfly.update(frame)
    
    # Write message (only once)
    if frame == 10:
        write_message()
    
    screen.update()
    frame += 1
    time.sleep(0.016)  # ~60 FPS