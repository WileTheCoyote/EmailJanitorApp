#!/usr/bin/python
# -*- coding: utf-8 -*-
import imaplib
import email
import smtplib
import datetime
import email.mime.multipart
# adapted from https://github.com/awangga/outlook
# changed login() function and added getEmailFrom() function
# some functions were removed if not relevant to this project
# other functions are not used but could prove helpful for exapanding project

class Outlook:
    
    def __init__(self):
        mydate = datetime.datetime.now() - datetime.timedelta(1)
        self.today = mydate.strftime('%d-%b-%Y')
    
    def login(self, username, password):
        self.username = username
        self.password = password
        errorMessage = 1
        i = 0
        while True:
            try:
                self.imap = imaplib.IMAP4_SSL('imap-mail.outlook.com')
                (r, d) = self.imap.login(username, password)
                assert r == 'OK', 'login failed'
                print ' > Sign as ', d
                errorMessage = 0
                break
            except:
                # try and connect to server with given username and password 5
                # times, if still login fails, exit While, with errorMessage = 1
                if i < 5:
                   print ' > Sign In ...'
                   i = i + 1
                   continue
                else:
                   errorMessage = 1
                   break
        return errorMessage

    
    def list(self):
        
        # self.login()
        
        return self.imap.list()
    
    def select(self, str):
        return self.imap.select(str)
    
    def inbox(self):
        return self.imap.select('Inbox')
    
    def junk(self):
        return self.imap.select('Junk')
    
    def logout(self):
        return self.imap.logout()
    
    def today(self):
        mydate = datetime.datetime.now()
        return mydate.strftime('%d-%b-%Y')
    
    def getIdswithWord(self, ids, word):
        stack = []
        for id in ids:
            self.getEmail(id)
            curr_mailmsg = self.mailbody()
            if word in self.mailbody().lower():
                stack.append(id)
        return stack
    
    def unreadIds(self):
        (r, d) = self.imap.search(None, 'UNSEEN')
        list = d[0].split(' ')
        return list

    def allIds(self):
        (r, d) = self.imap.search(None, 'ALL')
        list = d[0].split(' ')
        return list
    
    def readIds(self):
        (r, d) = self.imap.search(None, 'SEEN')
        list = d[0].split(' ')
        return list
    
    def getEmailFrom(self, id):
        (r, d) = self.imap.fetch(id, '(RFC822)')
        self.raw_email = d[0][1]
        self.email_message = email.message_from_string(self.raw_email)
        return self.email_message['from']
    
    def unread(self):
        list = self.unreadIds()
        latest_id = list[-1]
        return self.getEmail(latest_id)
    
    def read(self):
        list = self.readIds()
        latest_id = list[-1]
        return self.getEmail(latest_id)
    
    def readToday(self):
        list = self.readIdsToday()
        latest_id = list[-1]
        return self.getEmail(latest_id)
    
    def unreadToday(self):
        list = self.unreadIdsToday()
        latest_id = list[-1]
        return self.getEmail(latest_id)
    
    def readOnly(self, folder):
        return self.imap.select(folder, readonly=True)
    
    def writeEnable(self, folder):
        return self.imap.select(folder, readonly=False)
    
    def rawRead(self):
        list = self.readIds()
        latest_id = list[-1]
        (r, d) = self.imap.fetch(latest_id, '(RFC822)')
        self.raw_email = d[0][1]
        return self.raw_email
    
    def mailsubject(self):
        return self.email_message['Subject']
    
    def mailfrom(self):
        return self.email_message['from']
    
    def mailto(self):
        return self.email_message['to']
    
    def mailreturnpath(self):
        return self.email_message['Return-Path']
    
    def mailreplyto(self):
        return self.email_message['Reply-To']
    
    def mailall(self):
        return self.email_message
