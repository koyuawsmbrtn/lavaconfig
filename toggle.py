#!/usr/bin/python
import os
cwd = "/home/koyu/lavaconfig/"
os.system("python3 "+cwd+"configure.py")
if os.system("pgrep -x lavalauncher") == 0:
    os.system("killall lavalauncher -9")
else:
    os.system("lavalauncher -c ~/.config/lavalauncher/lavalauncher &")