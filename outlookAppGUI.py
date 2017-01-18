#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
import time
import janitor
import paths
from PIL import ImageTk, Image
from cryptography.fernet import Fernet
# Author ~ WileTheCoyote

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        # on initialize load intro page
        self.introPage()
    
    def introPage(self):
        # intro page is the first page of our GUI the user will see
        self.grid()
        
        # use _meipass temporary folder to store path of logo
        Logo = paths.resource_path("jan.jpg")
        
        # find absolute path of usernameFile and passwordFile which will store
        # our email address its corresponding password        
        self.userFileAbsolutePath = paths.absolute_path("userFile.txt")
        self.passFileAbsolutePath = paths.absolute_path("passFile.txt")
        
        # open, resize, and display image
        self.load = Image.open(Logo)
        self.load = self.load.resize((115, 115), Image.ANTIALIAS)
        self.render = ImageTk.PhotoImage(self.load)
        
        # place image in img label and place on window
        # this element (logo) will not be removed and thus
        # will exist for every page of GUI (not just intro page)
        self.img = Tkinter.Label(self, image=self.render)
        self.img.image = self.render
        self.img.place(x=0, y=148)
        
        # key for encryting and decrypting password data
        key = 'Alj0UzPBA0GqJc7VU3S1cYXhtGu0OvoGbS0ZdprRS5I='
        # implement key using Fernet symmetric authenticated cryptography
        self.cipher_suite = Fernet(key)
        
        # The main idea of this feature is that a user that uses the
        # Email Janitor may find it tiresome re-entering their username and
        # password upon each use of the application. So upon a successful login
        # the application saves the username and password (encrypted) to a file,
        # which then can be used to populate the entry fields upon the next
        # initialization of the program.
        
        # first try and read from username and password text files
        try:
           self.userNameFile = open(self.userFileAbsolutePath, "r")
           self.passWordFile = open(self.passFileAbsolutePath, "r")
        
        # if unsuccesful then the text files do not exist, if so then..
        except:
           # create text files
           self.userNameFile = open(self.userFileAbsolutePath, "w")
           self.passWordFile = open(self.passFileAbsolutePath, "w")
           print self.userFileAbsolutePath
           print "hello"
           # write to file with example username; email address
           self.userNameFile.write("sample@msn.com")
           # write to file with example password (encrypted)
           cipherTextPassword = self.cipher_suite.encrypt("abcdefghij")
           self.passWordFile.write(cipherTextPassword)
           # lastly read from newly created files
           self.userNameFile = open(self.userFileAbsolutePath, "r")
           self.passWordFile = open(self.passFileAbsolutePath, "r")
           pass
        
        # set last used username name and password using text file
        self.lastPassWordUsed = self.passWordFile.read()
        self.lastUserNameUsed = self.userNameFile.read()
        # decrypt password from text word
        plainTextPassword = self.cipher_suite.decrypt(self.lastPassWordUsed)
        
        # if last username used is empty, we want to over write it with a default
        # email address. - note this is more or less a sanity check and ensures our
        # email entry field is either populated with that last used email address
        # used in a successful login or our sample default address.
        # The only true way lastUserNameUsed should be empty is if someone
        # manually opened our username text file and deleted the content
        if self.lastUserNameUsed == "":
            self.userNameFile = open(self.userFileAbsolutePath, "w")
            self.userNameFile.write("sample@msn.com")
            self.userNameFile = open(self.userFileAbsolutePath, "r")
            self.lastUserNameUsed = self.userNameFile.read()
        
        # create entry field and variable for our user's email
        self.emailEntryVariable = Tkinter.StringVar()
        self.emailEntry = Tkinter.Entry(self,textvariable=self.emailEntryVariable)
        # use grid to place its location on page, sticky option specifies in the
        # part of the cell (in grid) that the element (entry field) sits
        self.emailEntry.grid(column=0,row=2, columnspan=4, sticky='EW')
        # bind event, while cursor is in emailEntry field the user presses enter
        self.emailEntry.bind("<Return>", self.OnPressEnterAddress)
        # bind event, when user clicks on emailEntry field
        self.emailEntry.bind("<Button-1>", self.OnEmailFieldClick)
        # populate initial value of emailEntry to contain last username used
        self.emailEntryVariable.set(self.lastUserNameUsed)

        # create entry field and variable for our user's email password
        self.passwordEntryVariable = Tkinter.StringVar()
        self.passwordEntry = Tkinter.Entry(self,textvariable=self.passwordEntryVariable)
        # use grid to place its location on page
        self.passwordEntry.grid(column=0,row=4, columnspan=4, sticky='EW')
        # bind event, while cursor is in password field the user presses enter
        self.passwordEntry.bind("<Return>", self.OnPressEnterPassword)
        # bind event, when user clicks on password field
        self.passwordEntry.bind("<Button-1>", self.OnPassFieldClick)
        # populate initial value of emailEntry to contain last password used
        self.passwordEntryVariable.set(plainTextPassword)
        # hide password from view by showing * symbol instead of characters
        self.passwordEntry.config(show="*")

        # create login button and place on page
        self.loginButton = Tkinter.Button(self,text=u"Login", command=self.OnLoginClick)
        self.loginButton.grid(column=3,row=9, sticky='E')

        # create label for title of page
        self.titleLabelVariable = Tkinter.StringVar()
        self.titleLabel = Tkinter.Label(self,textvariable=self.titleLabelVariable, anchor="center",fg="white",bg="blue")
        self.titleLabel.grid(column=0,row=0,columnspan=4,sticky='EW')
        self.titleLabelVariable.set(u"Email Log-in")

        # create label for email entry title
        self.emailEntryLabelVariable = Tkinter.StringVar()
        self.emailEntryLabel = Tkinter.Label(self,textvariable=self.emailEntryLabelVariable, anchor="w",fg="black",bg="white")
        self.emailEntryLabel.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.emailEntryLabelVariable.set(u"Email Address  ")

        # create label for password entry title
        self.passwordEntryLabelVariable = Tkinter.StringVar()
        self.passwordEntryLabel = Tkinter.Label(self,textvariable=self.passwordEntryLabelVariable, anchor="w",fg="black",bg="white")
        self.passwordEntryLabel.grid(column=0,row=3,columnspan=2,sticky='EW')
        self.passwordEntryLabelVariable.set(u"Password")

        # create invisible border label which is empty (only contains spaces) but
        # helps stretch our page to desired width
        self.invisibleBorderLabelVariable = Tkinter.StringVar()
        self.invisibleBorderLabel = Tkinter.Label(self,textvariable=self.invisibleBorderLabelVariable, anchor="w",fg="black",bg="white")
        self.invisibleBorderLabel.grid(column=2,row=6,columnspan=1,sticky='EW')
        self.invisibleBorderLabelVariable.set(u"                ")

        # create login detail label
        self.loginDetailLabelVariable = Tkinter.StringVar()
        self.loginDetailLabel = Tkinter.Label(self,textvariable=self.loginDetailLabelVariable, anchor="w",fg="blue",bg="white")
        self.loginDetailLabel.grid(column=0,row=5,columnspan=4,sticky='EW')
        self.loginDetailLabelVariable.set(u"~ Works with all Microsoft domains i.e. Outlook, Hotmail, MSN, and Live")
        self.loginDetailLabel.config(font=("TkDefaultFont", 10))
       
        # label and labelBlank are both also invisible and simply ensure correct
        # stretching of intro page to desired size
        self.labelVariable = Tkinter.StringVar()
        self.label = Tkinter.Label(self,textvariable=self.labelVariable, anchor="w",fg="white",bg="white")
        self.label.grid(column=3,row=7,columnspan=1, rowspan = 1, sticky='EW')
        self.labelVariable.set(u" \nsdsd")
        self.labelBlankVariable = Tkinter.StringVar()
        self.labelBlank = Tkinter.Label(self,textvariable=self.labelBlankVariable, anchor="w",fg="white",bg="white")
        self.labelBlank.grid(column=3,row=8,columnspan=1, rowspan = 1, sticky='EW')
        self.labelBlankVariable.set(u" \nsds")

        # configue, resize, and set geometry of page
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())

        # set cursor to email field, selecting (highlighting) entire text in field
        self.emailEntry.focus_set()
        self.emailEntry.selection_range(0, Tkinter.END)
    
    def optionsPage(self):
        # optionsPage is the second page in the GUI and allows user to specifiy
        # "spam" words that the program will search for in an email's address
        # i.e. user wants to delete all emails that have amazon in the email
        # address
        
        # this section hides or destroys elements from the prev. page (introPage)
        self.loginDetailLabel.grid_forget()
        self.emailEntry.destroy()
        self.passwordEntry.destroy()
        self.titleLabel.grid_forget()
        self.emailEntryLabel.grid_forget()
        self.passwordEntryLabel.grid_forget()
        self.loginButton.grid_forget()
        self.labelVariable.set(u" ")
        self.grid()
        
        # create continue button which takes us to next page
        self.continueButton = Tkinter.Button(self,text=u"Continue", command=self.OnContinueClick)
        self.continueButton.grid(column=3,row=7)
        
        # create add button which adds a new word to our list of "spam" words
        self.addButton = Tkinter.Button(self,text=u"Add", command=self.OnAddClick)
        self.addButton.grid(column=2,row=7, sticky='W')
        
        # intialize list for "spam" words
        self.wordList = []
        
        # create entry field for user to enter in "spam" words
        self.wordEntryVariable = Tkinter.StringVar()
        self.wordEntry = Tkinter.Entry(self,textvariable=self.wordEntryVariable)
        self.wordEntry.grid(column=0,row=7, columnspan=2, sticky='EW')
        # bind event, cursor is in wordEntry Field and user presses enter
        self.wordEntry.bind("<Return>", self.OnPressEnterAdd)
        # bind event, user clicks on wordEntry field
        self.wordEntry.bind("<Button-1>", self.OnAddFieldClick)
        # populate wordEntry field with example text
        self.wordEntryVariable.set(u"i.e. Target")
        
        # create label for title of optionsPage
        self.labelVariable = Tkinter.StringVar()
        self.label = Tkinter.Label(self,textvariable=self.labelVariable, anchor="center",fg="white",bg="blue")
        self.label.grid(column=0,row=0,columnspan=4, sticky='EW')
        self.labelVariable.set(u" Deletion Options")
        
        # create message label with decription for adding words to "spam" list
        self.label2Variable = Tkinter.StringVar()
        self.label2 = Tkinter.Message(self,textvariable=self.label2Variable, anchor="w",fg="black",bg="white", width=305)
        self.label2.grid(column=0,row=5,columnspan=5, sticky='EW')
        self.label2Variable.set("Add a word if you want the Janitor to also delete an email if its address contains a given word")
        
        # create messafe label with detail about adding words to "spam" list
        self.label3Variable = Tkinter.StringVar()
        self.label3 = Tkinter.Message(self,textvariable=self.label3Variable, anchor="w",fg="blue",bg="white", width=305)
        self.label3.grid(column=0,row=6,columnspan=5, sticky='EW')
        self.label3Variable.set("~ By default emails are only deleted if they have one of our preset spam patterns")
        self.label3.config(font=("TkDefaultFont", 10))
        
        # configue, resize, and set geometry of page
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())
    
    def mailboxPage(self):
        # mailboxPage is the third page in our GUI
        
        # this section hides elements from the prev. page (optionsPage)
        self.wordEntry.grid_forget()
        self.addButton.grid_forget()
        self.label2.grid_forget()
        self.label3.grid_forget()
        self.passwordEntryLabel.grid_forget()
        self.continueButton.grid_forget()
        self.labelVariable.set(u" ")
        self.grid()
        
        # create junk button so user can specify specific mailbox
        self.junkButton = Tkinter.Button(self,text=u"Junk", command=self.OnJunkClick)
        self.junkButton.grid(column=3,row=5)
        
        # create inbox button so user can specify specific mailbox
        self.inboxButton = Tkinter.Button(self,text=u"Inbox", command=self.OnInboxClick)
        self.inboxButton.grid(column=2,row=5, sticky='E')
        
        # create exit button, so program terminates
        self.exitButton = Tkinter.Button(self,text=u"Exit", command=self.OnExitClick)
        self.exitButton.grid(column=3,row=7, sticky='E')

        # create label for title of mailboxPage
        self.labelVariable = Tkinter.StringVar()
        self.label = Tkinter.Label(self,textvariable=self.labelVariable, anchor="w",fg="white",bg="blue")
        self.label.grid(column=0,row=0,columnspan=4, sticky='EW')
        self.labelVariable.set(u" Select Mailbox to delete from")
        
        # create label which adds blue line simply for aesthetics
        self.label2Variable = Tkinter.StringVar()
        self.label2 = Tkinter.Label(self,textvariable=self.label2Variable, anchor="w",fg="white",bg="blue")
        self.label2.grid(column=0,row=6,columnspan=4, sticky='EW')
        self.label2Variable.set(u" ")
        
        # configue, resize, and set geometry of page
        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,False)
        self.update()
        self.geometry(self.geometry())


    def OnLoginClick(self):
        # for introPage, user tries to log on to server
        
        # create instance of Janitor class; initializing class
        self.janitorInst = janitor.Janitor(self.emailEntryVariable.get(), self.passwordEntryVariable.get())
        # use username and password to attempt and login to server
        # save logOn()'s returned value to message, this tells if login was
        # successful
        message = self.janitorInst.logOn()
        
        # print to terminal if login was successful
        if message == 0:
           print "[Credentials Accepted] Login Successful"
        
        if message == 1:
                
           # Try and print labelBlank2, if you can't, it means it doesn't exist
           # and thus create it, if you can, do nothing and move on.
           # this keeps us from creating multiple instances of the label
           try:
               print self.labelBlank2Variable.get()
           except:
               # if reached, it means that this is the first failed login attempt
               self.labelBlank2Variable = Tkinter.StringVar()
               self.labelBlank2 = Tkinter.Label(self,textvariable=self.labelBlank2Variable, anchor="w",fg="red",bg="white")
               self.labelBlank2.grid(column=2,row=9, sticky='E')
               self.labelBlank2Variable.set("Login Failed..")
               pass
           
           # we must hide or destroy elements of introPage before we re-initialize
           # the page and re-call the introPage() function
           self.loginDetailLabel.grid_forget()
           self.emailEntry.destroy()
           self.passwordEntry.destroy()
           self.titleLabel.grid_forget()
           self.emailEntryLabel.grid_forget()
           self.passwordEntryLabel.grid_forget()
           self.loginButton.grid_forget()
           self.labelVariable.set(u" ")

           # if our login failed than rewrite username and password text files
           # to the default values
           self.userNameFile = open(self.userFileAbsolutePath, "w")
           self.passWordFile = open(self.passFileAbsolutePath, "w")
           self.userNameFile.write("sample@msn.com")
           cipherTextPassword = self.cipher_suite.encrypt("abcdefghij")
           self.passWordFile.write(cipherTextPassword)

           # call introPage() again
           self.introPage()
        else:
           # if reached, login was successful
           
           # write new successful login credentials to text file
           self.userNameFile = open(self.userFileAbsolutePath, "w")
           self.passWordFile = open(self.passFileAbsolutePath, "w")
           self.userNameFile.write(self.emailEntryVariable.get())
           cipherTextPassword = self.cipher_suite.encrypt(self.passwordEntryVariable.get())
           self.passWordFile.write(cipherTextPassword)
           
           # try and delete the "Login Failed" label if you can't, it means
           # it doesn't exist and our login was successful on first attempt
           try:
              self.labelBlank2.grid_forget()
           except:
              pass
           
           # call next page (options page)
           self.optionsPage()
    
    def OnContinueClick(self):
        # for optionsPage, continue to next page (mailboxPage)
        
        # try and set word list title, if unsuccessful it means no "spam" words
        # were specified
        try:
           self.wordTitleVariable.set("Flagged Words:")
        except:
           pass
        
        # call last page (mailbox page)
        self.mailboxPage()


    def OnAddClick(self):
        # for optionsPage, adds word to "spam" word list by button click
        
        # if wordEntry field is not empty
        if self.wordEntry.get() != "":
            
            # add text in wordEntry field to wordList but delete any spaces
            self.wordList.insert(0, self.wordEntry.get().replace(" ", ""))
            
            # delete text from field
            self.wordEntry.delete(0, 'end')
            
            # move cursor to wordEntry field
            self.wordEntry.focus_set()
            self.wordEntry.selection_range(0, Tkinter.END)
            
            # create message label for title of wordList
            self.wordTitleVariable = Tkinter.StringVar()
            self.wordTitleLabel = Tkinter.Message(self,textvariable=self.wordTitleVariable, anchor="w",fg="black",bg="white", width=100)
            self.wordTitleLabel.grid(column=2,row=8,columnspan=1, sticky='N')
            self.wordTitleVariable.set("Added Words:")
            
            # create message label for all words added by user
            self.wordVariable = Tkinter.StringVar()
            self.wordLabel = Tkinter.Message(self,textvariable=self.wordVariable, anchor="w",fg="red",bg="white", width=100)
            self.wordLabel.grid(column=3,row=8,columnspan=1, sticky='N')
            wordlistSize = len(self.wordList)
            
            # counter variable for words added by user
            i = 0
            
            # string for words list
            words = ""
            
            # stay in loop til all words are added to wordsList label
            while ( i <= wordlistSize-1):
                words += self.wordList[i]
                self.wordVariable.set(words)
                words += "\n"
                i = i + 1


    def OnPressEnterAdd(self, event):
        # for optionsPage, adds word to "spam" word list by pressing enter
        
        # if wordEntry field is not empty
        if self.wordEntry.get() != "":
            
            # add text in wordEntry field to wordList but delete any spaces
            self.wordList.insert(0, self.wordEntry.get().replace(" ", ""))
            
            # delete text from field
            self.wordEntry.delete(0, 'end')
            
            # move cursor to wordEntry field
            self.wordEntry.focus_set()
            self.wordEntry.selection_range(0, Tkinter.END)
            
            # create message label for title of wordList
            self.wordTitleVariable = Tkinter.StringVar()
            self.wordTitleLabel = Tkinter.Message(self,textvariable=self.wordTitleVariable, anchor="w",fg="black",bg="white", width=100)
            self.wordTitleLabel.grid(column=2,row=8,columnspan=1, sticky='N')
            self.wordTitleVariable.set("Added Words:")
            
            # create message label for all words added by user
            self.wordVariable = Tkinter.StringVar()
            self.wordLabel = Tkinter.Message(self,textvariable=self.wordVariable, anchor="w",fg="red",bg="white", width=100)
            self.wordLabel.grid(column=3,row=8,columnspan=1, sticky='N')
            wordlistSize = len(self.wordList)
            
            # counter variable for words added by user
            i = 0
            
            # string for words list
            words = ""
            
            # stay in loop til all words are added to wordsList label
            while ( i <= wordlistSize-1):
                words += self.wordList[i]
                self.wordVariable.set(words)
                words += "\n"
                i = i + 1
    
    def OnJunkClick(self):
        # for mailboxPage, sets mailbox folder specified by user
       
        # set mailbox folder we want to junk
        self.mailboxVariable = "Junk"
        
        # set title label for mailboxPage
        self.labelVariable.set("Deleting From " + self.mailboxVariable + "...")
        self.label.grid(column=0,row=6,columnspan=4, sticky='EW')
        
        # delete "spam" from specified mailbox folder, and provide wordList
        self.janitorInst.zapAwayJunk(self.mailboxVariable, self.wordList)
        
        # set label specifying how many emails got deleted
        self.label2Variable.set(str(self.janitorInst.numDeleted) + " emails were deleted")
        
        # hide button hoices from view
        self.junkButton.grid_forget()
        self.inboxButton.grid_forget()
    
    def OnInboxClick(self):
        # for mailboxPage, sets mailbox folder specified by user
        
        # set mailbox folder we want to inbox
        self.mailboxVariable = "Inbox"

        # set title label for mailboxPage
        self.labelVariable.set("Deleting From " + self.mailboxVariable + "...")
        self.label.grid(column=0,row=6,columnspan=4, sticky='EW')
       
        # delete "spam" from specified mailbox folder, and provide wordList
        self.janitorInst.zapAwayJunk(self.mailboxVariable, self.wordList)
        
        # set label specifying how many emails got deleted
        self.label2Variable.set(str(self.janitorInst.numDeleted) + " emails were deleted")
        # hide button hoices from view
        self.junkButton.grid_forget()
        self.inboxButton.grid_forget()
    
    def OnEmailFieldClick(self, event):
        # for introPage, when email field is clicked on
        # erase both email and password fields when email field is clicked on
        # fix so its only when self.passwordEntryVariable == self.lastUsedPassword:
        print self.emailEntryVariable.get(), self.lastUserNameUsed
        if self.emailEntryVariable.get() == self.lastUserNameUsed :
           self.emailEntryVariable.set("")
           self.passwordEntryVariable.set("")
    
    def OnPassFieldClick(self, event):
        # for introPage, when password field is clicked on
        # delete field when clicked on
        # fix so its only when self.passwordEntryVariable == self.lastUsedPassword:
        self.passwordEntryVariable.set("")
    
    def OnAddFieldClick(self, event):
        # for optionsPage, when add field clicked on
        # if field is populated with default value erase it when field is clicked
        if self.wordEntryVariable.get() == "i.e. Target":
           self.wordEntryVariable.set("")

    def OnExitClick(self):
        # for mailboxPage, exit from program
        self.quit()
    
    def OnPressEnterPassword(self,event):
        # for introPage, when cursor's in email field and user presses enter key
        # keep cursor to password field, highlighting/selecting any text in field
        self.passwordEntry.focus_set()
        self.passwordEntry.selection_range(0, Tkinter.END)

    def OnPressEnterAddress(self,event):
        # for introPage, when cursor's in password field and user presses enter key
        # move cursor to password field, highlighting/selecting any text in field
        self.passwordEntry.focus_set()
        self.passwordEntry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('Email Janitor')
    app.mainloop()