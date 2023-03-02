import MainWindow
import _thread
import math
import random
from tkinter import *
from tkinter import messagebox

# We created them 
import SQLiteDatabase as sq
import TwoFactorAuthentication as fa

# Regex
import re

class LoginScreen (object):
    def __init__(self):
        pass

    def MainScreen(self, root):

        # Creating the database
        sq.createDatabse ()

        self.appwindow = root
        self.appwindow.geometry ("350x500")
        self.appwindow.resizable (width=False, height=False)
        self.appwindow.title ("Sign In")
        self.SignInBackground = PhotoImage (file="Backgrounds/backgroundForLoginScreen.png")
        self.SigninLabelBackgroud = PhotoImage (file="Backgrounds/SignInLabelBg.png")
        self.loginBtnBg = PhotoImage (file="Backgrounds/loginbutton.png")
        self.removeUserbg = PhotoImage (file="Backgrounds/removeUserBtn.png")
        self.createUserbg = PhotoImage (file="Backgrounds/createUserBtn.png")
        self.closeBtnBg = PhotoImage (file="Backgrounds/close_bg.png")
        self.createNewUserBg = PhotoImage (file="Backgrounds/CreateNewUserBtn.png")
        self.SignInBgLabel = Label (self.appwindow, image=self.SignInBackground)
        self.SignInBgLabel.place (x=0, y=0)

        self.isRegistering = False
        self.RGB_Pattern = "NONE"
        self.PicturePattern = "NONE"

        if not sq.defaultUserExists():
            self.isRegistering = True

        self.loginLabel = Label (self.appwindow, image=self.SigninLabelBackgroud, width=125, height=25)
        self.loginLabel.pack (pady=25, padx=5)

        self.usernameInput = Entry (self.appwindow, width=40, relief=SUNKEN)
        self.usernameInput.bind ("<Button-1>", self.click)
        self.usernameInput.pack (padx=5, ipady=3)
        self.usernameInput.insert (0, "Username")

        self.passwordInput = Entry (self.appwindow, width=40, show="*", relief=SUNKEN)
        self.passwordInput.bind ("<Button-1>", self.click1)
        self.passwordInput.pack (padx=5, pady=10, ipady=3)
        self.passwordInput.insert (0, "Password")

        self.emailInput = Entry (self.appwindow, width=40, relief=SUNKEN)
        self.emailInput.bind ("<Button-1>", self.click2)

        self.CreateNewUserBtn = Button (self.appwindow, image=self.createNewUserBg, width=200, height=25,
                                        command=self.createNewUser)

        self.loginBtn = Button (self.appwindow, image=self.loginBtnBg, width=125, height=25, command=self.login)
        self.loginBtn.pack (pady=10)

        self.removeUserbtn = Button (self.appwindow, image=self.removeUserbg, width=125, height=25,
                                     command=self.removeUser)
        self.removeUserbtn.pack (pady=10)

        self.createUserbtn = Button (self.appwindow, image=self.createUserbg, width=125, height=25,
                                     command=self.createUser)
        self.createUserbtn.pack (pady=10)

        self.closeBtn = Button (self.appwindow, image=self.closeBtnBg, width=125, height=25, command=self.close)
        self.closeBtn.pack (pady=15, side=BOTTOM)

        if sq.defaultUserExists ():
            self.createUserbtn.config (state=DISABLED)
        else:
            self.loginBtn.config (state=DISABLED)
            self.removeUserbtn.config (state=DISABLED)

        self.appwindow.mainloop ()

