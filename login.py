from tkinter import *
from tkinter import messagebox
from PIL import ImageTk

class TaxiBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("990x660+50+50")
        self.root.resizable(0, 0)
        self.root.title("Taxi Booking Login Page")
        self.root.configure(bg="#f8f9fa")

        # Background Image
        try:
            bgImage = ImageTk.PhotoImage(file="background img.png")  # Check if image exists
        except Exception as e:
            print("Error loading background image:", e)
            bgImage = None
        bgLabel = Label(self.root, image=bgImage)
        bgLabel.place(x=0, y=0)
        self.bgImage = bgImage  # Prevent garbage collection

        # UI Elements
        self.create_ui()

    def create_ui(self):
        """Creates the login UI."""
        # Heading
        heading = Label(
            self.root, text="Welcome to Taxi Booking System", font=("Aptos Black", 16, "bold"), bg="white", fg="#FFC107"
        )
        heading.place(x=550, y=100)

        # Username Entry
        self.username_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray")
        self.username_entry.place(x=550, y=200)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.user_enter)
        self.username_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.username_entry, "Username"))

        Frame(self.root, width=325, height=2, bg="#0275d8").place(x=550, y=225)

        # Password Entry
        self.password_entry = Entry(self.root, width=25, font=("Aptos Black", 14), bd=0, fg="gray", show="*")
        self.password_entry.place(x=550, y=300)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.password_enter)
        self.password_entry.bind("<FocusOut>", lambda e: self.reset_placeholder(e, self.password_entry, "Password"))

        Frame(self.root, width=325, height=2, bg="#FFC107").place(x=550, y=325)

        # Login Button
        loginButton = Button(
            self.root,
            text="Login",
            font=("Aptos Black", 14, "bold"), fg="white", bg="#0275d8", activeforeground="yellow", activebackground="#025aa5", cursor="hand2",
            bd=0, width=19, command=self.login_user, )
        loginButton.place(x=600, y=390)
        
        # OR Label
        orLabel = Label(
            self.root,
            text="----------------------------OR----------------------------", font=("Aptos Black", 12, "bold"), fg="#FFC107", bg="white", )
        orLabel.place(x=565, y=450, anchor=W)

        # Sign-Up Label
        signupLabel = Label(self.root, text="Don't have an account?", font=("Aptos Black", 12), fg="#FFC107", bg="white")
        signupLabel.place(x=650, y=490)

        # Create Account Button
        newaccountButton = Button( self.root, text="Create New One",
        font=("Aptos Black", 12, "bold underline"), fg="#FFC107", activeforeground="#FFC107", activebackground="yellow", cursor="hand2", bd=0, width=19, command=self.register_user,
        )
        newaccountButton.place(x=620, y=530)

    def reset_placeholder(self, event, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="gray")
        else:
            entry.config(fg="black")

    def user_enter(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, "end")
        self.username_entry.config(fg="black")

    def password_enter(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, "end")
        self.password_entry.config(fg="black")

    def register_user(self):
        """Opens the Registration page (signup.py)."""
        import signup  # Import the signup.py script

        # Create a new window for registration
        self.new_window = Toplevel(self.root)  # Create a new top-level window
        app = signup.TaxiBookingApp(self.new_window)  # Pass the new window to the signup.py class

    def login_user(self):
        """Validates user login."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or username == "Username":
            messagebox.showerror("Error", "Please enter a username.")
            return
        if not password or password == "Password":
            messagebox.showerror("Error", "Please enter a password.")
            return

        # Simulated login logic (replace with actual logic as needed)
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", f"Welcome, {username}!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def on_close(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = TaxiBookingApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
