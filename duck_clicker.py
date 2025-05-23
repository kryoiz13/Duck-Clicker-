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

def abbreviate(n):
    # Abbreviate numbers: 1.2K, 2.5M, 3.1B, etc.
    n = float(n)
    for unit in ['','K','M','B','T','Q']:
        if abs(n) < 1000:
            if unit == '':
                return f"{int(n)}"
            return f"{n:.1f}{unit}"
        n /= 1000.0
    return f"{n:.1f}Q"

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

        # Main frame for duck and counter
        main_frame = tk.Frame(root, bg="#232946")
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
                font=("Segoe UI", 15, "bold"),
                command=command,
                bg="#eebbc3", fg="#232946",
                activebackground="#fffffe", activeforeground="#232946",
                bd=0, relief="flat", cursor="hand2",
                wraplength=200, justify="center", height=2, width=20,
                highlightthickness=0
            )

        # --- Upgrades (use pretty_button for all) ---
        self.upgrade1_button = pretty_button(
            self.upgrades_frame,
            f"+1/click | {abbreviate(self.upgrade1_cost)}",
            self.buy_upgrade1
        )
        self.upgrade1_button.pack(pady=4)

        self.upgrade2_button = pretty_button(
            self.upgrades_frame,
            f"+1/sec | {abbreviate(self.upgrade2_cost)}",
            self.buy_upgrade2
        )
        self.upgrade2_button.pack(pady=4)

        self.upgrade3_button = pretty_button(
            self.upgrades_frame,
            f"+50 | {abbreviate(self.upgrade3_cost)}",
            self.buy_upgrade3
        )
        self.upgrade3_button.pack(pady=4)

        # Example for other upgrades (add your own buy_xxx methods as needed)
        self.super_duck_button = pretty_button(
            self.upgrades_frame,
            f"+10/sec | {abbreviate(self.super_duck_cost)}",
            getattr(self, 'buy_super_duck', lambda: None)
        )
        self.super_duck_button.pack(pady=4)

        self.ultra_click_button = pretty_button(
            self.upgrades_frame,
            f"x10/click 10s | {abbreviate(self.ultra_click_cost)}",
            getattr(self, 'buy_ultra_click', lambda: None)
        )
        self.ultra_click_button.pack(pady=4)

        self.mega_click_button = pretty_button(
            self.upgrades_frame,
            f"x100/click 5s | {abbreviate(self.mega_click_cost)}",
            getattr(self, 'buy_mega_click', lambda: None)
        )
        self.mega_click_button.pack(pady=4)

        self.duck_factory_button = pretty_button(
            self.upgrades_frame,
            f"+100/sec | {abbreviate(self.duck_factory_cost)}",
            getattr(self, 'buy_duck_factory', lambda: None)
        )
        self.duck_factory_button.pack(pady=4)

        self.duck_god_button = pretty_button(
            self.upgrades_frame,
            f"+1K/sec | {abbreviate(self.duck_god_cost)}",
            getattr(self, 'buy_duck_god', lambda: None)
        )
        self.duck_god_button.pack(pady=4)

        self.diamond_duck_button = pretty_button(
            self.upgrades_frame,
            f"+500 | {abbreviate(self.diamond_duck_cost)}",
            getattr(self, 'buy_diamond_duck', lambda: None)
        )
        self.diamond_duck_button.pack(pady=4)

        self.duck_army_button = pretty_button(
            self.upgrades_frame,
            f"+5K/sec | {abbreviate(self.duck_army_cost)}",
            getattr(self, 'buy_duck_army', lambda: None)
        )
        self.duck_army_button.pack(pady=4)

        self.duck_portal_button = pretty_button(
            self.upgrades_frame,
            f"x2/sec | {abbreviate(self.duck_portal_cost)}",
            getattr(self, 'buy_duck_portal', lambda: None)
        )
        self.duck_portal_button.pack(pady=4)

        self.duck_bank_button = pretty_button(
            self.upgrades_frame,
            f"+25K/sec | {abbreviate(self.duck_bank_cost)}",
            getattr(self, 'buy_duck_bank', lambda: None)
        )
        self.duck_bank_button.pack(pady=4)

        self.duck_rocket_button = pretty_button(
            self.upgrades_frame,
            f"+100K/sec | {abbreviate(self.duck_rocket_cost)}",
            getattr(self, 'buy_duck_rocket', lambda: None)
        )
        self.duck_rocket_button.pack(pady=4)

        self.duck_empire_button = pretty_button(
            self.upgrades_frame,
            f"+500K/sec | {abbreviate(self.duck_empire_cost)}",
            getattr(self, 'buy_duck_empire', lambda: None)
        )
        self.duck_empire_button.pack(pady=4)

        self.duck_universe_button = pretty_button(
            self.upgrades_frame,
            f"+2.5M/sec | {abbreviate(self.duck_universe_cost)}",
            getattr(self, 'buy_duck_universe', lambda: None)
        )
        self.duck_universe_button.pack(pady=4)

        # --- 23 Named Upgrades ---
        for idx, name in enumerate(self.extra_upgrade_names):
            btn = pretty_button(
                self.upgrades_frame,
                f"+{abbreviate(self.extra_upgrade_incomes[idx])}/sec | {abbreviate(self.extra_upgrade_costs[idx])}\n{name}",
                lambda i=idx: self.buy_extra_upgrade(i)
            )
            btn.pack(pady=4)
            self.extra_upgrade_buttons.append(btn)

        self.rebirth_button = pretty_button(
            self.upgrades_frame,
            f"REBIRTH | {abbreviate(self.rebirth_cost)}",
            self.rebirth
        )
        self.rebirth_button.config(font=("Segoe UI", 15, "bold"), bg="#f6c9d0", fg="#232946", height=2)
        self.rebirth_button.pack(pady=12)

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
        self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
        self.status.config(text="Quack! 🦆", fg="#b8c1ec")

    def buy_upgrade1(self):
        if self.ducks >= self.upgrade1_cost:
            self.ducks -= self.upgrade1_cost
            self.ducks_per_click += 1
            self.upgrade1_cost = int(self.upgrade1_cost * 1.5) + 2
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.upgrade1_button.config(
                text=f"+1/click | {abbreviate(self.upgrade1_cost)}"
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
                text=f"+1/sec | {abbreviate(self.upgrade2_cost)}"
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
                text=f"+50 | {abbreviate(self.upgrade3_cost)}"
            )
            self.status.config(text="Golden Duck! That's a lot of ducks!", fg="#fbc02d")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def buy_extra_upgrade(self, idx):
        if self.ducks >= self.extra_upgrade_costs[idx]:
            self.ducks -= self.extra_upgrade_costs[idx]
            self.auto_ducks += self.extra_upgrade_incomes[idx]
            self.extra_upgrade_costs[idx] = int(self.extra_upgrade_costs[idx] * 2.5)
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.extra_upgrade_buttons[idx].config(
                text=f"+{abbreviate(self.extra_upgrade_incomes[idx])}/sec | {abbreviate(self.extra_upgrade_costs[idx])}\n{self.extra_upgrade_names[idx]}"
            )
            self.status.config(text=f"{self.extra_upgrade_names[idx]} hired! +{abbreviate(self.extra_upgrade_incomes[idx])}/sec!", fg="#00bcd4")
        else:
            self.status.config(text="Not enough ducks! 🦆", fg="#d32f2f")

    def rebirth(self):
        if self.ducks >= self.rebirth_cost:
            self.rebirths += 1
            self.ducks = 0
            self.ducks_per_click = 1
            self.auto_ducks = 0
            self.super_ducks = 0
            self.super_duck_cost = 1000
            self.ultra_click_cost = 500
            self.ultra_click_active = False
            self.ultra_click_duration = 10
            self.mega_click_cost = 5000
            self.mega_click_active = False
            self.mega_click_duration = 5
            self.duck_factory_cost = 20000
            self.duck_factory_count = 0
            self.duck_god_cost = 100000
            self.duck_god_count = 0
            self.upgrade1_cost = 10
            self.upgrade2_cost = 50
            self.upgrade3_cost = 200
            self.diamond_duck_cost = 50000
            self.duck_army_cost = 250000
            self.duck_portal_cost = 1000000
            self.duck_bank_cost = 2000000
            self.duck_rocket_cost = 10000000
            self.duck_empire_cost = 50000000
            self.duck_universe_cost = 250000000
            self.rebirth_cost = int(self.rebirth_cost * 2.5)
            self.label.config(text=f"Ducks: {abbreviate(self.ducks)}")
            self.rebirth_label.config(text=f"Rebirths: {self.rebirths}")
            self.rebirth_button.config(
                text=f"REBIRTH | {abbreviate(self.rebirth_cost)}"
            )
            self.status.config(text=f"Rebirth! Permanent +50% ducks/click! Total rebirths: {self.rebirths}", fg="#eebbc3")
            # Reset all upgrade buttons
            self.upgrade1_button.config(text=f"+1/click | {abbreviate(self.upgrade1_cost)}")
            self.upgrade2_button.config(text=f"+1/sec | {abbreviate(self.upgrade2_cost)}")
            self.upgrade3_button.config(text=f"+50 | {abbreviate(self.upgrade3_cost)}")
            self.super_duck_button.config(text=f"+10/sec | {abbreviate(self.super_duck_cost)}")
            self.ultra_click_button.config(text=f"x10/click 10s | {abbreviate(self.ultra_click_cost)}")
            self.mega_click_button.config(text=f"x100/click 5s | {abbreviate(self.mega_click_cost)}")
            self.duck_factory_button.config(text=f"+100/sec | {abbreviate(self.duck_factory_cost)}")
            self.duck_god_button.config(text=f"+1K/sec | {abbreviate(self.duck_god_cost)}")
            self.diamond_duck_button.config(text=f"+500 | {abbreviate(self.diamond_duck_cost)}")
            self.duck_army_button.config(text=f"+5K/sec | {abbreviate(self.duck_army_cost)}")
            self.duck_portal_button.config(text=f"x2/sec | {abbreviate(self.duck_portal_cost)}")
            self.duck_bank_button.config(text=f"+25K/sec | {abbreviate(self.duck_bank_cost)}")
            self.duck_rocket_button.config(text=f"+100K/sec | {abbreviate(self.duck_rocket_cost)}")
            self.duck_empire_button.config(text=f"+500K/sec | {abbreviate(self.duck_empire_cost)}")
            self.duck_universe_button.config(text=f"+2.5M/sec | {abbreviate(self.duck_universe_cost)}")
            # Reset extra upgrades
            for idx, btn in enumerate(self.extra_upgrade_buttons):
                btn.config(
                    text=f"+{abbreviate(self.extra_upgrade_incomes[idx])}/sec | {abbreviate(self.extra_upgrade_costs[idx])}\n{self.extra_upgrade_names[idx]}"
                )
        else:
            self.status.config(text="Not enough ducks to rebirth!", fg="#d32f2f")

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
