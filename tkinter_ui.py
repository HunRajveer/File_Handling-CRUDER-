import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path


# ─── Core CRUD Logic ────────────────────────────────────────────────────────

def get_all_items():
    p = Path("")
    return list(p.rglob("*"))

def read_file(file_name):
    p = Path(file_name)
    if p.exists():
        with open(file_name, "r") as f:
            return f.read()
    return None

def create_file(file_name, content):
    p = Path(file_name)
    if p.exists():
        return False, "File already exists."
    with open(file_name, "w") as f:
        f.write(content)
    return True, "File created successfully."

def update_file(file_name, content, mode="w"):
    p = Path(file_name)
    if not p.exists():
        return False, "File does not exist."
    with open(file_name, mode) as f:
        f.write("\n" + content)
    return True, "File updated successfully."

def delete_file(file_name):
    p = Path(file_name)
    if not p.exists():
        return False, "File does not exist."
    os.remove(p)
    return True, "File deleted successfully."

def rename_file(file_name, new_name):
    p = Path(file_name)
    if not p.exists():
        return False, "File does not exist."
    p.rename(new_name)
    return True, "File renamed successfully."

def create_folder(folder_name):
    p = Path(folder_name)
    if p.exists():
        return False, "Folder already exists."
    p.mkdir()
    return True, "Folder created successfully."

def remove_folder(folder_name):
    p = Path(folder_name)
    if not p.exists():
        return False, "Folder does not exist."
    p.rmdir()
    return True, "Folder removed successfully."


# ─── Tkinter App ─────────────────────────────────────────────────────────────

