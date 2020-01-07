# Author: GasinAn


import os
import sys


print('Installing Requests and BeautifulSoup4...')
if os.system('conda install requests beautifulsoup4') is 0:
    pass
elif os.system('pip install requests beautifulsoup4') is 0:
    pass
else:
    raise OSError

print('Installing Js2Py...')
if os.system('pip install js2py') is 0:
    pass
else:
    raise OSError

print('Setting up...')
for path in sys.path:
    if path[-13:] == 'site-packages':
        easy_bnu_connector_path = path+'\\easy_bnu_connector'
        break
with open('easy_bnu_connector\\Easy-BNU-Connector.bat', 'w') as f:
    f.write('python '+easy_bnu_connector_path+'\\login.py\t\nexit')
os.system('mkdir '+easy_bnu_connector_path)
os.system('copy /y easy_bnu_connector\\* '+easy_bnu_connector_path)

with open('..\\Easy-BNU-Connector.bat', 'w') as f:
    f.write('start /min '+easy_bnu_connector_path+'\\Easy-BNU-Connector.bat')

with open('setup.reg', 'w') as f:
    f.write('Windows Registry Editor Version 5.00\t\n\t\n')
    f.wrtie('[HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services')
    f.write('\\NlaSvc\\Parameters\\Internet]\t\n')
    f.wrtie('"EnableActiveProbing"=dword:00000000')
os.system('regedit /s '+sys.path[0]+'\\setup.reg')