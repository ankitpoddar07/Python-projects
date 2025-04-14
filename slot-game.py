import random

# Define slot symbols and their weights (probabilities)
symbols = ["🍒", "🍋", "🔔", "💎", "7️⃣"]
weights = [40, 30, 15, 10, 5]  # Higher number = more common

# Define payout multiplier
payouts = {
    "🍒": 2,
    "🍋": 3,
    "🔔": 5,
    "💎": 10,
    "7️⃣": 20
}

def spin_slot():
    return random.choices(symbols, weights=weights, k=3)

def display_slots(reel):
    print(" | ".join(reel))

def calculate_payout(reel, bet):
    if reel.count(reel[0]) == 3:
        return bet * payouts[reel[0]]
    return 0

def slot_game():
    balance = 100
    print("🎰 Welcome to the Python Slot Machine! 🎰")
    print("Your starting balance is $100.")

    while balance > 0:
        try:
            bet = int(input(f"\nYour balance: ${balance} — Enter your bet (0 to quit): "))
            if bet == 0:
                print("Thanks for playing!")
                break
            if bet > balance or bet < 0:
                print("Invalid bet amount.")
                continue

            balance -= bet
            reel = spin_slot()
            print("\nSpinning...")
            display_slots(reel)

            winnings = calculate_payout(reel, bet)
            if winnings > 0:
                print(f"🎉 You won ${winnings}!")
                balance += winnings
            else:
                print("😢 No match. Better luck next time!")

        except ValueError:
            print("Please enter a valid number.")

    if balance == 0:
        print("You're out of money! Game over.")

# Run the game
slot_game()
