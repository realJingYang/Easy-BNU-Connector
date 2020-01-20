# -*- coding: UTF-8 -*-
# Easy-BNU-Connector v0.2.4
# File: easy_bnu_connector\login.py
# Author: GasinAn
# License: GNU General Public License v3.0

from methods import *

def keep_connection():
    # Initialize.
    global status
    status = 'no_connection'
    other_situations_interface_set()

    # Try to keep connection.    
    test_url = 'http://www.4399.com/robots.txt'        
    while True:
        if status == 'no_connection':
            check_possibility_of_connection()

        # Preparing to login.
        elif status == 'preparing':
            try:
                r = request('GET', test_url, timeout=5)
                if r.text[:10] == 'User-agent':
                    text_message.set('用户已在线')
                    login_interface_forget()
                    other_situations_interface_set()
                    status = 'online'
            except:
                login_interface_forget()
                other_situations_interface_set()
                status = 'no_connection'

        # Already Online.
        else:
            try:
                r = request('GET', test_url, timeout=5)
                if r.text[:10] != 'User-agent':
                    status = 'no_connection'
            except:
                status = 'no_connection'

def check_possibility_of_connection():
    # Check whether it is possible to make connection.
    try:
        try:
            with os.popen('netsh wlan show networks') as p:
                networks = p.read()
        except:
            os.system('chcp 850')
            with os.popen('netsh wlan show networks') as p:
                networks = p.read()
        status_bnu_student = networks.find('BNU-Student\n')
        status_bnu = networks.find('BNU\n')

        # Try to search networks and make connection.
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

    # WLAN switch haven't been turned on. 
    except:      
        text_message.set('WLAN开关未打开')

def try_to_make_connection(network):
    # Try to make connection.
    try:
        os.system('netsh wlan connect '+network)
        for _ in range(30):
            if os.system('ping -n 1 -w 5 www.4399.com') == 0:
                r = request('GET', 'https://www.bnu.edu.cn/', timeout=5)
                break
        goto_url = re.search('<a.+?href="(.+?)".*?>', r.text).group(1)
        r = request('GET', goto_url, timeout=5)

        # Try to get useful parameters.
        global srun_portal_pc_url, ip, ac_id
        srun_portal_pc_url = re.match('https?://.+?/', r.url).group()
        tag_user_ip = re.search('<.+?id="user_ip".*?>', r.text).group()
        ip = re.search('.+?value="(.*?)".*?', tag_user_ip).group(1)
        tag_ac_id = re.search('<.+?id="ac_id".*?>', r.text).group()
        ac_id = re.search('.+?value="(.*?)".*?', tag_ac_id).group(1)

        # Succeeded.
        text_message.set('')
        login_interface_set()
        status = 'preparing'

    # Already online. 
    except AttributeError:
        text_message.set('用户已在线')
        status = 'ok'
    
    # Failed
    except:
        text_message.set('校园网信号差')

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

def login_interface_forget():
    # Remove the "Login" interface.
    for widget in (b_login, e_password, l_password, e_username, l_username):
        widget.place_forget()

def other_situations_interface_set():
    # Show the "Other Situations" interface.
    l_symbol.place(relx=0.3, rely=0.2, relwidth=0.4, relheight=0.1)
    l_title.place(relx=0.15, rely=0.35, relwidth=0.7, relheight=0.1)
    l_message.place(relx=0.3, rely=0.55, relwidth=0.4, relheight=0.1)
    b_setting.place(relx=0.2, rely=0.7, relwidth=0.6, relheight=0.125)

def login():
    # Try to send parameters to get token then login.
    try:
        username = e_username.get()
        password = e_password.get()
        params = {'callback': 'jQuery', 'username': username, 'ip': ip}
        get_challenge_url = srun_portal_pc_url+'cgi-bin/get_challenge'
        r = request('GET', get_challenge_url, params=params, timeout=5)

        # Receive token, and calculate parameters to send.
        token = re.search('"challenge":"(.*?)"', r.text).group(1)
        d = {'username': username,
             'password': password,
             'ip': ip,
             'acid': ac_id,
             'enc_ver': 'srun_bx1'}
        json_d = str(d).replace(chr(39), chr(34)).replace(' ', '')
        i = '{SRBX1}'+base64_encode(x_encode(json_d, token))
        hmd5 = md5(password, token)
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
                  'chksum': sha1(chkstr),
                  'info': i,
                  'n': '200',
                  'type': '1',
                  'os': DEVICE,
                  'name': 'Windows',
                  'double_stack': '0'}

        # Send parameters to login.
        srun_portal_url = srun_portal_pc_url+'cgi-bin/srun_portal'
        r = request('GET', srun_portal_url, params=params, timeout=5)
        if re.search('"error":"(.*?)"', r.text) == 'ok':
            text_message.set('登录成功')
            login_interface_forget()
            other_situations_interface_set()
            status = 'ok'
        else:
            id_errmsg = re.search('"error_msg":"(.+?):.+?"', r.text).group(1)
            text_message.set(ZH_CN[id_errmsg])

    # Error occurred.
    except:
        text_message.set('')
        login_interface_forget()
        other_situations_interface_set()
        status = 'no_connection'

# Create the GUI.
gui = tkinter.Tk()

# Widgets which appear in both of two interfaces.
text_message = tkinter.StringVar()
l_symbol = tkinter.Label(gui, text='ต⦕⦁.⦁⦖ต', font=('Times New Roman', 20))
l_title = tkinter.Label(gui, text='Easy-BNU-Connector v0.2.4')
l_message = tkinter.Label(gui, textvariable=text_message)
b_setting = tkinter.Button(gui, text='设置', relief='groove')

# Widgets which appear only in "Login" interface.
l_username = tkinter.Label(gui, text='用户名')
e_username = tkinter.Entry(gui)
l_password = tkinter.Label(gui, text='密码')
e_password = tkinter.Entry(gui, show='A')
b_login = tkinter.Button(gui, text='登录', relief='groove', command=login)

# Try to keep connection.
_thread.start_new_thread(keep_connection, ())

# Initialize the GUI.
initialize()

# Show the GUI.
gui.mainloop()
