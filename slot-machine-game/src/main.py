import tkinter as tk
from tkinter import messagebox
from game_logic import spin_slot, calculate_payout

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slot Machine Game")
        self.balance = 100

        self.balance_label = tk.Label(root, text=f"Balance: ${self.balance}", font=("Helvetica", 16))
        self.balance_label.pack(pady=20)

        self.spin_button = tk.Button(root, text="Spin", command=self.spin, font=("Helvetica", 14))
        self.spin_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=20)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Helvetica", 14))
        self.quit_button.pack(pady=10)

    def spin(self):
        bet = 10  # Fixed bet for simplicity
        if self.balance < bet:
            messagebox.showinfo("Insufficient Funds", "You don't have enough balance to spin!")
            return

        self.balance -= bet
        self.balance_label.config(text=f"Balance: ${self.balance}")

        reel = spin_slot()
        self.result_label.config(text=" | ".join(reel))

        winnings = calculate_payout(reel, bet)
        if winnings > 0:
            self.balance += winnings
            messagebox.showinfo("Congratulations!", f"You won ${winnings}!")
        else:
            messagebox.showinfo("Try Again", "No match. Better luck next time!")

        self.balance_label.config(text=f"Balance: ${self.balance}")

        if self.balance == 0:
            messagebox.showinfo("Game Over", "You're out of money! Game over.")
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()