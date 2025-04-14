import tkinter as tk
import random

# Initialize score
user_score = 0
computer_score = 0

# Choices with emojis
choices = {
    "rock": "🪨 Rock",
    "paper": "📄 Paper",
    "scissors": "✂️ Scissors"
}

# Functions
def get_computer_choice():
    return random.choice(list(choices.keys()))

def determine_winner(player, computer):
    global user_score, computer_score
    if player == computer:
        return "It's a tie!"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        user_score += 1
        return "You win!"
    else:
        computer_score += 1
        return "Computer wins!"

def play(choice):
    comp = get_computer_choice()
    result = determine_winner(choice, comp)
    user_choice_label.config(text=f"You chose: {choices[choice]}")
    comp_choice_label.config(text=f"Computer chose: {choices[comp]}")
    result_label.config(text=result)
    score_label.config(text=f"Score: You {user_score} - {computer_score} Computer")

# GUI setup
root = tk.Tk()
root.title("Rock, Paper, Scissors")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

title = tk.Label(root, text="Rock, Paper, Scissors", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
title.pack(pady=10)

# Frame for buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=20)

# Buttons
tk.Button(button_frame, text="🪨 Rock", width=12, font=("Helvetica", 14), command=lambda: play("rock")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="📄 Paper", width=12, font=("Helvetica", 14), command=lambda: play("paper")).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="✂️ Scissors", width=12, font=("Helvetica", 14), command=lambda: play("scissors")).grid(row=0, column=2, padx=10)

# Labels
user_choice_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
user_choice_label.pack(pady=5)

comp_choice_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#f0f0f0")
comp_choice_label.pack(pady=5)

result_label = tk.Label(root, text="", font=("Helvetica", 16, "bold"), fg="blue", bg="#f0f0f0")
result_label.pack(pady=10)

score_label = tk.Label(root, text="Score: You 0 - 0 Computer", font=("Helvetica", 14), bg="#f0f0f0")
score_label.pack(pady=10)

# Start the GUI
root.mainloop()
