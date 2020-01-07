# -*- coding: UTF-8 -*-
# Easy-BNU-Connector v0.2.0
# Author: GasinAn
# License: GNU General Public License v3.0


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

from requests import request
from bs4 import BeautifulSoup

from methods import methods


def device():
    # Get the version of Windows.
    with os.popen('ver') as p:
        ver = p.read()
    if ver.find('版本 10.0') >= 0 or ver.find('Version 10.0') >= 0:
        return 'Windows 10'
    elif ver.find('版本 6.3') >= 0 or ver.find('Version 6.3') >= 0:
        return 'Windows 8'
    elif ver.find('版本 6.2') >= 0 or ver.find('Version 6.2') >= 0:
        return 'Windows 8'
    elif ver.find('版本 6.1') >= 0 or ver.find('Version 6.1') >= 0:
        return 'Windows 7'
    elif ver.find('版本 6.0') >= 0 or ver.find('Version 6.0') >= 0:
        return 'Windows Vista'
    elif ver.find('版本 5.1') >= 0 or ver.find('Version 5.1') >= 0:
        return 'Windows XP'
    elif ver.find('版本 5.0') >= 0 or ver.find('Version 5.0') >= 0:
        return 'Windows 2000'
    elif ver.find('版本 4.9') >= 0 or ver.find('Version 4.9') >= 0:
        return 'Windows ME'
    elif ver.find('版本 4.1') >= 0 or ver.find('Version 4.1') >= 0:
        return 'Windows 98'
    elif ver.find('版本 4.0') >= 0 or ver.find('Version 4.0') >= 0:
        return 'Windows 95'
    else:
        return 'Windows NT' 

def keep_connection():
    # Try to keep connection.
    while True:
        if parameters[0] == 'OK':
            try:
                r = request('GET', 'http://www.4399.com/robots.txt')
                if r.text[:10] != 'User-agent':
                    parameters[0] = ''
            except:
                parameters[0] = ''

        # Preparing to login.
        elif parameters[0] == 'Preparing':
            try:
                r = request('GET', 'http://www.4399.com/robots.txt')
                time.sleep(1)
                if r.text[:10] == 'User-agent':
                    parameters[0] = 'OK'
                    text_message.set('用户已在线')
                    other_situations_interface_set()
            except:
                parameters[0] = ''

        # No connection now.
        else:
            check_possibility_of_connection()

def check_possibility_of_connection():
    # Check whether it is possible to make connection.
    try:
        with os.popen('netsh wlan show networks') as p:
            networks = p.read()
        status_bnu_student = networks.find('BNU-Student\n')
        status_bnu = networks.find('BNU\n')
        
        # Try to find a network and make connection
        if status_bnu_student >= 0:
            if status_bnu >= status_bnu_student or status_bnu < 0:
                try_to_make_connection('BNU-Student')
            else:
                try_to_make_connection('BNU')
        else:
            if status_bnu >= 0:
                try_to_make_connection('BNU')
            else:
                text_message.set('没有校园网信号')
                other_situations_interface_set()

    # WLAN switch haven't been turned on. 
    except:      
        text_message.set('WLAN开关未打开')
        other_situations_interface_set()

def try_to_make_connection(network):
    # Try to make connection.
    try:
        os.system('netsh wlan connect '+network)
        time.sleep(1.8)
        r = request('GET', 'http://www.bnu.edu.cn')
        soup = BeautifulSoup(r.text, 'html.parser')
        r = request('GET', soup.a['href'])
        srun_portal_pc_url = r.url[:21]
        soup = BeautifulSoup(r.text, 'html.parser')
        ip = soup.find(id='user_ip')['value']
        ac_id = soup.find(id='ac_id')['value']

        # Succeeded.
        parameters[0] = 'Preparing'
        parameters[1] = srun_portal_pc_url
        parameters[2] = ip
        parameters[3] = ac_id
        text_message.set('')
        login_interface_set()

    # Already online. 
    except TypeError:
        parameters[0] = 'OK'
        text_message.set('用户已在线')
        other_situations_interface_set()
    
    # Failed
    except:
        text_message.set('校园网信号差')
        other_situations_interface_set()

def initialize():
    # Initialize the GUI.
    gui.title('')
    screenwidth = gui.winfo_screenwidth()
    screenheight = gui.winfo_screenheight()
    width = str(int(254/1280*screenwidth))
    height = str(int(238/720*screenheight))
    location_x = str(int(502/1280*screenwidth))
    location_y = str(int(190/720*screenheight))
    gui.geometry(width+'x'+height+'+'+location_x+'+'+location_y)
    gui.minsize(int(width), int(height))
    gui.maxsize(int(width), int(height))

