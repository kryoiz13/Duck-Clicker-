import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import urllib.request
import json

# --- AUTO-UPDATE SETTINGS ---
UPDATE_URL = "https://raw.githubusercontent.com/kryoiz13/Duck-Clicker-/main/duck_clicker.py"
LOCAL_FILE = os.path.abspath(__file__)
SAVE_FILE = "savegame.json"

def normalize_line_endings(s):
    return s.replace('\r\n', '\n').replace('\r', '\n')

def abbreviate(n):
    n = float(n)
    for unit in ['','K','M','B','T','Q']:
        if abs(n) < 1000:
            if unit == '':
                return f"{int(n)}"
            return f"{n:.1f}{unit}"
        n /= 1000.0
    return f"{n:.1f}Q"

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
        "extra_upgrade_costs": getattr(game, "extra_upgrade_costs", []),
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

        # --- Tabs setup ---
        self.notebook = ttk.Notebook(root)
        self.main_tab = tk.Frame(self.notebook, bg="#232946")
        self.stats_tab = tk.Frame(self.notebook, bg="#232946")
        self.notebook.add(self.main_tab, text="Game")
        self.notebook.add(self.stats_tab, text="Stats")
        self.notebook.pack(fill="both", expand=True)

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

        # --- 23 Named Upgrades ---
        self.extra_upgrade_names = [
            "Quantum Duck", "Time Duck", "Space Duck", "Dark Duck", "Light Duck", "Infinity Duck",
            "Omega Duck", "Alpha Duck", "Beta Duck", "Gamma Duck", "Delta Duck", "Epsilon Duck",
            "Zeta Duck", "Eta Duck", "Theta Duck", "Iota Duck", "Kappa Duck", "Lambda Duck",
            "Mu Duck", "Nu Duck", "Xi Duck", "Omicron Duck", "Ultimate Duck"
        ]
        self.extra_upgrade_costs = progress.get("extra_upgrade_costs", [
            500_000_000, 2_000_000_000, 8_000_000_000, 30_000_000_000, 120_000_000_000,
            500_000_000_000, 2_000_000_000_000, 8_000_000_000_000, 30_000_000_000_000,
            120_000_000_000_000, 500_000_000_000_000, 2_000_000_000_000_000, 8_000_000_000_000_000,
            30_000_000_000_000_000, 120_000_000_000_000_000, 500_000_000_000_000_000,
            2_000_000_000_000_000_000, 8_000_000_000_000_000_000, 30_000_000_000_000_000_000,
            120_000_000_000_000_000_000, 500_000_000_000_000_000_000, 2_000_000_000_000_000_000_000,
            8_000_000_000_000_000_000_000
        ])
        self.extra_upgrade_incomes = [
            5_000_000, 20_000_000, 80_000_000, 300_000_000, 1_200_000_000, 5_000_000_000,
            20_000_000_000, 80_000_000_000, 300_000_000_000, 1_200_000_000_000, 5_000_000_000_000,
            20_000_000_000_000, 80_000_000_000_000, 300_000_000_000_000, 1_200_000_000_000_000,
            5_000_000_000_000_000, 20_000_000_000_000_000, 80_000_000_000_000_000,
            300_000_000_000_000_000, 1_200_000_000_000_000_000, 5_000_000_000_000_000_000,
            20_000_000_000_000_000_000, 80_000_000_000_000_000_000
        ]
        self.extra_upgrade_buttons = []

        # Main frame for duck and counter (parent is self.main_tab)
        main_frame = tk.Frame(self.main_tab, bg="#232946")
        main_frame.pack(side="left", fill="both", expand=True)

        self.title = tk.Label(
            main_frame, text="Duck Clicker!", font=("Segoe UI", 44, "bold"),
            bg="#232946", fg="#eebbc3"
        )
        self.title.pack(pady=(40, 10))

        self.label = tk.Label(
            main_frame, text=f"Ducks: {abbreviate(self.ducks)}", font=("Segoe UI", 28, "bold"),
            bg="#232946", fg="#fffffe"
        )
        self.label.pack(pady=10)

        self.rebirth_label = tk.Label(
            main_frame, text=f"Rebirths: {abbreviate(self.rebirths)}", font=("Segoe UI", 18, "bold"),
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
        upgrades_outer = tk.Frame(self.main_tab, bg="#232946", bd=0, relief="flat")
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
            f"Stronger Beak (+1/click)\nCost: {abbreviate(self.upgrade1_cost)} ducks",
            self.buy_upgrade1
        )
        self.upgrade1_button.pack(pady=7)

        self.upgrade2_button = pretty_button(
            self.upgrades_frame,
            f"Auto Duck (+1/sec)\nCost: {abbreviate(self.upgrade2_cost)} ducks",
            self.buy_upgrade2
        )
        self.upgrade2_button.pack(pady=7)

        self.upgrade3_button = pretty_button(
            self.upgrades_frame,
            f"Golden Duck (+50 ducks)\nCost: {abbreviate(self.upgrade3_cost)} ducks",
            self.buy_upgrade3
        )
        self.upgrade3_button.pack(pady=7)

        self.super_duck_button = pretty_button(
            self.upgrades_frame,
            f"Super Duck (+10/sec)\nCost: {abbreviate(self.super_duck_cost)} ducks",
            self.buy_super_duck
        )
        self.super_duck_button.pack(pady=7)

        self.ultra_click_button = pretty_button(
            self.upgrades_frame,
            f"Ultra Click (x10 for 10s)\nCost: {abbreviate(self.ultra_click_cost)} ducks",
            self.buy_ultra_click
        )
        self.ultra_click_button.pack(pady=7)

        self.mega_click_button = pretty_button(
            self.upgrades_frame,
            f"Mega Click (x100 for 5s)\nCost: {abbreviate(self.mega_click_cost)} ducks",
            self.buy_mega_click
        )
        self.mega_click_button.pack(pady=7)

        self.duck_factory_button = pretty_button(
            self.upgrades_frame,
            f"Duck Factory (+100/sec)\nCost: {abbreviate(self.duck_factory_cost)} ducks",
            self.buy_duck_factory
        )
        self.duck_factory_button.pack(pady=7)

        self.duck_god_button = pretty_button(
            self.upgrades_frame,
            f"Duck God (+1000/sec)\nCost: {abbreviate(self.duck_god_cost)} ducks",
            self.buy_duck_god
        )
        self.duck_god_button.pack(pady=7)

        self.diamond_duck_button = pretty_button(
            self.upgrades_frame,
            f"Diamond Duck (+500 ducks)\nCost: {abbreviate(self.diamond_duck_cost)} ducks",
            self.buy_diamond_duck
        )
        self.diamond_duck_button.pack(pady=7)

        self.duck_army_button = pretty_button(
            self.upgrades_frame,
            f"Duck Army (+5000/sec)\nCost: {abbreviate(self.duck_army_cost)} ducks",
            self.buy_duck_army
        )
        self.duck_army_button.pack(pady=7)

        self.duck_portal_button = pretty_button(
            self.upgrades_frame,
            f"Duck Portal (x2 ducks/sec)\nCost: {abbreviate(self.duck_portal_cost)} ducks",
            self.buy_duck_portal
        )
        self.duck_portal_button.pack(pady=7)

        self.duck_bank_button = pretty_button(
            self.upgrades_frame,
            f"Duck Bank (+25000/sec)\nCost: {abbreviate(self.duck_bank_cost)} ducks",
            self.buy_duck_bank
        )
        self.duck_bank_button.pack(pady=7)

        self.duck_rocket_button = pretty_button(
            self.upgrades_frame,
            f"Duck Rocket (+100000/sec)\nCost: {abbreviate(self.duck_rocket_cost)} ducks",
            self.buy_duck_rocket
        )
        self.duck_rocket_button.pack(pady=7)

        self.duck_empire_button = pretty_button(
            self.upgrades_frame,
            f"Duck Empire (+500000/sec)\nCost: {abbreviate(self.duck_empire_cost)} ducks",
            self.buy_duck_empire
        )
        self.duck_empire_button.pack(pady=7)

        self.duck_universe_button = pretty_button(
            self.upgrades_frame,
            f"Duck Universe (+2,500,000/sec)\nCost: {abbreviate(self.duck_universe_cost)} ducks",
            self.buy_duck_universe
        )
        self.duck_universe_button.pack(pady=7)

        # --- 23 Named Upgrades ---
        for idx, name in enumerate(self.extra_upgrade_names):
            btn = pretty_button(
                self.upgrades_frame,
                f"{name} (+{abbreviate(self.extra_upgrade_incomes[idx])}/sec)\nCost: {abbreviate(self.extra_upgrade_costs[idx])} ducks",
                lambda i=idx: self.buy_extra_upgrade(i)
            )
            btn.pack(pady=7)
            self.extra_upgrade_buttons.append(btn)

        # --- Stats tab content ---
        self.stats_title = tk.Label(
            self.stats_tab, text="Duck Stats", font=("Segoe UI", 32, "bold"),
            bg="#232946", fg="#eebbc3"
        )
        self.stats_title.pack(pady=30)

        self.stats_click_label = tk.Label(
            self.stats_tab, text="", font=("Segoe UI", 22),
            bg="#232946", fg="#fffffe"
        )
        self.stats_click_label.pack(pady=15)

        self.stats_auto_label = tk.Label(
            self.stats_tab, text="", font=("Segoe UI", 22),
            bg="#232946", fg="#fffffe"
        )
        self.stats_auto_label.pack(pady=15)

        self.update_stats_tab()  # Start updating stats

        self.auto_duck_loop()
        self.root.after(1000, self.auto_save)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_stats_tab(self):
        # Calculate per-click ducks (with rebirth and multipliers)
        bonus = 1 + self.rebirths * 0.5
        if self.ultra_click_active:
            per_click = int(self.ducks_per_click * 10 * bonus)
        elif self.mega_click_active:
            per_click = int(self.ducks_per_click * 100 * bonus)
        else:
            per_click = int(self.ducks_per_click * bonus)
        self.stats_click_label.config(
            text=f"Ducks per click: {abbreviate(per_click)}"
        )
        self.stats_auto_label.config(
            text=f"Ducks per second (auto): {abbreviate(self.auto_ducks)}"
        )
        self.root.after(200, self.update_stats_tab)  # Update every 0.2s

    def click_duck(self):
        bonus = 1 + self.rebirths * 0.5
        if self.ultra_click_active:
            self.ducks += int(self.ducks_per_click * 10 * bonus)
        elif self.mega_click_active:
            self.ducks += int(self.ducks_per_click * 100 * bonus)
        else:
            self.ducks += int(self.ducks_per_click * bonus)
        self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
        self.status.config(text="Quack! 🦆", fg="#b8c1ec")

    def buy_upgrade1(self):
        if self.ducks >= self.upgrade1_cost:
            self.ducks -= self.upgrade1_cost
            self.ducks_per_click += 1
            self.upgrade1_cost = int(self.upgrade1_cost * 1.5) + 2
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.upgrade1_button.config(
                text=f"Stronger Beak (+1/click)\nCost: {abbreviate(self.upgrade1_cost)} ducks"
            )
            self.status.config(text="Your duck click is stronger!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_upgrade2(self):
        if self.ducks >= self.upgrade2_cost:
            self.ducks -= self.upgrade2_cost
            self.auto_ducks += 1
            self.upgrade2_cost = int(self.upgrade2_cost * 1.7) + 5
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.upgrade2_button.config(
                text=f"Auto Duck (+1/sec)\nCost: {abbreviate(self.upgrade2_cost)} ducks"
            )
            self.status.config(text="Auto Duck hired! Ducks per second increased!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_upgrade3(self):
        if self.ducks >= self.upgrade3_cost:
            self.ducks -= self.upgrade3_cost
            self.ducks += 50
            self.upgrade3_cost = int(self.upgrade3_cost * 2.2) + 10
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.upgrade3_button.config(
                text=f"Golden Duck (+50 ducks)\nCost: {abbreviate(self.upgrade3_cost)} ducks"
            )
            self.status.config(text="Golden Duck! That's a lot of ducks!", fg="#fbc02d")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    # --- All other upgrade methods ---
    def buy_super_duck(self):
        if self.ducks >= self.super_duck_cost:
            self.ducks -= self.super_duck_cost
            self.auto_ducks += 10
            self.super_duck_cost = int(self.super_duck_cost * 2.2) + 100
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.super_duck_button.config(
                text=f"Super Duck (+10/sec)\nCost: {abbreviate(self.super_duck_cost)} ducks"
            )
            self.status.config(text="Super Duck hired! +10/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_ultra_click(self):
        if self.ducks >= self.ultra_click_cost and not self.ultra_click_active:
            self.ducks -= self.ultra_click_cost
            self.ultra_click_active = True
            self.ultra_click_cost = int(self.ultra_click_cost * 2.5) + 100
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.ultra_click_button.config(
                text=f"Ultra Click (x10 for 10s)\nCost: {abbreviate(self.ultra_click_cost)} ducks"
            )
            self.status.config(text="Ultra Click active! x10/click for 10s!", fg="#b8c1ec")
            self.root.after(self.ultra_click_duration * 1000, self.end_ultra_click)
        else:
            self.status.config(text="Not enough ducks or already active!", fg="#d32f2f")

    def end_ultra_click(self):
        self.ultra_click_active = False
        self.status.config(text="Ultra Click ended.", fg="#b8c1ec")

    def buy_mega_click(self):
        if self.ducks >= self.mega_click_cost and not self.mega_click_active:
            self.ducks -= self.mega_click_cost
            self.mega_click_active = True
            self.mega_click_cost = int(self.mega_click_cost * 2.5) + 500
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.mega_click_button.config(
                text=f"Mega Click (x100 for 5s)\nCost: {abbreviate(self.mega_click_cost)} ducks"
            )
            self.status.config(text="Mega Click active! x100/click for 5s!", fg="#b8c1ec")
            self.root.after(self.mega_click_duration * 1000, self.end_mega_click)
        else:
            self.status.config(text="Not enough ducks or already active!", fg="#d32f2f")

    def end_mega_click(self):
        self.mega_click_active = False
        self.status.config(text="Mega Click ended.", fg="#b8c1ec")

    def buy_duck_factory(self):
        if self.ducks >= self.duck_factory_cost:
            self.ducks -= self.duck_factory_cost
            self.auto_ducks += 100
            self.duck_factory_cost = int(self.duck_factory_cost * 2.5) + 1000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_factory_button.config(
                text=f"Duck Factory (+100/sec)\nCost: {abbreviate(self.duck_factory_cost)} ducks"
            )
            self.status.config(text="Duck Factory built! +100/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_god(self):
        if self.ducks >= self.duck_god_cost:
            self.ducks -= self.duck_god_cost
            self.auto_ducks += 1000
            self.duck_god_cost = int(self.duck_god_cost * 2.5) + 5000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_god_button.config(
                text=f"Duck God (+1000/sec)\nCost: {abbreviate(self.duck_god_cost)} ducks"
            )
            self.status.config(text="Duck God summoned! +1000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_diamond_duck(self):
        if self.ducks >= self.diamond_duck_cost:
            self.ducks -= self.diamond_duck_cost
            self.ducks += 500
            self.diamond_duck_cost = int(self.diamond_duck_cost * 2.5) + 5000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.diamond_duck_button.config(
                text=f"Diamond Duck (+500 ducks)\nCost: {abbreviate(self.diamond_duck_cost)} ducks"
            )
            self.status.config(text="Diamond Duck! +500 ducks!", fg="#fbc02d")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_army(self):
        if self.ducks >= self.duck_army_cost:
            self.ducks -= self.duck_army_cost
            self.auto_ducks += 5000
            self.duck_army_cost = int(self.duck_army_cost * 2.5) + 25000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_army_button.config(
                text=f"Duck Army (+5000/sec)\nCost: {abbreviate(self.duck_army_cost)} ducks"
            )
            self.status.config(text="Duck Army recruited! +5000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_portal(self):
        if self.ducks >= self.duck_portal_cost:
            self.ducks -= self.duck_portal_cost
            self.auto_ducks *= 2
            self.duck_portal_cost = int(self.duck_portal_cost * 3) + 100000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_portal_button.config(
                text=f"Duck Portal (x2 ducks/sec)\nCost: {abbreviate(self.duck_portal_cost)} ducks"
            )
            self.status.config(text="Duck Portal opened! Ducks/sec doubled!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_bank(self):
        if self.ducks >= self.duck_bank_cost:
            self.ducks -= self.duck_bank_cost
            self.auto_ducks += 25000
            self.duck_bank_cost = int(self.duck_bank_cost * 2.5) + 200000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_bank_button.config(
                text=f"Duck Bank (+25000/sec)\nCost: {abbreviate(self.duck_bank_cost)} ducks"
            )
            self.status.config(text="Duck Bank built! +25000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_rocket(self):
        if self.ducks >= self.duck_rocket_cost:
            self.ducks -= self.duck_rocket_cost
            self.auto_ducks += 100000
            self.duck_rocket_cost = int(self.duck_rocket_cost * 2.5) + 1000000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_rocket_button.config(
                text=f"Duck Rocket (+100000/sec)\nCost: {abbreviate(self.duck_rocket_cost)} ducks"
            )
            self.status.config(text="Duck Rocket launched! +100000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_empire(self):
        if self.ducks >= self.duck_empire_cost:
            self.ducks -= self.duck_empire_cost
            self.auto_ducks += 500000
            self.duck_empire_cost = int(self.duck_empire_cost * 2.5) + 5000000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_empire_button.config(
                text=f"Duck Empire (+500000/sec)\nCost: {abbreviate(self.duck_empire_cost)} ducks"
            )
            self.status.config(text="Duck Empire founded! +500000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_duck_universe(self):
        if self.ducks >= self.duck_universe_cost:
            self.ducks -= self.duck_universe_cost
            self.auto_ducks += 2500000
            self.duck_universe_cost = int(self.duck_universe_cost * 2.5) + 25000000
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.duck_universe_button.config(
                text=f"Duck Universe (+2,500,000/sec)\nCost: {abbreviate(self.duck_universe_cost)} ducks"
            )
            self.status.config(text="Duck Universe created! +2,500,000/sec!", fg="#b8c1ec")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_extra_upgrade(self, idx):
        if self.ducks >= self.extra_upgrade_costs[idx]:
            self.ducks -= self.extra_upgrade_costs[idx]
            self.auto_ducks += self.extra_upgrade_incomes[idx]
            self.extra_upgrade_costs[idx] = int(self.extra_upgrade_costs[idx] * 2.5)
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.extra_upgrade_buttons[idx].config(
                text=f"{self.extra_upgrade_names[idx]} (+{abbreviate(self.extra_upgrade_incomes[idx])}/sec)\nCost: {abbreviate(self.extra_upgrade_costs[idx])} ducks"
            )
            self.status.config(text=f"{self.extra_upgrade_names[idx]} hired! +{abbreviate(self.extra_upgrade_incomes[idx])}/sec!", fg="#00bcd4")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def auto_duck_loop(self):
        if self.auto_ducks > 0:
            self.ducks += self.auto_ducks
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
        self.root.after(1000, self.auto_duck_loop)

    def on_close(self):
        save_progress(self)
        self.root.destroy()

    def auto_save(self):
        save_progress(self)
        self.root.after(1000, self.auto_save)

if __name__ == "__main__":
    root = tk.Tk()
    game = DuckClicker(root)
    root.mainloop()
