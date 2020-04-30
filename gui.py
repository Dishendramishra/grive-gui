import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as tkfiledialog
import ttkthemes as theme
import os
import tkinter.font as font
from tkinter import N,S,E,W
import webbrowser
from termcolor import colored
from pprint import pprint
import json
from os.path import expanduser
import base64

from time import sleep

class MyText(tk.Text):
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
        self.bind("<Control-a>", self.select_all)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        self.tag_remove(tk.SEL,"1.0",tk.END)
        self.see(tk.END)
    # text = self.selection_get(selection='CLIPBOARD')

    def select_all(self,even):
        self.tag_add(tk.SEL,"1.0",tk.END)
        #    self.mark_set(tk.INSERT, "1.0")   # move cursor to start
        return "break"

class GriveGUI():
    def __init__(self):
        self.root = theme.ThemedTk(theme="scidmint")
        self.root.title("Grive GUI")
        img = "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"
        img = base64.urlsafe_b64decode(img)

        self.icon = tk.PhotoImage(data=img) 
        self.root.iconphoto(False, self.icon)

        # self.root = theme.ThemedTk(theme="black")
        # self.root.config(background="#424242")

        self.window_auth = None
        self.window_auth_status = None
        self.flag_dry_run       = tk.BooleanVar()
        self.flag_upload_only   = tk.BooleanVar()
        self.flag_force_download= tk.BooleanVar()
        self.flag_no_remote_new = tk.BooleanVar()
        self.flag_single_dir    = tk.BooleanVar()

        self.cwd = os.getcwd()

        self.set_theme()
        # Sections
        # =====================================================
        self.frame_dir      = ttk.Frame(self.root)
        self.frame_options  = ttk.Frame(self.root)
        self.frame_status   = ttk.Frame(self.root)
        self.frame_actions  = ttk.Frame(self.root)

        self.frame_dir.grid(row=0,column=0,padx=10,pady=(10,0),sticky=W+E)
        self.frame_options.grid(row=1,column=0,padx=10,pady=(10,0),sticky=W+E)
        self.frame_status.grid(row=2,column=0,padx=10,pady=(10,0),sticky=W+E+N+S)
        self.frame_actions.grid(row=3,column=0,padx=10,pady=(10,10),sticky=W+E)

        self.root.columnconfigure(0,weight=True)
        self.root.rowconfigure(2,weight=True)
        self.frame_status.columnconfigure(0,weight=True)
        self.frame_status.rowconfigure(1,weight=True)
        # =====================================================


        # Directory Section
        # =====================================================
        self.lbl_dir     = ttk.Label(self.frame_dir,text="Directory: ")
        self.lbl_dir_loc = ttk.Label(self.frame_dir,text=self.cwd)
        self.btn_dir     = ttk.Button(self.frame_dir,text="Choose Directory")

        self.lbl_dir.pack(side=tk.LEFT,padx=(0,20))
        self.lbl_dir_loc.pack(side=tk.LEFT,padx=(0,15),fill=tk.X,expand=True)
        self.btn_dir.pack(side=tk.RIGHT)
        # =====================================================

        # Options Section
        # =====================================================
        self.lbl_options         = ttk.Label(self.frame_options,text="Options: ")
        self.cbtn_dry_run        = ttk.Checkbutton(self.frame_options,text="Dry Run",\
                                    variable=self.flag_dry_run,onvalue=True,offvalue=False)
        self.cbtn_upload_only    = ttk.Checkbutton(self.frame_options,text="Upload Only",\
                                    variable=self.flag_upload_only,onvalue=True,offvalue=False)
        self.cbtn_force_download = ttk.Checkbutton(self.frame_options,text="Force Download",\
                                    variable=self.flag_force_download,onvalue=True,offvalue=False)
        self.cbtn_no_remote_new  = ttk.Checkbutton(self.frame_options,text="No Remote New",\
                                    variable=self.flag_no_remote_new,onvalue=True,offvalue=False)

        self.cbtn_single_dir     = ttk.Checkbutton(self.frame_options,text="Single Directory",\
                                    variable=self.flag_single_dir,onvalue=True,offvalue=False)
        self.entry_single_dir    = tk.Entry(self.frame_options)

        self.lbl_options.grid(padx=(0,20),row=0,column=0,sticky=tk.W)
        self.cbtn_dry_run.grid(padx=(0,20),row=0,column=1,sticky=tk.W)
        self.cbtn_upload_only.grid(padx=(0,20),row=0,column=2,sticky=tk.W)
        self.cbtn_force_download.grid(padx=(0,20),row=0,column=3,sticky=tk.W)
        self.cbtn_no_remote_new.grid(padx=(0,20),row=0,column=4,sticky=tk.W)

        self.cbtn_single_dir.grid(padx=(0,20),row=1,column=1)
        self.entry_single_dir.grid(padx=(0,0),row=1,column=2,columnspan=2,sticky=tk.W)
        # =====================================================

        # Status Section
        # =====================================================
        self.lbl_status     = ttk.Label(self.frame_status,text="Message")
        self.txt_status     = tk.Text(self.frame_status,height=10)
        self.scroll_status  = ttk.Scrollbar(self.frame_status)

        self.lbl_status.grid(row=0,column=0,sticky=W+E)
        self.txt_status.grid(row=1,column=0,sticky=W+E+N+S)
        self.scroll_status.grid(row=1,column=1,sticky=N+S)

        self.txt_status.config(state="disabled")
        self.txt_status.config(yscrollcommand=self.scroll_status.set)
        self.scroll_status.config(command=self.txt_status.yview)
        # =====================================================

        # Actions Section
        # =====================================================
        self.btn_auth = ttk.Button(self.frame_actions,text="Authenticate")
        self.btn_clear = ttk.Button(self.frame_actions,text="Clear")
        self.btn_sync = ttk.Button(self.frame_actions,text="Sync")
        self.btn_stop = ttk.Button(self.frame_actions,text="Stop")
        
        self.btn_auth.pack(side=tk.LEFT)
        self.btn_clear.pack(padx=(10,0) ,side=tk.RIGHT)
        self.btn_stop.pack(padx=(10,0) ,side=tk.RIGHT)
        self.btn_sync.pack(padx=(10,0),side=tk.RIGHT)
        # =====================================================

        # Text Colors
        # =====================================================
        self.txt_status.tag_config("ok",foreground="#A6E22E",font=('calibri', 9, 'bold'))
        self.txt_status.tag_config("ok_big",foreground="#A6E22E",font=('calibri', 14, 'bold'))
        self.txt_status.tag_config("warning",foreground="#F92672",font=('calibri', 9, 'bold'))
        self.txt_status.tag_config("warning_big",foreground="#F92672",font=('calibri', 14, 'bold'))
        self.txt_status.tag_config("default",foreground="white",font=('calibri', 9))
        # ===================================================== 

        #  Wigets Config
        # =====================================================
        self.btn_auth.config(command=self.authentication_window)
        self.btn_dir.config(command=self.choose_dir)
        self.btn_sync.config(command=self.start_sync)
        self.cbtn_single_dir.config(command = self.single_dir)
        self.entry_single_dir.config(state="disabled")
        self.btn_clear.config(command=self.clear_status)
        self.btn_stop.config(state="disabled")
        self.root.minsize(580,290)
        self.txt_status.config(bg="#424242")
        # =====================================================

        self.on_startup()
        self.check_grive()

    def on_startup(self):
        config_file = expanduser("~")+"/.config/grivegui.conf"

        if os.path.isfile(config_file):
            previous_run_path = None

            with open(config_file,"r") as f:
                previous_run_path = f.read().strip()

            print(previous_run_path)
            try:
                os.chdir(previous_run_path)
                self.lbl_dir_loc.config(text=previous_run_path)
            except Exception as e:
                print(e)
                print("Invalid Contents! Removing.....")
                os.remove(config_file)

    def single_dir(self):
        print("single checkbutton")
        if self.flag_single_dir.get():
            self.entry_single_dir.config(state="normal")
        else:
            self.entry_single_dir.config(state="disabled")

    def clear_options(self):
        self.flag_dry_run.set(0)
        self.flag_upload_only.set(0)
        self.flag_force_download.set(0)
        self.flag_no_remote_new.set(0)
        self.flag_single_dir.set(0)
        self.entry_single_dir.config(state="normal")
        self.entry_single_dir.delete(0,tk.END)
        self.entry_single_dir.config(state="disabled")

    def choose_dir(self):
        path = tkfiledialog.askdirectory(initialdir=os.getcwd())
        self.lbl_dir_loc.config(text=path)
        self.cwd = path
        os.chdir(self.cwd)
        print(colored("current path: "+path,"green"))
        self.clear_options()
        self.clear_status()
        self.check_grive()

    def set_theme(self):
        ttk.Style().configure("TLabel", font=("calibri","9"))
        ttk.Style().configure("TButton", font=("calibri","9"))
        ttk.Style().configure("TCheckbutton", font=("calibri","9"))

    def write_status(self, msg, color="default"):
        self.txt_status.config(state="normal")
        self.txt_status.insert(tk.END,msg, color)
        self.txt_status.config(state="disabled")
        self.txt_status.see(tk.END)

    def clear_status(self):
        self.txt_status.config(state="normal")
        self.txt_status.delete("1.0",tk.END)
        self.txt_status.config(state="disabled")

    def start_sync(self):
        self.save_settings()

    def check_grive(self):

        if not os.path.isfile(".grive"):
            self.write_status("Grive NOT Configured!","warning")
            self.write_status("😣\n","warning_big")
            self.btn_sync.config(state="disabled")
            
        else:
            self.write_status("Grive is Configured!","ok")
            self.write_status("😁\n","ok_big")
            self.btn_sync.config(state="normal")
            

            if os.path.isfile(".grivegui"):
                print(colored("Found!: .grivegui","green"))
                settings = None
                with open(".grivegui","r") as f:
                    settings = f.read()
                    settings = json.loads(settings)
                
                print(settings)
                
                self.entry_single_dir.config(state="normal")
                self.entry_single_dir.delete(1,tk.END)
                self.entry_single_dir.insert(tk.END,settings.get("single_dir")[1])
                self.entry_single_dir.config(state="disabled")

                if settings.get("dry_run"):
                    self.cbtn_dry_run.invoke()
                if settings.get("upload_only"):
                    self.cbtn_upload_only.invoke()
                if settings.get("force_download"):
                    self.cbtn_force_download.invoke()
                if settings.get("no_remote_new"):
                    self.cbtn_no_remote_new.invoke()
                if settings.get("single_dir")[0]:
                    print("ran")
                    self.entry_single_dir.config(state="normal")
                    self.cbtn_single_dir.invoke()

                # print(settings)

    def save_settings(self):        
        settings = {"dry_run":False,\
                    "upload_only":False,\
                    "force_download":False,\
                    "no_remote_new":False,\
                    "single_dir":[False,""],\
                    }

        if self.flag_dry_run.get():
            settings["dry_run"] = True
        if self.flag_upload_only.get():
            settings["upload_only"] = True
        if self.flag_force_download.get():
            settings["force_download"] = True
        if self.flag_no_remote_new.get():
            settings["no_remote_new"] = True
        if self.flag_single_dir.get():
            settings["single_dir"][0] = True

        settings["single_dir"][1] = self.entry_single_dir.get()


        json_dump = json.dumps(settings)
        pprint(json_dump)

        if not os.path.isfile("grivegui"):
            with open(".grivegui","w") as f:
                f.write(json_dump)

        home = expanduser("~")
        with open(home+"/.config/grivegui.conf","w") as f:
            f.write(self.cwd)
            f.write("\n")


    def create_url(self,url=None):
        id     = self.txt_client_id.get("1.0",tk.END).strip()
        secret = self.txt_secret.get("1.0",tk.END).strip()
        
        url = "https://accounts.google.com/o/oauth2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive&redirect_uri=urn:ietf:wg:oauth:2.0:oob&response_type=code&client_id="
        url += id

        if id != "" and secret != "":
            self.msg_url.bind("<Enter>",lambda e: self.msg_url.config())
            self.msg_url.bind("<Button-1>",lambda e: webbrowser.open_new_tab(url))
            self.msg_url.config(text=url)
            self.msg_url.config(cursor="hand2")
            self.btn_auth_token.config(state="normal")
            self.txt_auth_token.config(bg="white")
            self.txt_auth_token.config(state="normal")

    def authentication_window(self):
        self.root.withdraw()

        self.window_auth = tk.Toplevel()
        self.window_auth.iconphoto(False, self.icon)
        self.window_auth.title("Grive GUI")
        self.window_auth.minsize(400,400)

        self.window_auth.protocol("WM_DELETE_WINDOW",self.go_home)
        
        # Widgets
        # =====================================================
        self.lbl_client_id   = ttk.Label(self.window_auth,text="Client Id")
        self.txt_client_id   = MyText(self.window_auth,height=3,width=50)
        self.lbl_secret      = ttk.Label(self.window_auth,text="Secret")
        self.txt_secret      = MyText(self.window_auth,height=3,width=50)
        self.btn_submit      = ttk.Button(self.window_auth,text="Submit")
        self.lblframe_url    = ttk.LabelFrame(self.window_auth,text="URL")
        self.msg_url         = tk.Message(self.lblframe_url)
        self.lblframe_token  = ttk.LabelFrame(self.window_auth,text="Auth Token")
        self.txt_auth_token  = MyText(self.lblframe_token,height=3,width=50)        
        self.btn_auth_token  = ttk.Button(self.window_auth,text="Authenticate",command=self.authentication_status)

        self.lbl_client_id.grid(row=0,column=0,padx=10,pady=(0),sticky=W)
        self.txt_client_id.grid(row=1,column=0,padx=10,pady=(0,10),sticky=W+E+N+S)
        self.lbl_secret.grid(row=2,column=0,padx=10,pady=(0),sticky=W)
        self.txt_secret.grid(row=3,column=0,padx=10,pady=(0,10),sticky=W+E+N+S)
        self.btn_submit.grid(row=4,column=0,padx=10,pady=0,sticky=E)      
        self.lblframe_url.grid(row=5,column=0,padx=10,pady=0,sticky=W+E+N+S)      
        self.msg_url.pack(expand=True,fill="x") 
        self.lblframe_token.grid(row=6,column=0,padx=10,pady=0,sticky=W+E+N+S)
        self.txt_auth_token.pack(expand=True,fill="both")
        self.btn_auth_token.grid(row=7,column=0,padx=10,pady=10,sticky=E)
        # =====================================================

        # Widgets Config
        # =====================================================
        self.window_auth.rowconfigure(1,weight=True)
        self.window_auth.rowconfigure(3,weight=True)
        self.window_auth.columnconfigure(0,weight=True)
        
        self.btn_auth_token.config(state="disabled")
        self.txt_auth_token.config(bg="grey")
        self.txt_auth_token.config(state="disabled")
        self.btn_submit.config(command=self.create_url)


        self.msg_url.config(fg="blue")
        self.msg_url.bind("<Configure>", lambda e: self.msg_url.configure(width=e.width-10))
        # =====================================================

    def auth_msg_done(self):
        self.window_auth.deiconify()
        self.window_auth_status.destroy()

    def go_home(self):
        if self.window_auth:
            self.window_auth.destroy()
        if self.window_auth_status:
            self.window_auth_status.destroy()
        self.root.deiconify()
        self.clear_options()
        self.clear_status()
        self.check_grive()

    def authentication_status(self):
        if self.txt_auth_token.get("1.0",tk.END).strip() == "":
            print(colored("token can't be empty","red"))
            return

        # Widgets
        # =====================================================   
        self.window_auth_status = tk.Toplevel()
        self.window_auth_status.iconphoto(False, self.icon)
        self.window_auth_status.title("Grive GUI")
        self.window_auth_status.minsize(350,250)
        self.window_auth.withdraw()
        self.window_auth_status.protocol("WM_DELETE_WINDOW",self.auth_msg_done)

        self.txt_auth_status = MyText(self.window_auth_status,height=10,width=50)
        self.btn_auth_status = ttk.Button(self.window_auth_status,text="Done")
        
        self.txt_auth_status.pack(padx=10,pady=(10),expand=True,fill="both")
        self.btn_auth_status.pack(padx=10,pady=(0,10),side=tk.BOTTOM)
        # =====================================================

        # Widgets Config
        # =====================================================
        self.txt_auth_status.config(state="disabled")
        self.btn_auth_status.config(state="disabled")
        self.btn_auth_status.config(command=self.go_home)
        # =====================================================

    def write_authentication_status(self,msg):
        self.txt_auth_status.config(state="normal")
        self.txt_auth_status.insert(tk.END,msg)
        self.txt_auth_status.config(state="disabled")
        self.txt_auth_status.see(tk.END)

    def run(self):
        self.root.mainloop()
    
    def kill(self):
        self.root.destroy()
    
    def get_window_size(self,event):
        print(self.window_auth.winfo_reqheight())
        print(self.window_auth.winfo_reqwidth())

if __name__ == '__main__':
    app = GriveGUI()
    app.run()