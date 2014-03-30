#!/usr/bin/env python

#Author: Haelwenn Monnier (lanodan) <haelwenn.monnier@gmail.com>
#License: CC-BY-SA

import socket
import sys
import re
import time
import urllib
import subprocess
import ConfigParser
import os

def get_element(textInput, elem):
  idx1=textInput.find('<'+elem+'>')
  idx2=textInput.find('</'+elem+'>')
  return textInput[idx1+len('<'+elem+'>'):idx2].strip()

# Output string into the channel
def printIrc(ircout):
  irc.send('PRIVMSG '+channel+' :'+ircout+'\n')

#line: string of text to add in the log
def log(line):
  print '[LOG] '+line
  log = open('IRCBot.log', 'a')
  log.write(line+'\n')
  log.close()

config = ConfigParser.ConfigParser()
if (config.read('config.ini')):
  botnick = config.get('Config', 'nick')
  passwd  = config.get('Config', 'passwd')
  server  = config.get('Config', 'server')
  port    = config.get('Config', 'port')
  channel = config.get('Config', 'channel')
  quitMsg = config.get('Config', 'quitMessage')
  source  = config.get('Config', 'source')
else:
  print '[ERROR] Couln\'d load config.ini. Example config file: config.ini.example. Exiting'
  sys.exit(1)

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
irc.connect((server, int(port)))                                                         #connects to the server
irc.send('PASS '+ passwd +'\n')
irc.send('NICK '+ botnick +'\n')
irc.send('USER '+ botnick +' Feyris NyanNyan :Bot made by lanodan using python!\n') #user authentication
time.sleep(1)
irc.send('JOIN '+ channel +'\n')        #join the chan
printIrc('Ohayo-nyan ! [http://i.imgur.com/vzYFOkp.jpg]')

while 1:    #puts it in a loop
  text=irc.recv(2048)  #receive the text
  print text

  if text.find('PING') != -1:                          #check if 'PING' is found
    irc.send('PONG ' + text.split() [1] + '\n')      #returnes 'PONG' back t
  if text.find(':!hi') !=-1: #you can change !hi to whatever you want
    t = text.split(':!hi') #you can change t and to :)
    to = t[1].strip() #this code is for getting the first word after !hi
    printIrc('Ohayo-nyan '+str(to)+' ! [http://i.imgur.com/vzYFOkp.jpg]')
  if text.find(':!say') != -1: #you can change !hi to whatever you want
    t = text.split(':!say') #you can change t and to :)
    out = t[1].strip() #this code is for getting the first word after !hi
    printIrc(str(out))
  if text.find(':!action') != -1: #you can change !hi to whatever you want
    t = text.split(':!action') #you can change t and to :)
    out = t[1].strip() #this code is for getting the first word after !hi
    printIrc('\x01ACTION '+out+'\x01')
  if text.find('http') != -1:
    parse = re.findall('https?://[^\"\'\(\)\[\]\{\}\<\>\ ]+', text)
    try:
      url = str(parse[0]).rstrip() #took the first link and remove newline and whitespaces
      if (len(url) > 8) : # I assume a link is more than 8 characters long (thx NyanKiyoshi for spotting my drunkness here xD)
        try:
          get = urllib.urlopen(url)
          wget = get.read()
          mimeType = get.info().type
          get.close()
          if (re.search('text/x?html', mimeType)):
            if wget.find('<title>') != -1:
              title = get_element(wget, 'title')
              printIrc('Title: '+title)
              log(url+', '+title)
            if wget.find('<TITLE>') != -1:
              title = get_element(wget, 'TITLE')
              printIrc('Title: '+title)
              log(url+', '+title)
          else:
            printIrc('Type: '+mimeType)
            log(url+', '+mimeType)
        except:
          printIrc('[ERROR] Can\'t open the page')
      else:
        printIrc('Link too short')
    except:
      printIrc('[ERROR] Invalid URL')
  if text.find(':!source') != -1:
    printIrc(source)
  #if text.find(':!'+nick+' help') != -1:
  #  asker = 
  if text.find(' JOIN ') != -1:

  if text.find(':!stop in the name of sey') != -1:
    irc.send('QUIT : '+quitMsg+'\n')
    time.sleep(1)
    sys.exit(0)
