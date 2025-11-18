import tkinter as tk
from tkinter import messagebox
import random
import os

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Water Gun - Pro Edition")
        self.root.geometry("500x600")
        self.root.configure(bg="#212121")

        # --- Game Variables ---
        self.choices = {"Gun": 1, "Snake": 2, "Water": 3}
        self.reverse = {1: "Gun", 2: "Snake", 3: "Water"}
        self.user_score = 0
        self.comp_score = 0
        self.streak = 0
        self.high_score = self.load_high_score() # File Handling Feature

        # --- UI Layout ---
        
        # Top Bar (High Score)
        self.top_frame = tk.Frame(root, bg="#1a1a1a", pady=5)
        self.top_frame.pack(fill="x")
        self.highscore_lbl = tk.Label(self.top_frame, text=f"🏆 High Score: {self.high_score}", 
                                      font=("Arial", 10, "bold"), bg="#1a1a1a", fg="#FFD700")
        self.highscore_lbl.pack()

        # Title
        self.title_lbl = tk.Label(root, text="SNAKE WATER GUN", font=("Verdana", 22, "bold"), 
                                  bg="#212121", fg="#00e676")
        self.title_lbl.pack(pady=15)

        # Score Board
        self.score_frame = tk.Frame(root, bg="#212121")
        self.score_frame.pack(pady=5)
        
        self.score_lbl = tk.Label(self.score_frame, text="You: 0  |  Comp: 0", font=("Arial", 16), 
                                  bg="#212121", fg="white")
        self.score_lbl.pack()
        
        self.streak_lbl = tk.Label(self.score_frame, text="Streak: 0 🔥", font=("Arial", 10), 
                                   bg="#212121", fg="#ff9800")
        self.streak_lbl.pack()

        # Main Result Area
        self.result_lbl = tk.Label(root, text="READY?", font=("Arial", 24, "bold"), 
                                   bg="#212121", fg="#29b6f6")
        self.result_lbl.pack(pady=20)
        
        self.detail_lbl = tk.Label(root, text="Select a weapon below", font=("Arial", 11), 
                                   bg="#212121", fg="#bdbdbd")
        self.detail_lbl.pack()

        # Buttons
        self.btn_frame = tk.Frame(root, bg="#212121")
        self.btn_frame.pack(pady=20)

        btn_config = {"font": ("Arial", 11, "bold"), "width": 12, "height": 2, "bd": 0, "fg": "white", "cursor": "hand2"}

        self.btn_snake = tk.Button(self.btn_frame, text="🐍 SNAKE", bg="#00c853", **btn_config, 
                                   command=lambda: self.play("Snake"))
        self.btn_snake.grid(row=0, column=0, padx=10)

        self.btn_water = tk.Button(self.btn_frame, text="💧 WATER", bg="#29b6f6", **btn_config, 
                                   command=lambda: self.play("Water"))
        self.btn_water.grid(row=0, column=1, padx=10)

        self.btn_gun = tk.Button(self.btn_frame, text="🔫 GUN", bg="#d50000", **btn_config, 
                                 command=lambda: self.play("Gun"))
        self.btn_gun.grid(row=0, column=2, padx=10)

        # History Log (Listbox)
        tk.Label(root, text="Match History:", bg="#212121", fg="gray").pack(pady=(20, 0))
        self.history_list = tk.Listbox(root, height=6, width=50, bg="#303030", fg="white", bd=0, highlightthickness=0)
        self.history_list.pack(pady=5)

        # Reset Button
        tk.Button(root, text="RESET ALL", font=("Arial", 9), bg="#424242", fg="white", bd=0, 
                  command=self.reset_game).pack(side="bottom", pady=15)

    def load_high_score(self):
        """Reads highscore from a file. Creates file if not exists."""
        if not os.path.exists("highscore.txt"):
            return 0
        try:
            with open("highscore.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        """Writes new highscore to file."""
        with open("highscore.txt", "w") as f:
            f.write(str(self.high_score))

    def flash_bg(self, color):
        """Creates a flash effect on the background."""
        original_color = "#212121"
        self.root.configure(bg=color)
        self.score_frame.configure(bg=color)
        self.btn_frame.configure(bg=color)
        # Revert back after 100ms
        self.root.after(100, lambda: [
            self.root.configure(bg=original_color),
            self.score_frame.configure(bg=original_color),
            self.btn_frame.configure(bg=original_color)
        ])

    def update_history(self, text, result):
        """Adds move to the history list box."""
        color = "white"
        if result == "WIN": color = "#00e676"
        elif result == "LOSE": color = "#ff1744"
        
        self.history_list.insert(0, text) # Insert at top
        self.history_list.itemconfig(0, {'fg': color})
        
        # Keep only last 10 logs
        if self.history_list.size() > 10:
            self.history_list.delete(10)

    def play(self, user_choice_str):
        computer = random.randint(1, 3)
        you = self.choices[user_choice_str]
        comp_str = self.reverse[computer]

        # Game Logic
        if you == computer:
            self.result_lbl.config(text="IT'S A DRAW!", fg="orange")
            self.streak = 0
            self.update_history(f"Draw: {user_choice_str} vs {comp_str}", "DRAW")
        else:
            if (computer == 1 and you == 3) or \
               (computer == 2 and you == 1) or \
               (computer == 3 and you == 2):
                # WIN
                self.result_lbl.config(text="YOU WON!", fg="#00e676")
                self.user_score += 1
                self.streak += 1
                self.update_history(f"Win: {user_choice_str} beat {comp_str}", "WIN")
                self.flash_bg("#1b5e20") # Flash Dark Green
                
                # Check High Score
                if self.user_score > self.high_score:
                    self.high_score = self.user_score
                    self.save_high_score()
                    self.highscore_lbl.config(text=f"🏆 High Score: {self.high_score}")
            else:
                # LOSE
                self.result_lbl.config(text="YOU LOST!", fg="#ff1744")
                self.comp_score += 1
                self.streak = 0
                self.update_history(f"Loss: {user_choice_str} lost to {comp_str}", "LOSE")
                self.flash_bg("#b71c1c") # Flash Dark Red

        # Update UI Text
        self.score_lbl.config(text=f"You: {self.user_score}  |  Comp: {self.comp_score}")
        self.streak_lbl.config(text=f"Streak: {self.streak} 🔥")
        self.detail_lbl.config(text=f"You chose {user_choice_str} | Computer chose {comp_str}")

    def reset_game(self):
        self.user_score = 0
        self.comp_score = 0
        self.streak = 0
        self.score_lbl.config(text="You: 0  |  Comp: 0")
        self.streak_lbl.config(text="Streak: 0 🔥")
        self.result_lbl.config(text="Game Reset", fg="white")
        self.detail_lbl.config(text="")
        self.history_list.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
