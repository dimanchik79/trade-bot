from tkinter import *
from tkinter import ttk
from loader import bot
from database.models import CurrentUser
import requests
from config import URL


class MainWindow:
    """Класс обеспечивает работы графического интерфейса
    root - userform Tk,
    bg - background формы
    tree - виджет ttk.TreeView
    """

    def __init__(self):
        self.root = Tk()
        self.bg = "CadetBlue"
        self.tree = None
        self.frame = Frame(self.root, width=490, height=100)
        self.send_entry = Entry(self.root)
        self.send_entry.grid(column=0, pady=5, padx=5, row=4, sticky="ew", columnspan=1)
        self.http_response = Label(self.root, bg='blue1')

    def window_show(self) -> None:
        """Метод - конструктор формы Tk"""
        self.root.title("Bot Master")
        self.root.geometry("500x410")
        self.root.protocol("WM_DELETE_WINDOW", self.close_bot)
        self.root.configure(background=self.bg)
        self.root.grid_columnconfigure(0, weight=1)
        Label(self.root, text="Registered Users", bg=self.bg).grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        Button(self.root, text="Update", command=self.fill_tree).grid(column=1, pady=5, padx=5, row=0, sticky="ew",
                                                                      columnspan=1)
        self.frame.grid(column=0, row=1, padx=5, pady=0, sticky="ew", columnspan=3, rowspan=3)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=('Calibri', 9, "roman"), foreground="black")
        style.configure("Treeview", background="aquamarine3", foreground="black", fieldbackground="aquamarine3")
        columns = ("chat_id", "user_id", "user_name", "registration")
        self.tree = ttk.Treeview(self.frame, style="Treeview", name="tree", columns=columns, show="headings", height=10,
                                 padding=1, selectmode="browse")
        self.tree.heading("chat_id", text="CHAT_ID", anchor=W)
        self.tree.heading("user_id", text="USER_ID", anchor=W)
        self.tree.heading("user_name", text="USER_NAME", anchor=W)
        self.tree.heading("registration", text="REGISTRATION", anchor=W)
        self.tree.column("#1", stretch=YES, width=85, anchor=W)
        self.tree.column("#2", stretch=YES, width=85, anchor=W)
        self.tree.column("#3", stretch=YES, width=190, anchor=W)
        self.tree.column("#4", stretch=YES, width=110, anchor=W)
        self.tree.pack(side=LEFT)
        scrollbar = ttk.Scrollbar(self.frame, orient=VERTICAL, command=self.tree.yview)
        self.tree["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side="right", fill="y")

        btn_one = Button(self.root, text="Send Message", command=self.send_message)
        btn_one.grid(column=1, pady=5, padx=5, row=4, sticky="ew", columnspan=1)
        Label(self.root, text="TuTu API Server status", bg=self.bg).grid(row=5, column=0, padx=5, sticky="w")

        self.http_response.grid(row=6, column=0, padx=5, sticky="ew", columnspan=1)
        btn_get = Button(self.root, text="Get", command=self.get_status_api)
        btn_get.grid(row=6, column=1, padx=5, sticky="ew", columnspan=1)
        btn_close = Button(self.root, text="Close Bot", command=self.close_bot)
        btn_close.grid(column=0, row=7, padx=5, pady=20, sticky="ew", columnspan=3)
        self.fill_tree()
        self.root.mainloop()

    def close_bot(self):
        """Метод закрывает ворму и останавливает бота"""
        print("Bot OFF...")
        bot.stop_polling()
        self.root.destroy()

    def send_message(self) -> None:
        """Метод отсылает сообщение выбранному в TreeView пользователю"""
        items = self.tree.item(self.tree.focus())
        chat_id = items['values'][0]
        bot.send_message(chat_id, self.send_entry.get())
        self.send_entry['text'] = None
        self.send_entry.focus_set()

    def fill_tree(self) -> None:
        """Метод заполняет виджет treeview из CurrentUser"""
        for delete_row in self.tree.get_children():
            self.tree.delete(delete_row)
        users = [user for user in CurrentUser.select()]
        if not users:
            return
        else:
            for user in users:
                self.tree.insert("", END, iid=str(user.id), values=(user.chat_id,
                                                                    user.user_id,
                                                                    user.user_name,
                                                                    str(user.enter_date)[:19],))
            self.tree.selection_set(self.tree.get_children()[0])
            self.tree.focus(self.tree.get_children()[0])

    def get_status_api(self):
        querystring = {'service': 'tutu_trains',
                       'term': 2000003,
                       'term2': 2064130}
        response = requests.get(URL, params=querystring)
        if response.status_code in range(200, 300):
            self.http_response['text'] = f"{response.status_code}. Server is ready!"
            self.http_response.config(fg="white")
        elif response.status_code in range(300, 400):
            self.http_response['text'] = f"{response.status_code}. Attention!"
            self.http_response.config(fg="yellow")
        elif response.status_code in range(400, 500):
            self.http_response['text'] = f"{response.status_code}. Server is down((("
            self.http_response.config(fg="red")
