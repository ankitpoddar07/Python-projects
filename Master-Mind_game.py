import random
import tkinter as tk
from tkinter import messagebox

def generate_code(length=4):
    return [str(random.randint(0, 9)) for _ in range(length)]

def get_feedback(secret, guess):
    red = 0  # Correct position
    white = 0  # Wrong position

    secret_copy = secret.copy()
    guess_copy = guess.copy()

    # First pass: Check for exact matches
    for i in range(len(secret)):
        if guess[i] == secret[i]:
            red += 1
            secret_copy[i] = guess_copy[i] = None

    # Second pass: Check for correct digits in wrong positions
    for i in range(len(secret)):
        if guess_copy[i] is not None and guess_copy[i] in secret_copy:
            white += 1
            secret_copy[secret_copy.index(guess_copy[i])] = None

    return red, white

class MastermindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mastermind Game")
        self.secret_code = generate_code()
        self.attempts = 0
        self.max_attempts = 10

        self.label = tk.Label(root, text="🎯 Welcome to Mastermind!", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.input_label = tk.Label(root, text="Enter your 4-digit guess:", font=("Helvetica", 14))
        self.input_label.pack(pady=5)

        self.entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
        self.entry.pack(pady=5)

        self.submit_button = tk.Button(root, text="Submit", command=self.check_guess, font=("Helvetica", 14))
        self.submit_button.pack(pady=10)

        self.feedback_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.feedback_label.pack(pady=10)

    def check_guess(self):
        guess = self.entry.get()
        if len(guess) != 4 or not guess.isdigit():
            messagebox.showerror("Invalid Input", "Please enter exactly 4 digits.")
            return

        self.attempts += 1
        guess_list = list(guess)
        red, white = get_feedback(self.secret_code, guess_list)

        self.feedback_label.config(text=f"🔴 {red} correct place | ⚪ {white} correct digit wrong place")

        if red == 4:
            messagebox.showinfo("Congratulations!", "🎉 You broke the code!")
            self.root.quit()
        elif self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"😢 Out of attempts. The code was: {''.join(self.secret_code)}")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MastermindApp(root)
    root.mainloop()