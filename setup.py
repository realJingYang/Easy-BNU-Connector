# Author: GasinAn

import sys
assert sys.getwindowsversion().major >= 5

import os
import re
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
    from js2py import translate_js
except:
    print('Installing Js2Py...')
    if os.system('pip install js2py') is 0:
        pass
    else:
        raise OSError
    from js2py import translate_js

print('Setting up...')
for path in sys.path:
    if path != '':
        if re.match('.+\\\\(.+)', path).group(1) == 'site-packages':
            easy_bnu_connector_path = path+'\\easy_bnu_connector'
            break

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

with open('easy_bnu_connector\\methods.js', 'rb') as f:
    js = f.read().decode('utf-8')
py_code = "__all__ = ['methods']\n\n"
py_code += translate_js(js)
py_code += "\n\nmethods = var.to_python()"
py_code += "\n\nmethods.device = "+get_windows_version()

with open('easy_bnu_connector\\methods.py', 'wb') as f:
    f.write((py_code).encode('utf-8'))
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

with open('Easy-BNU-Connector-0.2.2.vbs', 'w') as f:
    f.write('set ws = createobject("wscript.shell")\n')
    f.write('ws.run "python '+easy_bnu_connector_path+'\\login.py", vbhide')