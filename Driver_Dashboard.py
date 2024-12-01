import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import sqlite3

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("taxi_booking.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pickup_location TEXT,
        dropoff_location TEXT,
        pickup_date TEXT,
        pickup_time TEXT,
        status TEXT DEFAULT 'Active'
    )
    """)
    conn.commit()
    return conn, cursor

#Function to check if the 'status' column exists, and add it if not
def add_status_column():
    conn = sqlite3.connect("taxi_booking.db")
    cursor = conn.cursor()
    
    # Query to check the columns in the bookings table
    cursor.execute("PRAGMA table_info(bookings)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'status' not in columns:
        cursor.execute("ALTER TABLE bookings ADD COLUMN status TEXT DEFAULT 'Active'")
        conn.commit()
        print("Status column added.")
    else:
        print("Status column already exists.")
    
    conn.close()

# Example usage (assuming main and other functions are already defined)
def main():
    add_status_column()  # Ensure the status column exists
    # Continue with your other logic

if __name__ == "__main__":
    main()

# Function to create a new booking in the database
def book_trip(pickup_location, dropoff_location, pickup_date, pickup_time):
    conn, cursor = connect_db()
    cursor.execute("""
    INSERT INTO bookings (pickup_location, dropoff_location, pickup_date, pickup_time)
    VALUES (?, ?, ?, ?)
    """, (pickup_location, dropoff_location, pickup_date, pickup_time))
    conn.commit()
    conn.close()

# Function to view all active bookings for the driver
def view_active_bookings():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM bookings WHERE status = 'Active'")
    active_bookings = cursor.fetchall()
    conn.close()
    return active_bookings

# Function to view completed trips for the driver
def view_completed_bookings():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM bookings WHERE status = 'Completed'")
    completed_bookings = cursor.fetchall()
    conn.close()
    return completed_bookings

# Function to mark a booking as completed
def mark_completed(booking_id):
    conn, cursor = connect_db()
    cursor.execute("UPDATE bookings SET status = 'Completed' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

# Function to cancel a booking
def cancel_booking(booking_id):
    conn, cursor = connect_db()
    cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()

# Driver Dashboard UI
def driver_dashboard():
    def refresh_bookings():
        for widget in content_frame.winfo_children():
            widget.destroy()

        active_bookings = view_active_bookings()
        completed_bookings = view_completed_bookings()

        # Active bookings frame
        if active_bookings:
            bookings_frame = tk.LabelFrame(content_frame, text="Active Bookings", padx=10, pady=10, font=("Aptos Black", 12))
            bookings_frame.pack(pady=30, fill="x", padx=20)

            for idx, booking in enumerate(active_bookings):
                row = f"Booking {idx + 1}:"
                booking_details = f"PickUp: {booking[1]}, DropOff: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}"

                # Booking details label
                tk.Label(bookings_frame, text=row, font=("Aptos Black", 10, "bold")).grid(row=idx * 2, column=0, sticky="w", padx=10)
                tk.Label(bookings_frame, text=booking_details, font=("Aptos Black", 10)).grid(row=idx * 2 + 1, column=0, sticky="w", padx=10)

                # Completed button
                complete_button = tk.Button(
                    bookings_frame, text="Mark as Completed", bg="green", fg="white", 
                    font=("Aptos Black", 10),
                    command=lambda booking_id=booking[0]: mark_completed(booking_id)
                )
                complete_button.grid(row=idx * 2 + 1, column=1, padx=10)

        else:
            messagebox.showinfo("No Active Bookings", "No active bookings are available.")

        # Completed bookings frame
        if completed_bookings:
            completed_frame = tk.LabelFrame(content_frame, text="Completed Bookings", padx=10, pady=10, font=("Aptos Black", 12))
            completed_frame.pack(pady=30, fill="x", padx=20)

            for idx, booking in enumerate(completed_bookings):
                row = f"Completed Booking {idx + 1}:"
                booking_details = f"PickUp: {booking[1]}, DropOff: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}"

                # Completed booking details
                tk.Label(completed_frame, text=row, font=("Aptos Black", 10, "bold")).grid(row=idx * 2, column=0, sticky="w", padx=10)
                tk.Label(completed_frame, text=booking_details, font=("Aptos Black", 10)).grid(row=idx * 2 + 1, column=0, sticky="w", padx=10)

    # Main window setup
    root = tk.Tk()
    root.title("Driver Dashboard")
    root.geometry("990x660+50+50")
    root.resizable(0, 0)
    root.config(bg="black")

    # Side menu (for navigation)
    menu_frame = tk.Frame(root, bg="#FFC107", width=250, height=500)
    menu_frame.pack(side="left", fill="y")

    menu_buttons = [
        ("Home", refresh_bookings),
        ("View Active Bookings", refresh_bookings),
        ("View Completed Bookings", refresh_bookings),
    ]

    for text, command in menu_buttons:
        btn = tk.Button(menu_frame, text=text, command=command, bg="#FFC107", fg="white", font=("Aptos Black", 12, "bold"), bd=0)
        btn.pack(fill="x", padx=10, pady=10)

    # Content area for the main window
    content_frame = tk.Frame(root, bg="white", width=600, height=500)
    content_frame.pack(side="left", fill="both", expand=True)

    # Show the Home page initially
    refresh_bookings()

    # Start the main loop for the GUI
    root.mainloop()

# Customer Dashboard UI
def customer_dashboard():
    def go_home():
        for widget in content_frame.winfo_children():
            widget.destroy()
        welcome_label = tk.Label(content_frame, text="Welcome", font=("Aptos Black", 20, "bold"), bg="white", fg="#343a40")
        welcome_label.pack(pady=10)
        logout_button = tk.Button(content_frame, text="Log Out", bg="#FFC107", fg="#343a40", font=("Aptos Black", 12), command=logout)
        logout_button.pack(pady=290)

    def book_trip():
        for widget in content_frame.winfo_children():
            widget.destroy()

        ride_frame = tk.LabelFrame(content_frame, text="Customer Ride", padx=10, pady=10, font=("Aptos Black", 12))
        ride_frame.pack(pady=30, fill="x", padx=20)

        ride_fields = ["PickUp Location", "Drop-off Location"]
        ride_entries = {}

        for idx, field in enumerate(ride_fields):
            label = tk.Label(ride_frame, text=f"{field}:", font=("Aptos Black", 10))
            label.grid(row=idx, column=0, sticky="e", pady=5, padx=5)
            entry = ttk.Entry(ride_frame, width=25)
            entry.grid(row=idx, column=1, pady=5)
            ride_entries[field] = entry

        date_label = tk.Label(ride_frame, text="Pickup Date:", font=("Aptos Black", 10))
        date_label.grid(row=len(ride_fields), column=0, sticky="e", pady=5, padx=5)

        date_picker = DateEntry(ride_frame, width=23, background="darkblue", foreground="white", borderwidth=2)
        date_picker.set_date(datetime.now().date())  
        date_picker.grid(row=len(ride_fields), column=1, pady=5)

        time_label = tk.Label(ride_frame, text="Pickup Time:", font=("Aptos Black", 10))
        time_label.grid(row=len(ride_fields) + 1, column=0, sticky="e", pady=5, padx=5)

        start_time = datetime.strptime("06:00", "%H:%M")
        end_time = datetime.strptime("22:00", "%H:%M")
        time_options = []
        while start_time <= end_time:
            time_options.append(start_time.strftime("%H:%M"))
            start_time += timedelta(minutes=30)

        time_picker = ttk.Combobox(ride_frame, values=time_options, width=23)
        time_picker.set(time_options[0])  # Default to the first time
        time_picker.grid(row=len(ride_fields) + 1, column=1, pady=5)

        def submit_booking():
            pickup_location = ride_entries["PickUp Location"].get()
            dropoff_location = ride_entries["Drop-off Location"].get()
            pickup_date = date_picker.get_date().strftime("%Y-%m-%d")
            pickup_time = time_picker.get()

            if pickup_location and dropoff_location:
                book_trip(pickup_location, dropoff_location, pickup_date, pickup_time)
                messagebox.showinfo("Booking Confirmed", "Your trip has been booked successfully!")
                go_home()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        submit_button = tk.Button(ride_frame, text="Submit Booking", bg="#28a745", fg="white", font=("Aptos Black", 12), command=submit_booking)
        submit_button.grid(row=len(ride_fields) + 2, column=0, columnspan=2, pady=10)

    def logout():
        root.quit()

    # Main window setup
    root = tk.Tk()
    root.title("Customer Dashboard")
    root.geometry("990x660+50+50")
    root.resizable(0, 0)
    root.config(bg="black")

    # Side menu (for navigation)
    menu_frame = tk.Frame(root, bg="#FFC107", width=250, height=500)
    menu_frame.pack(side="left", fill="y")

    menu_buttons = [
        ("Home", go_home),
        ("Book a Trip", book_trip),
        ("View Trip History", go_home),  # You can create this view if needed
        ("View Active Bookings", go_home),  # You can create this view if needed
    ]

    for text, command in menu_buttons:
        btn = tk.Button(menu_frame, text=text, command=command, bg="#FFC107", fg="white", font=("Aptos Black", 12, "bold"), bd=0)
        btn.pack(fill="x", padx=10, pady=10)

    # Content area for the main window
    content_frame = tk.Frame(root, bg="white", width=600, height=500)
    content_frame.pack(side="left", fill="both", expand=True)

    # Show the Home page initially
    go_home()

    # Start the main loop for the GUI
    root.mainloop()

# Main Function to test both dashboards
#def main():
#    add_status_column()  # Add the status column if it doesn't exist
#    choice = input("Enter 1 for Driver Dashboard or 2 for Customer Dashboard: ")
#
#    if choice == "1":
#        driver_dashboard()
#    elif choice == "2":
#        customer_dashboard()
#    else:
#        print("Invalid choice. Please enter 1 or 2.")
#        
#if __name__ == "__main__":
#    main()
