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
        # Normalize line endings for both
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

        # Main frame for duck and counter
        main_frame = tk.Frame(root, bg="#b3e5fc")
        main_frame.pack(side="left", fill="both", expand=True)

        # Title label
        self.title = tk.Label(
            main_frame, text="Duck Clicker!", font=("Comic Sans MS", 40, "bold"),
            bg="#b3e5fc", fg="#ffb300"
        )
        self.title.pack(pady=(40, 10))

        # Duck counter label
        self.label = tk.Label(
            main_frame, text=f"Ducks: {self.ducks}", font=("Comic Sans MS", 28, "bold"),
            bg="#b3e5fc", fg="#1976d2"
        )
        self.label.pack(pady=10)

        # Cute duck (drawn with emoji and text)
        self.duck_button = tk.Button(
            main_frame, text="(•ᴥ•)\n  🦆", font=("Comic Sans MS", 80, "bold"),
            command=self.click_duck,
            bg="#fffde7", activebackground="#ffe082", bd=6, relief="ridge", cursor="hand2", fg="#ffb300"
        )
        self.duck_button.pack(pady=20)

        # Status label
        self.status = tk.Label(
            main_frame, text="", font=("Comic Sans MS", 16, "italic"),
            bg="#b3e5fc", fg="#388e3c"
        )
        self.status.pack(pady=10)

        # Fun footer
        self.footer = tk.Label(
            main_frame, text="Quack your way to the top!", font=("Comic Sans MS", 16),
            bg="#b3e5fc", fg="#0288d1"
        )
        self.footer.pack(side="bottom", pady=20)

        # --- Upgrades panel on the right ---
        upgrades_frame = tk.Frame(root, bg="#e1bee7", bd=4, relief="ridge")
        upgrades_frame.pack(side="right", fill="y", padx=20, pady=40)

        upgrades_title = tk.Label(
            upgrades_frame, text="Upgrades", font=("Comic Sans MS", 24, "bold"),
            bg="#e1bee7", fg="#6a1b9a"
        )
        upgrades_title.pack(pady=(10, 20))

        # Upgrade 1: Increase ducks per click
        self.upgrade1_button = tk.Button(
            upgrades_frame,
            text=f"Stronger Beak (+1/click)\nCost: {self.upgrade1_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade1,
            bg="#ffd54f", fg="#6d4c41", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade1_button.pack(pady=10)

        # Upgrade 2: Auto Duck (ducks per second)
        self.upgrade2_button = tk.Button(
            upgrades_frame,
            text=f"Auto Duck (+1/sec)\nCost: {self.upgrade2_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade2,
            bg="#aed581", fg="#33691e", activebackground="#dcedc8", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade2_button.pack(pady=10)

        # Upgrade 3: Golden Duck (big bonus)
        self.upgrade3_button = tk.Button(
            upgrades_frame,
            text=f"Golden Duck (+50 ducks)\nCost: {self.upgrade3_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_upgrade3,
            bg="#fff176", fg="#f57c00", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.upgrade3_button.pack(pady=10)

        # Upgrade 4: Super Duck (adds 10 ducks/sec)
        self.super_duck_button = tk.Button(
            upgrades_frame,
            text=f"Super Duck (+10/sec)\nCost: {self.super_duck_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_super_duck,
            bg="#81d4fa", fg="#01579b", activebackground="#b3e5fc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.super_duck_button.pack(pady=10)

        # Upgrade 5: Ultra Click (10x click for 10 seconds)
        self.ultra_click_button = tk.Button(
            upgrades_frame,
            text=f"Ultra Click (x10 for 10s)\nCost: {self.ultra_click_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_ultra_click,
            bg="#ff8a65", fg="#4e342e", activebackground="#ffe0b2", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.ultra_click_button.pack(pady=10)

        # Upgrade 6: Mega Click (x100 for 5s)
        self.mega_click_button = tk.Button(
            upgrades_frame,
            text=f"Mega Click (x100 for 5s)\nCost: {self.mega_click_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_mega_click,
            bg="#d500f9", fg="#fff", activebackground="#ea80fc", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.mega_click_button.pack(pady=10)

        # Upgrade 7: Duck Factory (+100/sec)
        self.duck_factory_button = tk.Button(
            upgrades_frame,
            text=f"Duck Factory (+100/sec)\nCost: {self.duck_factory_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_factory,
            bg="#ffb300", fg="#4e342e", activebackground="#ffe082", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_factory_button.pack(pady=10)

        # Upgrade 8: Duck God (+1000/sec)
        self.duck_god_button = tk.Button(
            upgrades_frame,
            text=f"Duck God (+1000/sec)\nCost: {self.duck_god_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_god,
            bg="#212121", fg="#ffd600", activebackground="#616161", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_god_button.pack(pady=10)

        # Upgrade 9: Diamond Duck (+500 ducks instantly)
        self.diamond_duck_button = tk.Button(
            upgrades_frame,
            text=f"Diamond Duck (+500 ducks)\nCost: {self.diamond_duck_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_diamond_duck,
            bg="#b9f6ca", fg="#00695c", activebackground="#e0f2f1", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.diamond_duck_button.pack(pady=10)

        # Upgrade 10: Duck Army (+5000/sec)
        self.duck_army_button = tk.Button(
            upgrades_frame,
            text=f"Duck Army (+5000/sec)\nCost: {self.duck_army_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_army,
            bg="#ff5252", fg="#fff", activebackground="#ff8a80", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_army_button.pack(pady=10)

        # Upgrade 11: Duck Portal (doubles all ducks/sec)
        self.duck_portal_button = tk.Button(
            upgrades_frame,
            text=f"Duck Portal (x2 ducks/sec)\nCost: {self.duck_portal_cost} ducks",
            font=("Comic Sans MS", 14, "bold"),
            command=self.buy_duck_portal,
            bg="#7c4dff", fg="#fff", activebackground="#b388ff", bd=3, relief="raised", cursor="hand2", width=22, height=2
        )
        self.duck_portal_button.pack(pady=10)

        # Start auto duck loop
        self.auto_duck_loop()

        # Save progress every 1 second as backup
        self.root.after(1000, self.auto_save)
        # Save on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        save_progress(self)
        self.root.destroy()

    def auto_save(self):
        save_progress(self)
        self.root.after(1000, self.auto_save)

    def click_duck(self):
        if self.ultra_click_active:
            self.ducks += self.ducks_per_click * 10
        elif self.mega_click_active:
            self.ducks += self.ducks_per_click * 100
        else:
            self.ducks += self.ducks_per_click
        self.label.config(text=f"Ducks: {self.ducks}")
        self.status.config(text="Quack! 🦆", fg="#388e3c")

    def buy_upgrade1(self):
        if self.ducks >= self.upgrade1_cost:
            self.ducks -= self.upgrade1_cost
            self.ducks_per_click += 1
            self.upgrade1_cost = int(self.upgrade1_cost * 1.5) + 2
            self.label.config(text=f"Ducks: {self.ducks}")
            self.upgrade1_button.config(
                text=f"Stronger Beak (+1/click)\nCost: {self.upgrade1_cost} ducks"
            )
            self.status.config(text="Your duck click is stronger!", fg="#388e3c")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_upgrade2(self):
        if self.ducks >= self.upgrade2_cost:
            self.ducks -= self.upgrade2_cost
            self.auto_ducks += 1
            self.upgrade2_cost = int(self.upgrade2_cost * 1.7) + 5
            self.label.config(text=f"Ducks: {self.ducks}")
            self.upgrade2_button.config(
                text=f"Auto Duck (+1/sec)\nCost: {self.upgrade2_cost} ducks"
            )
            self.status.config(text="Auto Duck hired! Ducks per second increased!", fg="#388e3c")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_upgrade3(self):
        if self.ducks >= self.upgrade3_cost:
            self.ducks -= self.upgrade3_cost
            self.ducks += 50
            self.upgrade3_cost = int(self.upgrade3_cost * 2.2) + 10
            self.label.config(text=f"Ducks: {self.ducks}")
            self.upgrade3_button.config(
                text=f"Golden Duck (+50 ducks)\nCost: {self.upgrade3_cost} ducks"
            )
            self.status.config(text="Golden Duck! That's a lot of ducks!", fg="#fbc02d")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_super_duck(self):
        if self.ducks >= self.super_duck_cost:
            self.ducks -= self.super_duck_cost
            self.auto_ducks += 10
            self.super_duck_cost = int(self.super_duck_cost * 2.5)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.super_duck_button.config(
                text=f"Super Duck (+10/sec)\nCost: {self.super_duck_cost} ducks"
            )
            self.status.config(text="Super Duck hired! Ducks per second +10!", fg="#0288d1")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_ultra_click(self):
        if self.ducks >= self.ultra_click_cost and not self.ultra_click_active:
            self.ducks -= self.ultra_click_cost
            self.ultra_click_cost = int(self.ultra_click_cost * 2.5)
            self.ultra_click_button.config(
                text=f"Ultra Click (x10 for 10s)\nCost: {self.ultra_click_cost} ducks"
            )
            self.label.config(text=f"Ducks: {self.ducks}")
            self.ultra_click_active = True
            self.status.config(text="Ultra Click activated! 10x for 10s!", fg="#ff7043")
            self.root.after(self.ultra_click_duration * 1000, self.deactivate_ultra_click)
        elif self.ultra_click_active:
            self.status.config(text="Ultra Click already active!", fg="#d32f2f")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def deactivate_ultra_click(self):
        self.ultra_click_active = False
        self.status.config(text="Ultra Click ended!", fg="#388e3c")

    def buy_mega_click(self):
        if self.ducks >= self.mega_click_cost and not self.mega_click_active:
            self.ducks -= self.mega_click_cost
            self.mega_click_cost = int(self.mega_click_cost * 2.5)
            self.mega_click_button.config(
                text=f"Mega Click (x100 for 5s)\nCost: {self.mega_click_cost} ducks"
            )
            self.label.config(text=f"Ducks: {self.ducks}")
            self.mega_click_active = True
            self.status.config(text="Mega Click activated! 100x for 5s!", fg="#d500f9")
            self.root.after(self.mega_click_duration * 1000, self.deactivate_mega_click)
        elif self.mega_click_active:
            self.status.config(text="Mega Click already active!", fg="#d32f2f")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def deactivate_mega_click(self):
        self.mega_click_active = False
        self.status.config(text="Mega Click ended!", fg="#388e3c")

    def buy_duck_factory(self):
        if self.ducks >= self.duck_factory_cost:
            self.ducks -= self.duck_factory_cost
            self.auto_ducks += 100
            self.duck_factory_count += 1
            self.duck_factory_cost = int(self.duck_factory_cost * 2.5)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.duck_factory_button.config(
                text=f"Duck Factory (+100/sec)\nCost: {self.duck_factory_cost} ducks"
            )
            self.status.config(text=f"Duck Factory built! Total: {self.duck_factory_count}", fg="#ffb300")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_god(self):
        if self.ducks >= self.duck_god_cost:
            self.ducks -= self.duck_god_cost
            self.auto_ducks += 1000
            self.duck_god_count += 1
            self.duck_god_cost = int(self.duck_god_cost * 3)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.duck_god_button.config(
                text=f"Duck God (+1000/sec)\nCost: {self.duck_god_cost} ducks"
            )
            self.status.config(text=f"Duck God ascended! Total: {self.duck_god_count}", fg="#ffd600")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_diamond_duck(self):
        if self.ducks >= self.diamond_duck_cost:
            self.ducks -= self.diamond_duck_cost
            self.ducks += 500
            self.diamond_duck_cost = int(self.diamond_duck_cost * 2.5)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.diamond_duck_button.config(
                text=f"Diamond Duck (+500 ducks)\nCost: {self.diamond_duck_cost} ducks"
            )
            self.status.config(text="Diamond Duck! Shiny and rich!", fg="#00bfae")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_army(self):
        if self.ducks >= self.duck_army_cost:
            self.ducks -= self.duck_army_cost
            self.auto_ducks += 5000
            self.duck_army_cost = int(self.duck_army_cost * 2.5)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.duck_army_button.config(
                text=f"Duck Army (+5000/sec)\nCost: {self.duck_army_cost} ducks"
            )
            self.status.config(text="Duck Army assembled! +5000/sec!", fg="#ff5252")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_portal(self):
        if self.ducks >= self.duck_portal_cost:
            self.ducks -= self.duck_portal_cost
            self.auto_ducks *= 2
            self.duck_portal_cost = int(self.duck_portal_cost * 3)
            self.label.config(text=f"Ducks: {self.ducks}")
            self.duck_portal_button.config(
                text=f"Duck Portal (x2 ducks/sec)\nCost: {self.duck_portal_cost} ducks"
            )
            self.status.config(text="Duck Portal opened! Ducks/sec doubled!", fg="#7c4dff")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def auto_duck_loop(self):
        if self.auto_ducks > 0:
            self.ducks += self.auto_ducks
            self.label.config(text=f"Ducks: {self.ducks}")
        self.root.after(1000, self.auto_duck_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = DuckClicker(root)
    root.mainloop()
