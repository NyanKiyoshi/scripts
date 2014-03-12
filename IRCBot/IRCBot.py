#!/usr/bin/env python
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
    out = Config.get(section)[option]
    return out
  except:
    print('exception on '+option)

def load_config():
  config = ConfigParser.ConfigParser()
  configLocation = os.path.join(os.path.dirname(__file__), 'config.ini')
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
  try:
    urllib.urlopen(url)
    return True
  except:
    return False

botnick = 'lanobot'
server  = 'holmes.freenode.net'
port    = '6667'
channel = '#kisune'
quitMsg = 'Emergency time shift !'

load_config()

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
irc.connect((server, int(port)))                                                         #connects to the server
irc.send("USER "+ botnick +" Lanodan Bot :Bot made by lanodan using python!\n") #user authentication
irc.send("NICK "+ botnick +"\n")
time.sleep(1)
irc.send("JOIN "+ channel +"\n")        #join the chan
irc.send('PRIVMSG '+channel+' :Hello there !\n')

while 1:    #puts it in a loop
  text=irc.recv(2040)  #receive the text
  print text   #print text to console

  if text.find('PING') != -1:                          #check if 'PING' is found
    irc.send('PONG ' + text.split() [1] + '\n')      #returnes 'PONG' back t
  if text.find(':!hi') !=-1: #you can change !hi to whatever you want
    t = text.split(':!hi') #you can change t and to :)
    to = t[1].strip() #this code is for getting the first word after !hi
    irc.send('PRIVMSG '+channel+' :Hello '+str(to)+' ! \n')
  if text.find(':!say') !=-1: #you can change !hi to whatever you want
    t = text.split(':!say') #you can change t and to :)
    to = t[1].strip() #this code is for getting the first word after !hi
    irc.send('PRIVMSG '+channel+' :'+str(to)+'\n')
  if text.find('http://') != -1:
    t = text.split('http://')
    line = t[1].strip()
    t = line.split()
    url = 'http://'+t[0].strip()
    if check_url(url):
      get = urllib.urlopen(url)
      wget = get.read()
      get.close()
      if wget.find('<title>') != -1:
        title = get_title(wget)
        irc.send('PRIVMSG '+channel+' :('+url+')Title: '+title+' \n')
  if text.find(':!stop in the name of sey') != -1:
    irc.send('QUIT : '+quitMsg+'\n')
    sys.exit(0)
