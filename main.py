import os
import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
from converter import SQL


class back:
    def fnc(self,event=None):
        try:
            canvas1.delete(self.statr)
        except Exception:
            pass   
        self.user_name = user_name.get()
        self.password = password.get()
        try:
            SQL(self.user_name,self.password).login()
            select_file = tk.Button(win, text = 'Select File',command = back.search,font="ComicSansMSBold 10")
            canvas1.create_window(250,90,window=select_file)
            self.select_file = select_file
            database_name = canvas1.create_text(450,20,text="Database",font="ComicSansMS 14",fill="white")
            self.database_name = database_name
            database_entry = AutocompleteCombobox(win,width = 20,font =('Times',12))
            canvas1.create_window(610,20,window = database_entry)
            self.database_entry = database_entry
            SQL(self.user_name,self.password).login(drop_list=database_entry)
            if status_var.get() == "Login Failed!":
                status_var.set("Login successful!")
                canvas1.delete(self.statf)
                stat = canvas1.create_text(240,120,text=status_var.get(),font="ComicSansMS 14",fill="green")
                self.stat = stat
            elif status_var.get() != "Login successful!":
                status_var.set("Login successful!")
                stat = canvas1.create_text(240,120,text=status_var.get(),font="ComicSansMS 14",fill="green")
                self.stat = stat

            
        except Exception:  
            if status_var.get() == "Login successful!":
                self.database_entry.destroy()
                canvas1.delete(self.database_name)
                self.select_file.destroy()
                status_var.set("Login Failed!")
                canvas1.delete(self.stat)
                statf = canvas1.create_text(240,120,text=status_var.get(),font="ComicSansMS 14",fill="red")
                self.statf = statf 
                try:
                    self.convert_but.destroy()
                    canvas1.delete(self.table_name)
                    self.table_name_entry.destroy()
                except Exception:
                    pass    
            elif status_var.get() != "Login Failed!": 
                status_var.set("Login Failed!")
                statf = canvas1.create_text(240,120,text=status_var.get(),font="ComicSansMS 14",fill="red")
                self.statf = statf
              

        back.log_input(status_var.get())        
        print(status_var.get())
            
    def search(self,event = None):
        type_of_file = (('Excel file', '*.xlsx*'), ('All files', '*.*'))
        search_file = filedialog.askopenfilename(filetypes=type_of_file)
        self.search_file = search_file
        if self.search_file != "":
            back.log_input(self.search_file)
            convert_but = tk.Button(win, text = 'Convert',command = back.convert)
            canvas1.create_window(350,90,window=convert_but)
            self.convert_but = convert_but
            table_name = canvas1.create_text(460,50,text = "TableName",font="ComicSansMS 14",fill="white")
            self.table_name = table_name
            table_name_entry = tk.Entry(win,font = "Times 12")
            self.table_name_entry = table_name_entry
            canvas1.create_window(600,50,window = self.table_name_entry)
            self.table_name_entry.insert(0,os.path.basename(self.search_file).replace('.xlsx','').replace(" ",""))
            
            
    def convert(self,event =None):
        back.log_input("Converting...")
        try:
            SQL(self.user_name,self.password,file=self.search_file).read(back.log_input,datab_name=self.database_entry.get(),file_name=self.table_name_entry.get())
            canvas1.delete(self.stat)
            status_var.set("Successfully Converted!")
            statr = canvas1.create_text(240,120,text=status_var.get(),font="ComicSansMS 14",fill="green")
            self.statr = statr
        except Exception:
            back.log_input("ERROR!")    
    def log_input(self,ltxt):
        log_text.configure(state = "normal")
        log_text.insert("end",f"{ltxt}\n")
        log_text.configure(state="disabled")
        log_text.yview("end")
        log_text.update()

back = back()


win = tk.Tk()
win.title("Exql")
win.geometry("800x700")
win.maxsize(width=800,height=700)
win.minsize(width=800,height=700)
win.iconphoto(False,tk.PhotoImage(file="sqlserver.png"))
bg = tk.PhotoImage(file = "image2.png")
canvas1 = tk.Canvas( win, width = 800,height = 700)
canvas1.grid(row = 0)

canvas1.create_image( 0, 0, image = bg, anchor = "nw")

canvas1.create_text(100,20,text="Server Username",font="ComicSansMS 14",fill="white")

user_name = tk.Entry(win,font="Times 13")
canvas1.create_window(275,20,window=user_name)

canvas1.create_text(68,50,text="Password",font="ComicSansMS 14",fill="white")
              
password = tk.Entry(win,show="*",font="Times 13")
canvas1.create_window(275,50,window=password)

login_but = tk.Button(win, text = 'Login',command = back.fnc,font="ComicSansMSBold 10")
canvas1.create_window(150,90,window=login_but)

log_text = ScrolledText(win,width=93,height=6,state="disabled",font="ComicSansMS 11")
canvas1.create_window(20,635,window=log_text,anchor="w")

status_var = tk.StringVar()


win.bind("<Return>",back.fnc)


win.mainloop()