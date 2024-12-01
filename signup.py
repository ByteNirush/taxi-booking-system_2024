from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

class TaxiBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)
        self.root.title("Taxi Booking Registration Page")
        self.root.configure(bg="#f8f9fa")

        # Background Image
        bgImage = ImageTk.PhotoImage(file="background img.png")
        bgLabel = Label(self.root, image=bgImage)
        bgLabel.place(x=0, y=0)
        self.bgImage = bgImage  # Prevent garbage collection

        # UI Elements
        self.create_ui()

    def create_ui(self):
        """Creates the registration UI."""
        # Heading
        heading = Label(
            self.root, text="Welcome to Register for Customer", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        
        
        heading.place(x=550, y=80)

        # Name Entry
        self.name_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.name_entry.place(x=550, y=150)
        self.name_entry.insert(0, "Full Name")
        self.name_entry.bind("<FocusIn>", self.user_enter)
        self.name_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.name_entry, "Full Name"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=175)

        # Address Entry
        self.address_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.address_entry.place(x=550, y=225)
        self.address_entry.insert(0, "Address")
        self.address_entry.bind("<FocusIn>", self.user_enter)
        self.address_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.address_entry, "Address"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=250)

        # Phone Entry
        self.phone_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.phone_entry.place(x=550, y=300)
        self.phone_entry.insert(0, "Phone Number")
        self.phone_entry.bind("<FocusIn>", self.user_enter)
        self.phone_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.phone_entry, "Phone Number"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=325)

        # Email Entry
        self.email_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.email_entry.place(x=550, y=375)
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", self.user_enter)
        self.email_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.email_entry, "Email"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=400)

        # Username Entry
        self.username_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.username_entry.place(x=550, y=450)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.user_enter)
        self.username_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.username_entry, "Username"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=475)

        # Password Entry
        self.password_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray", show="*")
        self.password_entry.place(x=550, y=525)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.password_enter)
        self.password_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.password_entry, "Password"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=550)

        # Register Button
        registerButton = Button(
            self.root,
            text="Register",
            font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", activeforeground="white", activebackground="#025aa5", cursor="hand2",
            bd=0, width=19, command=self.register_user,
        )
        registerButton.place(x=610, y=580)

        # Back Button
        backButton = Button(
            self.root,
            text="Back",
            font=("Aptos Black", 12, "bold"), fg="white", bg="#d9534f", activeforeground="white", activebackground="#c9302c", cursor="hand2",
            bd=0, width=10, command=self.go_back,
        )
        backButton.place(x=20, y=20)

    def reset_placeholder(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def user_enter(self, event):
        if event.widget.get() in ["Full Name", "Address", "Phone Number", "Email", "Username"]:
            event.widget.delete(0, "end")
        event.widget.config(fg="black")

    def password_enter(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
        self.password_entry.config(fg="black")

    def register_user(self):
        """Registers a new user."""
        name = self.name_entry.get()
        address = self.address_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if any(field == "" for field in [name, address, phone, email, username, password]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Placeholder for successful registration
        messagebox.showinfo("Success", "Account created successfully!")
        self.root.destroy()  # Close the registration window after successful registration

    def go_back(self):
        """Closes the registration window to return to the login page."""
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = TaxiBookingApp(root)
    #root.mainloop()
