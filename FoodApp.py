import tkinter as tk
from tkinter import messagebox

# Menu data
menus = {
    "Beverages": {"Mango Lassi": 60, "Masala Chai": 30, "Cold Coffee": 80, "Fresh Lime": 50, "Buttermilk": 40},
    "Appetizers": {"Samosa (2 pcs)": 40, "Bhaji Plate": 50, "Paneer Chilli": 120, "Chicken Wings": 150, "Chaat Special": 80},
    "Main Dishes": {"Paneer Butter Masala": 220, "Dal Tadka": 150, "Veg Biryani": 200, "Butter Naan": 40, "Steam Rice": 150, "Jeera Rice": 180}
}

quantities, customer_info = {}, {}

def update_cart():
    total = sum(quantities.get(dish, tk.IntVar()).get() * price for category in menus for dish, price in menus[category].items())
    cart_total.set(f"₹{total}")

def btn(parent, text, command, bg="#3498db", fg="white", **kwargs):
    return tk.Button(parent, text=text, command=command, bg=bg, fg=fg, font=("Segoe UI", 11, "bold"), relief="raised", bd=2, pady=10, cursor="hand2", **kwargs)

def get_customer_info():
    if not any(quantities.get(dish, tk.IntVar()).get() > 0 for category in menus for dish in menus[category]):
        return messagebox.showwarning("Empty Cart", "Please add items first!")
    
    win = tk.Toplevel(root)
    win.title("Customer Details")
    win.geometry("360x465")
    win.config(bg="white")
    win.resizable(True, True)
    
    tk.Label(win, text="Customer Information", font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50", pady=20).pack()
    frame = tk.Frame(win, bg="white")
    frame.pack(pady=10, padx=40, fill="both", expand=True)
    
    entries = {}
    for i, (label, key) in enumerate([("Name:", "name"), ("Phone:", "phone"), ("Table No:", "table")]):
        tk.Label(frame, text=label, font=("Segoe UI", 12), bg="white", fg="#34495e").grid(row=i*2, column=0, sticky="w", pady=(15,5))
        entries[key] = tk.Entry(frame, font=("Segoe UI", 12), width=30, relief="solid", bd=1)
        entries[key].grid(row=i*2+1, column=0, pady=(0,5), ipady=10)
    
    def save_info():
        data = {k: v.get().strip() for k, v in entries.items()}
        if not all(data.values()): return messagebox.showerror("Error", "Please fill all fields!")
        customer_info.update(data)
        win.destroy()
        show_bill()
    
    btn(frame, "Proceed to Bill", save_info, "#27ae60", width=25).grid(row=7, pady=25)

def show_bill():
    total, order_items = 0, []
    for category in menus:
        for dish, price in menus[category].items():
            qty = quantities.get(dish, tk.IntVar()).get()
            if qty > 0:
                cost = qty * price
                total += cost
                order_items.append((dish, qty, price, cost))
    
    gst, grand_total = total * 0.05, total * 1.05
    win = tk.Toplevel(root)
    win.title("Order Summary")
    win.geometry("450x500")
    win.iconbitmap(r"s.ico")
    win.config(bg="white")
    
    tk.Label(win, text="Order Summary", font=("Segoe UI", 18, "bold"), bg="white", fg="#2c3e50", pady=20).pack()
    frame = tk.Frame(win, bg="white")
    frame.pack(fill="both", expand=True, padx=40, pady=10)
    
    info_frame = tk.Frame(frame, bg="#f8f9fa")
    info_frame.pack(fill="x", pady=(0,20), ipady=15, ipadx=15)
    for key, label in [("name", "Customer"), ("phone", "Phone"), ("table", "Table")]:
        tk.Label(info_frame, text=f"{label}: {customer_info[key]}", font=("Segoe UI", 11), bg="#f8f9fa", fg="#2c3e50").pack(anchor="w")
    
    for dish, qty, price, cost in order_items:
        item_frame = tk.Frame(frame, bg="white")
        item_frame.pack(fill="x", pady=3)
        tk.Label(item_frame, text=f"{dish}", font=("Segoe UI", 11), bg="white").pack(side="left")
        tk.Label(item_frame, text=f"{qty} × ₹{price} = ₹{cost}", font=("Segoe UI", 11), bg="white", fg="#7f8c8d").pack(side="right")
    
    tk.Frame(frame, height=1, bg="#ecf0f1").pack(fill="x", pady=15)
    for label, amount in [("Subtotal:", f"₹{total:.2f}"), ("GST (5%):", f"₹{gst:.2f}")]:
        total_frame = tk.Frame(frame, bg="white")
        total_frame.pack(fill="x", pady=2)
        tk.Label(total_frame, text=label, font=("Segoe UI", 11), bg="white").pack(side="left")
        tk.Label(total_frame, text=amount, font=("Segoe UI", 11), bg="white").pack(side="right")
    
    grand_frame = tk.Frame(frame, bg="white")
    grand_frame.pack(fill="x", pady=(10,20))
    tk.Label(grand_frame, text="Total:", font=("Segoe UI", 12, "bold"), bg="white").pack(side="left")
    tk.Label(grand_frame, text=f"₹{grand_total:.2f}", font=("Segoe UI", 12, "bold"), bg="white", fg="#27ae60").pack(side="right")
    
    btn_frame = tk.Frame(win, bg="white")
    btn_frame.pack(pady=20, padx=40, fill="x")
    btn(btn_frame, "Confirm Order", lambda: [messagebox.showinfo("Success", "Order placed! Food will be served soon."), win.destroy()], "#27ae60").pack(fill="x", pady=5)
    btn(btn_frame, "Cancel", win.destroy, "#f8f9fa", "#2c3e50").pack(fill="x", pady=5)

def open_menu(category):
    win = tk.Toplevel(root)
    win.title(f"{category} Menu")
    win.geometry("800x700")
    win.config(bg="#f5f7fa")
    win.resizable(False, False)
    
    header = tk.Frame(win, bg="#3498db", height=80)
    header.pack(fill="x")
    header.pack_propagate(False)
    icons = {"Main Dishes": "🍛", "Beverages": "🥤", "Appetizers": "🍟"}
    tk.Label(header, text=f"{icons.get(category, '🍽️')} {category}", font=("Segoe UI", 20, "bold"), bg="#3498db", fg="white").pack(expand=True)
    
    container = tk.Frame(win, bg="#f5f7fa")
    container.pack(fill="both", expand=True, padx=30, pady=20)
    grid_frame = tk.Frame(container, bg="#f5f7fa")
    grid_frame.pack(expand=True)
    
    items = list(menus[category].items())
    for i, (dish, price) in enumerate(items):
        row, col = i // 2, i % 2
        item_frame = tk.Frame(grid_frame, bg="white", relief="raised", bd=3, width=350, height=150)
        item_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
        item_frame.pack_propagate(False)
        
        content = tk.Frame(item_frame, bg="white")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        tk.Label(content, text=dish, font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50", wraplength=300).pack(anchor="w", pady=(0,5))
        tk.Label(content, text=f"₹{price}", font=("Segoe UI", 16, "bold"), bg="white", fg="#e74c3c").pack(anchor="w", pady=(0,15))
        
        if dish not in quantities: quantities[dish] = tk.IntVar()
        
        controls = tk.Frame(content, bg="white")
        controls.pack(fill="x")
        tk.Label(controls, text="Quantity:", font=("Segoe UI", 11), bg="white", fg="#7f8c8d").pack(side="left")
        qty_frame = tk.Frame(controls, bg="white")
        qty_frame.pack(side="right")
        
        tk.Button(qty_frame, text="−", command=lambda d=dish: [quantities[d].set(max(0, quantities[d].get()-1)), update_cart()], bg="#e74c3c", fg="white", font=("Segoe UI", 14, "bold"), width=3, height=1, relief="raised", bd=2).pack(side="left")
        tk.Label(qty_frame, textvariable=quantities[dish], width=4, bg="#ecf0f1", relief="sunken", font=("Segoe UI", 14, "bold"), bd=2).pack(side="left", padx=8)
        tk.Button(qty_frame, text="+", command=lambda d=dish: [quantities[d].set(quantities[d].get()+1), update_cart()], bg="#27ae60", fg="white", font=("Segoe UI", 14, "bold"), width=3, height=1, relief="raised", bd=2).pack(side="left")
    
    for i in range(2): grid_frame.columnconfigure(i, weight=1)

# Main window setup
root = tk.Tk()
root.title("Spice Garden Restaurant")
root.geometry("700x900")
root.config(bg="#f5f7fa")
root.resizable(True, True)
cart_total = tk.StringVar()

# Header
header_frame = tk.Frame(root, bg="#3498db", height=120)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)
tk.Label(header_frame, text="🍴 SPICE GARDEN", font=("Segoe UI", 26, "bold"), bg="#3498db", fg="white", pady=5).pack(expand=True, anchor="center")
tk.Label(header_frame, text="Authentic Indian Restaurant", font=("Segoe UI", 14), bg="#3498db", fg="#ecf0f1").pack()

# Menu section
menu_section = tk.Frame(root, bg="#f5f7fa")
menu_section.pack(pady=30, padx=40, fill="x")
header_label = tk.Frame(menu_section, bg="#f5f7fa")
header_label.pack(fill="x", pady=(0,20))
tk.Label(header_label, text="📋 Browse Our Menu", font=("Segoe UI", 16, "bold"), bg="white", fg="#2c3e50", relief="raised", bd=2, padx=10, pady=5).pack(side="left")

icons = {"Main Dishes": "🍛", "Beverages": "🥤", "Appetizers": "🍟"}
for category in menus.keys():
    card_frame = tk.Frame(menu_section, bg="white", relief="raised", bd=3)
    card_frame.pack(pady=8, fill="x")
    btn_frame = tk.Frame(card_frame, bg="white")
    btn_frame.pack(fill="x", padx=15, pady=15)
    tk.Label(btn_frame, text=icons.get(category, "🍽️"), font=("Segoe UI", 20), bg="white").pack(side="left", padx=(0,10))
    text_frame = tk.Frame(btn_frame, bg="white")
    text_frame.pack(side="left", fill="x", expand=True)
    tk.Label(text_frame, text=category, font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
    tk.Label(text_frame, text=f"{len(menus[category])} items available", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(anchor="w")
    btn(btn_frame, "View →", lambda c=category: open_menu(c), "#ffffff", "#2c3e50", width=8).pack(side="right")

# Cart section
cart_section = tk.Frame(root, bg="#2c3e50", relief="raised", bd=3)
cart_section.pack(fill="x", padx=40, pady=20)
cart_header = tk.Frame(cart_section, bg="#2c3e50")
cart_header.pack(fill="x", padx=20, pady=15)
tk.Label(cart_header, text="🛒 Your Order", font=("Segoe UI", 14, "bold"), bg="#2c3e50", fg="white").pack(side="left")
tk.Label(cart_header, textvariable=cart_total, font=("Segoe UI", 16, "bold"), bg="#2c3e50", fg="#f1c40f").pack(side="right")

# Action buttons
button_section = tk.Frame(root, bg="#f5f7fa")
button_section.pack(pady=30, padx=40, fill="x")
btn(button_section, "💳 Proceed to Checkout", get_customer_info, "#27ae60").pack(pady=8, fill="x", ipady=8)
btn(button_section, "🗑️ Clear Cart", lambda: [q.set(0) for q in quantities.values()] + [update_cart()], "#e74c3c").pack(pady=5, fill="x", ipady=5)

# Footer
footer = tk.Frame(root, bg="#34495e", height=40)
footer.pack(side="bottom", fill="x")
footer.pack_propagate(False)
tk.Label(footer, text="✨ Thank you for choosing Spice Garden! ✨", font=("Segoe UI", 11), bg="#34495e", fg="#ecf0f1").pack(expand=True)

cart_total.set("₹0")

root.mainloop()

