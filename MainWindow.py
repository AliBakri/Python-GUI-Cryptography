import datetime
import string
from math import ceil
from tkinter import *           # tkinter is the GUI module in python
from tkinter import ttk, messagebox
import SQLiteDatabase as sq

# Main Page and Main Function for execution

class MainScreen():
    def __init__(self):
        pass
    def main(self, root):
        # Creating parent Application Window
        self.MainScreenWindow = root
        self.MainScreenWindow.resizable(width=False, height=False)
        # Setting the Window Title
        self.MainScreenWindow.title("ICT 444 - FINAL PROJECT")
        # Setting the window size
        self.MainScreenWindow.geometry("1000x500")
        # Importing pre-photoshopped .png Images to use as widget backgrounds
        global bg
        bg = PhotoImage (file="Backgrounds/vintage-brown-paper-with-wrinkles-abstract-old-paper-textures-background_7182-982.png")
        self.btn_caesar_bg = PhotoImage(file ="Backgrounds/btn_caesar_bg.png")
        self.btn_Rail_fence_bg = PhotoImage(file="Backgrounds/btn_RailFence_bg.png")
        self.btn_logs_bg = PhotoImage(file="Backgrounds/logsButton.png")
        self.closeBtn_bg = PhotoImage(file="Backgrounds/close_bg.png")
        # Creating a Main Label that holds the main background and placing it in the middle of the widget
        self.background = Label(self.MainScreenWindow, image=bg).place(x=0, y=0)

        # Creating the Buttons
        # The Button class in tkinter features many options to manipulate button.
        # First we specify a the parent window to attach our widget to.
        # Then we modify the Buttons as needed.

        self.btn_caesar_cipher = Button(self.MainScreenWindow, width=300, height=75, image=self.btn_caesar_bg, command=lambda: [self.MainScreenWindow.withdraw(), self.Caeser()])
        self.btn_rail_fence = Button(self.MainScreenWindow, width=300, height=75, image=self.btn_Rail_fence_bg, command=lambda: [self.MainScreenWindow.withdraw(), self.RailFence()])
        self.btn_logs = Button(self.MainScreenWindow, width=300, height=75, image=self.btn_logs_bg, command=lambda : [self.MainScreenWindow.withdraw(), self.Logs()])
        self.closeBtn = Button(self.MainScreenWindow, width=300, height=75, image=self.closeBtn_bg, command=lambda: [self.MainScreenWindow.destroy()])

        # The destroy() method closes the app window specified
        # So it was used with conjuction with another function so when we open a certain screen, the main one disappears.
        # When dealing the multiple methods or methods that require parameters, we use command=lambda:

        # Placing the Buttons per the grid system and applying some corresponding paddings.
        self.btn_caesar_cipher.pack(padx=20, pady=10)
        self.btn_rail_fence.pack(padx=20, pady=10)
        self.btn_logs.pack(padx=20, pady=10)
        self.closeBtn.pack(padx=20, pady=10)


        # mainloop() keeps the window running, without it the window  does not show
        self.MainScreenWindow.mainloop()

    def Caeser(self):

        # Encryption Method using ascii Positioni
        def encryption():
            type = 'ENCRYPT'
            try:
                message = str (self.message_Entry.get ("1.0", 'end-1c'))
                rotations = self.rotations.get ()
                if message == "":
                    messagebox.showerror ("Error", "Please Enter A Message.")
                elif self.rotations.get () == "":
                    messagebox.showerror ("Error", "Please Specify Number of Rotations.")
                elif int (rotations) not in range (1, 26):
                    messagebox.showerror ("Error", "Wrong Rotation Value!")
                else:
                    result = ""
                    for i in range (len (message)):
                        char = message[i]
                        if char.isupper ():
                            result += chr ((ord (char) + int (rotations) - 65) % 26 + 65)
                        elif char == " ":
                            pass
                        else:
                            result += chr ((ord (char) + int (rotations) - 97) % 26 + 97)
                    self.message_Entry.delete (1.0, END)
                    self.message_Entry.insert (END, f"MESSAGE: {message}\nCipher: {result}")
                    self.message_Entry.config (state=DISABLED)
                    self.rotations.config (state=DISABLED)
                    self.rotations_1.config (state=DISABLED)
                    self.encrypt_btn.config (state=DISABLED)
                    self.decrypt_btn.config (state=DISABLED)
                    self.btn_bruteForce.config (state=DISABLED)
                    sq.add_Caeser_cipher (type, str (result), int (rotations), str (message),
                                          str (datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y")))
            except ValueError:
                messagebox.showwarning ("Error", "Wrong Input!")

        # Decryption Method Using A Variable Containing the Alphabets
        def decryption():
            type = 'DECRYPTION'
            try:
                message = self.message_Entry.get ("1.0", END)
                rotation = self.rotations_1.get ()
                decryption = ""

                if message == "":
                    messagebox.showerror ("Error", "Please Enter CipherText!")
                elif rotation == "":
                    messagebox.showerror ("Error", "Please Specify Rotation key!")
                elif int (rotation) not in range (1, 26):
                    messagebox.showerror ("Error", "Wrong Rotation Value!")
                else:
                    alphabet = string.ascii_letters

                    for c in message:
                        if c in alphabet:
                            position = alphabet.find (c)
                            new_position = (position - int (rotation)) % 26
                            new_character = alphabet[new_position]
                            decryption += new_character
                        else:
                            decryption += c

                    self.message_Entry.delete (1.0, END)
                    self.message_Entry.insert (END, f"Cipher: {message}\nMessage: {decryption}")
                    self.message_Entry.config (state=DISABLED)
                    self.rotations.config (state=DISABLED)
                    self.rotations_1.config (state=DISABLED)
                    self.encrypt_btn.config (state=DISABLED)
                    self.decrypt_btn.config (state=DISABLED)
                    self.btn_bruteForce.config (state=DISABLED)
                    sq.add_Caeser_cipher (type, message, float (rotation), decryption,
                                          datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y"))

            except ValueError:
                messagebox.showwarning ("Error", "Wrong Input!")

        # Brute Forcing using the Same Decryption Method
        def brute_force():
            message = self.message_Entry.get ("1.0", 'end-1c')
            if len (message) == 0:
                messagebox.showerror ("Error", "Please Enter CipherText!")
            else:
                alphabet = string.ascii_letters
                decryptions = ""
                decryptions_list = []
                for key in range (0, len (alphabet)):
                    if key > 25:
                        break
                    translated = ''
                    for c in message:
                        if c in alphabet:
                            position = alphabet.find (c)
                            new_position = (position - int (key)) % 26
                            new_character = alphabet[new_position]
                            translated += new_character
                        else:
                            translated += c

                    decryptions += "K = " + str (key) + ": " + translated + "\n"
                    decryptions_list.append ([translated, key])
                self.correct_decryptions = []
                for decryption in decryptions_list:
                    for word in self.word_List:
                        found = decryption[0].lower ().find (str (word).lower ())
                        if found >= 0 and len (word) >= 5:
                            self.correct_decryptions.append (decryption)
                            break
                correct_decryptions_string = ""
                for dec in self.correct_decryptions:
                    correct_decryptions_string += f"K={dec[1]}, {dec[0]}\n"
                final_message = decryptions + "\nPossible Correct Ciphers:\n---------------------------------------\n\n" + correct_decryptions_string
                self.message_Entry.delete (1.0, END)
                self.message_Entry.insert (END, final_message)
                self.message_Entry.config (state=DISABLED)
                self.rotations.config (state=DISABLED)
                self.rotations_1.config (state=DISABLED)
                self.encrypt_btn.config (state=DISABLED)
                self.decrypt_btn.config (state=DISABLED)
                self.btn_bruteForce.config (state=DISABLED)
                sq.add_Caeser_cipher ("BRUTE FORCE", message, "N/A", final_message,
                                      datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y"))

        # Clearing All the widgets and reverting Disabled States
        def clear():
            self.message_Entry.delete (1.0, END)
            self.rotations.delete (0, END)
            self.rotations_1.delete (0, END)
            self.message_Entry.config (state=NORMAL)
            self.rotations.config (state=NORMAL)
            self.rotations_1.config (state=NORMAL)
            self.encrypt_btn.config (state=NORMAL)
            self.decrypt_btn.config (state=NORMAL)
            self.btn_bruteForce.config (state=NORMAL)

        # Closing the Page and returning to main
        def close():
            self.appwindow.destroy ()
            self.MainScreenWindow.deiconify()
        # Creating the word list from an external .txt file and saving it as a python list for use in brute forcing Caeser
        self.wordList_file = open("Wordlist.txt", "r")
        self.content = self.wordList_file.read()
        self.word_List = self.content.split("\n")
        self.wordList_file.close()


        # Removing words of length less that 4
        # This is done to minimize false positives for language detection
        # for Example, there is a large likelihood to find a 2-letter word in a cipher such as "to" "if" "so"
        # this way, if a 4 letter word like "king" was found, this deciphering can be a possible solution.
        for word in self.word_List:
            if len(word) < 4:
                self.word_List.remove(word)

        # Same methods as main() function
        # Creating main RGB_WINDOW, creating widgets and assigning commands for buttons
        self.appwindow = Toplevel(self.MainScreenWindow)
        self.appwindow.resizable(height=False, width=False)
        self.bg = PhotoImage (file="Backgrounds/Bakgrounf_for_Ceaser_Cipher.png")
        self.encrypt_label_bg = PhotoImage(file="Backgrounds/encrypt_label_bg.png")
        self.rotation_label_bg = PhotoImage(file="Backgrounds/encrypt_label_bg copy.png")
        self.rotation_label_bg_Derypt = PhotoImage(file="Backgrounds/encrypt_label_bg copy 2.png")
        self.bruteForce_bg = PhotoImage(file="Backgrounds/brute_force_bg.png")
        self.close_btn_bg = PhotoImage(file="Backgrounds/close_bg.png")
        self.clear_btn_bg = PhotoImage(file="Backgrounds/Rail_fence_clearButton.png")
        self.appwindow.geometry("350x500")
        self.appwindow.title("Caesar Cipher: Encrypt - Decrypt - Brute Force")
        self.background = Label(self.appwindow, image=self.bg).place(x=0, y=0)

        self.encrypt_label = Label(self.appwindow, image=self.encrypt_label_bg, width=125, height=25)
        self.encrypt_label.grid(row=0, column=0, pady=10)

        self.clear_btn = Button(self.appwindow, image=self.clear_btn_bg, width=125, height=25, command=lambda : [clear(), clear()])
        self.clear_btn.grid(row=0, column=1)

        self.message_Entry = Text(self.appwindow, width=40, height=10, relief=SUNKEN, borderwidth=2)
        self.message_Entry.grid(row=1, column=0, columnspan=2, padx=5)

        self.encrypt_btn = Button(self.appwindow, image=self.rotation_label_bg, width=125, height=25, command=encryption)
        self.encrypt_btn.grid(row=2, column=0, pady=10)
        self.categories = ("", "1", "2", "3", "4", "5", "6", "7", "8", "9","10",
                           "11", "12", "13", "14", "15", "16", "17", "18", "19",
                           "20", "21", "22", "23", "24", "25")
        self.rotations = ttk.Combobox(self.appwindow, values=self.categories)
        self.rotations.grid(row=2, column=1, columnspan=1)

        self.decrypt_btn = Button(self.appwindow, image=self.rotation_label_bg_Derypt, width=125, height=25, command=decryption)
        self.decrypt_btn.grid(row=3, column=0)

        self.rotations_1 = ttk.Combobox (self.appwindow, values=self.categories)
        self.rotations_1.grid (row=3, column=1, columnspan=1)

        self.btn_bruteForce = Button(self.appwindow, image=self.bruteForce_bg, width=330, height=25, command=brute_force)
        self.btn_bruteForce.grid(row=4, column=0, columnspan=2, pady=10, padx=10)

        self.btn_close = Button (self.appwindow, image=self.close_btn_bg, width=330, height=25, command=close)
        self.btn_close.grid (row=5, column=0, columnspan=2, padx=10)

        self.appwindow.mainloop()

    def RailFence(self):

        def encryption():
            password = self.key_entry.get ()
            message_str = self.message_Entry.get ("1.0", "end-1c")

            if len (password) == 0:
                messagebox.showerror ("Error", "Please Enter a password!")
            elif len (message_str) == 0:
                messagebox.showerror ("Error", "Please Enter Text!")
            else:
                message = [i for i in message_str]
                column_num = len (password)
                row_num = ceil (len (message) / column_num)
                cnt = 0
                result = []

                for row in range (0, row_num):
                    col = []
                    for columns in range (0, column_num):
                        if cnt < len (message):
                            col.append (message[cnt])
                        else:
                            col.append ("x")
                        cnt += 1
                    result.append (col)

                result_Encrypted = []
                for col1 in range (0, column_num):
                    c = []
                    for row1 in range (0, row_num):
                        c.append (result[row1][col1])
                    result_Encrypted.append (c)

                result_Dict = {}
                cnt = 0
                for char in password:
                    result_Dict[char] = result_Encrypted[cnt]
                    cnt += 1

                final_result = ""
                pass_alpha = sorted ([j for j in password])

                for letter in pass_alpha:
                    for letters in result_Dict[letter]:
                        final_result += letters

                self.message_Entry.delete ("1.0", "end")

                final_result_formatted = f"Message: {message_str}\nCipher: {final_result}"

                self.message_Entry.insert (END, final_result_formatted)
                self.message_Entry.config (state=DISABLED)
                self.encrypt_key_btn.config (state=DISABLED)
                self.decrypt_key_btn.config (state=DISABLED)
                sq.add_RailFence ("ENCRYPT", password, final_result, message_str,
                                  datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y"))

        # Decryption Using Class method
        def decryption():
            password = self.key_entry.get ()
            text = self.message_Entry.get ("1.0", "end-1c")
            if len (password) == 0:
                messagebox.showerror ("Error", "Please Enter a password!")
            elif len (text) == 0:
                messagebox.showerror ("Error", "Please Enter Text!")
            else:
                token_len = int (len (text) / len (password))
                chunks, chunk_size = len (text), token_len
                tokens = [text[i:i + chunk_size] for i in range (0, chunks, chunk_size)]
                pass_list = sorted (char for char in password)
                encryption_dict = {}

                for letter, encryption in zip (pass_list, tokens):
                    encryption_dict[letter] = encryption
                result = []
                for character in password:
                    result.append (encryption_dict[character])

                row = len (password)
                col = token_len
                final_result_list = []

                for i in range (len (result[0])):
                    cols = []
                    for j in range (len (result)):
                        cols.append (result[j][i])
                    final_result_list.append (cols)

                final_result_string = ""

                for letters in final_result_list:
                    for letter in letters:
                        final_result_string += letter

                self.message_Entry.delete ("1.0", "end")

                final_result_formatted = ""

                for letter in password:
                    final_result_formatted += letter + "\t"
                final_result_formatted += "\n--------------------------------------------------------\n"

                newline_count = 1
                for letter in final_result_string:
                    final_result_formatted += letter + "\t"
                    if newline_count % (len (password)) == 0:
                        final_result_formatted += "\n"
                    newline_count += 1

                final_result_formatted += "-------------------------------------------------------\n"
                final_result_formatted += f"Cipher: /{text}/\n"
                final_result_formatted += f"Message: /{final_result_string}/"

                self.message_Entry.insert (END, final_result_formatted)
                self.message_Entry.config (state=DISABLED)
                self.encrypt_key_btn.config (state=DISABLED)
                self.decrypt_key_btn.config (state=DISABLED)
                sq.add_RailFence ("DECRYPT", password, text, final_result_string,
                                  datetime.datetime.now ().strftime ("%I:%M%p on %B %d, %Y"))

        # Clearing all the widgets and revertind Disabled States
        def clear():
            self.message_Entry.delete (1.0, END)
            self.key_entry.delete (0, END)
            self.message_Entry.config (state=NORMAL)
            self.encrypt_key_btn.config (state=NORMAL)
            self.decrypt_key_btn.config (state=NORMAL)

        # Closing the window and returning to main Screen
        def close():
            self.RailFenceWindow.destroy ()
            self.MainScreenWindow.deiconify()

        self.RailFenceWindow = Toplevel(self.MainScreenWindow)
        self.RailFenceWindow.resizable (height=False, width=False)
        self.bg = PhotoImage (file="Backgrounds/background_for_rail_fence.png")
        self.key_label_bg = PhotoImage (file="Backgrounds/Rail_fence_keyMessage.png")
        self.encrypt_label_bg = PhotoImage (file="Backgrounds/encrypt_label_bg.png")
        self.key_entry_bg = PhotoImage (file="Backgrounds/encryptforkeylength.png")
        self.close_btn_bg = PhotoImage (file="Backgrounds/close_bg.png")
        self.clear_btn_bg = PhotoImage (file="Backgrounds/Rail_fence_clearButton.png")
        self.RailFenceWindow.geometry ("500x500")
        self.RailFenceWindow.title ("Rail-Fence: Encrypt - Decrypt")
        self.background = Label (self.RailFenceWindow, image=self.bg).place (x=0, y=0)

        self.encrypt_label = Label (self.RailFenceWindow, text="Encrypt", font=("Old English Text MT", 14),
                                    image=self.encrypt_label_bg, width=125, height=25)
        self.encrypt_label.grid (row=0, column=0, pady=10, columnspan=2)

        self.message_Entry = Text (self.RailFenceWindow, width=59, height=12, relief=SUNKEN, borderwidth=2)
        self.message_Entry.grid (row=1, column=0, columnspan=2, padx=12.5)

        self.decrypt_key_btn = Button (self.RailFenceWindow, image=self.key_label_bg, width=175, height=25,
                                       command=decryption)
        self.decrypt_key_btn.grid (row=2, column=0, pady=10, columnspan=2)

        self.encrypt_key_btn = Button (self.RailFenceWindow, image=self.key_entry_bg, width=175, height=25,
                                       command=encryption)
        self.encrypt_key_btn.grid (row=3, column=0, columnspan=2)

        self.key_entry = Entry (self.RailFenceWindow, relief=RIDGE, width=30, justify=CENTER)
        self.key_entry.grid (row=4, column=0, columnspan=2, pady=10)

        self.clear_btn = Button (self.RailFenceWindow, image=self.clear_btn_bg, width=175, height=25,
                                 command=lambda: [clear (), clear ()])
        self.clear_btn.grid (row=5, column=0, columnspan=2)

        self.close_button = Button (self.RailFenceWindow, image=self.close_btn_bg, width=175, height=25,
                                    command=close)
        self.close_button.grid (row=6, column=0, columnspan=2, pady=10)

        self.RailFenceWindow.mainloop ()

    def Logs(self):

        def caeserCipher_IsChecked():
            caeserLogs = sq.get_CaeserCipherLog ()
            self.logList.delete (0, END)
            for log in caeserLogs:
                spacing = "  "
                body = f"{log[0]}{4 * spacing}{log[5]}{4 * spacing}{log[1]}"
                self.logList.insert (END, body)

            self.checkBox_RailFence.deselect ()

        def railFence_IsChecked():
            railFenceLogs = sq.get_RailFenceLog ()
            self.logList.delete (0, END)
            for log in railFenceLogs:
                spacing = "  "
                body = f"{log[0]}{4 * spacing}{log[5]}{4 * spacing}{log[1]}"
                self.logList.insert (END, body)

            self.checkBox_CaeserCipher.deselect ()

        def onLogClick(event):
            selection = event.widget.curselection ()
            if selection:
                self.informationtext.config (state=NORMAL)
                self.informationtext.delete ("1.0", END)
                index = selection[0]
                data = event.widget.get (index)
                ID = data[0]

                if self.var1.get () == 1:
                    logData = sq.get_CaeserCipherLogPerID (ID)
                    body = ""
                    if logData[1] == "ENCRYPT" or logData[1] == "DECRYPTION":
                        body += f"Original Message:\n{logData[4]}\n\n"
                        body += f"Cipher:\n{logData[2]}\n\n"
                        body += f"key:\n{logData[3]}\n\n"
                    else:
                        body += f"Cipher:\n{logData[2]}\n\n"
                        body += f"Decryptions:\n{logData[4]}\n\n"
                    self.informationtext.insert (END, body)
                    self.informationtext.config (state=DISABLED)
                elif self.var2.get () == 1:
                    logData = sq.get_RailFenceLogPerID (ID)
                    body = ""
                    body += f"Original Message:\n{logData[4]}\n\n"
                    body += f"Cipher:\n{logData[3]}\n\n"
                    body += f"Password:\n{logData[2]}\n\n"
                    self.informationtext.insert (END, body)
                    self.informationtext.config (state=DISABLED)
                else:
                    return

        def clearLogs():
            sq.clear_all_logs ()
            self.logList.delete (0, "end")
            self.informationtext.config (state=NORMAL)
            self.informationtext.delete ("1.0", END)
            self.checkBox_CaeserCipher.deselect ()
            self.checkBox_RailFence.deselect ()
            self.informationtext.config (state=DISABLED)

        def close():
            self.LogsScreen.destroy ()
            self.MainScreenWindow.deiconify()

        self.LogsScreen = Toplevel(self.MainScreenWindow)
        self.LogsScreen.resizable (height=False, width=False)
        self.LogsScreen.title ("Logs")
        self.LogsScreen.geometry ("935x500")
        self.background_bg = PhotoImage (file="Backgrounds/BackgroundForLogs.png")
        self.caeser_Check_bg = PhotoImage (file="Backgrounds/caeserCipherCheckbox.png")
        self.railfence_Check_bg = PhotoImage (file="Backgrounds/RailFenceCheckbox.png")
        self.close_bg = PhotoImage (file="Backgrounds/close_bg.png")
        self.clear_bg = PhotoImage (file="Backgrounds/Rail_fence_clearButton.png")
        self.background = Label (self.LogsScreen, image=self.background_bg).place (x=0, y=0)

        self.var1 = IntVar ()
        self.var2 = IntVar ()

        self.checkBox_CaeserCipher = Checkbutton (self.LogsScreen, image=self.caeser_Check_bg,
                                                  command=caeserCipher_IsChecked,
                                                  width=100, height=25, variable=self.var1)
        self.checkBox_RailFence = Checkbutton (self.LogsScreen, image=self.railfence_Check_bg,
                                               command=railFence_IsChecked,
                                               width=100, height=25, variable=self.var2)
        self.closeButton = Button (self.LogsScreen, image=self.close_bg, command=close, width=175, height=25)
        self.clearLogsBtn = Button (self.LogsScreen, image=self.clear_bg, command=clearLogs, width=175, height=25)

        self.logList = Listbox (self.LogsScreen, width=100, height=25, relief="sunken")
        self.logList.bind ("<<ListboxSelect>>", onLogClick)
        self.informationtext = Text (self.LogsScreen, width=39, height=25)

        self.checkBox_CaeserCipher.grid (row=0, column=0, sticky="w", pady=5, padx=5)
        self.checkBox_RailFence.grid (row=0, column=1, sticky="w", pady=5)
        self.logList.grid (row=2, column=0, columnspan=3, padx=5, sticky="w")
        self.informationtext.grid (row=2, column=3, columnspan=2, sticky="e")
        self.closeButton.grid (row=3, column=0, sticky="w", padx=5, pady=10, columnspan=2)
        self.clearLogsBtn.grid (row=3, column=1, sticky="w", padx=5, pady=10, columnspan=2)
        self.LogsScreen.mainloop ()

def main():
    root = Tk()
    app = MainScreen()
    app.main (root)










