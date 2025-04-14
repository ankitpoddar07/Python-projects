import random
import os
from PIL import Image

# Define the path to the symbols
SYMBOLS_PATH = os.path.join("src", "assets", "symbols")

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
    """Spin the slot machine and return three symbols"""
    return random.choices(symbols, weights=weights, k=3)

def calculate_payout(reel, bet):
    """Calculate the payout based on the reel result and bet amount"""
    if reel.count(reel[0]) == 3:  # All three symbols are the same
        return bet * payouts[reel[0]]
    return 0

def load_symbol_images():
    """Load symbol images from the assets directory"""
    images = {}
    for symbol in symbols:
        image_path = os.path.join(SYMBOLS_PATH, f"{symbol}.png")
        if os.path.exists(image_path):
            images[symbol] = Image.open(image_path)
        else:
            print(f"Warning: Image not found for symbol {symbol}")
    return images

def get_balance_after_bet(balance, bet):
    """Calculate the new balance after placing a bet"""
    return balance - bet

def update_balance(balance, winnings):
    """Update the balance with winnings"""
    return balance + winnings

def is_valid_bet(balance, bet):
    """Check if the bet is valid (positive and within balance)"""
    return 0 < bet <= balance

def is_game_over(balance):
    """Check if the game is over (balance reached zero)"""
    return balance <= 0

def play_round(balance, bet):
    """Play one round of the slot machine"""
    if not is_valid_bet(balance, bet):
        print("Invalid bet amount!")
        return balance
    
    balance = get_balance_after_bet(balance, bet)
    reel = spin_slot()
    winnings = calculate_payout(reel, bet)
    balance = update_balance(balance, winnings)
    
    print(f"Spin result: {' '.join(reel)}")
    if winnings > 0:
        print(f"Congratulations! You won {winnings}!")
    else:
        print("No win this time.")
    print(f"Current balance: {balance}")
    
    return balance