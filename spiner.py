import turtle
import random

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("🌀 Realistic Fidget Spinner")

# Create turtle
spinner = turtle.Turtle()
spinner.speed(0)
spinner.pensize(3)

# Draw spinner arms
def draw_circle(x, y, color):
    spinner.penup()
    spinner.goto(x, y - 50)
    spinner.pendown()
    spinner.fillcolor(color)
    spinner.begin_fill()
    spinner.circle(50)
    spinner.end_fill()

def draw_spinner():
    spinner.setheading(0)
    colors = ["cyan", "magenta", "yellow", "lime", "orange", "red"]
    for _ in range(3):  # 3 arms
        spinner.forward(100)
        draw_circle(spinner.xcor(), spinner.ycor(), random.choice(colors))
        spinner.backward(100)
        spinner.left(120)

# Rotation logic
angle = 0
speed = 0  # Initial speed

def spin():
    global angle, speed
    spinner.clear()
    spinner.setheading(angle)
    draw_spinner()
    angle += speed

    # Gradual deceleration
    if speed > 0:
        speed -= 0.1
    screen.ontimer(spin, 20)  # Call spin() every 20 ms

def accelerate():
    global speed
    speed += 5  # Increase speed
    if speed > 50:  # Cap the speed
        speed = 50

# Bind spacebar to accelerate
screen.listen()
screen.onkey(accelerate, "space")

# Start spinning
spin()

# Keep window open
turtle.done()