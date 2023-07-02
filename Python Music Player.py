import os
import random
import tkinter as tk
from tkinter import filedialog
import pygame


class MusicPlayer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Music Player")

        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False
        self.is_paused = False
        self.is_shuffled = False
        self.repeat_mode = "Off"

        self.volume = 0.5

        self.initialize_gui()

        self.root.mainloop()

    def initialize_gui(self):
        # Create and configure GUI elements
        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_music_folder)
        self.browse_button.pack()

        self.playlist_box = tk.Listbox(self.root)
        self.playlist_box.pack()

        self.play_button = tk.Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack()

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack()

        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL,
                                      command=self.set_volume)
        self.volume_slider.pack()
        self.volume_slider.set(self.volume)

        self.shuffle_button = tk.Button(self.root, text="Shuffle", command=self.toggle_shuffle)
        self.shuffle_button.pack()

        self.repeat_button = tk.Button(self.root, text="Repeat: Off", command=self.toggle_repeat)
        self.repeat_button.pack()

    def browse_music_folder(self):
        folder_path = filedialog.askdirectory()
        self.playlist = []
        self.current_song_index = 0

        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                self.playlist.append(os.path.join(folder_path, file))
                self.playlist_box.insert(tk.END, file)

    def play_music(self):
        if not pygame.mixer.music.get_busy():
            if self.is_paused:
                pygame.mixer.music.unpause()
            else:
                if self.is_shuffled:
                    self.current_song_index = random.randint(0, len(self.playlist) - 1)
                self.load_song()

            self.is_playing = True
            self.is_paused = False
            self.play_button.config(text="Play")

    def pause_music(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="Play")

    def stop_music(self):
        if self.is_playing or self.is_paused:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.is_paused = False
            self.play_button.config(text="Play")

    def set_volume(self, value):
        self.volume = float(value)
        pygame.mixer.music.set_volume(self.volume)

    def toggle_shuffle(self):
        self.is_shuffled = not self.is_shuffled
        if self.is_shuffled:
            self.shuffle_button.config(text="Shuffle: On")
        else:
            self.shuffle_button.config(text="Shuffle: Off")

    def toggle_repeat(self):
        if self.repeat_mode == "Off":
            self.repeat_mode = "Repeat One"
        elif self.repeat_mode == "Repeat One":
            self.repeat_mode = "Repeat All"
        else:
            self.repeat_mode = "Off"
        self.repeat_button.config(text="Repeat: " + self.repeat_mode)

    def load_song(self) -> object:
        pygame.mixer.music.load(self.playlist[self.current_song_index])
        pygame.mixer.music.play()

    def next_song(self):
        if self.repeat_mode == "Repeat One":
            self.load_song()
        elif self.repeat_mode == "Repeat All":
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.load_song()
        else:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            if self.current_song_index == 0 and not self.is_shuffled:
                self.stop_music()
            else:
                self.load_song()

    def prev_song(self):
        if pygame.mixer.music.get_pos() < 3000:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.load_song()
        else:
            pygame.mixer.music.rewind()


# Initialize and run the music player
pygame.init()
music_player = MusicPlayer()
