import outlook
import imaplib
import re

class Janitor():

   def __init__(self, userName, passWord):
      self.mail = outlook.Outlook()
      self.userName = userName
      self.passWord = passWord

   def logOn(self):
      message = self.mail.login(self.userName, self.passWord)
      return message

   def zapAwayJunk(self, mailboxType, wordList):
      self.mailboxType = mailboxType
      self.wordList = wordList
      print self.mailboxType
      if self.mailboxType == "Inbox":
         self.mail.inbox()
      elif self.mailboxType == "Junk":
         self.mail.junk()
      else:
         print "Grave Error"
         return None

      mailBox = self.mail.allIds()
      boxSize = len(mailBox)

      i = 0;
      d = 0;
 
      l = 1;
      self.wordListSize = len(self.wordList)
      print self.wordListSize
      specificJunk = ""
      sj = 0
      if self.wordListSize > 0:
         sj = 1
         specificJunk = self.wordList[0]
      if self.wordListSize > 1:
          while (l <= self.wordListSize-1):
            specificJunk += "|" + self.wordList[l]
            l = l + 1
      
      print specificJunk
      while (i <= boxSize-1):
         val = mailBox[i]
         emailAddress = self.mail.getEmailFrom(val).split('>')[0].split('<')[1]
         print val, emailAddress
         superJunk = 0
         if re.match(r'([0-9])+.([0-9])(([0-9]|[A-Z]))+-([0-9])+@[0-9]', emailAddress):
            print "**matched on",emailAddress
            superJunk = 1
         if re.search(r'ixfumaroidal|frgenuclast', emailAddress):
            print "** ixfuma",emailAddress
            superJunk = 1
         
         if sj == 1:
            if re.search(r''+specificJunk+'' , emailAddress):
               superJunk = 1
               print "** WUNDER or bovada or hillary",emailAddress

      
         if superJunk == 1:
            print val, "deleted**"
            self.mail.imap.store(val, '+FLAGS', '\\Deleted')
            # delete flagged email
            self.mail.imap.expunge()
            # adjust counter beacause next email now has the same id as
            # the email we just deleted
            i = i - 1
            # change d count
            d = d + 1
            # adjust new size of junk email id's; we
            boxSize = boxSize - 1
         i = i+1
      self.mail.imap.close()
      self.mail.logout()
      self.numDeleted = d
          
   def printPass(self):
       print self.passWord
