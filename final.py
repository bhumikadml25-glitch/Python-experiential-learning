import string
import secrets
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime


APP_NAME = "SecurePass | Password Generator"

# ---------- Colors ----------
BG = "#071426"
PANEL = "#0D2038"
PANEL_LIGHT = "#122B49"
ACCENT = "#4263F5"
ACCENT_HOVER = "#5B78FF"
GREEN = "#10B981"
TEXT = "#F4F7FF"
MUTED = "#A9B8D0"
BORDER = "#244365"
RED = "#FB7185"


class PasswordGenerator:
    """Generate passwords using Python's cryptographically secure secrets module."""

    def __init__(
        self,
        length=16,
        use_upper=True,
        use_lower=True,
        use_digits=True,
        use_symbols=True,
        exclude_ambiguous=False,
    ):
        self.length = length
        self.use_upper = use_upper
        self.use_lower = use_lower
        self.use_digits = use_digits
        self.use_symbols = use_symbols
        self.exclude_ambiguous = exclude_ambiguous

    def _categories(self):
        categories = []
        if self.use_upper:
            categories.append(string.ascii_uppercase)
        if self.use_lower:
            categories.append(string.ascii_lowercase)
        if self.use_digits:
            categories.append(string.digits)
        if self.use_symbols:
            categories.append(string.punctuation)

        if self.exclude_ambiguous:
            confusing = "O0Il1"
            categories = [
                "".join(ch for ch in category if ch not in confusing)
                for category in categories
            ]

        return [category for category in categories if category]

    def generate(self):
        if self.length < 4:
            raise ValueError("Password length must be at least 4.")

        categories = self._categories()
        if not categories:
            raise ValueError("Select at least one character category.")

        if self.length < len(categories):
            raise ValueError(
                "Password length is too short for all selected character categories."
            )

        pool = "".join(categories)
        chars = [secrets.choice(category) for category in categories]

        while len(chars) < self.length:
            chars.append(secrets.choice(pool))

        secrets.SystemRandom().shuffle(chars)
        return "".join(chars)

    @staticmethod
    def analyze(password):
        """Simple educational strength estimate; not a security guarantee."""
        checks = {
            "At least 12 characters": len(password) >= 12,
            "Uppercase letters": any(c.isupper() for c in password),
            "Lowercase letters": any(c.islower() for c in password),
            "Numbers": any(c.isdigit() for c in password),
            "Special symbols": any(c in string.punctuation for c in password),
        }

        score = sum(checks.values())
        if len(password) < 8 or score <= 2:
            rating = "Weak"
        elif len(password) >= 12 and score >= 4:
            rating = "Strong"
        else:
            rating = "Moderate"

        return rating, checks


class SecurePassApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x780")
        self.minsize(900, 650)
        self.configure(bg=BG)

        self.generated_passwords = []
        self.saved_history = []

        self._setup_styles()
        self._build_ui()
        self._refresh_history()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            "TNotebook",
            background=BG,
            borderwidth=0,
        )
        style.configure(
            "TNotebook.Tab",
            background=PANEL_LIGHT,
            foreground=TEXT,
            padding=(18, 10),
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", ACCENT)],
            foreground=[("selected", "white")],
        )
        style.configure(
            "TCombobox",
            fieldbackground=PANEL_LIGHT,
            background=PANEL_LIGHT,
            foreground=TEXT,
            arrowcolor=TEXT,
        )
        style.configure(
            "Treeview",
            background=PANEL,
            fieldbackground=PANEL,
            foreground=TEXT,
            rowheight=30,
            bordercolor=BORDER,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Treeview.Heading",
            background=PANEL_LIGHT,
            foreground=TEXT,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )
        style.map("Treeview", background=[("selected", ACCENT)])

    def _button(self, parent, text, command, color=ACCENT, width=None):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=10,
        )
        if width:
            button.configure(width=width)
        return button

    def _label(self, parent, text, size=10, color=TEXT, bold=False):
        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal"),
        )

    def _card(self, parent, title=None):
        frame = tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1)
        if title:
            tk.Label(
                frame,
                text=title,
                bg=PANEL,
                fg=TEXT,
                font=("Segoe UI", 13, "bold"),
                anchor="w",
            ).pack(fill="x", padx=16, pady=(14, 8))
        return frame

    def _build_ui(self):
        header = tk.Frame(self, bg="#0A1B31", height=76)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg="#0A1B31")
        brand.pack(side="left", padx=22, pady=12)
        tk.Label(
            brand, text="◆", bg="#0A1B31", fg="#7C9AFF",
            font=("Segoe UI", 28, "bold")
        ).pack(side="left", padx=(0, 12))
        title_box = tk.Frame(brand, bg="#0A1B31")
        title_box.pack(side="left")
        tk.Label(
            title_box, text="SecurePass", bg="#0A1B31", fg=TEXT,
            font=("Segoe UI", 19, "bold")
        ).pack(anchor="w")
        tk.Label(
            title_box, text="Password Generator & Security Checker",
            bg="#0A1B31", fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w")

        tk.Label(
            header, text="●  LOCAL DESKTOP APP", bg="#0A1B31",
            fg="#6EE7B7", font=("Segoe UI", 9, "bold")
        ).pack(side="right", padx=24)

        intro = tk.Frame(self, bg=BG)
        intro.pack(fill="x", padx=24, pady=(18, 12))
        tk.Label(
            intro, text="Create stronger passwords.", bg=BG, fg=TEXT,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w")
        tk.Label(
            intro,
            text="Customize your settings, generate passwords, and check their estimated strength.",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 0))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 14))

        self.generate_tab = tk.Frame(self.notebook, bg=BG)
        self.check_tab = tk.Frame(self.notebook, bg=BG)
        self.history_tab = tk.Frame(self.notebook, bg=BG)
        self.about_tab = tk.Frame(self.notebook, bg=BG)

        self.notebook.add(self.generate_tab, text="  Generate  ")
        self.notebook.add(self.check_tab, text="  Strength Checker  ")
        self.notebook.add(self.history_tab, text="  Saved History  ")
        self.notebook.add(self.about_tab, text="  About  ")

        self._build_generate_tab()
        self._build_check_tab()
        self._build_history_tab()
        self._build_about_tab()

        footer = tk.Frame(self, bg="#0A1B31", height=34)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer, text="SecurePass  •  Python + Tkinter",
            bg="#0A1B31", fg=MUTED, font=("Segoe UI", 9)
        ).pack(side="left", padx=20, pady=7)
        tk.Label(
            footer, text="Passwords are not saved unless you choose Save",
            bg="#0A1B31", fg=MUTED, font=("Segoe UI", 9)
        ).pack(side="right", padx=20, pady=7)

    def _build_generate_tab(self):
        container = tk.Frame(self.generate_tab, bg=BG)
        container.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(container, bg=BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 8))
        right = tk.Frame(container, bg=BG, width=360)
        right.pack(side="right", fill="both", padx=(8, 0))
        right.pack_propagate(False)

        settings = self._card(left, "⚙  Custom generation")
        settings.pack(fill="x", pady=(0, 12))

        fields = tk.Frame(settings, bg=PANEL)
        fields.pack(fill="x", padx=16, pady=4)

        tk.Label(fields, text="Password length", bg=PANEL, fg=MUTED).grid(
            row=0, column=0, sticky="w", padx=(0, 12), pady=(4, 6)
        )
        tk.Label(fields, text="Number to generate", bg=PANEL, fg=MUTED).grid(
            row=0, column=1, sticky="w", padx=12, pady=(4, 6)
        )

        self.length_var = tk.IntVar(value=16)
        self.count_var = tk.IntVar(value=3)
        self.length_spin = tk.Spinbox(
            fields, from_=4, to=128, textvariable=self.length_var,
            bg=PANEL_LIGHT, fg=TEXT, insertbackground=TEXT,
            buttonbackground=PANEL_LIGHT, relief="flat", width=12,
            font=("Segoe UI", 11)
        )
        self.count_spin = tk.Spinbox(
            fields, from_=1, to=50, textvariable=self.count_var,
            bg=PANEL_LIGHT, fg=TEXT, insertbackground=TEXT,
            buttonbackground=PANEL_LIGHT, relief="flat", width=12,
            font=("Segoe UI", 11)
        )
        self.length_spin.grid(row=1, column=0, sticky="ew", padx=(0, 12), pady=(0, 12))
        self.count_spin.grid(row=1, column=1, sticky="ew", padx=12, pady=(0, 12))
        fields.columnconfigure(0, weight=1)
        fields.columnconfigure(1, weight=1)

        tk.Label(
            settings, text="CHARACTER TYPES", bg=PANEL, fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=16, pady=(4, 6))

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=False)

        options = [
            ("Uppercase letters (A–Z)", self.upper_var),
            ("Lowercase letters (a–z)", self.lower_var),
            ("Numbers (0–9)", self.digits_var),
            ("Special symbols (!@#$…)", self.symbols_var),
            ("Exclude confusing characters (O, 0, I, l, 1)", self.ambiguous_var),
        ]
        for label, variable in options:
            row = tk.Frame(settings, bg=PANEL)
            row.pack(fill="x", padx=16, pady=2)
            tk.Checkbutton(
                row, text=label, variable=variable,
                bg=PANEL, fg=TEXT, selectcolor=PANEL_LIGHT,
                activebackground=PANEL, activeforeground=TEXT,
                font=("Segoe UI", 10), cursor="hand2",
            ).pack(anchor="w")
        self._button(
            settings, "✦  Generate password(s)", self.generate_custom, ACCENT
        ).pack(fill="x", padx=16, pady=16)

        presets = self._card(left, "★  Quick presets")
        presets.pack(fill="x")
        tk.Label(
            presets, text="Choose a ready-made configuration.",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16)
        preset_row = tk.Frame(presets, bg=PANEL)
        preset_row.pack(fill="x", padx=12, pady=12)
        self._button(preset_row, "Easy · 8", lambda: self.generate_preset("easy"), "#375477").pack(
            side="left", expand=True, fill="x", padx=4
        )
        self._button(preset_row, "Moderate · 12", lambda: self.generate_preset("moderate"), "#375477").pack(
            side="left", expand=True, fill="x", padx=4
        )
        self._button(preset_row, "Strong · 16", lambda: self.generate_preset("strong"), GREEN).pack(
            side="left", expand=True, fill="x", padx=4
        )

        results = self._card(right, "🔑  Generated passwords")
        results.pack(fill="both", expand=True)
        tk.Label(
            results, text="Select a password to copy it.",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 8))

        list_frame = tk.Frame(results, bg=PANEL)
        list_frame.pack(fill="both", expand=True, padx=12)
        self.password_list = tk.Listbox(
            list_frame, bg=PANEL_LIGHT, fg=TEXT, selectbackground=ACCENT,
            selectforeground="white", font=("Consolas", 11),
            relief="flat", highlightthickness=1, highlightbackground=BORDER,
            activestyle="none"
        )
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.password_list.yview)
        self.password_list.configure(yscrollcommand=scrollbar.set)
        self.password_list.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.strength_label = tk.Label(
            results, text="Strength: —", bg=PANEL, fg="#6EE7B7",
            font=("Segoe UI", 10, "bold")
        )
        self.strength_label.pack(anchor="w", padx=16, pady=(10, 4))
        actions = tk.Frame(results, bg=PANEL)
        actions.pack(fill="x", padx=12, pady=(4, 12))
        self._button(actions, "Copy selected", self.copy_selected, ACCENT).pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )
        self._button(actions, "Copy all", self.copy_all, "#375477").pack(
            side="left", fill="x", expand=True, padx=(5, 0)
        )
        self._button(results, "Save to file…", self.save_to_file, GREEN).pack(
            fill="x", padx=12, pady=(0, 12)
        )
        self.password_list.bind("<<ListboxSelect>>", self.on_password_select)

    def _build_check_tab(self):
        outer = tk.Frame(self.check_tab, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=24)
        card = self._card(outer, "🔎  Password strength checker")
        card.pack(fill="x", anchor="n")
        tk.Label(
            card,
            text="Enter a password to see a basic strength estimate. The text stays in this app.",
            bg=PANEL, fg=MUTED, wraplength=760, justify="left"
        ).pack(anchor="w", padx=16, pady=(0, 14))

        line = tk.Frame(card, bg=PANEL)
        line.pack(fill="x", padx=16)
        self.check_var = tk.StringVar()
        self.check_entry = tk.Entry(
            line, textvariable=self.check_var, show="•",
            bg=PANEL_LIGHT, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=("Segoe UI", 12)
        )
        self.check_entry.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))
        self._button(line, "Show / hide", self.toggle_check_visibility, "#375477").pack(side="left", padx=4)
        self._button(line, "Analyze", self.analyze_entered, ACCENT).pack(side="left", padx=(4, 0))

        self.check_result = tk.Label(
            card, text="Your result will appear here.",
            bg=PANEL, fg=TEXT, font=("Segoe UI", 13, "bold")
        )
        self.check_result.pack(anchor="w", padx=16, pady=(18, 8))
        self.check_details = tk.Label(
            card, text="", bg=PANEL, fg=MUTED,
            justify="left", font=("Segoe UI", 10)
        )
        self.check_details.pack(anchor="w", padx=16, pady=(0, 16))

        tip = self._card(outer, "Quick security tips")
        tip.pack(fill="x", pady=14)
        tips = (
            "• Use long, unique passwords for each account.\n"
            "• Consider a reputable password manager.\n"
            "• Never share passwords or store them in unprotected files.\n"
            "• This checker is educational and cannot guarantee security."
        )
        tk.Label(tip, text=tips, bg=PANEL, fg=MUTED, justify="left",
                 font=("Segoe UI", 10), padx=16, pady=12).pack(anchor="w")

    def _build_history_tab(self):
        outer = tk.Frame(self.history_tab, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=24)
        card = self._card(outer, "Recent generated passwords")
        card.pack(fill="both", expand=True)
        tk.Label(
            card,
            text="History is kept only while this app is open. It is not saved automatically.",
            bg=PANEL, fg=MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w", padx=16, pady=(0, 12))
        columns = ("time", "password", "strength")
        self.history_tree = ttk.Treeview(card, columns=columns, show="headings")
        self.history_tree.heading("time", text="Time")
        self.history_tree.heading("password", text="Password")
        self.history_tree.heading("strength", text="Strength")
        self.history_tree.column("time", width=170, anchor="w")
        self.history_tree.column("password", width=460, anchor="w")
        self.history_tree.column("strength", width=120, anchor="center")
        self.history_tree.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        buttons = tk.Frame(card, bg=PANEL)
        buttons.pack(fill="x", padx=12, pady=(0, 12))
        self._button(buttons, "Copy selected", self.copy_history_selected).pack(side="left", padx=(0, 8))
        self._button(buttons, "Clear history", self.clear_history, "#8A3548").pack(side="left")

    def _build_about_tab(self):
        outer = tk.Frame(self.about_tab, bg=BG)
        outer.pack(fill="both", expand=True, padx=24, pady=24)
        card = self._card(outer, "About SecurePass")
        card.pack(fill="x", anchor="n")
        content = (
            "SecurePass is a student experiential-learning project built with Python and Tkinter.\n\n"
            "Main concepts demonstrated:\n"
            "• Object-oriented programming and classes\n"
            "• Secure random generation using the secrets module\n"
            "• Input validation and exception handling\n"
            "• GUI design, event handling, and clipboard operations\n"
            "• File handling and password-strength estimation\n\n"
            "Privacy note: passwords are displayed in the application and only written to a file "
            "when you explicitly choose Save. Saved files contain plain text, so protect them.\n\n"
            "Version 1.0"
        )
        tk.Label(
            card, text=content, bg=PANEL, fg=MUTED,
            justify="left", anchor="w", wraplength=820,
            font=("Segoe UI", 11), padx=18, pady=18
        ).pack(fill="x")

    def generate_custom(self):
        try:
            length = int(self.length_var.get())
            count = int(self.count_var.get())
            if length < 4 or length > 128:
                raise ValueError("Length must be between 4 and 128.")
            if count < 1 or count > 50:
                raise ValueError("Generate between 1 and 50 passwords.")

            generator = PasswordGenerator(
                length=length,
                use_upper=self.upper_var.get(),
                use_lower=self.lower_var.get(),
                use_digits=self.digits_var.get(),
                use_symbols=self.symbols_var.get(),
                exclude_ambiguous=self.ambiguous_var.get(),
            )
            passwords = [generator.generate() for _ in range(count)]
            self._show_passwords(passwords)

        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Check your settings", str(error))

    def generate_preset(self, level):
        settings = {
            "easy": dict(length=8, use_upper=False, use_lower=True,
                         use_digits=True, use_symbols=False),
            "moderate": dict(length=12, use_upper=True, use_lower=True,
                             use_digits=True, use_symbols=False),
            "strong": dict(length=16, use_upper=True, use_lower=True,
                           use_digits=True, use_symbols=True),
        }
        count = self.count_var.get()
        try:
            count = int(count)
            if count < 1 or count > 50:
                raise ValueError("Generate between 1 and 50 passwords.")
            generator = PasswordGenerator(**settings[level])
            passwords = [generator.generate() for _ in range(count)]
            self._show_passwords(passwords)
        except (ValueError, tk.TclError) as error:
            messagebox.showerror("Check your settings", str(error))

    def _show_passwords(self, passwords):
        self.generated_passwords = passwords
        self.password_list.delete(0, tk.END)
        for password in passwords:
            rating, _ = PasswordGenerator.analyze(password)
            self.password_list.insert(tk.END, f"{password}     | {rating}")
            self.saved_history.insert(
                0, (datetime.now().strftime("%H:%M:%S"), password, rating)
            )
        self._refresh_history()
        if passwords:
            self.password_list.selection_set(0)
            self.on_password_select()
        self.notebook.select(self.generate_tab)

    def on_password_select(self, _event=None):
        selection = self.password_list.curselection()
        if not selection:
            return
        password = self.generated_passwords[selection[0]]
        rating, _ = PasswordGenerator.analyze(password)
        color = "#6EE7B7" if rating == "Strong" else "#FBBF24" if rating == "Moderate" else RED
        self.strength_label.configure(text=f"Estimated strength: {rating}", fg=color)

    def copy_selected(self):
        selection = self.password_list.curselection()
        if not selection:
            messagebox.showinfo("Select a password", "Choose a generated password first.")
            return
        password = self.generated_passwords[selection[0]]
        self._copy_text(password, "Selected password copied.")

    def copy_all(self):
        if not self.generated_passwords:
            messagebox.showinfo("No passwords", "Generate passwords first.")
            return
        self._copy_text("\n".join(self.generated_passwords), "All generated passwords copied.")

    def _copy_text(self, text, success_message):
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        messagebox.showinfo("Copied", success_message)

    def save_to_file(self):
        if not self.generated_passwords:
            messagebox.showinfo("No passwords", "Generate passwords before saving.")
            return

        filename = filedialog.asksaveasfilename(
            title="Save generated passwords",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="generated_passwords.txt",
        )
        if not filename:
            return

        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"SecurePass export — {datetime.now():%Y-%m-%d %H:%M:%S}\n")
                file.write("Keep this file private. Passwords are stored as plain text.\n\n")
                for index, password in enumerate(self.generated_passwords, start=1):
                    rating, _ = PasswordGenerator.analyze(password)
                    file.write(f"{index}. {password} [{rating}]\n")
            messagebox.showinfo("Saved", "Passwords saved successfully.")
        except OSError as error:
            messagebox.showerror("Save failed", str(error))

    def toggle_check_visibility(self):
        self.check_entry.configure(show="" if self.check_entry.cget("show") else "•")

    def analyze_entered(self):
        password = self.check_var.get()
        if not password:
            messagebox.showwarning("Enter a password", "Type a password to analyze.")
            return
        rating, checks = PasswordGenerator.analyze(password)
        color = "#6EE7B7" if rating == "Strong" else "#FBBF24" if rating == "Moderate" else RED
        self.check_result.configure(
            text=f"Estimated result: {rating}  •  Length: {len(password)} characters",
            fg=color,
        )
        details = "\n".join(
            f"{'✓' if passed else '○'}  {label}" for label, passed in checks.items()
        )
        self.check_details.configure(text=details)

    def _refresh_history(self):
        if not hasattr(self, "history_tree"):
            return
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        for item in self.saved_history[:200]:
            self.history_tree.insert("", tk.END, values=item)

    def copy_history_selected(self):
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showinfo("Select an item", "Choose a history row first.")
            return
        values = self.history_tree.item(selection[0], "values")
        if values:
            self._copy_text(values[1], "Password copied from history.")

    def clear_history(self):
        if not self.saved_history:
            return
        if messagebox.askyesno("Clear history", "Clear the in-memory password history?"):
            self.saved_history.clear()
            self._refresh_history()


if __name__ == "__main__":
    app = SecurePassApp()
    app.mainloop()
