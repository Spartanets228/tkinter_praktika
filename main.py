from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

def clicked():
    from tkinter import messagebox
    messagebox.showinfo('Кнопка нажата', 'Клик')
    print('Клик')

if __name__ == '__main__':
    root = Tk()
    root.title("Имя окна")
    root.geometry('400x400')

    style = ttk.Style(root)
    root.tk.call('source', 'forest-dark.tcl')  
    style.theme_use('azure')
    root.option_add("*tearOff", FALSE)

    label = Label(root, text='Это метка')
    label.place(x=200, y=10)

    button = Button(root, text='Клик', command=clicked)
    button.place(x=100, y=100)

    entry = Entry(root)
    entry.place(x=200, y=100)

    languages = ["Python", "JavaScript", "C#", "Java"]
    languages_var = Variable(value=languages)
    listbox = Listbox(listvariable=languages_var)
    listbox.place(x=200, y=200)

    checkbutton = Checkbutton(text='чекбокс')
    checkbutton.place(x=100, y=200)

    radio_var = StringVar(value="Value 1")
    radiobutton1 = Radiobutton(root, text='радиокнопка 1', value="Value 1", variable=radio_var)
    radiobutton2 = Radiobutton(root, text='радиокнопка 2', value="Value 2", variable=radio_var)
    radiobutton1.place(x=50, y=230)
    radiobutton2.place(x=50, y=250)

    verticalScale = Scale(root, orient=VERTICAL, length=200, from_=1.0, to=100.0)
    verticalScale.place(x=10, y=100)

    horizontalScale = Scale(root, orient=HORIZONTAL, length=150, from_=1.0, to=100.0)
    horizontalScale.place(x=30, y=350)

    file_menu = Menu(root, tearoff=0)
    file_menu.add_command(label="Save")
    file_menu.add_command(label="Save as")
    file_menu.add_command(label="Open")
    file_menu.add_command(label="Click", command=clicked)

    main_menu = Menu(root)
    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Edit")
    main_menu.add_cascade(label="View")

    root.config(menu=main_menu)
    root.mainloop()
