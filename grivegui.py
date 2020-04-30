from termcolor import colored
from subprocess import Popen, PIPE, STDOUT

from pprint import pprint

import threading
import os

from gui import GriveGUI
import tkinter as tk

import json
from time import sleep

class GriveWrapper():
    def __init__(self,cmd):
        
        cmd = cmd.split()
        self.process = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)

    def write_stdin(self,cmd):
        print(colored("grive: ","blue"),end="")
        print(colored(cmd,"red"))
        cmd = cmd+"\n"
        self.process.stdin.write(cmd.encode())
        self.process.stdin.flush()

    def read_stdout(self,break_flag=None):
        text  = []
        for line in self.process.stdout:
            line = line.decode("utf-8")
            text.append(line)

            if break_flag and line.startswith(break_flag):
                break

        return text        

    def kill(self):
        self.process.kill()

class Grive(GriveGUI):

    def __init__ (self):
        super().__init__()
        self.grive = None
        self.cwd = os.getcwd()

    def check_grive(self):
        super().check_grive()

    def start_sync(self):
        super().start_sync()

        settings = None
        with open(".grivegui","r") as f:
            settings = f.read()
            settings = json.loads(settings)

        # in future implement progess bar

        cmd = "grive"

        if settings.get("dry_run"):
            cmd += " --dry-run"
        if settings.get("upload_only"):
            cmd += " --upload-only"
        if settings.get("force_download"):
            cmd += " --force"
        if settings.get("no_remote_new"):
            cmd += " --no-remote-new"
        if settings.get("single_dir")[0]:
            cmd += " -s "+settings.get("single_dir")[1]

        print(cmd)

        if not self.grive:
            self.btn_sync.config(state="disabled")
            self.btn_stop.config(state="normal")

            self.grive = GriveWrapper(cmd)

            thread = threading.Thread(target=self.status_update,args=(self.grive.process.stdout,None))
            thread.setDaemon(True)
            thread.start()
            
            self.btn_stop.config(command=self.grive.kill)

    def status_update(self,process,buffer=None):
        line = None
        self.write_status("\nStarting Sync...\n","ok")
        while True:
            line = process.readline().decode("utf-8")

            if line:
                self.write_status(line)
                # sleep(0.1)
            else:
                self.write_status("Done!\n","ok")
                break
        
        self.btn_sync.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.grive = None

    def authentication_window(self):
        super().authentication_window()

    def authentication_done(self):
        super().authentication_done()
        print("thread killed")
        if self.grive:
            self.grive.kill()
            self.grive = None

    def create_url(self):
        super().create_url()

    def write_authentication_status(self,msg):
        super().write_authentication_status(msg)

    def auth_status_update(self,process,buffer):
        line = None

        error = False

        while True:
            line = process.readline().decode("utf-8")

            if line:
                print(line)
                self.write_authentication_status(line)
                if line.startswith("Failed to obtain auth token:") or line.startswith("exception:"):
                    error = True
            else:
                if error:
                    self.write_authentication_status("FAILED!")
                else:
                    self.write_authentication_status("SUCCESS!")
                print(colored("closing thread!","red"))
                self.grive = None
                self.btn_auth_status.config(state="normal")
                break
                
    def authentication_status(self):

        print(colored(self.cwd,"red"))

        token   = self.txt_auth_token.get("1.0",tk.END).strip()
        
        if self.txt_auth_token.get("1.0",tk.END).strip() == "":
            print(colored("token can't be empty","red"))
            return
        
        id      = self.txt_client_id.get("1.0",tk.END).strip() 
        secret  = self.txt_secret.get("1.0",tk.END).strip()
        
        print(self.grive)

        if os.path.isfile(".grive"):
            print(colored("removing .grive","blue"))
            os.remove(".grive")

        if os.path.isfile(".grivegui"):
            os.remove(".grivegui")
            print(colored("removing .grivegui","blue"))

        if id!="" and secret!="" and not self.grive: 
            self.grive = GriveWrapper("grive -a --id {} --secret {} -s None --dry-run".format(id,secret))
            output = self.grive.read_stdout("Please input the authentication")
        
            print(colored("\ncommand ouput:","blue"))
            print(colored("".join(output),"red"))        

            super().authentication_status()

            self.grive.write_stdin(token)
            self.thread = threading.Thread(target=self.auth_status_update,args=(self.grive.process.stdout,None))
            self.thread.setDaemon(True)
            self.thread.start()
        
if __name__ == "__main__":
    app = Grive()
    app.run()