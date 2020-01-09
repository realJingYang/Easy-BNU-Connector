# Author: GasinAn

import sys
assert (sys.platform in {'win32', 'cygwin'})

import os
import time
try:
    import _thread
except:
    import thread as _thread
try:
    import tkinter
except:
    import Tkinter as tkinter

try:
    from requests import request
except:
    print('Installing Requests...')
    if os.system('conda install requests') is 0:
        pass
    elif os.system('pip install requests') is 0:
        pass
    else:
        raise OSError
    from requests import request

try:
    from bs4 import BeautifulSoup
except:
    print('Installing Beautifulsoup4...')
    if os.system('conda install beautifulsoup4') is 0:
        pass
    elif os.system('pip install beautifulsoup4') is 0:
        pass
    else:
        raise OSError
    from bs4 import BeautifulSoup

try:
    from js2py import translate_file as trans
except:
    print('Installing Js2Py...')
    if os.system('pip install js2py') is 0:
        pass
    else:
        raise OSError
    from js2py import translate_file as trans

print('Setting up...')
for path in sys.path:
    if path[-13:] == 'site-packages':
        easy_bnu_connector_path = path+'\\easy_bnu_connector'
        break

with open('..\\Easy-BNU-Connector.bat', 'w') as f:
    f.write('start /min '+easy_bnu_connector_path+'\\Easy-BNU-Connector.bat')

trans('easy_bnu_connector\\methods.js', 'easy_bnu_connector\\methods.py')
with open('easy_bnu_connector\\Easy-BNU-Connector.bat', 'w') as f:
    try:
        f.write('python '+easy_bnu_connector_path+'\\login.py\t\nexit')
    except:
        easy_bnu_connector_path = sys.path[0]+'\\easy_bnu_connector'
        f.write('python '+easy_bnu_connector_path+'\\login.py\t\nexit')
with open('easy_bnu_connector\\warmup.py', 'w') as f:
    f.write('from methods import methods')

os.system('mkdir '+easy_bnu_connector_path)
os.system('move /y easy_bnu_connector\\* '+easy_bnu_connector_path)
os.system('python '+easy_bnu_connector_path+'\\warmup.py')

def add_profile(netname, ssid, xml):
    with open('WLAN-'+netname+'.xml', 'w') as f:
        f.write(xml.replace('netname', netname).replace('ssid', ssid))
    os.system('netsh wlan add profile filename="WLAN-'+netname+'.xml"')

with open('setup.xml') as f:
    xml = f.read().replace('\n', '\t\n')
add_profile('BNU-Student', '424E552D53747564656E74', xml)
add_profile('BNU', '424E55', xml)

def change_regedit(header, reg):
    with open(header.replace(' ', '-')+'.reg', 'w') as f:
        f.write(reg.replace('HEADER', header))
    os.system('regedit /s '+sys.path[0]+'\\'+header.replace(' ', '-')+'.reg')

with open('setup.reg') as f:
    reg = f.read().replace('\n', '\t\n')
change_regedit('REGEDIT4', reg)   
change_regedit('Windows Registry Editor Version 5.00', reg)
