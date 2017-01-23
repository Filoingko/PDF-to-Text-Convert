from Tkinter import * 
from tkFileDialog import askopenfilename
import os

import re

from PDFMiner import main
class Running() :
    # Hold onto a global reference for the root window 
    root = Tk()
    root.geometry("590x550+300+300")
    root.resizable(width=False, height=False)
    # Hold onto the Text Entry Box also 
    entryBox = None 
    filename = ''
    path = ''
    getresos = None
    rn = None
    openFileText = StringVar()
    password = ""
    pwd = StringVar()
    textarea = Text(root)

    def openFile (self) :
        #Text.delete(1.0, Tkinter.END)
        self.textarea.delete(1.0 , END)
        try :  
            self.filename = askopenfilename( filetypes = (("PDF File" , "*.pdf"),("All Files","*.*")))
            filenameText = os.path.split(self.filename)[1]
            self.path = self.filename
            self.openFileText.set(filenameText)
        except :
            print sys.exc_info()[0]

    def extractText(self) :
        self.password = self.pwd.get()

        try : 
            extractText = main(self.path , self.pwd)
            self.textarea.insert(INSERT , extractText)
        except Exception, e:
            print str(e)
        

    def __init__(self): 
        # button for select file from file manager
        openButton = Button(self.root, text="Open File" , command=self.openFile)
        openButton.pack()
        openButton.place(x=20, y=20)  #height=100, width=100

        # frame to display open file name and enter password field
        name_pwdFrame = Frame(self.root)

        fileNameLabel = Label(name_pwdFrame, text='File Name:')
        fileNameLabel.grid (row = 0 , column = 0)
        # to disply open pdf file name
        openFileName = Entry(name_pwdFrame , textvariable = self.openFileText , state=DISABLED)
        openFileName.grid (row = 0 , column = 1)

        passwordLable = Label(name_pwdFrame, text='Enter Password:')
        passwordLable.grid (row = 1 , column = 0)
        password = Entry(name_pwdFrame , textvariable = self.password)
        password.grid (row = 1 , column = 1)
        
        name_pwdFrame.pack()
        name_pwdFrame.place(x=20, y=60)

        genarateButton = Button(self.root, text="Genarate" , command=self.extractText) 
        genarateButton.pack()
        genarateButton.place(x=20, y=120)

        self.textarea.pack()
        self.textarea.place(x=10, y=160)

        self.root.mainloop() # Start the event loop 


if __name__=='__main__':
    Running()
