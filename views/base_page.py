
import customtkinter as ctk
from tkinter import ttk, messagebox
import csv
from tkinter import filedialog

# =============================================
#  BASE PAGE
#  Every admin page (Categories, Products…)
#  inherits from this class.
#  It provides:
#   • A page title header
#   • A styled Treeview (data table)
#   • Helper methods for sorting columns
# =============================================

class BasePage(ctk.CTkFrame):

    # Color palette used across all pages
    BG       = "#0d0d1a"   # Main background
    CARD     = "#1a1a2e"   # Card / panel color
    BORDER   = "#3a3a6e"   # Border color
    ACCENT   = "#7c83fd"   # Highlight / accent purple-blue
    TEXT     = "#ccccdd"   # Normal text
    MUTED    = "#888899"   # Gray / muted text

    def __init__(self, parent, controller, title):
        super().__init__(parent, fg_color=self.BG)
        self.controller = controller  # MainController instance

        # --- PAGE TITLE HEADER ---
        header = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=0, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.ACCENT,
        ).pack(side="left", padx=25, pady=15)

    # --------------------------------------------------
    def setup_treeview(self, columns):
        """
        Create a styled data table (Treeview).
        Call this from child pages after the buttons.
        `columns` is a tuple of column header names, e.g. ("ID", "Name", "Price")
        """
        # Container frame for the table
        self.tree_frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=12)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        # --- DARK THEME FOR TREEVIEW ---
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Custom.Treeview",
            background="#1a1a2e",
            foreground="#ccccdd",
            fieldbackground="#1a1a2e",
            rowheight=34,
            font=("Segoe UI", 12),
            borderwidth=0,
        )
        style.configure(
            "Custom.Treeview.Heading",
            background="#252545",
            foreground="#7c83fd",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
        )
        style.map(
            "Custom.Treeview",
            background=[("selected", "#3a3a6e")],
            foreground=[("selected", "#ffffff")],
        )

        # --- TREEVIEW WIDGET ---
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
        )

        # Set up each column heading (click to sort)
        for col in columns:
            self.tree.heading(
                col,
                text=col,
                command=lambda _c=col: self._sort_column(_c, False),
            )
            self.tree.column(col, width=130, anchor="center")

        # Scrollbar
        sb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        sb.pack(side="right", fill="y", padx=(0, 5), pady=10)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Alternating row colors
        self.tree.tag_configure("odd",  background="#1e1e38")
        self.tree.tag_configure("even", background="#1a1a2e")

    # --------------------------------------------------
    def insert_row(self, values):
        """Insert a row with alternating color tags."""
        count = len(self.tree.get_children())
        tag = "odd" if count % 2 == 0 else "even"
        self.tree.insert("", "end", values=values, tags=(tag,))

    # --------------------------------------------------
    def _sort_column(self, col, reverse):
        """Sort the treeview table when a column header is clicked."""
        data = [(self.tree.set(k, col), k) for k in self.tree.get_children("")]
        data.sort(reverse=reverse)
        for index, (_, k) in enumerate(data):
            self.tree.move(k, "", index)
        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))

    # --------------------------------------------------
    def export_to_csv(self, rows, filename_hint="export"):
        """
        Open a Save-file dialog and write `rows` (list of dicts) to CSV.
        Call this from child pages.
        """
        if not rows:
            messagebox.showwarning("No Data", "There is nothing to export.", parent=self.winfo_toplevel())
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialfile=filename_hint,
        )
        if path:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            messagebox.showinfo("Exported!", f"File saved to:\n{path}", parent=self.winfo_toplevel())