class CRUDApp(tk.Tk):
    # Colour palette
    BG        = "#1e1e2e"
    PANEL     = "#2a2a3e"
    ACCENT    = "#7c6af7"
    ACCENT2   = "#56cfb2"
    TEXT      = "#cdd6f4"
    MUTED     = "#6c7086"
    SUCCESS   = "#a6e3a1"
    ERROR     = "#f38ba8"
    ENTRY_BG  = "#313244"
    BTN_FG    = "#ffffff"

    def __init__(self):
        super().__init__()
        self.title("File Manager — CRUD")
        self.geometry("1000x680")
        self.resizable(True, True)
        self.configure(bg=self.BG)
        self._build_ui()
        self.refresh_tree()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        # ── Top bar ────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=self.BG, pady=14)
        top.pack(fill="x", padx=20)
        tk.Label(top, text="📁  File Manager", font=("Courier", 22, "bold"),
                 bg=self.BG, fg=self.ACCENT).pack(side="left")
        tk.Label(top, text="CRUD Operations", font=("Courier", 11),
                 bg=self.BG, fg=self.MUTED).pack(side="left", padx=12, pady=6)

        # ── Main panes ─────────────────────────────────────────────────────
        main = tk.Frame(self, bg=self.BG)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self._build_left(main)
        self._build_right(main)

        # ── Status bar ─────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready.")
        status = tk.Label(self, textvariable=self.status_var,
                          bg=self.PANEL, fg=self.MUTED,
                          font=("Courier", 10), anchor="w", padx=10, pady=4)
        status.pack(fill="x", side="bottom")

    def _build_left(self, parent):
        left = tk.Frame(parent, bg=self.PANEL, bd=0,
                        highlightthickness=1, highlightbackground=self.ACCENT)
        left.pack(side="left", fill="y", padx=(0, 12), pady=4, ipadx=6, ipady=6)

        tk.Label(left, text="Explorer", font=("Courier", 13, "bold"),
                 bg=self.PANEL, fg=self.ACCENT2).pack(pady=(10, 4))

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                        background=self.ENTRY_BG, foreground=self.TEXT,
                        fieldbackground=self.ENTRY_BG, rowheight=24,
                        font=("Courier", 10))
        style.configure("Custom.Treeview.Heading",
                        background=self.PANEL, foreground=self.ACCENT,
                        font=("Courier", 10, "bold"))
        style.map("Custom.Treeview",
                  background=[("selected", self.ACCENT)],
                  foreground=[("selected", "#ffffff")])

        frame = tk.Frame(left, bg=self.PANEL)
        frame.pack(fill="both", expand=True, padx=8)

        self.tree = ttk.Treeview(frame, columns=("name", "type"),
                                  show="headings", style="Custom.Treeview")
        self.tree.heading("name", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.column("name", width=200)
        self.tree.column("type", width=60, anchor="center")

        sb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        btn = self._btn(left, "🔄  Refresh", self.refresh_tree, self.ACCENT)
        btn.pack(pady=8, padx=10, fill="x")

    def _build_right(self, parent):
        right = tk.Frame(parent, bg=self.BG)
        right.pack(side="left", fill="both", expand=True, pady=4)

        # ── Notebook tabs ──────────────────────────────────────────────────
        style = ttk.Style()
        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=self.PANEL, foreground=self.MUTED,
                        font=("Courier", 10, "bold"), padding=[12, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", self.ACCENT)],
                  foreground=[("selected", "#ffffff")])

        nb = ttk.Notebook(right)
        nb.pack(fill="both", expand=True)

        self._build_tab_create(nb)
        self._build_tab_read(nb)
        self._build_tab_update(nb)
        self._build_tab_delete(nb)
        self._build_tab_rename(nb)
        self._build_tab_folder(nb)

    # ── Tabs ────────────────────────────────────────────────────────────────

    def _build_tab_create(self, nb):
        tab = self._tab(nb, "➕ Create")
        self._label(tab, "Create a New File")
        self.create_name = self._entry(tab, "File name (e.g. notes.txt)")
        self._label(tab, "Content", small=True)
        self.create_content = self._text_area(tab)
        self._btn(tab, "Create File", self._do_create, self.SUCCESS).pack(pady=10, fill="x")

    def _build_tab_read(self, nb):
        tab = self._tab(nb, "📖 Read")
        self._label(tab, "Read a File")
        self.read_name = self._entry(tab, "File name")
        self._btn(tab, "Read File", self._do_read, self.ACCENT2).pack(pady=6, fill="x")
        self._label(tab, "Content", small=True)
        self.read_output = self._text_area(tab, readonly=True)

    def _build_tab_update(self, nb):
        tab = self._tab(nb, "✏️ Update")
        self._label(tab, "Update a File")
        self.update_name = self._entry(tab, "File name")
        self._btn(tab, "Load File", self._do_load_update, self.ACCENT).pack(pady=4, fill="x")
        self._label(tab, "New Content", small=True)
        self.update_content = self._text_area(tab)
        mode_frame = tk.Frame(tab, bg=self.PANEL)
        mode_frame.pack(fill="x", pady=4)
        self.update_mode = tk.StringVar(value="w")
        tk.Radiobutton(mode_frame, text="Overwrite", variable=self.update_mode,
                       value="w", bg=self.PANEL, fg=self.TEXT,
                       selectcolor=self.ACCENT, activebackground=self.PANEL,
                       font=("Courier", 10)).pack(side="left", padx=8)
        tk.Radiobutton(mode_frame, text="Append", variable=self.update_mode,
                       value="a", bg=self.PANEL, fg=self.TEXT,
                       selectcolor=self.ACCENT, activebackground=self.PANEL,
                       font=("Courier", 10)).pack(side="left")
        self._btn(tab, "Update File", self._do_update, self.ACCENT2).pack(pady=8, fill="x")

    def _build_tab_delete(self, nb):
        tab = self._tab(nb, "🗑️ Delete")
        self._label(tab, "Delete a File")
        self.delete_name = self._entry(tab, "File name")
        self._btn(tab, "Delete File", self._do_delete, self.ERROR).pack(pady=10, fill="x")

    def _build_tab_rename(self, nb):
        tab = self._tab(nb, "🔤 Rename")
        self._label(tab, "Rename a File")
        self.rename_old = self._entry(tab, "Current file name")
        self.rename_new = self._entry(tab, "New file name")
        self._btn(tab, "Rename File", self._do_rename, self.ACCENT2).pack(pady=10, fill="x")

    def _build_tab_folder(self, nb):
        tab = self._tab(nb, "📂 Folder")
        self._label(tab, "Folder Operations")
        self.folder_name = self._entry(tab, "Folder name")
        row = tk.Frame(tab, bg=self.PANEL)
        row.pack(fill="x", pady=6)
        self._btn(row, "Create Folder", self._do_create_folder, self.SUCCESS).pack(side="left", expand=True, fill="x", padx=(0, 4))
        self._btn(row, "Remove Folder", self._do_remove_folder, self.ERROR).pack(side="left", expand=True, fill="x")

    # ── CRUD Handlers ───────────────────────────────────────────────────────

    def _do_create(self):
        name = self.create_name.get().strip()
        content = self.create_content.get("1.0", "end-1c")
        if not name:
            return self._status("Please enter a file name.", error=True)
        ok, msg = create_file(name, content)
        self._status(msg, error=not ok)
        if ok:
            self.refresh_tree()

    def _do_read(self):
        name = self.read_name.get().strip()
        if not name:
            return self._status("Please enter a file name.", error=True)
        content = read_file(name)
        self.read_output.config(state="normal")
        self.read_output.delete("1.0", "end")
        if content is not None:
            self.read_output.insert("1.0", content)
            self._status(f"Loaded: {name}")
        else:
            self.read_output.insert("1.0", "⚠  File not found.")
            self._status("File not found.", error=True)
        self.read_output.config(state="disabled")

    def _do_load_update(self):
        name = self.update_name.get().strip()
        content = read_file(name)
        self.update_content.delete("1.0", "end")
        if content is not None:
            self.update_content.insert("1.0", content)
            self._status(f"Loaded: {name}")
        else:
            self._status("File not found.", error=True)

    def _do_update(self):
        name = self.update_name.get().strip()
        content = self.update_content.get("1.0", "end-1c")
        mode = self.update_mode.get()
        if not name:
            return self._status("Please enter a file name.", error=True)
        ok, msg = update_file(name, content, mode)
        self._status(msg, error=not ok)

    def _do_delete(self):
        name = self.delete_name.get().strip()
        if not name:
            return self._status("Please enter a file name.", error=True)
        if not messagebox.askyesno("Confirm Delete", f"Delete '{name}'?"):
            return
        ok, msg = delete_file(name)
        self._status(msg, error=not ok)
        if ok:
            self.refresh_tree()

    def _do_rename(self):
        old = self.rename_old.get().strip()
        new = self.rename_new.get().strip()
        if not old or not new:
            return self._status("Please fill both fields.", error=True)
        ok, msg = rename_file(old, new)
        self._status(msg, error=not ok)
        if ok:
            self.refresh_tree()

    def _do_create_folder(self):
        name = self.folder_name.get().strip()
        if not name:
            return self._status("Please enter a folder name.", error=True)
        ok, msg = create_folder(name)
        self._status(msg, error=not ok)
        if ok:
            self.refresh_tree()

    def _do_remove_folder(self):
        name = self.folder_name.get().strip()
        if not name:
            return self._status("Please enter a folder name.", error=True)
        if not messagebox.askyesno("Confirm Remove", f"Remove folder '{name}'?"):
            return
        ok, msg = remove_folder(name)
        self._status(msg, error=not ok)
        if ok:
            self.refresh_tree()

    # ── Tree ────────────────────────────────────────────────────────────────

    def refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        items = get_all_items()
        for item in items:
            kind = "DIR" if item.is_dir() else "FILE"
            self.tree.insert("", "end", values=(str(item), kind))
        self._status(f"Explorer refreshed — {len(items)} items.")

    def _on_select(self, _event):
        sel = self.tree.selection()
        if not sel:
            return
        name = self.tree.item(sel[0])["values"][0]
        # Auto-fill the visible entry fields
        for attr in ("create_name", "read_name", "update_name",
                     "delete_name", "rename_old", "folder_name"):
            widget = getattr(self, attr, None)
            if widget:
                widget.delete(0, "end")
                widget.insert(0, name)

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _tab(self, nb, title):
        frame = tk.Frame(nb, bg=self.PANEL, padx=20, pady=16)
        nb.add(frame, text=title)
        return frame

    def _label(self, parent, text, small=False):
        size = 10 if small else 13
        weight = "normal" if small else "bold"
        fg = self.MUTED if small else self.ACCENT
        tk.Label(parent, text=text, bg=self.PANEL, fg=fg,
                 font=("Courier", size, weight)).pack(anchor="w", pady=(8, 2))

    def _entry(self, parent, placeholder=""):
        e = tk.Entry(parent, bg=self.ENTRY_BG, fg=self.TEXT,
                     insertbackground=self.TEXT, relief="flat",
                     font=("Courier", 11), bd=0)
        e.pack(fill="x", pady=3, ipady=7)
        e.insert(0, placeholder)
        e.bind("<FocusIn>",  lambda ev, w=e, p=placeholder: w.delete(0, "end") if w.get() == p else None)
        e.bind("<FocusOut>", lambda ev, w=e, p=placeholder: w.insert(0, p) if not w.get() else None)
        return e

    def _text_area(self, parent, readonly=False):
        t = scrolledtext.ScrolledText(parent, bg=self.ENTRY_BG, fg=self.TEXT,
                                      insertbackground=self.TEXT,
                                      font=("Courier", 10), height=8,
                                      relief="flat", bd=0,
                                      state="disabled" if readonly else "normal")
        t.pack(fill="both", expand=True, pady=4)
        return t

    def _btn(self, parent, text, command, color):
        return tk.Button(parent, text=text, command=command,
                         bg=color, fg=self.BTN_FG,
                         font=("Courier", 11, "bold"),
                         relief="flat", bd=0, cursor="hand2",
                         activebackground=self.ACCENT,
                         activeforeground="#ffffff",
                         padx=10, pady=8)

    def _status(self, msg, error=False):
        self.status_var.set(("❌  " if error else "✅  ") + msg)


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = CRUDApp()
    app.mainloop()