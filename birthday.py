import turtle
import random
import time
from pygame import mixer

# Initialize pygame mixer
mixer.init()
try:
    mixer.music.load("happy-birthday-314197.mp3")  # add your music file name or path
    mixer.music.play()
except:
    print("Could not load music file")

# Set up screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Birthday Celebration")

# Create turtle for drawing
pen = turtle.Turtle()
pen.speed(0)  # fastest drawing speed

# Draw cake stand
def draw_cake_stand():
    pen.penup()
    pen.goto(-170, -180)
    pen.color("white")
    pen.pendown()
    pen.forward(350)  # Bottom line
    
    pen.penup()
    pen.goto(-160, -150)
    pen.pendown()
    pen.forward(300)  # Middle line
    
    pen.penup()
    pen.goto(-150, -120)
    pen.pendown()
    pen.forward(250)  # Top line

# Draw cake layers
def draw_cake():
    # Base layer
    draw_rectangle(-70, -100, 140, 100, "#F5CBA7")
    # Middle layer
    draw_rectangle(-60, 0, 120, 60, "#F1948A")
    # Top layer
    draw_rectangle(-50, 60, 100, 40, "#BB8FCE")

# Helper function to draw rectangles
def draw_rectangle(x, y, width, height, color):
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    pen.begin_fill()
    pen.pendown()
    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)
    pen.end_fill()

# Draw candles
def draw_candles():
    colors = ["red", "blue", "yellow", "green", "purple"]
    x_positions = [-40, -20, 0, 20, 40]
    for i in range(5):
        pen.penup()
        pen.goto(x_positions[i], 100)
        pen.color(colors[i])
        pen.pendown()
        pen.begin_fill()
        pen.setheading(90)
        pen.forward(20)
        pen.right(90)
        pen.forward(4)
        pen.right(90)
        pen.forward(20)
        pen.right(90)
        pen.forward(4)
        pen.end_fill()
        
        # Draw flame
        pen.penup()
        pen.goto(x_positions[i], 120)
        pen.color("orange")
        pen.begin_fill()
        pen.circle(5)
        pen.end_fill()

# Draw decorations
def draw_decorations():
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "white"]
    pen.penup()
    pen.goto(-40, -50)
    
    for each_color in colors:
        pen.color(each_color)
        pen.dot(20)
        pen.right(360 / len(colors))
        pen.forward(25)

# Draw confetti
def draw_confetti():
    colors = ["red", "orange", "yellow", "green", "blue", "purple", "white"]
    confetti = turtle.Turtle()
    confetti.speed(0)
    confetti.hideturtle()
    
    for _ in range(100):
        confetti.penup()
        x = random.randint(-200, 200)
        y = random.randint(-100, 200)
        confetti.goto(x, y)
        confetti.color(random.choice(colors))
        confetti.dot(random.randint(5, 10))

# Animated birthday message
def draw_birthday_message():
    message = turtle.Turtle()
    message.hideturtle()
    message.penup()
    message.color("white")
    
    y_positions = [50, 40, 60, 45, 55, 50]  # Bouncing pattern
    
    for i, y in enumerate(y_positions):
        screen.bgcolor(random.choice(["lightgreen", "lightblue", "pink", "black"]))
        message.clear()
        message.goto(0, y)
        message.write("Happy Birthday Baby! 🎉", align="center", font=("Arial", 24, "bold"))
        time.sleep(0.3)
    
    # Final position
    message.clear()
    message.goto(0, 50)
    message.write("Happy Birthday Baby! 🎉", align="center", font=("Arial", 24, "bold"))

# Main program
def main():
    # Draw all components
    draw_cake_stand()
    screen.bgcolor("lightgreen")
    draw_cake()
    screen.bgcolor("black")
    draw_candles()
    draw_decorations()
    draw_confetti()
    draw_birthday_message()
    
    # Hide turtle and display
    pen.hideturtle()
    turtle.done()

if __name__ == "__main__":
    main()