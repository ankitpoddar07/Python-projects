from tkinter import Tk, Frame, Label, Button, StringVar, messagebox, Entry
import random
from game_logic import spin_slot, calculate_payout

class SlotMachineGUI:
    def __init__(self, master):
        self.master = master
        master.title("Slot Machine Game")

        self.balance = 100
        self.bet_amount = StringVar(value="10")

        self.create_widgets()

    def create_widgets(self):
        # Balance display
        self.balance_label = Label(self.master, text=f"Balance: ${self.balance}", font=('Arial', 14))
        self.balance_label.pack(pady=10)

        # Bet entry
        self.bet_label = Label(self.master, text="Enter your bet:", font=('Arial', 12))
        self.bet_label.pack()

        self.bet_entry = Entry(self.master, textvariable=self.bet_amount, font=('Arial', 12))
        self.bet_entry.pack()

        # Spin button
        self.spin_button = Button(self.master, text="Spin", command=self.spin, font=('Arial', 12), bg='lightblue')
        self.spin_button.pack(pady=10)

        # Result display
        self.result_label = Label(self.master, text="", font=('Arial', 24))
        self.result_label.pack(pady=20)

    def spin(self):
        try:
            bet = int(self.bet_amount.get())
            if bet <= 0:
                messagebox.showerror("Error", "Bet must be positive.")
                return
            if bet > self.balance:
                messagebox.showerror("Error", "You don't have enough balance.")
                return

            # Deduct bet and update balance
            self.balance -= bet
            self.balance_label.config(text=f"Balance: ${self.balance}")

            # Spin and display results
            reel = spin_slot()
            self.display_slots(reel)

            # Calculate winnings
            winnings = calculate_payout(reel, bet)
            if winnings > 0:
                self.balance += winnings
                messagebox.showinfo("Congratulations!", f"You won ${winnings}!")
                self.balance_label.config(text=f"Balance: ${self.balance}")

            # Check game over
            if self.balance <= 0:
                messagebox.showinfo("Game Over", "You're out of money!")
                self.master.destroy()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def display_slots(self, reel):
        self.result_label.config(text=" | ".join(reel))

if __name__ == "__main__":
    root = Tk()
    root.geometry("400x300")
    gui = SlotMachineGUI(root)
    root.mainloop()