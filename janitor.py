import outlook
import imaplib
import re
# Author ~ WileTheCoyote

class Janitor():

   def __init__(self, userName, passWord):
      # intialize mailbox with Outlook class
      # save off given username and password
      self.mail = outlook.Outlook()
      self.userName = userName
      self.passWord = passWord
   
   def logOn(self):
      # log on to server using Outlook class (login)
      # login returns a success code (0 for successful login, 1 for failed login)
      # save code to variable message and return it
      message = self.mail.login(self.userName, self.passWord)
      return message
   
   # delete junk from specified folder given folder type (Junk or Inbox)
   # and any specified words to look for in email addresses
   def zapAwayJunk(self, mailboxType, wordList):
      # mailboxType is our specified folder
      self.mailboxType = mailboxType
      # wordlist is a list of words we want to look for in an email address
      self.wordList = wordList
      
      # check user specified mailbox folder and set the mailbox appropriately
      if self.mailboxType == "Inbox":
         self.mail.inbox()
      if self.mailboxType == "Junk":
         self.mail.junk()
      # sanity check for testing; never should reach
      else:
         print "Grave Error"
         return None
      
      # make array of ids for all emails in specified folder (Junk or Inbox)
      mailBox = self.mail.allIds()
      
      # find length of array of email ids; how emails must we looking at
      boxSize = len(mailBox)
      # find length of word list provided by user; how many words did user provide
      self.wordListSize = len(self.wordList)
      
      # counter variable for email we are currently looking at
      i = 0;
      # counter for deleted emails
      d = 0;
      # counter for word list provided by user
      l = 1;
      
      # specificJunk is a string variable used for our regex expression creation
      # intialized as empty string
      specificJunk = ""
      
      # bool variable that represents if our user gave us any words (wordList)
      # 0 if no words are given, 1 if any words are given
      sj = 0
      
      # if 1 or more words were given set sj bool to 1 and set specificJunk
      # to first word in wordList
      if self.wordListSize > 0:
         sj = 1
         specificJunk = self.wordList[0]
      # if more than 1 word was given, add each new word to specificJunk string
      if self.wordListSize > 1:
          # stay in while loop while we have more words in word list
          while (l <= self.wordListSize-1):
            specificJunk += "|" + self.wordList[l]
            l = l + 1
      # iterate through each email stopping when there are no more emails to look at
      while (i <= boxSize-1):
         # put email id for current email in eID variable
         eID = mailBox[i]
         
         # create variable for email address of current email we are looking at (i)
         # uses getEmailFrom function in Outlook class
         emailAddress = self.mail.getEmailFrom(eID).split('>')[0].split('<')[1]
         
         # print email ID and associated email address
         print eID, emailAddress
         
         # superJunk is a bool variable to flag an email we want to delete
         # 0 if email is non junk, 1 if email is junk and should be deleted
         superJunk = 0
         
         # regex expressions for checking if email is spam and delete worthy
         # common pattern for a dynamically created spam email pattern
         # Regex Exp. 1
         if re.match(r'^[0-9]{6}', emailAddress):
            print "**matched on",emailAddress
            # if matched regex exp, specify as spam and clear for deletion
            superJunk = 1
         # common spam emails contain these names in email address domain
         # Regex Exp. 2
         if re.search(r'ixfumaroidal|frgenuclast', emailAddress):
            print "** ixfuma or frgenu",emailAddress
            # if matched regex exp, specify as spam and clear for deletion
            superJunk = 1
         # if user has specified any words enter this section
         if sj == 1:
            # use specificJunk string to create regex expression
            # similar to Regex Exp. 2, this expression checks if any of
            # of the words specified by the user are found in the email's address
            if re.search(r''+specificJunk+'' , emailAddress):
               print "** From word list provided",emailAddress
               # if matched regex exp, specify as spam and clear for deletion
               superJunk = 1
         # if email was specified as spam
         if superJunk == 1:
            # print email ID of email we are deleting
            print eID, "deleted**"
            # use email ID to flag email (from imaplib module)
            self.mail.imap.store(eID, '+FLAGS', '\\Deleted')
            # delete flagged email
            self.mail.imap.expunge()
            # adjust counter beacause next email now has the same id as
            # the email we just deleted
            i = i - 1
            # change count of email we have deleted
            d = d + 1
            # adjust new size of junk email id's; we now have 1 less
            boxSize = boxSize - 1
         # increment email counter to next email
         i = i+1
      # exited while
      # close currently selected mailbox
      self.mail.imap.close()
      # shutdown connection to server
      self.mail.logout()
      # set final
      self.numDeleted = d
          
   def printPass(self):
       print self.passWord
