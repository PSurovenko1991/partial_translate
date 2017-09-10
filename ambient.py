from tkinter import *
from tkinter.filedialog import *
from core import main
from PIL import Image, ImageTk

def _open():
    # b = ""
    op = askopenfilename()
    tex.delete('1.0', END)
    tex.insert(END, op)
    # b = tex.get('1.0', END)

def _job():
    l = "en"
    Language_dict={
        0: "en",
        1: "zh",
        2: "fr",
        3: "de",
        4: "eo"
    } # словарь языков,
    if listbox2.curselection() !=():
        l = Language_dict[listbox2.curselection()[0]] # Выбор языка из представленных в listbox2, по умолчанию "EN"
    s = str(tex.get('1.0', END))[:-1]# метод get добавляет в конец строки /n, берем без последнего символа
    main(s,l)

root = Tk()
root.geometry('700x230')
root.resizable(width=False, height=False)

canvas = Canvas(root,width=999,height=999)
canvas.pack()
pilImage = Image.open("001")
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(0,0,image=image)

label = Label(canvas, text="Выберите текстовый файл для обработки,\n обработанный файл будет сохранен в ту же директорию:")
label.pack()

button = Button(canvas, bg="red",fg="blue",  text=u"Открыть",  command=_open)
button.pack()

tex=Text(canvas ,height=1,width=70,font='Arial 18',wrap=WORD)
tex.pack()

label = Label(canvas, text="Выберите язык перевода\n (по умолчанию будет оставлен EN):")
label.pack()

listbox2 = Listbox(canvas,height=5,width=15,selectmode=SINGLE)
list1=[u"Английский",u"Китайский",u"Французский",u"Немецкий",u"Эсперанто"]
for i in list1:
    listbox2.insert(END,i)
listbox2.pack()

button1 = Button(canvas, bg="red",fg="blue",  text=u"Обработать", command=_job)
button1.pack()

# Тест выбора языка
# def get_language():
#     s = listbox2.curselection()
#     tex1.delete("1.0",END)
#     tex1.insert(END,s)
#     print(type(s))
# button2 = Button(root, bg="red",fg="blue",  text=u"Язык", command=get_language)
# button2.pack()
# tex1=Text(root,height=1,width=70,font='Arial 20',wrap=WORD)
# tex1.pack()

root.mainloop()