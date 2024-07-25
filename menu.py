from tkinter import *
import subprocess, os, requests, json, socket

ws = Tk()
ws.title('Servers')
ws.geometry('230x320')
ws.config(bg='#c9c9c9')
ws.resizable(False, False)

server = None

player_name = open("data\\player.txt", "r").read()

class ToolTip(object): # tool tip code (not fully by me)

    def __init__(self, widget, event=None, use_mouse=False):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.mouse = use_mouse
        self.last_text = ''

    def showtip(self, text):
        self.text = text
        
        if self.text != self.last_text:
            self.hidetip()

        if self.tipwindow or not self.text:
            return
        if not self.mouse:
            x, y, cx, cy = self.widget.bbox("insert")
            x = x + self.widget.winfo_rootx() + 57
            y = y + cy + self.widget.winfo_rooty() + 27
        else:
            x, y, cx, cy = self.widget.bbox("insert")

            x = ws.winfo_pointerx()
            y = ws.winfo_pointery()
            abs_coord_x = ws.winfo_pointerx() - ws.winfo_vrootx()
            abs_coord_y = ws.winfo_pointery() - ws.winfo_vrooty()

            x, y = abs_coord_x, abs_coord_y
            ws.config(cursor="hand2")

        self.tipwindow = tw = Toplevel(self.widget)
        
        
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        
        label.pack(ipadx=1)

        self.last_text = text

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

        ws.config(cursor="")

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def CreateToolTip_Tag_Bind(widget_, link):
    toolTip = ToolTip(widget_, use_mouse=True)

    def enter(event):
        if event.widget.tag_names(CURRENT)[1] != "link":
            text_num = int(event.widget.tag_names(CURRENT)[1])

            toolTip.showtip(hyper_links[text_num])
        else:
            print("Do not select the download buttons !!!")

    def leave(event):
        toolTip.hidetip()

    widget_.tag_bind(link, '<Motion>', enter)

    widget_.tag_bind(link, '<Leave>', leave)

def join():
    global e1, server
    print(e1.get().replace(" ", "").replace("\n", ""))
    
    open('data\\current_server.txt', 'w').close()

    with open("data\\current_server.txt", "a") as f:
        f.write(e1.get().replace(" ", "").replace("\n", ""))

    server = e1.get().replace(" ", "").replace("\n", "")

    try:
        requests.get(server, timeout=5)
        request_to_server = requests.get(server + "identifier")
        if request_to_server.text == "9782364928734":
            pick_capital()
        else:
            os.startfile("scripts\\errors\\server_is_not_client.vbs")
    except requests.ConnectionError:
        os.startfile("scripts\\errors\\server_not_found.vbs")

def pick_capital():
    download_server_json()

    server_data_file = open(f'data\\server_data.json')
    server_data_file = json.load(server_data_file)

    for i in server_data_file['Server Data']:
        if i == 'started':
            server_started = server_data_file['Server Data'][i]
        
    print(server_started, type(server_started))

    if not server_started:
        upload_server_json()
        ws.destroy()
        os.system("python scripts\\waitingroom.py")
        quit()
    else:
        os.startfile("scripts\\errors\\server_started.vbs")

def upload_server_json():
    url = f'{server}/upload_server_data'
    nm = 'data\\server_data.json'

    server_data_file = open(f'data\\server_data.json')
    server_data_file = json.load(server_data_file)

    for i in server_data_file['Server Data']:
        if i == 'players':
            server_data_file['Server Data'][i].append(player_name)

            with open("data\\server_data.json", 'w') as fp:
                json.dump(server_data_file, fp)


    nmrb = open(nm, 'rb')

    files = [('file', nmrb)]

    r = requests.post(url, files=files)

    if r.ok:
        print("Uploaded JSON Succesfully")
    else:
        print("Error when trying to upload JSON to server !!!")

    nmrb.close()

def download_server_json():
    
    url = f'{server}/return_data'

    print("Downloading Server Data")
    
    os.system('del data\\server_data.json')

    with requests.get(url, stream=True) as r: # for downloading server data ONCE
        r.raise_for_status()
        with open('data\\server_data.json', 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def server(event):
    if event.widget.tag_names(CURRENT)[1] != "link":
        idx = int(event.widget.tag_names(CURRENT)[1])

        cmd='echo '+hyper_links[idx].split()[0].strip() +'|clip'
        return subprocess.check_call(cmd, shell=True)
    else:
        print("Do not select the server buttons !!!")

# def hover(event):
#     if event.widget.tag_names(CURRENT)[1] != "link":
#         idx = int(event.widget.tag_names(CURRENT)[1])
#         print(hyper_links[idx])
#     else:
#         print("Do not select the download buttons !!!")

# downloading the tools data from the server
# refresh()

msg = """
Officially Hosted Servers :

    [version v1.0] - 5/5/2024

"""

num = -1

tools = {}
cur_msg = ''

with open('data/servers.txt') as f:
    rs_tool_file = f.readlines()

text_box = Text(
    ws,
    height=18,
    width=30
)



text_box.insert('end', msg)
hyper_links = []

for line in rs_tool_file:
    cur_msg = ''
    line = line.partition('=') # cant have '=' in application name

    num += 1

    app_name = line[0]

    data_two = line[-1].partition('@')
    server_link = data_two[0]
    software_desc = data_two[2]

    tools[app_name] = server_link

    if len(list(tools.keys())[num]) >= 20:
        tool_name_app = list(tools.keys())[num][0:18] + '...' # no files + link over 30 characters
    else:
        tool_name_app = list(tools.keys())[num]

    # tool_name_app = list(tools.keys())[num]

    sp = ''

    for x in range(11 - len(tool_name_app)):
        sp += ' ' # spaces B)

    cur_msg += "    " + tool_name_app + ' : ' + sp # cant have projects with the same name or link
    
    text_box.insert(END, cur_msg)
    hyper_links.append(f"{server_link}\n\n""Description :\n"f"{software_desc}")
    
    print('"' + data_two[2] + '"')

    if data_two[2] != "no server provided\n" and data_two[2] != "no server provided":
        text_box.tag_config(f'link{num}', foreground="blue")
        print("blue")
    else:
        text_box.tag_config(f'link{num}', foreground="grey")
        print("grey")

    text_box.insert(END,'Copy HTTP\n', (f'link{num}', str(num))) # ,HyperlinkManager(text_box).add(partial(download, hyper_links[num]))
    text_box.tag_bind(f'link{num}', '<Button-1>', server)
    CreateToolTip_Tag_Bind(text_box, f'link{num}')

e1 = Entry(ws, width=19) # Input Server Address Then Press Enter or Join button
e1.focus() 
#e1.bind("<Return>", join)
e1.place(x=100,y=7)

text_box.pack(expand=True)
text_box.config(insertontime=0, state='disabled',font=('Consolas 9'), cursor="")

btn = Button(ws, text = 'Join Server', bd = '1', command = join, font=('Consolas 9'))

var = StringVar()
email = Label(ws, textvariable=var)
var.set("Submit server at rts71937@gmail.com")

btn.place(x=10, y=5)
email.place(x=12, y=295)
CreateToolTip(btn, text = 'Info:\n'
                 'Will join a server with a given link')

CreateToolTip(e1, text = 'Info:\n'
                 'Input Server Address Then Press Enter or Join button')

def on_select(event): # so you cant select text in text box
    print("Nuh uh uh")

text_box.bindtags((str(text_box), "TEntry", "PostEvent", ".", "all"))
text_box.bind_class("PostEvent", "<ButtonPress-1><Motion>", on_select)



ws.mainloop()