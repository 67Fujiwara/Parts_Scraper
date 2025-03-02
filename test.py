from bs4 import BeautifulSoup
import requests
from collections import Counter
from urllib.parse import urlparse, urljoin
import tkinter
import tkinter as tk
import tkinter.font as f
from tkinter import ttk, Toplevel
from tkinter import *

class WindowController:
    def __init__(self, master, title, bg_color, win_size):
        self.master = master
        self.master.title(title)
        self.master.config(bg=bg_color)
        self.master.geometry(win_size)
        self.font1 = f.Font(family="Meiryo UI", weight="normal", size=10, slant="italic")
        self.font2 = f.Font(family="Lucida Console", weight="bold", size=12, slant="italic")
        self.font3 = f.Font(family="Lucida Console", weight="bold", size=10, slant="italic")

    def create_frame(self, width, height, expand):
        self.frame = tkinter.Frame(self.master, width=width, height=height, bd=0, bg='white', relief=tkinter.RAISED)
        self.frame.pack(expand=expand, fill=tk.BOTH)
        # self.frame.rowconfigure(0, weight=1) # 0行目を縦方向に引き伸ばす
        # self.frame.columnconfigure(1, weight=1) # 1列目を横方向に引き伸ばす
        return self.frame
        
        
    def create_entry(self, frame, width, row, column):
        entry = tk.Entry(frame, width=width)
        entry.grid(row=row , column=column)
        return entry
    
       
    def create_button(self, frame, text, command, bg_color, font_color, row, column):
        button = tk.Button(frame, text=text, command=command, bg=bg_color, fg=font_color, cursor="hand2")
        button.grid(row=row , column=column)
        
       
    def create_label(self, frame, justify_pos, text, font, font_color, row, column, padx, pady):
        font = font
        label = tk.Label(frame, justify=justify_pos, text=text, bg='white', fg=font_color)
        label["font"] = font
        label.grid(padx=padx, pady=pady, row=row, column=column)
       
    
    def on_enter(self, event):
        event.widget.config(cursor="hand2")
        # print('on_enter')
        
        
    def on_leave(self, event):
        event.widget.config(cursor="")
        # print('on_leave')
       
      
    def create_combobox(self, frame, list_height, char_width, justify_pos, list, row, column):
        combobox = ttk.Combobox(frame, 
                                height=list_height, 
                                width=char_width, 
                                justify=justify_pos, 
                                state="readonly", 
                                values=list,
                                cursor="hand2")
        combobox.grid(row=row, column=column)
        # self.combobox.bind("<<ComboboxSelected>>", self.on_selection)
        # combobox.bind("<Enter>", self.on_enter)
        # combobox.bind("<Leave>", self.on_leave)
        return combobox
       
       
    
