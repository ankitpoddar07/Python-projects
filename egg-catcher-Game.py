from itertools import cycle
from random import randrange
from tkinter import Canvas, Tk, messagebox, font, Button, Label

canvas_width = 800
canvas_height = 400

root = Tk()
root.title("🥚 Egg Catcher Game")
root.configure(bg="deep sky blue")
c = Canvas(root, width=canvas_width, height=canvas_height, background="deep sky blue")
c.pack()

game_font = font.nametofont("TkFixedFont")
game_font.config(size=18)

color_cycle = cycle(["light blue", "light green", "light pink", "light yellow", "light cyan"])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 500
egg_interval = 4000
difficulty = 0.95
catcher_color = "blue"
catcher_width = 100
catcher_height = 100

# Global game variables
score = 0
lives_remaining = 3
eggs = []
update_game = True

def setup_game_canvas():
    c.delete("all")
    c.create_rectangle(-5, canvas_height - 100, canvas_width + 5, canvas_height + 5, fill="sea green", width=0)
    c.create_oval(-80, -80, 120, 120, fill='orange', width=0)

    global score_text, lives_text, catcher, score, lives_remaining, eggs, egg_speed, egg_interval, update_game
    score = 0
    lives_remaining = 3
    eggs.clear()
    egg_speed = 500
    egg_interval = 4000
    update_game = True

    catcher_startx = canvas_width / 2 - catcher_width / 2
    catcher_starty = canvas_height - catcher_height - 20
    catcher_startx2 = catcher_startx + catcher_width
    catcher_starty2 = catcher_starty + catcher_height

    catcher = c.create_arc(catcher_startx, catcher_starty, catcher_startx2, catcher_starty2,
                           start=200, extent=140, style="arc", outline=catcher_color, width=3)

    score_text = c.create_text(10, 10, anchor="nw", font=game_font, fill="darkblue", text="Score: 0")
    lives_text = c.create_text(canvas_width - 10, 10, anchor="ne", font=game_font, fill="darkblue", text="Lives: 3")

def create_egg():
    if not update_game: return
    x = randrange(10, 740)
    y = 40
    new_egg = c.create_oval(x, y, x + egg_width, y + egg_height, fill=next(color_cycle), width=0)
    eggs.append(new_egg)
    root.after(egg_interval, create_egg)

def move_eggs():
    if not update_game: return
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        c.move(egg, 0, 10)
        if eggy2 > canvas_height:
            egg_dropped(egg)
    root.after(egg_speed, move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaining == 0:
        end_game()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text=f"Lives: {lives_remaining}")

def check_catch():
    if not update_game: return
    (catcherx, catchery, catcherx2, catchery2) = c.coords(catcher)
    for egg in eggs:
        (eggx, eggy, eggx2, eggy2) = c.coords(egg)
        if catcherx < eggx and eggx2 < catcherx2 and catchery2 - eggy2 < 40:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    root.after(100, check_catch)

def increase_score(points):
    global score, egg_speed, egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty)
    egg_interval = int(egg_interval * difficulty)
    c.itemconfigure(score_text, text=f"Score: {score}")

def move_left(event):
    (x1, _, x2, _) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (_, _, x2, _) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

def start_game():
    welcome_frame.pack_forget()
    setup_game_canvas()
    c.bind("<Left>", move_left)
    c.bind("<Right>", move_right)
    c.focus_set()
    root.after(1000, create_egg)
    root.after(1000, move_eggs)
    root.after(1000, check_catch)

def end_game():
    global update_game
    update_game = False
    messagebox.showinfo("🥚 Game Over!", f"Final Score: {score}")
    restart = messagebox.askyesno("Restart?", "Do you want to play again?")
    if restart:
        start_game()
    else:
        root.destroy()

# Welcome screen
welcome_frame = Canvas(root, width=canvas_width, height=canvas_height, bg="deep sky blue", highlightthickness=0)
welcome_frame.pack()

welcome_frame.create_text(canvas_width // 2, 60, text="🥚 Egg Catcher Game 🧺", font=("Helvetica", 28, "bold"), fill="white")
welcome_frame.create_text(canvas_width // 2, 160, text="""
Instructions:
- Move the catcher left/right using arrow keys
- Catch the falling eggs before they hit the ground
- Each egg gives you 10 points
- Game speeds up over time
- You have 3 lives

Good luck!
""", font=("Helvetica", 14), fill="black", justify="center")

def add_play_button():
    play_button = Button(root, text="🎮 Play Now", font=("Helvetica", 14, "bold"),
                         bg="#4CAF50", fg="white", activebackground="#45a049",
                         command=start_game)
    play_button.place(x=canvas_width // 2 - 60, y=320)

add_play_button()

root.mainloop()
