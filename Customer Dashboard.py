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
        pickup_time TEXT
    )
    """)
    conn.commit()
    return conn, cursor

# Function to go to the Home page
def go_home():
    # Clear the content frame
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Welcome text
    welcome_label = tk.Label(content_frame, text="Welcome", font=("Aptos Black", 20, "bold"), bg="white", fg="#343a40")
    welcome_label.pack(pady=10)

    # Log out button
    logout_button = tk.Button(content_frame, text="Log Out", bg="#FFC107", fg="#343a40", font=("Aptos Black", 12), command=logout)
    logout_button.pack(pady=290)

# Function to handle the "Book a Trip" page
def book_trip():
    # Clear content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    ride_frame = tk.LabelFrame(content_frame, text="Customer Ride", padx=10, pady=10, font=("Aptos Black", 12))
    ride_frame.pack(pady=30, fill="x", padx=20)

    # Fields for the booking
    ride_fields = ["PickUp Location", "Drop-off Location"]
    ride_entries = {}

    # Create input fields for the ride details
    for idx, field in enumerate(ride_fields):
        label = tk.Label(ride_frame, text=f"{field}:", font=("Aptos Black", 10))
        label.grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        entry = ttk.Entry(ride_frame, width=25)
        entry.grid(row=idx, column=1, pady=5)
        ride_entries[field] = entry

    # Date picker for pickup date
    date_label = tk.Label(ride_frame, text="Pickup Date:", font=("Aptos Black", 10))
    date_label.grid(row=len(ride_fields), column=0, sticky="e", pady=5, padx=5)

    date_picker = DateEntry(ride_frame, width=23, background="darkblue", foreground="white", borderwidth=2)
    date_picker.set_date(datetime.now().date())  # Set today's date as default
    date_picker.grid(row=len(ride_fields), column=1, pady=5)

    # Time picker for pickup time
    time_label = tk.Label(ride_frame, text="Pickup Time:", font=("Aptos Black", 10))
    time_label.grid(row=len(ride_fields) + 1, column=0, sticky="e", pady=5, padx=5)

    start_time = datetime.strptime("06:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")
    time_values = []

    while start_time <= end_time:
        time_values.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=30)

    now = datetime.now()
    next_half_hour = (now + timedelta(minutes=30)).replace(minute=(0 if now.minute < 30 else 30), second=0, microsecond=0)
    if next_half_hour < now.replace(hour=6, minute=0):  # Ensure time is within range
        next_half_hour = now.replace(hour=6, minute=0)

    time_picker = ttk.Combobox(ride_frame, values=time_values, width=22, state="readonly")
    time_picker.grid(row=len(ride_fields) + 1, column=1, pady=5)
    time_picker.set(next_half_hour.strftime("%H:%M"))  # Set default value

    # Function to handle booking confirmation and save to SQLite
    def book_now():
        details = {
            "PickUp Location": ride_entries["PickUp Location"].get().strip(),
            "Drop-off Location": ride_entries["Drop-off Location"].get().strip(),
            "Pickup Date": date_picker.get(),
            "Pickup Time": time_picker.get()
        }

        # Validation
        if all(details.values()) and details["Pickup Time"] in time_values:
            # Save to SQLite database
            conn, cursor = connect_db()
            cursor.execute("""
            INSERT INTO bookings (pickup_location, dropoff_location, pickup_date, pickup_time)
            VALUES (?, ?, ?, ?)
            """, (details["PickUp Location"], details["Drop-off Location"], details["Pickup Date"], details["Pickup Time"]))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", f"Trip booked successfully!\n\nDetails:\n{details}")
            
            # Clear the input fields after successful booking
            for field in ride_entries.values():
                field.delete(0, tk.END)
            date_picker.set_date(datetime.now().date())
            time_picker.set(next_half_hour.strftime("%H:%M"))
        else:
            messagebox.showerror("Error", "Please fill in all fields and select a valid time.")

    # Booking button
    button_frame = tk.Frame(content_frame)
    button_frame.pack(pady=20)

    book_now_button = tk.Button(button_frame, text="Book Now!", bg="#FFC107", padx=20, pady=10, font=("Aptos Black", 10, "bold"), command=book_now)
    book_now_button.grid(row=0, column=0, padx=10)

# Function to view all bookings from the SQLite database with Delete and Update buttons
def view_bookings():
    for widget in content_frame.winfo_children():
        widget.destroy()

    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM bookings")
    all_bookings = cursor.fetchall()
    conn.close()

    if all_bookings:
        bookings_frame = tk.LabelFrame(content_frame, text="Booked Trips", padx=10, pady=10, font=("Aptos Black", 12))
        bookings_frame.pack(pady=30, fill="x", padx=20)

        # Display each booking with Delete and Update buttons
        for idx, booking in enumerate(all_bookings):
            row = f"Booking {idx + 1}:"
            booking_details = f"PickUp: {booking[1]}, DropOff: {booking[2]}, Date: {booking[3]}, Time: {booking[4]}"
            
            # Booking details label
            tk.Label(bookings_frame, text=row, font=("Aptos Black", 10, "bold")).grid(row=idx * 2, column=0, sticky="w", padx=10)
            tk.Label(bookings_frame, text=booking_details, font=("Aptos Black", 10)).grid(row=idx * 2 + 1, column=0, sticky="w", padx=10)

            # Delete button
            delete_button = tk.Button(
                bookings_frame, text="Delete", bg="red", fg="white", 
                font=("Aptos Black", 10),
                command=lambda booking_id=booking[0]: delete_booking(booking_id)
            )
            delete_button.grid(row=idx * 2 + 1, column=1, padx=10)

            # Update button
            update_button = tk.Button(
                bookings_frame, text="Update", bg="blue", fg="white", 
                font=("Aptos Black", 10),
                command=lambda booking=booking: update_booking(booking)
            )
            update_button.grid(row=idx * 2 + 1, column=2, padx=10)
    else:
        messagebox.showinfo("No Bookings", "No bookings have been made yet.")

# Function to delete a booking
def delete_booking(booking_id):
    conn, cursor = connect_db()
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Booking deleted successfully!")
    view_bookings()  # Refresh the bookings view

def update_booking(booking):
    # Define the start and end times for the time picker
    start_time = datetime.strptime("06:00", "%H:%M")
    end_time = datetime.strptime("22:00", "%H:%M")
    time_values = []

    # Generate time values in 30-minute intervals
    while start_time <= end_time:
        time_values.append(start_time.strftime("%H:%M"))
        start_time += timedelta(minutes=30)

    # Clear content area
    for widget in content_frame.winfo_children():
        widget.destroy()

    ride_frame = tk.LabelFrame(content_frame, text="Update Booking", padx=10, pady=10, font=("Aptos Black", 12))
    ride_frame.pack(pady=30, fill="x", padx=20)

    # Pre-fill booking details
    fields = ["PickUp Location", "Drop-off Location", "Pickup Date", "Pickup Time"]
    values = [booking[1], booking[2], booking[3], booking[4]]
    entries = {}

    for idx, field in enumerate(fields[:-2]):
        label = tk.Label(ride_frame, text=f"{field}:", font=("Aptos Black", 10))
        label.grid(row=idx, column=0, sticky="e", pady=5, padx=5)

        entry = ttk.Entry(ride_frame, width=25)
        entry.insert(0, values[idx])
        entry.grid(row=idx, column=1, pady=5)
        entries[field] = entry

    # Date picker
    date_label = tk.Label(ride_frame, text="Pickup Date:", font=("Aptos Black", 10))
    date_label.grid(row=2, column=0, sticky="e", pady=5, padx=5)

    date_picker = DateEntry(ride_frame, width=23, background="darkblue", foreground="white", borderwidth=2)
    date_picker.set_date(values[2])
    date_picker.grid(row=2, column=1, pady=5)

    # Time picker
    time_label = tk.Label(ride_frame, text="Pickup Time:", font=("Aptos Black", 10))
    time_label.grid(row=3, column=0, sticky="e", pady=5, padx=5)

    # Create combobox with time values
    time_picker = ttk.Combobox(ride_frame, values=time_values, width=22, state="readonly")
    time_picker.set(values[3])  # Set the default time
    time_picker.grid(row=3, column=1, pady=5)

    # Function to save the updated booking
    def save_update():
        updated_details = {
            "PickUp Location": entries["PickUp Location"].get().strip(),
            "Drop-off Location": entries["Drop-off Location"].get().strip(),
            "Pickup Date": date_picker.get(),
            "Pickup Time": time_picker.get()
        }

        if all(updated_details.values()):
            conn, cursor = connect_db()
            cursor.execute(""" 
                UPDATE bookings
                SET pickup_location = ?, dropoff_location = ?, pickup_date = ?, pickup_time = ?
                WHERE id = ?
            """, (updated_details["PickUp Location"], updated_details["Drop-off Location"], updated_details["Pickup Date"], updated_details["Pickup Time"], booking[0]))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Booking updated successfully!")
            view_bookings()  # Refresh the bookings view
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # Save button
    save_button = tk.Button(ride_frame, text="Save Changes", bg="#FFC107", padx=20, pady=10, font=("Aptos Black", 10, "bold"), command=save_update)
    save_button.grid(row=4, columnspan=2, pady=10)




# Function to log out and close the app
def logout():
    root.destroy()

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
    ("Book A Trip", book_trip),
    ("View Bookings", view_bookings),
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
