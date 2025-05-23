import tkinter as tk
import os
import sys
import urllib.request
import json
from tkinter import messagebox

# --- AUTO-UPDATE SETTINGS ---
UPDATE_URL = "https://raw.githubusercontent.com/kryoiz13/Duck-Clicker-/main/duck_clicker.py"
LOCAL_FILE = os.path.abspath(__file__)
SAVE_FILE = "savegame.json"

def normalize_line_endings(s):
    return s.replace('\r\n', '\n').replace('\r', '\n')

def check_for_update():
    try:
        with urllib.request.urlopen(UPDATE_URL) as response:
            remote_code = response.read().decode("utf-8")
        with open(LOCAL_FILE, "r", encoding="utf-8") as f:
            local_code = f.read()
        if normalize_line_endings(remote_code) != normalize_line_endings(local_code):
            with open(LOCAL_FILE, "w", encoding="utf-8") as f:
                f.write(remote_code)
            tk.Tk().withdraw()
            messagebox.showinfo("Update", "Game updated! Please restart the game.")
            sys.exit(0)
    except Exception as e:
        print("Update check failed:", e)

def save_progress(game):
    data = {
        "ducks": game.ducks,
        "ducks_per_click": game.ducks_per_click,
        "auto_ducks": game.auto_ducks,
        "rebirths": game.rebirths,
        "rebirth_cost": game.rebirth_cost,
        "super_ducks": getattr(game, "super_ducks", 0),
        "super_duck_cost": game.super_duck_cost,
        "ultra_click_cost": game.ultra_click_cost,
        "ultra_click_active": game.ultra_click_active,
        "ultra_click_duration": game.ultra_click_duration,
        "mega_click_cost": game.mega_click_cost,
        "mega_click_active": game.mega_click_active,
        "mega_click_duration": game.mega_click_duration,
        "duck_factory_cost": game.duck_factory_cost,
        "duck_factory_count": game.duck_factory_count,
        "duck_god_cost": game.duck_god_cost,
        "duck_god_count": game.duck_god_count,
        "upgrade1_cost": game.upgrade1_cost,
        "upgrade2_cost": game.upgrade2_cost,
        "upgrade3_cost": game.upgrade3_cost,
        "diamond_duck_cost": getattr(game, "diamond_duck_cost", 50000),
        "duck_army_cost": getattr(game, "duck_army_cost", 250000),
        "duck_portal_cost": getattr(game, "duck_portal_cost", 1000000),
        "duck_bank_cost": getattr(game, "duck_bank_cost", 2000000),
        "duck_rocket_cost": getattr(game, "duck_rocket_cost", 10000000),
        "duck_empire_cost": getattr(game, "duck_empire_cost", 50000000),
        "duck_universe_cost": getattr(game, "duck_universe_cost", 250000000),
    }
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        print("Save failed:", e)

def load_progress():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

check_for_update()

class DuckClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Duck Clicker 🦆")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#b3e5fc")

        # --- Load progress ---
        progress = load_progress()
        self.ducks = progress.get("ducks", 0)
        self.ducks_per_click = progress.get("ducks_per_click", 1)
        self.auto_ducks = progress.get("auto_ducks", 0)
        self.rebirths = progress.get("rebirths", 0)
        self.rebirth_cost = progress.get("rebirth_cost", 1000000)
        self.super_ducks = progress.get("super_ducks", 0)
        self.super_duck_cost = progress.get("super_duck_cost", 1000)
        self.ultra_click_cost = progress.get("ultra_click_cost", 500)
        self.ultra_click_active = False
        self.ultra_click_duration = 10
        self.mega_click_cost = progress.get("mega_click_cost", 5000)
        self.mega_click_active = False
        self.mega_click_duration = 5
        self.duck_factory_cost = progress.get("duck_factory_cost", 20000)
        self.duck_factory_count = progress.get("duck_factory_count", 0)
        self.duck_god_cost = progress.get("duck_god_cost", 100000)
        self.duck_god_count = progress.get("duck_god_count", 0)
        self.upgrade1_cost = progress.get("upgrade1_cost", 10)
        self.upgrade2_cost = progress.get("upgrade2_cost", 50)
        self.upgrade3_cost = progress.get("upgrade3_cost", 200)
        self.diamond_duck_cost = progress.get("diamond_duck_cost", 50000)
        self.duck_army_cost = progress.get("duck_army_cost", 250000)
        self.duck_portal_cost = progress.get("duck_portal_cost", 1000000)
        self.duck_bank_cost = progress.get("duck_bank_cost", 2000000)
        self.duck_rocket_cost = progress.get("duck_rocket_cost", 10000000)
        self.duck_empire_cost = progress.get("duck_empire_cost", 50000000)
        self.duck_universe_cost = progress.get("duck_universe_cost", 250000000)

        # Main frame for duck and counter
        main_frame = tk.Frame(root, bg="#b3e5fc")
        main_frame.pack(side="left", fill="both", expand=True)

        self.title = tk.Label(
            main_frame, text="Duck Clicker!", font=("Comic Sans MS", 40, "bold"),
            bg="#b3e5fc", fg="#ffb300"
        )
        self.title.pack(pady=(40, 10))

        self.label = tk.Label(
            main_frame, text=f"Ducks: {self.ducks}", font=("Comic Sans MS", 28, "bold"),
            bg="#b3e5fc", fg="#1976d2"
        )
        self.label.pack(pady=10)

        self.rebirth_label = tk.Label(
            main_frame, text=f"Rebirths: {self.rebirths}", font=("Comic Sans MS", 18, "bold"),
            bg="#b3e5fc", fg="#ab47bc"
        )
        self.rebirth_label.pack(pady=5)

        self.duck_button = tk.Button(
            main_frame, text="(•ᴥ•)\n  🦆", font=("Comic Sans MS", 80, "bold"),
            command=self.click_duck,
            bg="#fffde7", activebackground="#ffe082", bd=6, relief="ridge", cursor="hand2", fg="#ffb300"
        )
        self.duck_button.pack(pady=20)

        self.status = tk.Label(
            main_frame, text="", font=("Comic Sans MS", 16, "italic"),
            bg="#b3e5fc", fg="#388e3c"
        )
        self.status.pack(pady=10)

        self.footer = tk.Label(
            main_frame, text="Quack your way to the top!", font=("Comic Sans MS", 16),
            bg="#b3e5fc", fg="#0288d1"
        )
        self.footer.pack(side="bottom", pady=20)

        # --- Scrollable Upgrades panel on the right ---
        upgrades_outer = tk.Frame(root, bg="#e1bee7", bd=4, relief="ridge")
        upgrades_outer.pack(side="right", fill="y", padx=20, pady=40)

        canvas = tk.Canvas(upgrades_outer, bg="#e1bee7", highlightthickness=0)
        scrollbar = tk.Scrollbar(upgrades_outer, orient="vertical", command=canvas.yview)
        self.upgrades_frame = tk.Frame(canvas, bg="#e1bee7")

        self.upgrades_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.upgrades_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Enable mouse wheel scrolling on upgrades panel ---
        def _on_mousewheel(event):
            # Windows and MacOS
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            elif event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")
            elif event.delta:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        # Windows and Mac
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        # Linux (X11)
        canvas.bind_all("<Button-4>", _on_mousewheel)
        canvas.bind_all("<Button-5>", _on_mousewheel)

        upgrades_title = tk.Label(
            self.upgrades_frame, text="Upgrades", font=("Comic Sans MS", 24, "bold"),
            bg="#e1bee7", fg="#6a1b9a"
        )
        upgrades_title.pack(pady=(10, 20))

        # --- Upgrades ---
        self.upgrade1_button = tk.Button(
            self.upgrades_frame,
            text=f"Stronger Beak (+1/click)\nCost: {self.upgrade1_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade1,
            bg="#ffd54f", fg="#6d4c41", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade1_button.pack(pady=10)

        self.upgrade2_button = tk.Button(
            self.upgrades_frame,
            text=f"Auto Duck (+1/sec)\nCost: {self.upgrade2_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade2,
            bg="#aed581", fg="#33691e", activebackground="#dcedc8", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade2_button.pack(pady=10)

        self.upgrade3_button = tk.Button(
            self.upgrades_frame,
            text=f"Golden Duck (+50 ducks)\nCost: {self.upgrade3_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade3,
            bg="#fff176", fg="#f57c00", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade3_button.pack(pady=10)

        self.super_duck_button = tk.Button(
            self.upgrades_frame,
            text=f"Super Duck (+10/sec)\nCost: {self.super_duck_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_super_duck,
            bg="#81d4fa", fg="#01579b", activebackground="#b3e5fc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.super_duck_button.pack(pady=10)

        self.ultra_click_button = tk.Button(
            self.upgrades_frame,
            text=f"Ultra Click (x10 for 10s)\nCost: {self.ultra_click_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_ultra_click,
            bg="#ff8a65", fg="#4e342e", activebackground="#ffe0b2", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.ultra_click_button.pack(pady=10)

        self.mega_click_button = tk.Button(
            self.upgrades_frame,
            text=f"Mega Click (x100 for 5s)\nCost: {self.mega_click_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_mega_click,
            bg="#d500f9", fg="#fff", activebackground="#ea80fc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.mega_click_button.pack(pady=10)

        self.duck_factory_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Factory (+100/sec)\nCost: {self.duck_factory_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_factory,
            bg="#ffb300", fg="#4e342e", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_factory_button.pack(pady=10)

        self.duck_god_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck God (+1000/sec)\nCost: {self.duck_god_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_god,
            bg="#212121", fg="#ffd600", activebackground="#616161", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_god_button.pack(pady=10)

        self.diamond_duck_button = tk.Button(
            self.upgrades_frame,
            text=f"Diamond Duck (+500 ducks)\nCost: {self.diamond_duck_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_diamond_duck,
            bg="#b9f6ca", fg="#00695c", activebackground="#e0f2f1", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.diamond_duck_button.pack(pady=10)

        self.duck_army_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Army (+5000/sec)\nCost: {self.duck_army_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_army,
            bg="#ff5252", fg="#fff", activebackground="#ff8a80", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_army_button.pack(pady=10)

        self.duck_portal_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Portal (x2 ducks/sec)\nCost: {self.duck_portal_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_portal,
            bg="#7c4dff", fg="#fff", activebackground="#b388ff", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_portal_button.pack(pady=10)

        # --- New upgrades for more fun ---
        self.duck_bank_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Bank (+25000/sec)\nCost: {self.duck_bank_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_bank,
            bg="#ffe082", fg="#795548", activebackground="#fffde7", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_bank_button.pack(pady=10)

        self.duck_rocket_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Rocket (+100000/sec)\nCost: {self.duck_rocket_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_rocket,
            bg="#b0bec5", fg="#263238", activebackground="#cfd8dc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_rocket_button.pack(pady=10)

        self.duck_empire_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Empire (+500000/sec)\nCost: {self.duck_empire_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_empire,
            bg="#ffab91", fg="#bf360c", activebackground="#ffccbc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_empire_button.pack(pady=10)

        self.duck_universe_button = tk.Button(
            self.upgrades_frame,
            text=f"Duck Universe (+2,500,000/sec)\nCost: {self.duck_universe_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_universe,
            bg="#b388ff", fg="#311b92", activebackground="#ede7f6", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_universe_button.pack(pady=10)

        # --- Rebirth button ---
        self.rebirth_button = tk.Button(
            self.upgrades_frame,
            text=f"REBIRTH!\nCost: {self.rebirth_cost} ducks",
            font=("Comic Sans MS", 16, "bold"),
            command=self.rebirth,
            bg="#fff", fg="#ab47bc", activebackground="#f3e5f5", bd=4, relief="ridge", cursor="hand2", width=22, height=2
        )
        self.rebirth_button.pack(pady=20)

        self.auto_duck_loop()
        self.root.after(1000, self.auto_save)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ...rest of your class code (unchanged, as in your current file)...
    # (All upgrade methods, rebirth, auto_duck_loop, etc.)

    def on_close(self):
        save_progress(self)
        self.root.destroy()

    def auto_save(self):
        save_progress(self)
        self.root.after(1000, self.auto_save)

    def click_duck(self):
        bonus = 1 + self.rebirths * 0.5
        if self.ultra_click_active:
            self.ducks += int(self.ducks_per_click * 10 * bonus)
        elif self.mega_click_active:
            self.ducks += int(self.ducks_per_click * 100 * bonus)
        else:
            self.ducks += int(self.ducks_per_click * bonus)
        self.label.config(text=f"Ducks: {self.ducks}")
        self.status.config(text="Quack! 🦆", fg="#388e3c")

    # ...all other upgrade/buy methods and rebirth method...

    def auto_duck_loop(self):
        if self.auto_ducks > 0:
            self.ducks += self.auto_ducks
            self.label.config(text=f"Ducks: {self.ducks}")
        self.root.after(1000, self.auto_duck_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = DuckClicker(root)
    root.mainloop()
