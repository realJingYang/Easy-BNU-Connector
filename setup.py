# -*- coding: UTF-8 -*-
# Easy-BNU-Connector v0.2.4
# File: setup.py
# Author: GasinAn
# License: GNU General Public License v3.0

import sys
assert (sys.getwindowsversion().major >= 5)

import os

try:
    from requests import request
except:
    try:
        eval('print("Installing Requests...")')
    except:
        eval('print "Installing Requests..." ')
    if os.system('conda install requests') != 0:
        if os.system('pip install requests') != 0:
            raise OSError

try:
    eval('print("Setting up...")')
except:
    eval('print "Setting up..." ')
for path in sys.path:
    if path != '':
        if path[-13:] == 'site-packages':
            easy_bnu_connector_path = path+'\\easy_bnu_connector'
            break
if 'easy_bnu_connector_path' not in globals():
    easy_bnu_connector_path = sys.path[1]

def get_windows_version():
    with os.popen('ver') as p:
        ver = p.read()
    if ver.find('版本 10.0') >= 0 or ver.find('Version 10.0') >= 0:
        return "'Windows 10'"
    elif ver.find('版本 6.3') >= 0 or ver.find('Version 6.3') >= 0:
        return "'Windows 8'"
    elif ver.find('版本 6.2') >= 0 or ver.find('Version 6.2') >= 0:
        return "'Windows 8'"
    elif ver.find('版本 6.1') >= 0 or ver.find('Version 6.1') >= 0:
        return "'Windows 7'"
    elif ver.find('版本 6.0') >= 0 or ver.find('Version 6.0') >= 0:
        return "'Windows Vista'"
    elif ver.find('版本 5.1') >= 0 or ver.find('Version 5.1') >= 0:
        return "'Windows XP'"
    elif ver.find('版本 5.0') >= 0 or ver.find('Version 5.0') >= 0:
        return "'Windows 2000'"
    else:
        return "'Windows NT'"

with open('easy_bnu_connector\\methods.py', 'ab') as f:
    f.write(('\n\nDEVICE = '+get_windows_version()).encode('UTF-8'))
with open('easy_bnu_connector\\warmup.py', 'w') as f:
    f.write('from methods import *')

os.system('mkdir '+easy_bnu_connector_path)
os.system('move /y easy_bnu_connector\\* '+easy_bnu_connector_path)
os.system('python '+easy_bnu_connector_path+'\\warmup.py')

def add_profile(netname, ssid, xml):
    with open('WLAN-'+netname+'.xml', 'w') as f:
        f.write(xml.replace('netname', netname).replace('ssid', ssid))
    os.system('netsh wlan add profile filename="WLAN-'+netname+'.xml"')

with open('setup.xml') as f:
    xml = f.read()
add_profile('BNU-Student', '424E552D53747564656E74', xml)
add_profile('BNU', '424E55', xml)

def change_regedit(header, reg):
    with open(header.replace(' ', '-')+'.reg', 'w') as f:
        f.write(reg.replace('HEADER', header))
    os.system('regedit /s '+sys.path[0]+'\\'+header.replace(' ', '-')+'.reg')

with open('setup.reg') as f:
    reg = f.read()
change_regedit('Windows Registry Editor Version 5.00', reg)
change_regedit('REGEDIT4', reg)

with open('Easy-BNU-Connector-0.2.4.vbs', 'w') as f:
    f.write('set ws = createobject("wscript.shell")\n')
    f.write('ws.run "python '+easy_bnu_connector_path+'\\login.py", vbhide')