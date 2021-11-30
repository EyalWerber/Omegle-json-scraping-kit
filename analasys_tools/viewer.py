from tkinter import *
from omegle_analasis1_1 import *
from functools import partial
import subprocess

WELCOME_PROMPT = '''
Welcome to
 __      _______ ________          ________ _____  
 \ \    / /_   _|  ____\ \        / /  ____|  __ \ 
  \ \  / /  | | | |__   \ \  /\  / /| |__  | |__) |
   \ \/ /   | | |  __|   \ \/  \/ / |  __| |  _  / 
    \  /   _| |_| |____   \  /\  /  | |____| | \ \ 
     \/   |_____|______|   \/  \/   |______|_|  \_\
'''
ERROR_PROMPT = '''
  _   _  ___ _____   _____ ___  _   _ _   _ ____  _ 
 | \ | |/ _ \_   _| |  ___/ _ \| | | | \ | |  _ \| |
 |  \| | | | || |   | |_ | | | | | | |  \| | | | | |
 | |\  | |_| || |   |  _|| |_| | |_| | |\  | |_| |_|
 |_| \_|\___/ |_|   |_|   \___/ \___/|_| \_|____/(_)
'''

def copy():
    return subprocess.run(['powershell' ,'Get-Content temp.txt -encoding UTF8 | Set-Clipboard'],shell=True) #requires powershell!

def reverse_order():
    global conv_list
    conv_list = conv_list[::-1]
    latest_button['text'],oldest_button['text'] = oldest_button['text'],latest_button['text']
    update()

def index_check():
    global counter
    if counter == 0:
        prev_button['state'] = DISABLED
        latest_button['state'] = DISABLED
    else:
        prev_button['state'] = NORMAL
        latest_button['state'] = NORMAL

    if counter == len(conv_list)-1:
        next_button['state'] = DISABLED
        oldest_button['state'] = DISABLED
    else:
        next_button['state'] = NORMAL
        oldest_button['state'] = NORMAL

    if search_clicked.get()==('word' or 'disconnected'):
        
        search_word['state']=NORMAL
    else:
        
        search_word['state']=DISABLED

def update():
    global text_box
    
    index_check()
    text_box.delete(1.0, END)

    if (len(conv_list) !=0):
        text_box.insert(INSERT, conv_list[counter])
    else:
        text_box.insert(INSERT,ERROR_PROMPT)


    file = open('temp.txt','w',encoding="utf8")
    file.write(text_box.get(1.0,END))
    file.close() 

    length_num_label['text'] = f'conv - {counter+1}/{len(conv_list)} - length = {len(conv_list[counter])} '



def change_search_cat(event):
    
    global conv_list
    
    conv_list = ConversationList()
    conversations = conv_list.conversations

    match search_clicked.get():
        case 'date':
            conv_list = conversations[::-1]
            latest_button['text'],oldest_button['text']= 'newest','oldest'
            
        case 'length':
            conv_list = list(sorted(conversations, key=len))[::-1]
            latest_button['text'],oldest_button['text']= 'longest','shortest'
            

        case 'duration':
            conv_list = list(sorted(conversations,
                             key=lambda cl: cl.duration))[::-1]
            latest_button['text'],oldest_button['text']= 'longest','shortest'
            
        case 'word':
            conv_list = conv_list.get_conv_byWord(search_word.get())
            

            
        case 'disconnected':
            conv_list = conv_list.get_conv_byDisconnected(search_word.get()[0])




    conv_control('first')
    update()

def conv_control(cmd):
    global counter
    match cmd:
        case 'next':
            counter += 1
        case 'prev':
            counter -= 1
        case 'first':
            counter = 0
        case 'last':
            counter = len(conv_list)-1
        
    update()


counter = 0

# Window setup
root = Tk()
root.title('Viewer')
root.geometry("1000x600")

text_frame = Frame(root)
text_frame.pack()

text_box = Text(text_frame, width=100, height=10, font= ("Courier", 16))
text_box.pack(pady=20)

text_box.insert(INSERT, WELCOME_PROMPT)

info_frame = Frame(root)


# buttons
nav_frame = Frame(root)
nav_frame.pack()

oldest_button = Button(nav_frame, text="oldest",
                       command=partial(conv_control, 'last'))
oldest_button.grid(row=1, column=3)
prev_button = Button(nav_frame, text="Prev",
                     command=partial(conv_control, 'prev'))
prev_button.grid(row=1, column=1)
next_button = Button(nav_frame, text="Next",
                     command=partial(conv_control, 'next'))
next_button.grid(row=1, column=2)
latest_button = Button(nav_frame, text="newest",
                       command=partial(conv_control, 'first'))
latest_button.grid(row=1, column=0)

hud_frame = Frame(root)
hud_frame.pack()

length_num_label = Label(hud_frame)
length_num_label.grid(row=2, column=2)


# arrange by selector
search_options = ['word','date', 'length', 'duration','disconnected']
arrange_options = ['date','length','duration']

search_frame = Frame(root)
search_frame.pack()

search_clicked = StringVar()
search_clicked.set(search_options[0])

search_label = Label(search_frame,text = 'search by:')
search_label.grid(row=0,column=0)
search_menu = OptionMenu(search_frame, search_clicked, *search_options, command=change_search_cat)
search_menu.grid(row=0, column=1)

arrange_clicked = StringVar()
arrange_clicked.set(search_options[0])

# arrange_label = Label(search_frame,text = 'arrange by:')
# arrange_label.grid(row=1,column=0)
# arrange_menu = OptionMenu(search_frame, arrange_clicked, *arrange_options, command=change_search_cat)
# arrange_menu.grid(row=1, column=1)

order_buttun = Button(search_frame, text='↑↓',command=reverse_order)
order_buttun.grid(row=1,column=2)

search_word = Entry(search_frame)

search_word.grid(row=0, column=2)


get_button = Button(search_frame, text='Get', command=partial(change_search_cat,'event'))

get_button.grid(row=0, column=3)

action_frame = Frame(root)
action_frame.pack()

copy_button = Button(action_frame, text = 'Copy to clipboard', command=partial(copy))
copy_button.grid(row=0, column=2)

root.mainloop()
