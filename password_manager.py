import sqlite3
from tkinter import *
def show_info_on_listbox():
    con = sqlite3.connect("website.db")
    cur = con.cursor()
    sql = """\
        SELECT site FROM web
    """
    try:
        cur.execute(sql)
        t = tuple()
        site_list.delete(0, END)
        for site in cur:
            t = t + site
        for site in t:
            site_list.insert(0, site)
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)
        cur.close()
        con.close()
    else:
        print("Запрос на обновление выполнен")
        cur.close()
        con.close()
def add_into_db(site, login, password):
    con = sqlite3.connect("website.db")
    cur = con.cursor()
    sql = """\
    INSERT INTO web (site, login, passw) VALUES (?, ?, ?)"""
    t = (site, login, password)
    try:
        cur.execute(sql, t)
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)
    else:
        print("Запрос выполнен")
        con.commit()
    cur.close()
    con.close()
    show_info_on_listbox()
def add_into():
    root1 = Toplevel()
    root1.resizable(False, False)

    ad_name = Label(root1, text='Название сайта:')
    ad_login = Label(root1, text='Логин:')
    ad_password = Label(root1, text='Пароль:')

    en_name = Entry(root1)
    en_login = Entry(root1)
    en_password = Entry(root1)

    but_add = Button(root1, text='Добавить')

    ad_name.grid(row=0, column=0, padx=10, pady=1)
    ad_login.grid(row=1, column=0, padx=10, pady=1)
    ad_password.grid(row=2, column=0, padx=10, pady=1)

    en_name.grid(row=0, column=1, columnspan=2, padx=10, pady=1)
    en_login.grid(row=1, column=1, columnspan=2, padx=10, pady=1)
    en_password.grid(row=2, column=1, columnspan=2, padx=10, pady=1)

    but_add.grid(row=3, column=0, columnspan=3, padx=10, pady=1)
    but_add.config(command=lambda: add_into_db(en_name.get(), en_login.get(), en_password.get()))
def show_info_on_table(event):
    i = int(site_list.curselection()[0])
    value = (site_list.get(i),)
    con = sqlite3.connect("website.db")
    cur = con.cursor()
    sql = """\
        SELECT * FROM web WHERE site = (?)
        """
    try:
        cur.execute(sql, value)
        t = cur.fetchone()
        site['text'] = "site: " + t[0]
        login['text'] = "login: " + t[1]
        global p
        p = t[2]
    except sqlite3.DatabaseError as err:
        print("Ошибка:", err)
    else:
        print("Запрос выполнен")
        con.commit()
    cur.close()
    con.close()
def show_hide_password():
    l0 = password['text']
    try:
        if l0 == 'password: ':
            but_hide_show['text'] = 'Скрыть пароль'
            password['text'] = 'password: ' + p
        else:
            but_hide_show['text'] = 'Показать пароль'
            password['text'] = 'password: '
    except NameError as er:
        print("Переменная ещё неопределена:", er)
def copy_password():
    root.clipboard_clear()
    try:
        root.clipboard_append(p)
    except NameError as er:
        print('Переменная p ещё неопределена', er)
def choice(event):
    def focus_destroy(event):
        menu1.destroy()
    menu1 = Menu(tearoff=0)
    menu1.add_command(label='Обновить пароль', command=update_record)
    menu1.add_command(label='Удалить', command=delete_value)
    menu1.post(event.x_root, event.y_root)
    root.bind('<Button-1>', focus_destroy)
def delete_value():
    i = int(site_list.curselection()[0])
    value = (site_list.get(i),)
    con = sqlite3.connect("website.db")
    cur = con.cursor()
    sql = """\
            DELETE FROM web WHERE site = (?);
            """
    try:
        cur.execute(sql, value)
    except sqlite3.DatabaseError as err:
        print("Ошибка: ", err)
    else:
        print("Удаление выполнено")
        con.commit()
    cur.close()
    con.close()
    show_info_on_listbox()
def update_record():
    def show_update_record():
        i = int(site_list.curselection()[0])
        value = (site_list.get(i),)
        con = sqlite3.connect("website.db")
        cur = con.cursor()
        sql = """\
                SELECT * FROM web WHERE site = (?)
                """
        try:
            cur.execute(sql, value)
            t = cur.fetchone()
            up_name['text'] = t[0]
            en_login.insert(END, t[1])
            en_password.insert(END, t[2])
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("Запрос выполнен")
            con.commit()
        cur.close()
        con.close()
    def update():
        t = (en_login.get(), en_password.get(), up_name['text'])
        con = sqlite3.connect("website.db")
        cur = con.cursor()
        sql = """\
        UPDATE web 
        SET login = ?, passw = ? 
        WHERE site = ?;
        """
        try:
            cur.execute(sql, t)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("Данные обновлены")
            con.commit()
        cur.close()
        con.close()

    root2 = Toplevel()
    root2.resizable(False, False)

    up_name = Label(root2, text='Название сайта:')
    up_login = Label(root2, text='Логин:')
    up_password = Label(root2, text='Пароль:')

    up_name.grid(row=0, column=1, padx=10, pady=1)
    up_login.grid(row=1, column=0, padx=10, pady=1)
    up_password.grid(row=2, column=0, padx=10, pady=1)

    en_login = Entry(root2)
    en_password = Entry(root2)
    but_up = Button(root2, text='Обновить', command=update)

    en_login.grid(row=1, column=1, columnspan=2, padx=10, pady=1)
    en_password.grid(row=2, column=1, columnspan=2, padx=10, pady=1)

    but_up.grid(row=3, column=0, columnspan=3, padx=10, pady=1)
    show_update_record()

root = Tk()
root.geometry('400x225+500+150')

# МЕНЮ

mainmenu = Menu(root)
root.config(menu=mainmenu)
filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Добавить...", command=add_into);
filemenu.add_separator()
filemenu.add_command(label="Выход")

helpmenu = Menu(mainmenu, tearoff=0)
helpmenu.add_command(label="О программе")

mainmenu.add_cascade(label="Файл", menu=filemenu)
mainmenu.add_cascade(label="Справка", menu=helpmenu)

# СПИСОК САЙТОВ И ПАРОЛЕЙ К НИМ

site_list = Listbox(width=20, height=10)
site_list.grid(row=0, column=0, rowspan=5, padx=15, pady=15)

show_info_on_listbox()
site_list.bind("<Double-Button-1>", show_info_on_table)
site_list.bind("<Button-3>", choice)

scroll = Scrollbar(command=site_list.yview)
site_list.config(yscrollcommand=scroll.set)
scroll.grid(row=0, column=0, rowspan=5, sticky=E, ipady=58)

# ОСНОВНЫЕ ПОЛЯ С ИНФОРМАЦИЕЙ (ЛЕЙБЛЫ)

site = Label(text='site: ')
site.grid(row=0, column=1, sticky=W, padx=10, pady=5)

login = Label(text='login: ')
login.grid(row=1, column=1, sticky=W, padx=10, pady=5)

password = Label(text='password: ')
password.grid(row=2, column=1, sticky=W, padx=10, pady=5)

# ОСНОВНОЙ ФУНКЦИОНАЛ (КНОПКИ)

but_copy = Button(text='Скопировать пароль', command=copy_password, width=18, height=1)
but_copy.grid(row=3, column=1, padx=10, pady=1)

but_hide_show = Button(text='Показать пароль', command=show_hide_password, width=18, height=1)
but_hide_show.grid(row=4, column=1, padx=10, pady=1)

root.mainloop()
