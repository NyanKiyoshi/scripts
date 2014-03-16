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

def load_config_value(section, option):
  try:
    out = Config.get(section)[:option]
    return out
  except:
    print('exception on '+option)

def load_config():
  config = ConfigParser.ConfigParser()
  configLocation = os.path.join(os.path.dirname(__file__), './config.ini')
  config.read(configLocation)
  botnick = load_config_value('Config', 'Nick')
  server  = load_config_value('Config', 'Server')
  port    = load_config_value('Config', 'Port')
  channel = load_config_value('Config', 'Channel')
  quitMsg = load_config_value('Config', 'QuitMessage')

def get_title(textInput):
  idx1=textInput.find('<title>')
  idx2=textInput.find('</title>')
  return textInput[idx1+len('<title>'):idx2].strip()

def check_url(url):
  if (len(url) > 8) : # I assume a link is mkre than 8nchracter long
    try:
      urllib.urlopen(url)
      return True
    except:
      return False

def printIrc(ircout):
  irc.send('PRIVMSG '+channel+' :'+ircout+'\n')

botnick = 'feyris-nyanyan'
server  = 'holmes.freenode.net'
port    = '6667'
channel = '#kisune'
quitMsg = 'Sayonara-nyan !'
source  = 'My sourcecode is under CC-BY-SA and available at the following address: https://github.com/lanodan/scripts/tree/master/IRCBot'

load_config()

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
irc.connect((server, int(port)))                                                         #connects to the server
irc.send("USER "+ botnick +" Feyris NyanNyan :Bot made by lanodan using python!\n") #user authentication
irc.send("NICK "+ botnick +"\n")
time.sleep(1)
irc.send("JOIN "+ channel +"\n")        #join the chan
printIrc('Ohayo-nyan ! [http://i.imgur.com/vzYFOkp.jpg]')

while 1:    #puts it in a loop
  text=irc.recv(2040)  #receive the text
  print text   #print text to console

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
  if text.find(':!define') != -1:
    t = text.split(':!define')
    define = t[1].strip()
    if (define):
      printIrc('http://lmgtfy.com/?q='+define)
    else:
      printIrc('Are you drunk ?') 
  if text.find('http') != -1:
    parse = re.findall('https?://[^\"\'\(\)\[\]\{\}\<\>\ ]+', text)
    try:
      url = str(parse[0]).rstrip() #took the first link and remove newline and whitespaces
      if check_url(url):
        get = urllib.urlopen(url)
        wget = get.read()
        get.close()
        if wget.find('<title>') != -1:
          title = get_title(wget)
          printIrc('('+url+')Title: '+title)
          print '('+url+')Title: '+title
    except:
      print 'Invalid url'
  if text.find(':!source') != -1:
    printIrc(source)
  if text.find(':!stop in the name of sey') != -1:
    irc.send('QUIT : '+quitMsg+'\n')
    time.sleep(1)
    sys.exit(0)