def login_interface_set():
    # Show the "Login" interface.
    l_symbol.place(relx=0.3, rely=0.15, relwidth=0.4, relheight=0.1)
    l_title.place(relx=0.15, rely=0.3, relwidth=0.7, relheight=0.1)
    l_username.place(relx=0.065, rely=0.45, relwidth=0.2, relheight=0.1)
    e_username.place(relx=0.3, rely=0.45, relwidth=0.6, relheight=0.1)
    l_password.place(relx=0.065, rely=0.6, relwidth=0.2, relheight=0.1)
    e_password.place(relx=0.3, rely=0.6, relwidth=0.6, relheight=0.1)
    l_message.place(relx=0.3, rely=0.7, relwidth=0.4, relheight=0.1)
    b_setting.place(relx=0.105, rely=0.8, relwidth=0.375, relheight=0.125)
    b_login.place(relx=0.525, rely=0.8, relwidth=0.375, relheight=0.125)

def other_situations_interface_set():
    # Show the "Other Situations" interface.
    try:
        b_login.place_forget()
        e_password.place_forget()
        l_password.place_forget()
        e_username.place_forget()
        l_username.place_forget()
    except:
        pass
    l_symbol.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.1)
    l_title.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.1)
    l_message.place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
    b_setting.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.125)

def login():
    # Try to login.
    try:
        srun_portal_pc_url = parameters[1]
        ip = parameters[2]
        ac_id = parameters[3]

        # Send parameters to get token.
        username = e_username.get()
        password = e_password.get()
        params = {'callback': 'jQuery', 'username': username, 'ip': ip}
        get_challenge_url = srun_portal_pc_url+'/cgi-bin/get_challenge'
        r = request('GET', get_challenge_url, params=params)

        # Receive token, and calculate parameters to send.
        token = r.text[21:85]
        d = {'username': username,
            'password': password,
            'ip': ip,
            'acid': ac_id,
            'enc_ver': 'srun_bx1'}
        json_d = str(d).replace(chr(39), chr(34)).replace(' ', '')
        i = '{SRBX1}'+methods.base64_encode(methods.xEncode(json_d, token))
        hmd5 = methods.md5(password, token)
        chkstr = token+username
        chkstr += token+hmd5
        chkstr += token+ac_id
        chkstr += token+ip
        chkstr += token+'200'
        chkstr += token+'1'
        chkstr += token+i
        password = '{MD5}'+hmd5
        params = {'callback': 'jQuery',
                  'action': 'login',
                  'username': username,
                  'password': password,
                  'ac_id': ac_id,
                  'ip': ip,
                  'chksum': methods.sha1(chkstr),
                  'info': i,
                  'n': '200',
                  'type': '1',
                  'os': device(),
                  'name': 'Windows',
                  'double_stack': '0'}

        # Send parameters to login.
        srun_portal_url = srun_portal_pc_url+'/cgi-bin/srun_portal'
        r = request('GET', srun_portal_url, params=params)
        if r.text[61:72] == 'login_error':
            if r.text[94] == 'P':
                text_message.set('用户名或密码错误')
            elif r.text[94] == 'U':
                text_message.set('用户不存在')
            else:
                text_message.set('登录失败')
        else:
            text_message.set('登录成功')
            other_situations_interface_set()

    # Error occurred.
    except:
        parameters[0] = ''


# Initialize some useful parameters.
parameters = ['', '', '', '']

# Try to keep connection.
_thread.start_new_thread(keep_connection, ())

# Create the GUI.
gui = tkinter.Tk()

# Widgets which appear in both of two interfaces.
l_symbol = tkinter.Label(gui, text='ต⦕⦁.⦁⦖ต', font=('Times New Roman', 20))
l_title = tkinter.Label(gui, text='Easy-BNU-Connector v0.2.0')
text_message = tkinter.StringVar()
l_message = tkinter.Label(gui, textvariable=text_message)
b_setting = tkinter.Button(gui, text='设置', relief='groove')

# Widgets which appear only in "Login" interface.
l_username = tkinter.Label(gui, text='用户名')
e_username = tkinter.Entry(gui)
l_password = tkinter.Label(gui, text='密码')
e_password = tkinter.Entry(gui, show='A')
b_login = tkinter.Button(gui, text='登录', relief='groove', command=login)

# Initialize the GUI.
initialize()

# Show the GUI.
gui.mainloop()