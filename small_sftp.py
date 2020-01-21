# -*- coding:utf-8 -*-
# A small Python - SFTP client
# Last modified by Ruijie Shi 2020.01.21

import paramiko
import os
import stat

def ssh_connect(ip, port, user, password):

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # for host not in the know_hosts file
        ssh.connect(ip, port = port, username = user, password = password, allow_agent = False, look_for_keys = False)
        stdin, stdout, stderr = ssh.exec_command('date')
        print("\n----- SSH connected -----\n")
        print(stdout.readlines())
        return ssh
    
    except:
        print("\n----- SSH connect failed -----\n")
        exit()


def upload_file(ssh, local_file, remote_file):

    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    print("\n " + local_file + " → " + remote_file)
    sftp.close()
    return


def download_file(ssh, remote_file, local_file):

    sftp = ssh.open_sftp()
    sftp.get(remote_file, local_file)
    print("\n " + remote_file + " → " + local_file)
    sftp.close()
    return


def upload_dir(ssh, local_dir, remote_dir):

    sftp = ssh.open_sftp()

    try:
        sftp.stat(remote_dir)
    except IOError:
        sftp.mkdir(remote_dir)

    for root, dirlist, filelist in os.walk(local_dir):

        for filename in filelist:
            local_file = os.path.join(root,filename).replace(os.sep,"/")
            part_path = local_file.replace(local_dir.replace(os.sep,"/"), '') # the path without the part of current directory
            remote_file = os.path.join(remote_dir,part_path)
            try:
                sftp.put(local_file, remote_file)
                print("\n " + local_file + " → " + remote_file)
            except Exception as e:
                sftp.mkdir(os.path.split(remote_file)[0])
                sftp.put(local_file, remote_file)
                print("\n " + local_file + " → " + remote_file)

        for dirname in dirlist: # solve the problem of empty folder
            local_dir_x = os.path.join(root,dirname).replace(os.sep, "/")
            part_path_x = local_dir_x.replace(local_dir.replace(os.sep,"/"), '')
            remote_dir_x = os.path.join(remote_dir,part_path_x)
            try:
                sftp.mkdir(remote_dir_x)
                print("\n " + local_dir_x + " → " + remote_dir_x)
            except Exception as e:
                continue

    sftp.close()
    return


def download_dir(ssh, remote_dir, local_dir):

    sftp = ssh.open_sftp()
    if not os.path.exists(local_dir): os.mkdir(local_dir)
    filelist = sftp.listdir_attr(remote_dir)
    for item in filelist:
        remote_item = os.path.join(remote_dir,item.filename)
        local_item = os.path.join(local_dir,item.filename)
        if stat.S_ISREG(item.st_mode): # if regular file
            sftp.get(remote_item, local_item)
            print("\n " + remote_item + " → " + local_item)
        elif stat.S_ISDIR(item.st_mode): # if directory
            remote_item = remote_item + remote_dir[-1]
            download_dir(ssh, remote_item, local_item)
    sftp.close()
    return


ip = input("\n>>> IP address: ")
user = input("\n>>> Username: ")
password = input("\n>>> Password: ")
port = 22 # change if necessary

ssh = ssh_connect(ip, port, user, password)

while True:

    print('''
    -------- SFTP Tool --------
    Upload file           [ 1 ]
    Download file         [ 2 ]
    Upload directory      [ 3 ]
    Download dirctory     [ 4 ]
    Exit                  [ q ]
    ---------------------------
    Attention: please use ABSOLUTE PATH in this tool
    ''')
    choice = input(">>> ")

    if choice == "1":
        print("\n-------- Upload file --------")
        local_file = input("\n>>> Path of local file: ")
        remote_file = input("\n>>> Path of remote file: ")
        upload_file(ssh, local_file, remote_file)
        print("\n File upload completed")

    elif choice == "2":
        print("\n-------- Download file --------")
        remote_file = input("\n>>> Path of remote file: ")
        local_file = input("\n>>> Path of local file: ")
        download_file(ssh, remote_file, local_file)
        print("\n File download completed")

    elif choice == "3":
        print("\n-------- Upload dirctory --------")
        print('''
    Attention: the path of directory must be ENDED WITH forward
               slash (Unix) or double back slash (Windows)
        ''')
        local_dir = input("\n>>> Path of local directory: ")
        remote_dir = input("\n>>> Path of remote directory: ")
        upload_dir(ssh, local_dir, remote_dir)
        print("\n Directory upload completed")

    elif choice == "4":
        print("\n-------- Download dirctory --------")
        print('''
    Attention: the path of directory must be ENDED WITH forward
               slash (Unix) or double back slash (Windows)
        ''')
        remote_dir = input("\n>>> Path of remote directory: ")
        local_dir = input("\n>>> Path of local directory: ")
        download_dir(ssh, remote_dir, local_dir)
        print("\n Directory download completed")

    elif choice == "q":
        exit()

    else:
        print("\n Wrong Input")