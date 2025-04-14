import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pygame
import os
import time
from threading import Thread

# Initialize pygame mixer
pygame.mixer.init()

# Main window
root = tk.Tk()
root.title("Spotify-Like Music Player 🎧")
root.geometry("450x550")  # Increased height for time controls
root.configure(bg="#191414")  # Spotify black-green

# Global variables
current_song = None
is_paused = False
song_length = 0
updating_time = False

# Function to format time (seconds to MM:SS)
def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"

# Update time slider position
def update_time_slider():
    global updating_time
    while True:
        if pygame.mixer.music.get_busy() and not is_paused and not updating_time:
            current_pos = pygame.mixer.music.get_pos() / 1000  # Convert to seconds
            time_slider.set(current_pos)
            current_time_label.config(text=format_time(current_pos))
        time.sleep(0.5)  # Update twice per second

# Load song
def load_song():
    global current_song, song_length
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        current_song = file_path
        song_label.config(text=os.path.basename(file_path))
        
        # Get song length
        sound = pygame.mixer.Sound(file_path)
        song_length = sound.get_length()
        time_slider.config(to=song_length)
        total_time_label.config(text=format_time(song_length))
        
        play_music()

# Play song
def play_music():
    global is_paused
    if current_song:
        if is_paused:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.load(current_song)
            pygame.mixer.music.play()
            time_slider.set(0)  # Reset slider to start
        is_paused = False
        status_var.set("▶️ Playing")

# Pause/Unpause
def pause_music():
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        status_var.set("▶️ Resumed")
    else:
        pygame.mixer.music.pause()
        status_var.set("⏸️ Paused")
    is_paused = not is_paused

# Stop song
def stop_music():
    pygame.mixer.music.stop()
    status_var.set("⏹️ Stopped")
    time_slider.set(0)
    current_time_label.config(text="00:00")

# Volume control
def set_volume(val):
    volume = int(val) / 100
    pygame.mixer.music.set_volume(volume)
    status_var.set(f"🔊 Volume: {val}%")

# Seek in the song
def seek_song(val):
    global updating_time
    if current_song:
        updating_time = True
        seek_pos = float(val)
        pygame.mixer.music.set_pos(seek_pos)
        current_time_label.config(text=format_time(seek_pos))
        updating_time = False

# Start dragging the slider
def start_drag(event):
    global updating_time
    updating_time = True

# End dragging the slider
def end_drag(event):
    global updating_time
    updating_time = False
    if current_song:
        seek_pos = time_slider.get()
        pygame.mixer.music.set_pos(seek_pos)

# Album art placeholder
album_art = tk.Label(root, bg="#1DB954")
album_art.place(x=150, y=30, width=150, height=150)
album_art.config(text="🎵", font=("Helvetica", 60), fg="white")

# Song name label
song_label = tk.Label(root, text="No song loaded", font=("Helvetica", 14, "bold"),
                      fg="white", bg="#191414", wraplength=380)
song_label.pack(pady=(200, 10))

# Time display frame
time_frame = tk.Frame(root, bg="#191414")
time_frame.pack(pady=5)

current_time_label = tk.Label(time_frame, text="00:00", font=("Helvetica", 10),
                             fg="white", bg="#191414")
current_time_label.pack(side="left")

time_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=seek_song)
time_slider.pack(fill="x", padx=10, pady=5)
time_slider.bind("<ButtonPress-1>", start_drag)
time_slider.bind("<ButtonRelease-1>", end_drag)

total_time_label = tk.Label(time_frame, text="00:00", font=("Helvetica", 10),
                           fg="white", bg="#191414")
total_time_label.pack(side="right")

# Status bar
status_var = tk.StringVar()
status_var.set("Status: Idle")
status_label = tk.Label(root, textvariable=status_var, font=("Helvetica", 12),
                        fg="#1DB954", bg="#191414")
status_label.pack(pady=(0, 15))

# Buttons
button_frame = tk.Frame(root, bg="#191414")
button_frame.pack(pady=10)

style = {"font": ("Helvetica", 12), "bg": "#1DB954", "fg": "white", "activebackground": "#1ed760"}

tk.Button(button_frame, text="🎵 Load", command=load_song, width=10, **style).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="▶️ Play", command=play_music, width=10, **style).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="⏸️ Pause", command=pause_music, width=10, **style).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="⏹️ Stop", command=stop_music, width=10, **style).grid(row=0, column=3, padx=5)

# Volume slider
volume_label = tk.Label(root, text="Volume", font=("Helvetica", 12), fg="white", bg="#191414")
volume_label.pack(pady=5)

volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=set_volume)
volume_slider.set(70)
volume_slider.pack(pady=5)
pygame.mixer.music.set_volume(0.7)

# Start the time update thread
time_thread = Thread(target=update_time_slider, daemon=True)
time_thread.start()

# Run the app
root.mainloop()