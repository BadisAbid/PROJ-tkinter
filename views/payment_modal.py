import customtkinter as ctk
from tkinter import messagebox
import random

class PaymentModal(ctk.CTkToplevel):
    """
    A pop-up modal for processing a simulated 'Sandbox' payment.
    Displays an invoice (facture) on the left, and a simulated
    Visa card generator on the right.
    """
    
    BG     = "#0d0d1a"
    CARD   = "#1a1a2e"
    BORDER = "#3a3a6e"
    TEXT   = "#ccccdd"
    MUTED  = "#888899"
    ACCENT = "#28a745"

    def __init__(self, parent, cart_items, total_price, on_success):
        super().__init__(parent)
        self.cart_items = cart_items
        self.total_price = total_price
        self.on_success = on_success
        
        self.title("Checkout - Sandbox Payment")
        self.geometry("750x500")
        self.resizable(False, False)
        self.configure(fg_color=self.BG)
        
        # Make it a modal window that traps focus
        self.transient(parent)
        self.grab_set()

        # Simulated state
        self.has_card = False
        self.card_balance = 0.0

        # Create Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Invoice side
        self.grid_columnconfigure(1, weight=1) # Payment side
        
        self._build_invoice_side()
        self._build_payment_side()

    def _build_invoice_side(self):
        frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=16, border_width=1, border_color=self.BORDER)
        frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        frame.grid_propagate(False)

        ctk.CTkLabel(
            frame, text="🧾  Invoice Summary", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=self.TEXT
        ).pack(pady=(20, 10))

        # Divider
        ctk.CTkFrame(frame, height=1, fg_color=self.BORDER).pack(fill="x", padx=15, pady=(0, 15))

        # Items Scroll
        scroll = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)

        for _pid, item in self.cart_items.items():
            row = ctk.CTkFrame(scroll, fg_color="transparent")
            row.pack(fill="x", pady=4)
            name = item['name']
            if len(name) > 15: name = name[:13] + ".."
            subtotal = item['price'] * item['qty']
            
            ctk.CTkLabel(row, text=f"{item['qty']}x {name}", font=ctk.CTkFont(size=13), text_color=self.TEXT).pack(side="left")
            ctk.CTkLabel(row, text=f"${subtotal:.2f}", font=ctk.CTkFont(size=13), text_color=self.MUTED).pack(side="right")

        # Total footer
        ctk.CTkFrame(frame, height=1, fg_color=self.BORDER).pack(fill="x", padx=15, pady=(10, 10))
        total_lbl = ctk.CTkLabel(
            frame, text=f"Total: ${self.total_price:.2f}", 
            font=ctk.CTkFont(size=20, weight="bold"), text_color=self.ACCENT
        )
        total_lbl.pack(pady=(0, 20))


    def _build_payment_side(self):
        frame = ctk.CTkFrame(self, fg_color=self.CARD, corner_radius=16, border_width=1, border_color=self.BORDER)
        frame.grid(row=0, column=1, sticky="nsew", padx=(0,15), pady=15)
        
        ctk.CTkLabel(
            frame, text="💳  Sandbox Payment Area", 
            font=ctk.CTkFont(size=18, weight="bold"), text_color=self.TEXT
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            frame, text="Generate a mock Visa to test the checkout.", 
            font=ctk.CTkFont(size=12), text_color=self.MUTED
        ).pack(pady=(0, 15))

        # Visual Card Area
        self.visacard = ctk.CTkFrame(frame, fg_color="#1f2937", corner_radius=12, border_width=2, border_color="#374151")
        self.visacard.pack(fill="x", padx=20, pady=10)

        self.card_num_lbl = ctk.CTkLabel(self.visacard, text="**** **** **** ****", font=ctk.CTkFont(size=18, weight="bold", family="Courier"), text_color=self.MUTED)
        self.card_num_lbl.pack(pady=(20, 5))
        
        self.card_bal_lbl = ctk.CTkLabel(self.visacard, text="Balance: $0.00", font=ctk.CTkFont(size=14, weight="bold"), text_color=self.MUTED)
        self.card_bal_lbl.pack(pady=(5, 20))

        # Generate Button
        self.gen_btn = ctk.CTkButton(
            frame, text="🎲  Generate Sandbox Visa", 
            height=42, corner_radius=10, 
            fg_color="#007acc", hover_color="#005999",
            command=self._generate_card
        )
        self.gen_btn.pack(fill="x", padx=20, pady=(20, 10))

        # Pay Button
        self.pay_btn = ctk.CTkButton(
            frame, text="✅  Pay & Complete Order", 
            height=46, corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=self.ACCENT, hover_color="#1e7e34",
            state="disabled",
            command=self._process_payment
        )
        self.pay_btn.pack(fill="x", padx=20, pady=(10, 0))


    def _generate_card(self):
        """Simulates creating a test Visa card with a random sufficient balance"""
        # Card number format: 4xxx xxxx xxxx xxxx
        nums = [f"{random.randint(1000, 9999)}" for _ in range(3)]
        card_num = f"4000 {' '.join(nums)}"
        
        # Simulate a random balance that is slightly higher or lower than the total price
        # Giving 80% chance of sufficient funds for demonstration
        if random.random() < 0.8:
            self.card_balance = self.total_price + random.uniform(10, 100)
        else:
            self.card_balance = self.total_price - random.uniform(5, 10)
            if self.card_balance < 0:
                self.card_balance = 0.0

        # Update visuals
        self.card_num_lbl.configure(text=card_num, text_color="#facc15") # Gold color
        self.card_bal_lbl.configure(text=f"Balance: ${self.card_balance:.2f}", text_color="#ffffff")
        self.visacard.configure(border_color="#facc15")

        self.has_card = True
        self.pay_btn.configure(state="normal")
        
        if self.card_balance >= self.total_price:
            messagebox.showinfo("Card Created", f"Sandbox Visa generated with sufficient funds: ${self.card_balance:.2f}.", parent=self)
        else:
            messagebox.showwarning("Low Balance", f"Sandbox Visa generated, but balance (${self.card_balance:.2f}) is too low!", parent=self)


    def _process_payment(self):
        if not self.has_card:
            return

        if self.card_balance < self.total_price:
            messagebox.showerror("Sandbox Payment Declined", "Insufficient funds on your sandbox card. \nPlease generate a new one.", parent=self)
            self.pay_btn.configure(state="disabled")
            return

        # Success path!
        messagebox.showinfo("Sandbox Payment Successful", "Payment processed successfully!\nCompleting your order.", parent=self)
        self.destroy() # Close the modal
        self.on_success() # Trigger the main _checkout_success method back in client_page
