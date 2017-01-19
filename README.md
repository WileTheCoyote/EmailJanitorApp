# Email Janitor Application
An application that removes junk and spam from your MSN email account (Works with MSN, Live, Hotmail, Outlook, and Microsoft domains). 

The motivation for this project was that a few of my friends often complain that MSN does a poor job of indentifying 
spam and junk emails. Even if a user marks a specific email address as junk, spammers now-a-days use dynamically created addresses to 
continually bombard users. The application uses regular expressions to look for different types of dynamically created email addresses.
It also allows the user to enter specific "spam" words. The Email Janitor will then delete an email if its address contains a "spam"
word provided by the user. 

The stand-alone application can be found and downloaded via the StandaloneEJAPP.zip.

### Features:
  - Accepts login credentials from all MSN domains (MSN, Live, Hotmail, Outlook, and Microsoft)
  - Upon a successful login, the application saves the credentials to a file, allowing the user to quickly login next time
  - Looks for patterns used in dynamically created spam emails
  - Has option to delete from Inbox or Junk folder
  - Employs easy to use GUI interface
  - Stand-alone OSX app (runanble on machines that don't have python or otherwise necessary packages)  

### Libraries and Modules:
    Tkinter       -   graphical interface construction (GUI)
    Pyinstaller   -   creating stand-alone executables
    Cryptography  -   encrypting and decrypting login credentials 
    imaplib       -   communicating with email server
    regex         -   indentifying junk email patterns
  
### Contents:
    StandaloneEJAPP.zip   -   contains downloadable stand-alone application
    Email Janitor.app     -   stand-alone application (contains contents folder)
    Email Janitor         -   stand-alone terminal executable file 
    outlookAppGUI.py      -   contains code for graphical interface
    outlookAppGUI.spec    -   used by Pyinstaller to construct the stand-alone app 
    janitor.py            -   contains Janitor() class that handles basic operations for application
    outlook.py            -   contains Outlook() class that interacts with email server (*adapted from https://github.com/awangga/outlook)
    paths.py              -   contains functions that find the path of file 
    userFile.txt          -   holds the last successfully used username/email address (default - sample@msn.com) 
    passFile.txt          -   holds an encrypted version of the password that's associated with the last successfully used username
    trash.icns            -   icon for application
    jan.jpg               -   application logo

### Notes:
  If you want to change the app and or run the .spec file for yourself to create the stand-alone app:
  
      - First go to http://www.pyinstaller.org and download pyisntaller 3.2
      - Move PyInstaller-3.2 directory into this directory 
      - Put files from this directory into PyInstaller-3.2
      - Update outlookAppGUI.spec with correct file paths
      - Use "pyinstaller outlookAppGUI.spec" command to create stand-alone app

      
      
      
     






