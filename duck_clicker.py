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
        self.root.configure(bg="#232946")

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
        main_frame = tk.Frame(root, bg="#232946")
        main_frame.pack(side="left", fill="both", expand=True)

        self.title = tk.Label(
            main_frame, text="Duck Clicker!", font=("Segoe UI", 44, "bold"),
            bg="#232946", fg="#eebbc3"
        )
        self.title.pack(pady=(40, 10))

        self.label = tk.Label(
            main_frame, text=f"Ducks: {self.ducks}", font=("Segoe UI", 28, "bold"),
            bg="#232946", fg="#fffffe"
        )
        self.label.pack(pady=10)

        self.rebirth_label = tk.Label(
            main_frame, text=f"Rebirths: {self.rebirths}", font=("Segoe UI", 18, "bold"),
            bg="#232946", fg="#eebbc3"
        )
        self.rebirth_label.pack(pady=5)

        # --- Duck button: big emoji only ---
        self.duck_button = tk.Button(
            main_frame, text="🦆", font=("Segoe UI", 80, "bold"),
            command=self.click_duck,
            bg="#eebbc3", activebackground="#fffffe", bd=6, relief="ridge", cursor="hand2", fg="#232946"
        )
        self.duck_button.pack(pady=20)

        self.status = tk.Label(
            main_frame, text="", font=("Segoe UI", 16, "italic"),
            bg="#232946", fg="#b8c1ec"
        )
        self.status.pack(pady=10)

        self.footer = tk.Label(
            main_frame, text="Quack your way to the top!", font=("Segoe UI", 16),
            bg="#232946", fg="#b8c1ec"
        )
        self.footer.pack(side="bottom", pady=20)

        # --- Modern Scrollable Upgrades panel on the right ---
        upgrades_outer = tk.Frame(root, bg="#232946", bd=0, relief="flat")
        upgrades_outer.pack(side="right", fill="y", padx=0, pady=0)

        canvas = tk.Canvas(
            upgrades_outer, bg="#232946", highlightthickness=0, bd=0, relief="flat"
        )
        self.upgrades_frame = tk.Frame(canvas, bg="#393e6c")

        self.upgrades_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.upgrades_frame, anchor="nw")
        canvas.pack(side="left", fill="both", expand=True)

        # --- Mouse wheel scroll anywhere on upgrades panel ---
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.upgrades_frame.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.upgrades_frame.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        upgrades_title = tk.Label(
            self.upgrades_frame, text="Upgrades", font=("Segoe UI", 26, "bold"),
            bg="#393e6c", fg="#eebbc3", pady=10
        )
        upgrades_title.pack(pady=(10, 10))

        # --- Helper for pretty buttons ---
        def pretty_button(parent, text, command):
            return tk.Button(
                parent,
                text=text,
                font=("Segoe UI", 13, "bold"),
                command=command,
                bg="#eebbc3", fg="#232946",
                activebackground="#f6c9d0", activeforeground="#232946",
                bd=0, relief="flat", cursor="hand2",
                wraplength=220, justify="center", height=3, width=22,
                highlightthickness=0
            )

        # --- Upgrades (use pretty_button for all) ---
        self.upgrade1_button = pretty_button(
            self.upgrades_frame,
            f"Stronger Beak (+1/click)\nCost: {self.upgrade1_cost} ducks",
            self.buy_upgrade1
        )
        self.upgrade1_button.pack(pady=7)

        self.upgrade2_button = pretty_button(
            self.upgrades_frame,
            f"Auto Duck (+1/sec)\nCost: {self.upgrade2_cost} ducks",
            self.buy_upgrade2
        )
        self.upgrade2_button.pack(pady=7)

        self.upgrade3_button = pretty_button(
            self.upgrades_frame,
            f"Golden Duck (+50 ducks)\nCost: {self.upgrade3_cost} ducks",
            self.buy_upgrade3
        )
        self.upgrade3_button.pack(pady=7)

        self.super_duck_button = pretty_button(
            self.upgrades_frame,
            f"Super Duck (+10/sec)\nCost: {self.super_duck_cost} ducks",
            self.buy_super_duck
        )
        self.super_duck_button.pack(pady=7)

        self.ultra_click_button = pretty_button(
            self.upgrades_frame,
            f"Ultra Click (x10 for 10s)\nCost: {self.ultra_click_cost} ducks",
            self.buy_ultra_click
        )
        self.ultra_click_button.pack(pady=7)

        self.mega_click_button = pretty_button(
            self.upgrades_frame,
            f"Mega Click (x100 for 5s)\nCost: {self.mega_click_cost} ducks",
            self.buy_mega_click
        )
        self.mega_click_button.pack(pady=7)

        self.duck_factory_button = pretty_button(
            self.upgrades_frame,
            f"Duck Factory (+100/sec)\nCost: {self.duck_factory_cost} ducks",
            self.buy_duck_factory
        )
        self.duck_factory_button.pack(pady=7)

        self.duck_god_button = pretty_button(
            self.upgrades_frame,
            f"Duck God (+1000/sec)\nCost: {self.duck_god_cost} ducks",
            self.buy_duck_god
        )
        self.duck_god_button.pack(pady=7)

        self.diamond_duck_button = pretty_button(
            self.upgrades_frame,
            f"Diamond Duck (+500 ducks)\nCost: {self.diamond_duck_cost} ducks",
            self.buy_diamond_duck
        )
        self.diamond_duck_button.pack(pady=7)

        self.duck_army_button = pretty_button(
            self.upgrades_frame,
            f"Duck Army (+5000/sec)\nCost: {self.duck_army_cost} ducks",
            self.buy_duck_army
        )
        self.duck_army_button.pack(pady=7)

        self.duck_portal_button = pretty_button(
            self.upgrades_frame,
            f"Duck Portal (x2 ducks/sec)\nCost: {self.duck_portal_cost} ducks",
            self.buy_duck_portal
        )
        self.duck_portal_button.pack(pady=7)

        self.duck_bank_button = pretty_button(
            self.upgrades_frame,
            f"Duck Bank (+25000/sec)\nCost: {self.duck_bank_cost} ducks",
            self.buy_duck_bank
        )
        self.duck_bank_button.pack(pady=7)

        self.duck_rocket_button = pretty_button(
            self.upgrades_frame,
            f"Duck Rocket (+100000/sec)\nCost: {self.duck_rocket_cost} ducks",
            self.buy_duck_rocket
        )
        self.duck_rocket_button.pack(pady=7)

        self.duck_empire_button = pretty_button(
            self.upgrades_frame,
            f"Duck Empire (+500000/sec)\nCost: {self.duck_empire_cost} ducks",
            self.buy_duck_empire
        )
        self.duck_empire_button.pack(pady=7)

        self.duck_universe_button = pretty_button(
            self.upgrades_frame,
            f"Duck Universe (+2,500,000/sec)\nCost: {self.duck_universe_cost} ducks",
            self.buy_duck_universe
        )
        self.duck_universe_button.pack(pady=7)

        self.rebirth_button = pretty_button(
            self.upgrades_frame,
            f"REBIRTH!\nCost: {self.rebirth_cost} ducks",
            self.rebirth
        )
        self.rebirth_button.config(font=("Segoe UI", 15, "bold"), bg="#f6c9d0", fg="#232946", height=3)
        self.rebirth_button.pack(pady=18)

        self.auto_duck_loop()
        self.root.after(1000, self.auto_save)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def click_duck(self):
        bonus = 1 + self.rebirths * 0.5
        if self.ultra_click_active:
            self.ducks += int(self.ducks_per_click * 10 * bonus)
        elif self.mega_click_active:
            self.ducks += int(self.ducks_per_click * 100 * bonus)
        else:
            self.ducks += int(self.ducks_per_click * bonus)
        self.label.config(text=f"Ducks: {self.ducks}")
        self.status.config(text="Quack! 🦆", fg="#b8c1ec")

    # ... rest of your methods remain unchanged ...
    # (All your upgrade/buy/rebirth/loop methods are below, as in your current file)

if __name__ == "__main__":
    root = tk.Tk()
    game = DuckClicker(root)
    root.mainloop()