# To clear screen
    def click(self, *args):
        self.usernameInput.delete (0, 'end')

    def click1(self, *args):
        self.passwordInput.delete (0, 'end')

    def click2(self, *args):
        self.emailInput.delete (0, 'end')

    def login(self):
        username = self.usernameInput.get ()
        password = self.passwordInput.get ()
        if len (username) == 0 or len (password) == 0:
            messagebox.showerror ("Error", "All Fields Are Required!")
            self.usernameInput.delete (0, 'end')
            self.passwordInput.delete (0, 'end')
            self.usernameInput.insert (0, "Username")
            self.passwordInput.insert (0, "Password")
        elif sq.validate (username, password):
            self.loginBtn.config(state=DISABLED)
            self.removeUserbtn.config(state=DISABLED)
            self.twoFactor()

        else:
            messagebox.showerror ("Error", "Invalid Username/Password Combination")

    def removeUser(self):
        username = self.usernameInput.get ()
        password = self.passwordInput.get ()
        if len (username) == 0 or len (password) == 0:
            messagebox.showerror ("Error", "All Fields Are Required!")
        elif sq.validate (username, password):
            sq.removeUser ()
            self.createUserbtn.config (state=NORMAL)
            self.usernameInput.delete (0, "end")
            self.passwordInput.delete (0, "end")
            self.usernameInput.insert (0, "Username")
            self.passwordInput.insert (0, "Password")
            self.isRegistering = True
            self.loginBtn.config(state=DISABLED)
            self.removeUserbtn.config(state=DISABLED)
        else:
            messagebox.showerror ("Error", "Invalid Username/Password Combination")

    def createUser(self):
        self.emailInput.pack (padx=5, ipady=3)
        self.emailInput.insert (0, "Email")
        self.CreateNewUserBtn.pack (pady=20)
        self.createUserbtn.config (state=DISABLED)
        self.loginBtn.config (state=NORMAL)
        self.removeUserbtn.config (state=NORMAL)

    def createNewUser(self):
        self.username = self.usernameInput.get ()
        self.password = self.passwordInput.get ()
        self.email = self.emailInput.get ()
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        pat = re.compile (regex)
        if len (self.username) == 0 or len (self.password) == 0 or len (self.email) == 0:
            messagebox.showerror ("Error", "All Fields Are Required")
        elif not re.match (pat, self.email):
            messagebox.showerror ("Invalid Email", "Please Enter A Valid Email")
            self.emailInput.delete (0, 'end')
        else:
            self.RGB()
            self.usernameInput.config(state=DISABLED)
            self.passwordInput.config(state=DISABLED)
            self.loginBtn.config(state=DISABLED)
            self.createUserbtn.config(state=DISABLED)
            self.closeBtn.config(state=DISABLED)
            self.closeBtn.config(state=DISABLED)
            self.removeUserbtn.config(state=DISABLED)
            self.emailInput.config(state=DISABLED)
            self.CreateNewUserBtn.config(state=DISABLED)

    def RGB(self):
        def red():
            inputField.config (state=NORMAL)
            inputField.insert (END, "R")
            inputField.config (state=DISABLED)

        def green():
            inputField.config (state=NORMAL)
            inputField.insert (END, "G")
            inputField.config (state=DISABLED)

        def blue():
            inputField.config (state=NORMAL)
            inputField.insert (END, "B")
            inputField.config (state=DISABLED)

        def submit():
            patt = inputField.get()
            if self.isRegistering:
                if len (patt) < 10:
                    messagebox.showerror ("Error", "Password cannot be shorter than 10 characters")
                    return
                self.RGB_Pattern = patt
                self.PictureOrder()
                self.RGB_Window.destroy()
            elif not self.isRegistering:
                userCred = sq.getUser()
                userSavedPattern = userCred[0][5]
                if patt == userSavedPattern:
                    self.PictureOrder()
                    self.RGB_Window.destroy()
                elif patt != userSavedPattern:
                    inputField.config(state=NORMAL)
                    inputField.delete(0, 'end')
                    inputField.config(state=DISABLED)
                    self.RGB_Timer -=1
                    messagebox.showerror("Error", f"Invalid Pattern!\n{self.RGB_Timer} Attempts Left.")
                    if self.RGB_Timer == 0:
                        messagebox.showerror("Error", "Trials Exceeded!")
                        self.RGB_Window.destroy()
                        userCred = sq.getUser()
                        userEmail = userCred[0][4]
                        _thread.start_new_thread(fa.sendUnAuthorizedEmail, (userEmail,))


        self.RGB_Window = Toplevel(root)
        if self.isRegistering:
            self.RGB_Window.geometry("350x200")

            global background
            background = PhotoImage (file="Backgrounds/vintage-brown-paper-with-wrinkles-abstract-old-paper-textures-background_7182-982.png")
            backgroundLabel = Label (self.RGB_Window, image=background).place (x=0, y=0)

            text = "Please Register an RGB Pattern\nShould not be less than 10 chars"
            self.registerLabel = Label(self.RGB_Window, text=text, fg="red")
            self.registerLabel.grid(row=3, column=0, columnspan=3)
        else:
            self.RGB_Window.geometry("350x150")
        self.RGB_Window.title("RGB Verification")
        self.RGB_Timer = 3

        global RGB_Background
        RGB_Background = PhotoImage(file="Backgrounds/backgroundForRGB.png")
        RGB_Background_Label = Label(self.RGB_Window, image=RGB_Background).place(x=0, y=0)

        if self.isRegistering:
            text="Please Enter A RGB Verification pattern.\nPattern length should not be less than 10."
            registerLabel = Label(self.RGB_Window, text=text, fg="red").grid(row=3, column=0, columnspan=3, pady=10)


        redButton = Button(self.RGB_Window, bg="red", width=12, height=2, command=red)
        redButton.grid(row=0, column=0, pady=10, padx=10)

        greenButton = Button(self.RGB_Window, bg="green", width=12, height=2, command=green)
        greenButton.grid(row=0, column=1, pady=10, padx=10)

        blueButton = Button (self.RGB_Window, bg="blue", width=12, height=2, command=blue)
        blueButton.grid (row=0, column=2, pady=10, padx=10)

        inputField = Entry(self.RGB_Window, width=30, state=DISABLED, justify=CENTER, show="*")
        inputField.grid(row=1, column=0, columnspan=3, ipady=10)

        submitBtn = Button(self.RGB_Window, text="SUBMIT", width=12, height=1, command=submit)
        submitBtn.grid(row=2, column=0, columnspan=3, pady=10)

    def PictureOrder(self):

        def submit():
            patt = inputBox.get()
            if len(patt) != 9:
                messagebox.showerror("Error", "Pattern should include only 9 pictures")
            elif self.isRegistering:
                self.PicturePattern = patt
                self.pictureOrderWindow.destroy()
                self.emailInput.destroy()
                self.CreateNewUserBtn.destroy()
                self.closeBtn.config(state=NORMAL)
                self.passwordInput.config(state=NORMAL)
                self.loginBtn.config(state=NORMAL)
                self.removeUserbtn.config(state=NORMAL)
                sq.createUser(self.username, self.password, self.email, self.RGB_Pattern, self.PicturePattern)
                messagebox.showinfo("Success", "User Created Successfully!")
                self.usernameInput.config(state=NORMAL)
                self.usernameInput.delete(0, END)
                self.passwordInput.delete(0, END)
                self.isRegistering = False
            elif not self.isRegistering:
                userCred = sq.getUser()
                userPattern = userCred[0][6]
                if userPattern == patt:
                    self.pictureOrderWindow.destroy()
                    self.appwindow.destroy()
                    MainWindow.main()
                else:
                    self.pictureOrderTrial -=1
                    messagebox.showerror(f"Invalid Pattern!\nYou have {self.pictureOrderTrial} Trials Left")
                    inputBox.config(state=NORMAL)
                    inputBox.delete(0, END)
                    inputBox.config(state=DISABLED)
                    if self.pictureOrderTrial==0:
                        self.pictureOrderWindow.destroy()
                        messagebox.showerror("Error", "Maximum Trials Exceeded!")
                        userCred = sq.getUser ()
                        userEmail = userCred[0][4]
                        _thread.start_new_thread (fa.sendUnAuthorizedEmail, (userEmail,))



        self.pictureOrderWindow = Toplevel(root)
        self.pictureOrderWindow.geometry("800x410")
        self.pictureOrderWindow.title("Picture Order Verification")
        self.pictureOrderTrial = 3

        global background, pic1, pic2, pic3, pic4, pic5, pic6, pic7, pic8, pic9

        background = PhotoImage(file="Backgrounds/backgroundForPictureOrder.png")
        pic1 = PhotoImage(file="PictureOrder/1.png")
        pic2 = PhotoImage(file="PictureOrder/2.png")
        pic3 = PhotoImage(file="PictureOrder/3.png")
        pic4 = PhotoImage(file="PictureOrder/4.png")
        pic5 = PhotoImage(file="PictureOrder/5.png")
        pic6 = PhotoImage(file="PictureOrder/6.png")
        pic7 = PhotoImage(file="PictureOrder/7.png")
        pic8 = PhotoImage(file="PictureOrder/8.png")
        pic9 = PhotoImage(file="PictureOrder/9.png")

        backgroundLabel = Label(self.pictureOrderWindow, image=background).place(x=0, y=0)

        inputBox = Entry (self.pictureOrderWindow, width=50, justify=CENTER, state=DISABLED, show="*")
        inputBox.grid (row=1, column=3, ipady=10)

        submitBtn = Button(self.pictureOrderWindow, text="Submit", command=submit)
        submitBtn.grid(row=2, column=3, pady=10, padx=5)


        btn1 = Button(self.pictureOrderWindow, image=pic1, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "1"), inputBox.config(state=DISABLED)])
        btn2 = Button(self.pictureOrderWindow, image=pic2, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "2"), inputBox.config(state=DISABLED)])
        btn3 = Button(self.pictureOrderWindow, image=pic3, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "3"), inputBox.config(state=DISABLED)])
        btn4 = Button(self.pictureOrderWindow, image=pic4, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "4"), inputBox.config(state=DISABLED)])
        btn5 = Button(self.pictureOrderWindow, image=pic5, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "5"), inputBox.config(state=DISABLED)])
        btn6 = Button(self.pictureOrderWindow, image=pic6, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "6"), inputBox.config(state=DISABLED)])
        btn7 = Button(self.pictureOrderWindow, image=pic7, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "7"), inputBox.config(state=DISABLED)])
        btn8 = Button(self.pictureOrderWindow, image=pic8, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "8"), inputBox.config(state=DISABLED)])
        btn9 = Button(self.pictureOrderWindow, image=pic9, command=lambda :[inputBox.config(state=NORMAL) ,inputBox.insert(END, "9"), inputBox.config(state=DISABLED)])

        btn1.grid(row=0, column=0, pady=5, padx=5)
        btn2.grid(row=0, column=1, pady=5, padx=5)
        btn3.grid(row=0, column=2, pady=5, padx=5)
        btn4.grid(row=1, column=0, pady=5, padx=5)
        btn5.grid(row=1, column=1, pady=5, padx=5)
        btn6.grid(row=1, column=2, pady=5, padx=5)
        btn7.grid(row=2, column=0, pady=5, padx=5)
        btn8.grid(row=2, column=1, pady=5, padx=5)
        btn9.grid(row=2, column=2, pady=5, padx=5)

        text=""
        if self.isRegistering:
            text = "Choose a Picture Pattern Based On your Favorite animals\nPattern should be comprised of all the photos."
        else:
            text = "Enter Pre-set Animal Pattern:"

        registerLabel = Label(self.pictureOrderWindow, text=text).grid(row=0, column=3 )

    def twoFactor(self):

        def submit():
            userInput = codeInput.get()
            if len(userInput) == 0 or userInput != self.random_str:
                self.trialCount -= 1
                messagebox.showerror("Error", f"Invalid Code\n{self.trialCount} Attempts left.")
                if self.trialCount == 0:
                    messagebox.showerror("Error", "Maximum Attempts Reached.")
                    userCred = sq.getUser ()
                    userEmail = userCred[0][4]
                    _thread.start_new_thread (fa.sendUnAuthorizedEmail, (userEmail,))
                    twoFactorWindow.destroy()
            elif userInput == self.random_str:
                self.RGB()
                twoFactorWindow.destroy()

        twoFactorWindow = Toplevel(self.appwindow)
        twoFactorWindow.geometry("350x150")
        twoFactorWindow.title("Two Factor Authentication")

        global twoFatcorBackground
        twoFatcorBackground = PhotoImage(file="Backgrounds/backgroundForRGB.png")
        twoFatcorBackgroundLabel = Label(twoFactorWindow, image=twoFatcorBackground).place(x=0, y=0)

        digits= [i for i in range(0,10)]
        self.random_str = ""
        self.trialCount = 3

        for i in range(6):
            index = math.floor(random.random() * 10)
            self.random_str+= str(digits[index])

        userCred = sq.getUser()
        userEmail = userCred[0][4]

        _thread.start_new_thread(fa.sendVerificationCode, (userEmail, self.random_str,))

        labelText = f"A Code was sent to {userEmail}\nPlease Enter It below to proceed."
        label = Label(twoFactorWindow, text=labelText)
        label.grid(row=0, column=0, padx=40, pady=10)

        codeInput = Entry(twoFactorWindow, width=50, justify=CENTER)
        codeInput.grid(row=1, column=0, ipady=10, columnspan=2)

        submitBtn = Button(twoFactorWindow, text="Submit", command=submit)
        submitBtn.grid(row=2, column=0, pady=10)

    def close(self):
        self.appwindow.destroy ()


root = Tk()
app = LoginScreen()
app.MainScreen(root)
root.mainloop()