class MainApp:
    def __init__(self, root):
        self.root = root      
        self.bg_white = "white"
        self.font_black = "black"
        self.p_tag_list = []
        self.win_control = WindowController(root, "Parts_Scraper", self.bg_white, "300x200")
        frame1 = self.win_control.create_frame(380, 100, True)
        self.win_control.create_label(frame1, 'left', 'step1', self.win_control.font1, 'gray', 0, 0, 5, 5)
        self.win_control.create_label(frame1, 'center', 'URL:',self.win_control.font2, 'black', 1, 1, 0, 0)
        self.set_url = self.win_control.create_entry(frame1, 25, 1, 2)
        self.win_control.create_button(frame1, 'click', self.html_parser, 'white', 'black', 2, 3)
        frame2 = self.win_control.create_frame(380, 100, True)
        self.win_control.create_label(frame2, 'center', 'step2', self.win_control.font1, 'gray', 3, 0, 5, 5)
        self.win_control.create_label(frame2, 'center', 'Assy:',self.win_control.font2, 'black', 4, 1, 0, 0)
        self.combobox1 = self.win_control.create_combobox(frame2, 10, 20, 'center', self.p_tag_list, 4, 2)
        self.win_control.create_button(frame2, 'click', self.open_sub, 'white', 'black', 5, 3)
   
        
    def check_response(self, response):
        # session = requests.Session()
        if response.status_code == 200:
            print('response OK')
        else:
            print('response_NG')
    
        
    def html_parser(self):
        self.session = requests.Session()
        login_url = 'https://uta.pw/sakusibbs/users.php?action=login&m=try'

        USER = "山田太郎"
        PASS = "password"
        login_info = {
            'username_mmlbbs6':USER,
            'password_mmlbbs6':PASS,
            # 'back':'index.php',
            # 'mml_id':'1619'
            
        }
        response = self.session.post(login_url, data=login_info)
        self.check_response(response)

        protected_url = self.set_url.get()
        self.response1 = self.session.get(protected_url)
        self.check_response(self.response1)

        
        #URLを解析する
        parsed_url = urlparse(protected_url)
        # ドメイン(ネットﾛｹｰｼｮﾝ)とパスを取得します
        self.domain = parsed_url.netloc
        self.path = parsed_url.path  
        print(self.domain)
        print(self.path)
        self.search_assembly()


    def search_assembly(self):
        soup = BeautifulSoup(self.response1.text, 'html.parser')
        Top5_elems = soup.find_all('a', class_='indextitle')
        
        self.href_list = []
        for elem in Top5_elems:
            href = elem['href']
            href = 'https://' + self.domain + href
            self.href_list.append(href)
            print(href)
            
        self.Top5_texts = [elem.get_text() for elem in Top5_elems]
        print(self.Top5_texts)

        div_elem = soup.find('div', style='margin-left:auto; margin-right:auto; width:960px; text-align:left;')
        self.elem_machineID = div_elem.find('h2')
        print(self.elem_machineID.text)
    
        self.update_widget()
        
        
    def update_widget(self):
        # print('update_widget')
        self.combobox1['values'] = self.Top5_texts  #リストを更新
        self.combobox1.update_idletasks()   #再描画
        
        
    def open_sub(self):
        # print('open_sub')
        machine_ID = self.elem_machineID.text
        self.assembly = self.combobox1.get()
        sub_win = Toplevel(self.root)
        self.sub_control = WindowController(sub_win, "Parts_list", self.bg_white, "300x400")
        sub_frame1 = self.sub_control.create_frame(280, 50, False)
        self.sub_control.create_label(sub_frame1, 'center', machine_ID,self.win_control.font3, 'black', 0, 0, 5, 5)
        self.sub_control.create_label(sub_frame1, 'center', self.assembly,self.win_control.font3, 'black', 0, 1, 5, 5)
        self.create_treeview(sub_win)


    def create_treeview(self, parent):
        tree = ttk.Treeview(parent)
        tree["columns"] = ("Count")
        tree.heading("#0", text="P/N")
        # tree.heading("P/N", text="Name")
        tree.heading("Count", text="Count")
        tree.column("#0", width=250, anchor="center")
        # tree.column("Name", width=130, anchor="center")
        tree.column("Count", width=50, anchor="center")
        
        # 行の背景色を設定するタグを追加
        tree.tag_configure('oddrow', background='lightgrey')
        tree.tag_configure('evenrow', background='white')
        
        # データを取得してツリービューに挿入
       
        
        # self.combobox_index = self.combobox1['values'].index(self.assembly) 
        # print(self.href_list[self.combobox_index])  
        # res = requests.get(self.href_list[self.combobox_index])
        # soup = BeautifulSoup(res.text, 'html.parser')
        # div_tags = soup.find('div', class_='recipesDetailIngredients')
        # items = div_tags.find_all('li')
        # item_texts = [item.get_text() for item in items]
        items = ['test1 / ﾃｽﾄ1 / 1ｺ', 'test2 / ﾃｽﾄ2 / 2ｺ', 'test3 / ﾃｽﾄ3 / 3ｺ', 'test1 / ﾃｽﾄ1 / 4ｺ', 'test5 / ﾃｽﾄ5 / 5ｺ', 'test2 / ﾃｽﾄ2 / 6ｺ', 'test3 / ﾃｽﾄ3 / 7ｺ', 'test8 / ﾃｽﾄ8 / 8ｺ', 'test9 / ﾃｽﾄ9 / 9ｺ', 'test10 / ﾃｽﾄ10 / 10ｺ']
        item_text = [item.split(' / ') for item in items]
        item_counts = Counter(items)
        print(item_text)
        text_a = item.split(' / ')
        print(text_a)


        for index, (item, count) in enumerate(item_counts.items()):
            tag = 'oddrow' if index % 2 == 0 else 'evenrow'
            pn, name, count = item
            count = count.replace('ｺ', '')  #ｺを削除
            tree.insert("", "end", text=pn, values=(count,), tags=(tag,))
            print(item)
        tree.pack(expand=True, fill=tk.BOTH)
        tree.update()


root = tkinter.Tk()
app = MainApp(root)


root.mainloop()
