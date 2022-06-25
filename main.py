import tkinter
from create_papers import *
from sendings import *

def create_main_window():
    main_window = tkinter.Tk()
    main_window.geometry("600x400")
    main_window.title("Главная")
    main_window.configure(bg="#fbfbfb")
    main_window.resizable(width=False, height=False)

    ws = main_window.winfo_screenwidth()
    hs = main_window.winfo_screenheight()
    x = (ws/2) - (600/2)
    y = (hs/2) - (400/2)
    main_window.geometry('%dx%d+%d+%d' % (600, 400, x, y))

    canvas= tkinter.Canvas(main_window, width=600, height=400)
    canvas.create_text(300, 100, text="BUNNY COMMERCE SOFTWARE", fill="black", font=('Helvetica 15 bold'))
    canvas.pack()

    choose_create_papers_button = tkinter.Button(main_window, text="Сформировать бумаги", 
                                                command=create_papers_window, 
                                                height=2, width=20, bg="#111111", fg="#fbfbfb", 
                                                cursor="hand2")
    choose_send_notification_button = tkinter.Button(main_window, text="Отправить уведомления", 
                                                command=send_notifications_window, 
                                                height=2, width=20, bg="#111111", fg="#fbfbfb", 
                                                cursor="hand2")                                            
    choose_create_papers_button.place(x=225, y=250)
    choose_send_notification_button.place(x=225, y=300)
    main_window.mainloop()

def create_papers_window():
    papers_window = tkinter.Tk()
    papers_window.geometry("600x400")
    papers_window.title("Формирование бумаг")
    papers_window.configure(bg="#fbfbfb")
    papers_window.resizable(width=False, height=False)

    ws = papers_window.winfo_screenwidth()
    hs = papers_window.winfo_screenheight()
    x = (ws/2) - (200/2)
    y = (hs/2) - (200/2)
    papers_window.geometry('%dx%d+%d+%d' % (200, 200, x, y))

    papers_table = tkinter.filedialog.askopenfile(parent=papers_window,mode='rb',title='Choose a file')
    create_papers(papers_table)
    papers_window.destroy()

def send_notifications_window():
    notifications_window = tkinter.Tk()
    notifications_window.geometry("600x400")
    notifications_window.title("Рассылка уведомлений")
    notifications_window.configure(bg="#fbfbfb")
    notifications_window.resizable(width=False, height=False)

    ws = notifications_window.winfo_screenwidth()
    hs = notifications_window.winfo_screenheight()
    x = (ws/2) - (200/2)
    y = (hs/2) - (200/2)
    notifications_window.geometry('%dx%d+%d+%d' % (200, 200, x, y))

    notification_table = tkinter.filedialog.askopenfile(parent=notifications_window,mode='rb',title='Choose a file')
    send_notifications(notification_table)
    notifications_window.destroy()
    
if __name__ == '__main__':
    create_main_window()
