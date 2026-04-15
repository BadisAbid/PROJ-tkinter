import customtkinter as ctk
from tkinter import messagebox

class CounterPage(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.counter_value = 0

        # Configure main frame
        self.configure(fg_color="#0a0a0a")

        # Create main container with gradient-like effect
        self.main_container = ctk.CTkFrame(
            self,
            fg_color="#1a1a1a",
            border_width=2,
            border_color="#2a2a2a",
            corner_radius=20,
            width=450,
            height=550
        )
        self.main_container.place(relx=0.5, rely=0.5, anchor="center")

        # Welcome section
        self.create_header_section()

        # Counter display
        self.create_counter_display()

        # Control buttons
        self.create_control_buttons()

        # Footer
        self.create_footer()

    def create_header_section(self):
        """Create the header section"""
        # Header frame
        self.header_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.header_frame.pack(pady=(40, 20))

        # Counter icon
        self.icon_label = ctk.CTkLabel(
            self.header_frame,
            text="🔢",
            font=ctk.CTkFont(size=48)
        )
        self.icon_label.pack()

        # Main title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Smart Counter",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.pack(pady=(10, 5))

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Count with style and precision",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.subtitle_label.pack()

    def create_counter_display(self):
        """Create the counter display section"""
        # Display container
        self.display_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.display_frame.pack(pady=(20, 30), padx=40)

        # Counter value display
        self.counter_display = ctk.CTkLabel(
            self.display_frame,
            text=str(self.counter_value),
            font=ctk.CTkFont(size=72, weight="bold"),
            text_color="#007acc"
        )
        self.counter_display.pack(pady=(20, 10))

        # Counter label
        self.counter_label = ctk.CTkLabel(
            self.display_frame,
            text="Current Count",
            font=ctk.CTkFont(size=16),
            text_color="#a0a0a0"
        )
        self.counter_label.pack()

    def create_control_buttons(self):
        """Create the control buttons section"""
        # Buttons container
        self.buttons_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.buttons_frame.pack(pady=(20, 30), padx=40)

        # Buttons row
        self.buttons_row = ctk.CTkFrame(
            self.buttons_frame,
            fg_color="transparent"
        )
        self.buttons_row.pack()

        # Decrement button
        self.decrement_btn = ctk.CTkButton(
            self.buttons_row,
            text="➖",
            command=self.decrement,
            font=ctk.CTkFont(size=24, weight="bold"),
            width=80,
            height=80,
            corner_radius=15,
            fg_color="#dc3545",
            hover_color="#c82333"
        )
        self.decrement_btn.pack(side="left", padx=(0, 20))

        # Reset button
        self.reset_btn = ctk.CTkButton(
            self.buttons_row,
            text="🔄",
            command=self.reset,
            font=ctk.CTkFont(size=20, weight="bold"),
            width=80,
            height=80,
            corner_radius=15,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.reset_btn.pack(side="left", padx=(0, 20))

        # Increment button
        self.increment_btn = ctk.CTkButton(
            self.buttons_row,
            text="➕",
            command=self.increment,
            font=ctk.CTkFont(size=24, weight="bold"),
            width=80,
            height=80,
            corner_radius=15,
            fg_color="#28a745",
            hover_color="#218838"
        )
        self.increment_btn.pack(side="left")

        # Step control
        self.step_frame = ctk.CTkFrame(
            self.buttons_frame,
            fg_color="transparent"
        )
        self.step_frame.pack(pady=(30, 0))

        self.step_label = ctk.CTkLabel(
            self.step_frame,
            text="Step Size:",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.step_label.pack(side="left", padx=(0, 10))

        self.step_var = ctk.StringVar(value="1")
        self.step_entry = ctk.CTkEntry(
            self.step_frame,
            textvariable=self.step_var,
            width=60,
            height=35,
            font=ctk.CTkFont(size=14)
        )
        self.step_entry.pack(side="left")

    def create_footer(self):
        """Create the footer section"""
        self.footer_frame = ctk.CTkFrame(
            self.main_container,
            fg_color="transparent"
        )
        self.footer_frame.pack(pady=(20, 40))

        # Separator line
        self.separator = ctk.CTkFrame(
            self.footer_frame,
            height=1,
            fg_color="#404040"
        )
        self.separator.pack(fill="x", pady=(0, 20))

        # Statistics
        self.stats_label = ctk.CTkLabel(
            self.footer_frame,
            text=f"Operations: 0 | Min: 0 | Max: 0",
            font=ctk.CTkFont(size=12),
            text_color="#808080"
        )
        self.stats_label.pack()

        # Initialize stats
        self.operations_count = 0
        self.min_value = 0
        self.max_value = 0
        self.update_stats()

    def increment(self):
        """Increment the counter"""
        try:
            step = int(self.step_var.get())
            self.counter_value += step
            self.update_display()
            self.operations_count += 1
            self.update_stats()
        except ValueError:
            messagebox.showerror(
                "Invalid Step",
                "Please enter a valid integer for step size",
                parent=self.winfo_toplevel()
            )

    def decrement(self):
        """Decrement the counter"""
        try:
            step = int(self.step_var.get())
            self.counter_value -= step
            self.update_display()
            self.operations_count += 1
            self.update_stats()
        except ValueError:
            messagebox.showerror(
                "Invalid Step",
                "Please enter a valid integer for step size",
                parent=self.winfo_toplevel()
            )

    def reset(self):
        """Reset the counter to zero"""
        self.counter_value = 0
        self.update_display()
        self.operations_count += 1
        self.update_stats()

    def update_display(self):
        """Update the counter display"""
        self.counter_display.configure(text=str(self.counter_value))

        # Change color based on value
        if self.counter_value > 0:
            self.counter_display.configure(text_color="#28a745")  # Green
        elif self.counter_value < 0:
            self.counter_display.configure(text_color="#dc3545")  # Red
        else:
            self.counter_display.configure(text_color="#007acc")  # Blue

    def update_stats(self):
        """Update the statistics display"""
        if self.counter_value < self.min_value:
            self.min_value = self.counter_value
        if self.counter_value > self.max_value:
            self.max_value = self.counter_value

        self.stats_label.configure(
            text=f"Operations: {self.operations_count} | Min: {self.min_value} | Max: {self.max_value}"
        )