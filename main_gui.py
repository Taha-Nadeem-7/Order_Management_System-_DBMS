# main_gui.py
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk
import os
from db_connection import connect_to_db
from decimal import Decimal

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Management System")
        self.root.geometry("850x650")
        self.root.configure(bg="#E9E65A")

        self.db = connect_to_db()
        self.cursor = self.db.cursor()
        self.create_main_interface()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_interface(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome to", font=("Kristen ITC", 50), fg="black", bg="#E9E65A").pack(pady=20)

        img_path = os.path.join("images", "restaurant.jpg")
        if os.path.exists(img_path):
            image = Image.open(img_path).resize((700, 131))
            photo = ImageTk.PhotoImage(image)
            img_label = tk.Label(self.root, image=photo, bg="#E9E65A")
            img_label.image = photo
            img_label.pack(pady=10)

            tk.Button(self.root, text="View Menu", width=20,font=("Kristen ITC", 14, "bold"), command=self.view_menu, bg="orange", fg="white", bd=2, relief="solid",highlightbackground="black", highlightthickness=1).pack(pady=10)

            tk.Button(self.root, text="Place Order", width=20, font=("Kristen ITC", 14, "bold"),command=self.place_order,bg="orange", fg="white", bd=2, relief="solid",highlightbackground="black", highlightthickness=1).pack(pady=10)

            tk.Button(self.root, text="Customer Reviews", width=20, font=("Kristen ITC", 14, "bold"), command=self.view_reviews,bg="orange", fg="white", bd=2, relief="solid",highlightbackground="black", highlightthickness=1).pack(pady=10)

            tk.Button(self.root, text="Leave a Review",width=20, font=("Kristen ITC", 14, "bold"), command=self.leave_review,bg="orange", fg="white", bd=2, relief="solid",highlightbackground="black", highlightthickness=1).pack(pady=10)

            tk.Button(self.root, text="Admin Module", width=20, font=("Kristen ITC", 14, "bold"),command=self.admin_login,bg="orange", fg="white", bd=2, relief="solid",highlightbackground="black", highlightthickness=1).pack(pady=10)

    def view_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Restaurant Menu", font=("Kristen ITC", 50), fg="black", bg="#E9E65A").pack(pady=20)

        self.cursor.execute("SELECT name, category, price, image_path FROM menu_items")
        rows = self.cursor.fetchall()

        if not rows:
            tk.Label(self.root, text="No items in the menu yet.", fg="red",).pack()
            tk.Button(self.root, text="Back", command=self.create_main_interface).pack(pady=10)
            return

        # Group items by category
        categorized_items = {}
        for name, category, price, image_path in rows:
            if category not in categorized_items:
                categorized_items[category] = []
            categorized_items[category].append((name, price, image_path))

        # Scrollable canvas
        canvas = tk.Canvas(self.root,bg="#E9E65A")#masaly wala bg
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas,bg="#E9E65A")#pagal karday ne wala frame

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.image_refs = []

        for category, items in categorized_items.items():
            tk.Label(scrollable_frame, text=category, font=("Arial", 20, "bold"), fg="black",bg="#E9E65A").pack(anchor="w", padx=10, pady=(15, 5)) #font of frame items

            category_frame = tk.Frame(scrollable_frame,bg="#E9E65A") #YE ITEMS K PECHE WALA FRAME HAI
            category_frame.pack(padx=20, pady=5, fill="x")

            columns_per_row = 7
            row_idx = 0
            col_idx = 0

            for name, price, image_path in items:
                # Fixed size item_frame
                item_frame = tk.Frame(category_frame, borderwidth=1, relief="solid", width=180, height=230,bg="#FFA500") #orange background of items
                item_frame.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="n")
                item_frame.grid_propagate(False)  # Disable resizing

                # Use place geometry inside item_frame to strictly position widgets and avoid resizing issues
                # Create image label fixed size
                try:
                    img = Image.open(image_path)
                    img = img.resize((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    self.image_refs.append(img_tk)
                    img_label = tk.Label(item_frame, image=img_tk, width=100, height=100)
                except:
                    img_label = tk.Label(item_frame, text="No Image", width=12, height=6)
                
                img_label.place(x=40, y=10, width=100, height=100)  # centered horizontally

                # Name label fixed position and size
                name_label = tk.Label(item_frame, text=name, font=("Arial", 12, "bold"), bg ="#FEBA4F")
                name_label.place(x=10, y=120, width=160, height=25)

                # Price label fixed position and size
                price_label = tk.Label(item_frame, text=f"{price:.2f} PKR", font=("Arial", 12,"bold"), bg ="#FEBA4F")
                price_label.place(x=10, y=150, width=160, height=20)

                col_idx += 1
                if col_idx >= columns_per_row:
                    col_idx = 0
                    row_idx += 1

        tk.Button(self.root,width=10,height=2,bg="orange" ,text="⬅️", command=self.create_main_interface).pack(pady=10)



    def place_order(self):
        self.clear_frame()
        tk.Label(self.root, text="Place Your Order", bg="#E9E65A", font=("Kristen ITC", 50), fg="black").pack(pady=20)

        self.cursor.execute("SELECT name, category, price, image_path FROM menu_items")
        rows = self.cursor.fetchall()

        if not rows:
            tk.Label(self.root, text="No items in the menu yet.", fg="red").pack()
            tk.Button(self.root, text="Back", command=self.create_main_interface).pack(pady=10)
            return

        # Group items by category
        categorized_items = {}
        for name, category, price, image_path in rows:
            if category not in categorized_items:
                categorized_items[category] = []
            categorized_items[category].append((name, price, image_path))

        # Scrollable canvas (like view_menu)
        canvas = tk.Canvas(self.root, bg="#E9E65A")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#E9E65A")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.image_refs = []
        self.order_vars = {}

        for category, items in categorized_items.items():
            tk.Label(scrollable_frame, text=category, font=("Arial", 20, "bold"), fg="black", bg="#E9E65A").pack(anchor="w", padx=10, pady=(15, 5))

            category_frame = tk.Frame(scrollable_frame, bg="#E9E65A")
            category_frame.pack(padx=20, pady=5, fill="x")

            columns_per_row = 7
            row_idx = 0
            col_idx = 0

            for name, price, image_path in items:
                item_frame = tk.Frame(category_frame, borderwidth=1, relief="solid", width=180, height=230, bg="#FFA500") # same orange bg as view_menu
                item_frame.grid(row=row_idx, column=col_idx, padx=10, pady=10, sticky="n")
                item_frame.grid_propagate(False)

                try:
                    img = Image.open(image_path)
                    img = img.resize((100, 100))
                    img_tk = ImageTk.PhotoImage(img)
                    self.image_refs.append(img_tk)
                    img_label = tk.Label(item_frame, image=img_tk, width=100, height=100)
                except:
                    img_label = tk.Label(item_frame, text="No Image", width=12, height=6)

                img_label.place(x=40, y=10, width=100, height=100)

                name_label = tk.Label(item_frame, text=name, font=("Arial", 12, "bold"), bg="#FEBA4F")
                name_label.place(x=10, y=120, width=160, height=25)

                price_label = tk.Label(item_frame, text=f"{price:.2f} PKR", font=("Arial", 12, "bold"), bg="#FEBA4F")
                price_label.place(x=10, y=150, width=160, height=20)

                var = tk.BooleanVar()
                self.order_vars[name] = var

                def toggle(var=var, btn=None):
                    var.set(not var.get())
                    if var.get():
                        btn.config(text="✓ Added", bg="lightgreen")
                    else:
                        btn.config(text="Add", bg="lightgray")

                btn = tk.Button(item_frame, text="Add", bg="lightgray")
                btn.config(command=lambda v=var, b=btn: toggle(v, b))
                btn.place(x=40, y=190, width=100, height=30)

                col_idx += 1
                if col_idx >= columns_per_row:
                    col_idx = 0
                    row_idx += 1

        # Back and Submit Order Buttons (same style as view_menu)
        tk.Button(self.root, width=10, height=2, bg="orange", text="⬅️", command=self.create_main_interface).pack(pady=10)
        tk.Button(self.root, text="Submit Order", width=15, height=2, bg="skyblue", command=self.prepare_checkout).pack(pady=10)

    def prepare_checkout(self):
        total = Decimal(0)
        selected_items = []
        for item, var in self.order_vars.items():
            if var.get():
                self.cursor.execute("SELECT id, price, category FROM menu_items WHERE name=%s", (item,))
                result = self.cursor.fetchone()
                if result:
                    item_id, price, category = result
                    total += price
                    selected_items.append((item_id, category, item, price))

        if not selected_items:
            messagebox.showwarning("No Items", "Please select at least one item.")
            return

        tax = total * Decimal('0.1')
        service_fee = total * Decimal('0.05')
        final_amount = total + tax + service_fee

        self.checkout_data = {
            "total": total,
            "tax": tax,
            "service_fee": service_fee,
            "final_amount": final_amount,
            "selected_items": selected_items
        }

        self.show_checkout_screen()

    def show_checkout_screen(self):
        self.clear_frame()
        
        tk.Label(self.root, text="Checkout Summary", font=("Kristen ITC", 35, "bold"), fg="black", bg="#E9E65A").pack(pady=20)
        
        final_amount = self.checkout_data["final_amount"]

        summary_frame = tk.Frame(self.root, bg="#E9E65A", bd=2, relief="ridge")
        summary_frame.pack(pady=10)

        summary_text = (
            f"Total: {self.checkout_data['total']:.2f} PKR\n"
            f"Tax (10%): {self.checkout_data['tax']:.2f} PKR\n"
            f"Service Fee (5%): {self.checkout_data['service_fee']:.2f} PKR\n"
            f"Final Amount: {final_amount:.2f} PKR"
        )

        tk.Label(summary_frame, text=summary_text, font=("Arial", 14, "bold"), bg="#FFFACD", fg="black", justify="left", padx=20, pady=10).pack()

        # Cash Entry
        entry_frame = tk.Frame(self.root, bg="#E9E65A")
        entry_frame.pack(pady=10)

        tk.Label(entry_frame, text="Enter Cash Given:", font=("Arial", 14, "bold"), bg="#E9E65A", fg="black").grid(row=0, column=0, padx=10, pady=5)
        self.cash_entry = tk.Entry(entry_frame, width=20, font=("Arial", 12))
        self.cash_entry.grid(row=0, column=1, padx=10, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#E9E65A")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="✅ Confirm Payment", bg="lightgreen", fg="black", font=("Arial", 12, "bold"),
                command=self.process_payment, width=15, height=2).grid(row=0, column=0, padx=10)

        tk.Button(button_frame, text="❌ Cancel", bg="orange", fg="black", font=("Arial", 12, "bold"),
                command=self.create_main_interface, width=15, height=2).grid(row=0, column=1, padx=10)

    def process_payment(self):
        cash_str = self.cash_entry.get()
        try:
            cash_given = Decimal(cash_str)
        except:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric amount.")
            return

        final_amount = self.checkout_data["final_amount"]

        if cash_given < final_amount:
            messagebox.showwarning("Insufficient Cash", "The cash amount entered is less than the final amount.")
            return

        change = cash_given - final_amount

        name = simpledialog.askstring("Customer Name", "Please enter your name:")

        if not name:
            messagebox.showwarning("Missing Info", "Customer name is required to complete the order.")
            return

        includes_beverage = any(category == 'Beverage' for _, category, _, _ in self.checkout_data["selected_items"])

        self.cursor.execute(
            "INSERT INTO orders (customer_name, total, includes_beverage) VALUES (%s, %s, %s)",
            (name, float(final_amount), includes_beverage)
        )
        order_id = self.cursor.lastrowid

        for item_id, _, _, _ in self.checkout_data["selected_items"]:
            self.cursor.execute("INSERT INTO order_items (order_id, item_id) VALUES (%s, %s)", (order_id, item_id))

        self.db.commit()

        messagebox.showinfo("Payment Successful",
                            f"Order placed for {name}!\nChange to return: {change:.2f} PKR")
        self.create_main_interface()

    def view_reviews(self):
        self.clear_frame()

        bg_color = "#E9E65A"      # Main background
        panel_color = "#E9DE5F"   # Inner white panel

        self.root.configure(bg=bg_color)

        # Main Title
        tk.Label(self.root, text="Customer Reviews", font=("Kristen ITC", 35, "bold"),
                fg="black", bg=bg_color).pack(pady=20)

        # Main White Panel
        panel = tk.Frame(self.root, bg=panel_color, bd=4, relief="ridge")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

        # Scrollable Frame inside panel (not including Back button)
        scroll_canvas = tk.Canvas(panel, bg=panel_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(panel, orient="vertical", command=scroll_canvas.yview)

        scrollable_frame = tk.Frame(scroll_canvas, bg=panel_color)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: scroll_canvas.configure(
                scrollregion=scroll_canvas.bbox("all")
            )
        )

        scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)

        # Place scrollable canvas (top portion of the panel)
        scroll_canvas.place(x=0, y=0, width=680, height=420)
        scrollbar.place(x=680, y=0, height=420)

        # Fetch Reviews
        self.cursor.execute("SELECT customer_name, review FROM reviews")
        rows = self.cursor.fetchall()

        if not rows:
            tk.Label(scrollable_frame,
                    text="No reviews yet.",
                    font=("Arial", 16, "bold"),
                    fg="red",
                    bg=panel_color,
                    justify="center").pack(pady=10, fill="x", expand=True)
        else:
            for name, review in rows:
                review_text = f"{name}: {review}"
                tk.Label(scrollable_frame,
                        text=review_text,
                        wraplength=650,
                        bg=panel_color,
                        fg="black",
                        justify="left",
                        font=("Arial", 14),
                        anchor="w").pack(pady=8, padx=10, fill="x")

        # Fixed Back Button (bottom of white panel)
        back_btn = tk.Button(panel,
                            text="🔙 Back",
                            bg="red",
                            fg="white",
                            font=("Arial", 14, "bold"),
                            width=20,
                            height=2,
                            command=self.create_main_interface)
        back_btn.place(relx=0.5, rely=1.0, anchor="s", y=-10)  # 10px margin from bottom


    def leave_review(self):
        self.clear_frame()

        bg_color = "#E9E65A"      # Main background
        panel_color = "#E9DE5F"   # Panel background (white for contrast)

        self.root.configure(bg=bg_color)  # Set window background

        # Panel in center
        panel = tk.Frame(self.root, bg=panel_color, bd=4, relief="ridge")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        # Title
        title = tk.Label(panel,
                        text="Leave Your Review",
                        font=("Kristen ITC", 28, "bold"),
                        fg="black",
                        bg=panel_color)
        title.pack(pady=20)

        # Name Entry
        name_entry = tk.Entry(panel,
                            font=("Arial", 14),
                            width=40,
                            fg="gray",
                            relief="solid",
                            bd=2)
        name_entry.insert(0, "Enter your name")
        name_entry.pack(pady=10)

        # Review Text Box
        review_entry = tk.Text(panel,
                            height=5,
                            width=50,
                            font=("Arial", 14),
                            bg="white",
                            fg="black",
                            wrap="word",
                            relief="solid",
                            bd=2)
        review_entry.pack(pady=10)

        def save_review():
            name = name_entry.get().strip()
            review = review_entry.get("1.0", tk.END).strip()
            if name and review:
                self.cursor.execute("INSERT INTO reviews (customer_name, review) VALUES (%s, %s)", (name, review))
                self.db.commit()
                messagebox.showinfo("Thank You", "Your review has been submitted.")
                self.create_main_interface()
            else:
                messagebox.showwarning("Input Error", "Please enter both name and review.")

        # Submit Button
        submit_btn = tk.Button(panel,text="✅ Submit Review",bg="green",fg="white",font=("Arial", 14, "bold"),width=20,height=2,command=save_review)
        submit_btn.pack(pady=10)

        # Back Button
        back_btn = tk.Button(panel,text="🔙 Back",bg="red",fg="white",font=("Arial", 14, "bold"),width=20, height=2,command=self.create_main_interface)
        back_btn.pack(pady=10)

    def admin_login(self):
        self.clear_frame()

        bg_color = "#E9E65A"      # Background color of the main window
        panel_color = "#FFFACD"   # White panel for contrast

        self.root.configure(bg=bg_color)  # Set the background color for the root window

        # Enlarged Center Panel
        panel = tk.Frame(self.root, bg=panel_color, bd=4, relief="ridge")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=450)  # Increased size

        title = tk.Label(panel, text="Admin Login", font=("Kristen ITC", 36, "bold"), fg="red", bg=panel_color); title.pack(pady=20)

        lbl_user = tk.Label(panel, text="Username:", font=("Arial", 18), bg=panel_color); lbl_user.pack(pady=10)
        user_entry = tk.Entry(panel, width=30, font=("Arial", 16)); user_entry.pack(pady=5)
        

        lbl_pass = tk.Label(panel, text="Password:", font=("Arial", 18), bg=panel_color); lbl_pass.pack(pady=10)
        pass_entry = tk.Entry(panel, show="*", width=30, font=("Arial", 16)); pass_entry.pack(pady=5)

        def verify_login():
            username = user_entry.get().strip()
            password = pass_entry.get().strip()
            self.cursor.execute("SELECT * FROM admin_users WHERE username=%s AND password=%s", (username, password))
            if self.cursor.fetchone():
                self.admin_action()
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")

        btn_login = tk.Button(panel, text="Login", command=verify_login, width=20, height=2, bg="green", fg="white", font=("Arial", 16, "bold")); btn_login.pack(pady=15)
        btn_back = tk.Button(panel, text="Back", command=self.create_main_interface, width=20, height=2, bg="red", fg="white", font=("Arial", 16, "bold")); btn_back.pack(pady=5)


    def admin_action(self):
        self.clear_frame()

        bg_color = "#E9E65A"      # Background of main window
        panel_color = "#FFFACD"   # White panel for contrast

        self.root.configure(bg=bg_color)  # Set background

        # Centered panel with increased size
        panel = tk.Frame(self.root, bg=panel_color, bd=4, relief="ridge")
        panel.place(relx=0.5, rely=0.5, anchor="center", width=600, height=500)

        title = tk.Label(panel, text="Admin Panel", font=("Kristen ITC", 36, "bold"), fg="black", bg=panel_color); title.pack(pady=30)

        btn_add = tk.Button(panel, text="Add Item in Menu", width=25, height=2, font=("Kristen ITC", 16, "bold"), command=self.add_menu_item,
                            bg="orange", fg="white", bd=4, relief="solid", highlightbackground="black", highlightthickness=2); btn_add.pack(pady=15)
        
        btn_remove = tk.Button(panel, text="Remove Item from Menu", width=25, height=2, font=("Kristen ITC", 16, "bold"), command=self.remove_menu_item,
                            bg="orange", fg="white", bd=4, relief="solid", highlightbackground="black", highlightthickness=2); btn_remove.pack(pady=15)
        
        btn_back = tk.Button(panel, text="Back", width=25, height=2, font=("Kristen ITC", 16, "bold"), command=self.admin_login,
                            bg="red", fg="white", bd=4, relief="solid", highlightbackground="black", highlightthickness=2); btn_back.pack(pady=15)

    def add_menu_item(self):
        self.clear_frame()

        bg_color = "#E9E65A"  # Match window background

        title = tk.Label(self.root, text="Add New Menu Item", font=("Kristen ITC", 36, "bold"), fg="green", bg=bg_color); title.pack(pady=30)

        lbl_name = tk.Label(self.root, text="Item Name:", font=("Arial", 18), bg=bg_color); lbl_name.pack(pady=5)
        name_entry = tk.Entry(self.root, width=40, font=("Arial", 16)); name_entry.pack(pady=5)

        lbl_cat = tk.Label(self.root, text="Category:", font=("Arial", 18), bg=bg_color); lbl_cat.pack(pady=5)
        category_entry = tk.Entry(self.root, width=40, font=("Arial", 16)); category_entry.pack(pady=5)
        category_entry.insert(0, "Desi Food")
        lbl_price = tk.Label(self.root, text="Price (PKR):", font=("Arial", 18), bg=bg_color); lbl_price.pack(pady=5)
        price_entry = tk.Entry(self.root, width=40, font=("Arial", 16)); price_entry.pack(pady=5)

        lbl_img = tk.Label(self.root, text="Image path (images/Item_name.jpg):", font=("Arial", 18), bg=bg_color); lbl_img.pack(pady=5)
        image_entry = tk.Entry(self.root, width=40, font=("Arial", 16)); image_entry.pack(pady=5)
        image_entry.insert(0, "images/")

        def save_item():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            price_text = price_entry.get().strip()
            image_path = image_entry.get().strip()
            try:
                price = float(price_text)
            except:
                messagebox.showerror("Invalid Price", "Please enter a valid number for price.")
                return

            if name and category and price_text and image_path:
                self.cursor.execute(
                    "INSERT INTO menu_items (name, category, price, image_path) VALUES (%s, %s, %s, %s)",
                    (name, category, price, image_path)
                )
                self.db.commit()
                messagebox.showinfo("Success", f"Menu item '{name}' added.")
                self.admin_action()
            else:
                messagebox.showwarning("Input Error", "Please fill all fields.")

        btn_save = tk.Button(self.root, text="Add Item", command=save_item, width=25, height=2, bg="green", fg="white", font=("Kristen ITC", 16, "bold"), relief="solid", bd=3, highlightbackground="black", highlightthickness=1); btn_save.pack(pady=20)
        btn_back = tk.Button(self.root, text="Back", command=self.admin_action, width=25, height=2, bg="orange", fg="white", font=("Kristen ITC", 16, "bold"), relief="solid", bd=3, highlightbackground="black", highlightthickness=1); btn_back.pack(pady=10)

    def remove_menu_item(self):
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Menu Item")
        remove_window.geometry("400x300")
        remove_window.configure(bg="#ffeeee")

        tk.Label(remove_window, text="Select Item to Remove", font=("Arial", 16, "bold"), bg="#ffeeee").pack(pady=15)

        self.cursor.execute("SELECT name FROM menu_items")
        items = [row[0] for row in self.cursor.fetchall()]

        if not items:
            tk.Label(remove_window, text="No items available in menu.", fg="red", bg="#ffeeee", font=("Arial", 12)).pack(pady=20)
            return

        selected_item = tk.StringVar(remove_window)
        selected_item.set(items[0])

        dropdown = ttk.Combobox(remove_window, textvariable=selected_item, values=items, font=("Arial", 12), state="readonly")
        dropdown.pack(pady=10)

        def confirm_removal():
            name = selected_item.get()
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{name}'?")
            if confirm:
                self.cursor.execute("DELETE FROM menu_items WHERE name = %s", (name,))
                self.db.commit()
                messagebox.showinfo("Success", f"'{name}' removed from the menu.")
                remove_window.destroy()

        tk.Button(remove_window, text="❌ Remove", command=confirm_removal, bg="red", fg="white", font=("Arial", 12, "bold"), width=15, height=2).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()
