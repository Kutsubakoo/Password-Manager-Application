from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for letter in range(randint(8, 10))]
    symbols_list = [choice(symbols) for symbol in range(randint(2, 4))]
    number_list = [choice(numbers) for number in range(randint(2, 4))]

    password_list = letter_list + symbols_list + number_list

    shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    password = "".join(password_list)

    password_entry.insert(0, password)

    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email_username = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email_username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file: # Specify file
                data = json.load(data_file)  # get hold of the data

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4) # Saving the updated data
        else:
            data.update(new_data)  # update dict with new_data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            messagebox.showinfo(title=website, message=f"Account details for {website} added!")
            website_entry.delete(0, END)
            email_username_entry.delete(0, END)
            email_username_entry.insert(0, "@gmail.com")
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:  # Specify file
            data = json.load(data_file)  # get hold of the data
    except FileNotFoundError:
        messagebox.showerror(title="Uhh", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email/Username: {email}\nPassword: {password}")
        else:
            messagebox.showerror(title="Uhh", message="No details for the website exists!")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1, pady=5)

email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2, pady=5)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3, pady=5)

# Entries

website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

email_username_entry = Entry(width=53)
email_username_entry.grid(column=1, row=2, columnspan=2)
email_username_entry.insert(0, "@gmail.com")

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Buttons

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

password_button = Button(text="Generate Password", width=15, command=generate_pass)
password_button.grid(column=2, row=3)

add_button = Button(text="Add/Update", width=45, command=save)
add_button.grid(column=1, row=4, columnspan=2)


window.mainloop()