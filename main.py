import os
import time
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, messagebox
import pygame

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

pygame.mixer.init()

class AudioPlayer(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Аудиоплеер")
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        win_w = int(screen_w * 0.3)
        win_h = int(screen_h * 0.3)
        pos_x = (screen_w - win_w) // 2
        pos_y = (screen_h - win_h) // 2
        self.geometry(f"{win_w}x{win_h}+{pos_x}+{pos_y}")
        self.resizable(False, False)
        self.create_ui()
        self.after(200, self.update_ui)

    def create_ui(self):
        pad = 12

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=pad, pady=pad)

        self.title_label = ctk.CTkLabel(self.frame, text="Файл не выбран", anchor="w")
        self.title_label.pack(fill="x", pady=(8, 6))

        self.time_label = ctk.CTkLabel(self.frame, text="00:00 / 00:00", anchor="w")
        self.time_label.pack(fill="x", pady=(0, 10))

        self.progress = ctk.CTkSlider(
            self.frame,
            from_=0, to=100,
            command=self.on_seek_drag
        )
        self.progress.pack(fill="x", pady=(0, 10))

        btn_row = ctk.CTkFrame(self.frame)
        btn_row.pack(fill="x")

        self.open_btn = ctk.CTkButton(btn_row, text="Открыть", command=self.open_file, width=100)
        self.open_btn.pack(side="left", padx=(0, 8))

        self.play_btn = ctk.CTkButton(btn_row, text="▶︎ Play", command=self.toggle_play, width=100, state="disabled")
        self.play_btn.pack(side="left", padx=(0, 8))

        self.stop_btn = ctk.CTkButton(btn_row, text="⏹ Stop", command=self.stop, width=100, state="disabled")
        self.stop_btn.pack(side="left")

        self.progress.bind("<ButtonPress-1>", self._on_drag_start)
        self.progress.bind("<ButtonRelease-1>", self._on_drag_end)

    def open_file(self):
        filepath = filedialog.askopenfilename(
            title="Выберите аудиофайл",
            filetypes=[
                ("Audio", "*.mp3"),
                ("MP3", "*.mp3"),
                ("Все файлы", "*.*"),
            ]
        )
        if not filepath:
            return

        try:
            pygame.mixer.music.load(filepath)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось открыть файл:\n{e}")
            return

        self.filepath = filepath
        self.title_label.configure(text=os.path.basename(filepath))

        self.length_sec = self._probe_length(filepath)
        self.progress.set(0)
        self.time_label.configure(text=f"{self._fmt(0)} / {self._fmt(self.length_sec)}")

        self.play_btn.configure(state="normal")
        self.stop_btn.configure(state="normal")

        self.start_play()

    def start_play(self, start_pos=0.0):
        try:
            pygame.mixer.music.play(start=0)  
            if start_pos > 0:
                try:
                    pygame.mixer.music.set_pos(start_pos)
                except Exception:
                    pass
            self.is_playing = True
            self.play_btn.configure(text="⏸ Pause")
        except Exception as e:
            messagebox.showerror("Ошибка воспроизведения", str(e))

    def toggle_play(self):
        if not self.filepath:
            return
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.play_btn.configure(text="▶︎ Play")
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.play_btn.configure(text="⏸ Pause")

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_btn.configure(text="▶︎ Play")
        self.progress.set(0)
        self.time_label.configure(text=f"{self._fmt(0)} / {self._fmt(self.length_sec)}")

    def on_seek_drag(self, value):
        if self.length_sec > 0:
            target = (float(value) / 100.0) * self.length_sec
            self.time_label.configure(text=f"{self._fmt(target)} / {self._fmt(self.length_sec)}")

    def _on_drag_start(self, _event):
        self.user_dragging = True

    def _on_drag_end(self, _event):
        self.user_dragging = False
        if self.length_sec <= 0 or not self.filepath:
            return
        slider_val = float(self.progress.get())
        target_sec = (slider_val / 100.0) * self.length_sec

        try:
            pygame.mixer.music.set_pos(target_sec)
            if not self.is_playing:
                pygame.mixer.music.play()
                pygame.mixer.music.set_pos(target_sec)
                pygame.mixer.music.pause()
            else:
                pass
        except Exception:
            pygame.mixer.music.play()
            if target_sec > 0:
                try:
                    pygame.mixer.music.set_pos(target_sec)
                except Exception:
                    pass
    def update_ui(self):
        if self.filepath and not self.user_dragging:
            pos = self._get_position_sec()
            if self.length_sec > 0:
                pct = max(0.0, min(100.0, (pos / self.length_sec) * 100.0))
                self.progress.set(pct)
            self.time_label.configure(text=f"{self._fmt(pos)} / {self._fmt(self.length_sec)}")

            if self.is_playing and not pygame.mixer.music.get_busy():
                self.is_playing = False
                self.play_btn.configure(text="▶︎ Play")
                self.progress.set(100)
                self.time_label.configure(text=f"{self._fmt(self.length_sec)} / {self._fmt(self.length_sec)}")

        self.after(200, self.update_ui)

    def _get_position_sec(self) -> float:
        ms = pygame.mixer.music.get_pos()
        if ms < 0:
            return 0.0
        return ms / 1000.0

    def _fmt(self, seconds: float) -> str:
        seconds = max(0, int(seconds))
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def _probe_length(self, filepath: str) -> float:
        try:
            snd = pygame.mixer.Sound(filepath)
            return float(snd.get_length())
        except Exception:
            return 0.0

if __name__ == "__main__":
    app = AudioPlayer()
    app.mainloop()
